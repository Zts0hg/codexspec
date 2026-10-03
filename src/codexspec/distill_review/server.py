"""Authenticated loopback HTTP carrier for distill review."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
import socket
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .domain import ReviewError, ReviewService
from .models import SCHEMA_VERSION, ReviewDraft
from .session import SessionError, SessionStore
from .transaction import ProfileTransaction, TransactionError

MAX_BODY = 1_048_576
REQUEST_READ_TIMEOUT = 10.0
MAX_CONCURRENT_REQUESTS = 32
ASSET_DIR = Path(__file__).parent / "assets"


def gate_token(operation_key: str) -> str:
    """Opaque, stable identifier for one stored previewed-operation key."""
    return hashlib.sha256(operation_key.encode("utf-8")).hexdigest()


def _reject_unencodable(value: Any) -> None:
    """Refuse strings no later UTF-8 write can encode, such as lone surrogates."""
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            try:
                item.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ReviewError("invalid_encoding") from exc
        elif isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)


class ReviewHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], handler: type[BaseHTTPRequestHandler]) -> None:
        super().__init__(address, handler)
        self.service: ReviewService
        self.store: SessionStore
        self.token: str
        self.stop_event = threading.Event()
        self.final_result: dict[str, Any] | None = None
        self.state_lock = threading.Lock()
        self.previewed_operations: set[str] = set()
        self._request_slots = threading.BoundedSemaphore(MAX_CONCURRENT_REQUESTS)
        self._request_count_lock = threading.Lock()
        self.active_request_count = 0

    def process_request(self, request: Any, client_address: Any) -> None:
        if not self._request_slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        with self._request_count_lock:
            self.active_request_count += 1
        try:
            super().process_request(request, client_address)
        except Exception:
            self._request_finished()
            raise

    def process_request_thread(self, request: Any, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._request_finished()

    def _request_finished(self) -> None:
        with self._request_count_lock:
            self.active_request_count -= 1
        self._request_slots.release()


class ReviewHandler(BaseHTTPRequestHandler):
    server: ReviewHTTPServer

    def log_message(self, format: str, *args: object) -> None:
        return

    def setup(self) -> None:
        super().setup()
        self._request_deadline = time.monotonic() + REQUEST_READ_TIMEOUT
        self.connection.settimeout(REQUEST_READ_TIMEOUT)
        self._deadline_timer = threading.Timer(REQUEST_READ_TIMEOUT, self._expire_request)
        self._deadline_timer.daemon = True
        self._deadline_timer.start()

    def finish(self) -> None:
        self._cancel_request_deadline()
        super().finish()

    def _cancel_request_deadline(self) -> None:
        timer = getattr(self, "_deadline_timer", None)
        if timer is not None:
            timer.cancel()

    def _expire_request(self) -> None:
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    @property
    def expected_origin(self) -> str:
        return f"http://127.0.0.1:{self.server.server_port}"

    def _headers(self, content_type: str, length: int) -> None:
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
        )

    def _send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self._headers(content_type, len(body))
        self.end_headers()
        try:
            self.wfile.write(body)
        except OSError:
            return

    def _json(self, status: int, value: Any) -> None:
        try:
            body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        except UnicodeEncodeError:
            # Request content passed the boundary check, but a response must never
            # die for lack of an encoding.
            body = b'{"error":"unencodable_response"}'
        self._send(status, body)

    def _authorized(self) -> bool:
        provided = self.headers.get("Authorization", "")
        expected = f"Bearer {self.server.token}"
        # Header values arrive latin-1 decoded, and `compare_digest` refuses a non-ASCII
        # `str` operand with TypeError, which would drop the request instead of refusing
        # it. Comparing the latin-1 bytes keeps the comparison constant-time and total.
        if not secrets.compare_digest(provided.encode("latin-1"), expected.encode("latin-1")):
            self._json(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
            return False
        return True

    def _valid_mutation(self) -> bool:
        if self.headers.get("Origin") != self.expected_origin:
            self._json(HTTPStatus.FORBIDDEN, {"error": "invalid_origin"})
            return False
        if self.headers.get_content_type() != "application/json":
            self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "json_required"})
            return False
        return True

    def _payload(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ReviewError("invalid_content_length") from exc
        if length < 0 or length > MAX_BODY:
            raise ReviewError("request_too_large")
        try:
            body_deadline = time.monotonic() + REQUEST_READ_TIMEOUT
            request_deadline = getattr(self, "_request_deadline", None)
            deadline = min(request_deadline, body_deadline) if request_deadline is not None else body_deadline
            remaining = length
            chunks: list[bytes] = []
            read = self.rfile.read1 if hasattr(self.rfile, "read1") else self.rfile.read
            while remaining:
                timeout = deadline - time.monotonic()
                if timeout <= 0:
                    raise TimeoutError
                self.connection.settimeout(timeout)
                chunk = read(min(remaining, 64 * 1024))
                if not chunk:
                    raise ReviewError("invalid_json")
                chunks.append(chunk)
                remaining -= len(chunk)
            self._cancel_request_deadline()
            value = json.loads(b"".join(chunks) or b"{}")
        except TimeoutError as exc:
            raise ReviewError("request_timeout") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ReviewError("invalid_json") from exc
        if not isinstance(value, dict):
            raise ReviewError("object_required")
        _reject_unencodable(value)
        if value.get("schema_version") != SCHEMA_VERSION:
            raise ReviewError("unsupported_request_schema")
        return value

    def _operation_key(self, operation: object) -> str:
        encoded = json.dumps(operation, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return f"{self.server.service.draft.revision}:{encoded}"

    def _gate_tokens(self) -> list[str]:
        """Project the previewed-operation set so the page can display the gate instead of inferring it.

        A key is stored under the revision current at preview time and the enforcement lookup composes
        the revision current at staging time, so the set is cleared whenever the revision advances and
        every token listed here belongs to the current revision.
        """
        return sorted(gate_token(key) for key in self.server.previewed_operations)

    def do_GET(self) -> None:  # noqa: N802
        self._cancel_request_deadline()
        path = self.path.split("?", 1)[0]
        if path.startswith("/api/"):
            if not self._authorized():
                return
            if path == "/api/session":
                # Every mutation holds this lock; reading the same state without it can
                # observe a half-applied change and kill the handler with no response.
                with self.server.state_lock:
                    payload = {**self.server.service.snapshot(), "gate_tokens": self._gate_tokens()}
                self._json(HTTPStatus.OK, payload)
            else:
                self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        asset_name = {
            "/": "index.html",
            "/index.html": "index.html",
            "/app.js": "app.js",
            "/styles.css": "styles.css",
        }.get(path)
        if asset_name is None and re.fullmatch(r"/i18n/[A-Za-z-]+\.json", path):
            asset_name = path.removeprefix("/")
        if asset_name is None:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        asset = ASSET_DIR / asset_name
        content_type = {
            ".html": "text/html; charset=utf-8",
            ".js": "text/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".json": "application/json; charset=utf-8",
        }[asset.suffix]
        # The catalog route takes a caller-sized name, so a filesystem call here can fail
        # on a name the platform cannot represent. That is not a served path; answer it
        # rather than letting the handler die without a response.
        try:
            if not asset.is_file():
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "missing_asset"})
                return
            body = asset.read_bytes()
        except OSError:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        self._send(HTTPStatus.OK, body, content_type)

    def do_POST(self) -> None:  # noqa: N802
        if not self._authorized() or not self._valid_mutation():
            return
        try:
            payload = self._payload()
            with self.server.state_lock:
                if self.server.final_result is not None:
                    raise ReviewError("session_finished")
                self._dispatch_post(payload)
        except ReviewError as exc:
            status = (
                HTTPStatus.CONFLICT
                if str(exc) in {"stale_draft_revision", "session_finished"}
                else HTTPStatus.BAD_REQUEST
            )
            self._json(status, {"error": str(exc)})
        except TransactionError as exc:
            self._json(
                HTTPStatus.CONFLICT,
                {"error": str(exc), "records": exc.records, "failures": exc.failures},
            )
        except (SessionError, OSError):
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "persistence_failed"})

    def _dispatch_post(self, payload: dict[str, Any]) -> None:
        operation = payload.get("operation", {})
        if not isinstance(operation, dict):
            # The domain expects a mapping; anything else would crash the handler
            # instead of answering the request.
            raise ReviewError("object_required")
        if self.path == "/api/draft":
            if operation.get("action") in {"vet", "replace", "merge"}:
                if self._operation_key(operation) not in self.server.previewed_operations:
                    raise ReviewError("preview_required")
            previous_draft = ReviewDraft.from_dict(self.server.service.draft.to_dict())
            draft = self.server.service.stage(operation, expected_revision=payload.get("expected_revision"))
            try:
                self.server.store.save(self.server.service.draft)
            except (SessionError, OSError):
                self.server.service.draft = previous_draft
                raise
            # The revision has advanced, so no stored key can satisfy a lookup any more.
            self.server.previewed_operations.clear()
            self._json(
                HTTPStatus.OK,
                {**draft, "summary": self.server.service.summary(), "gate_tokens": self._gate_tokens()},
            )
        elif self.path == "/api/preview":
            preview = self.server.service.preview_operation(operation)
            operation_key = self._operation_key(operation)
            self.server.previewed_operations.add(operation_key)
            self._json(HTTPStatus.OK, {**preview, "gate_token": gate_token(operation_key)})
        elif self.path == "/api/apply":
            if payload.get("expected_revision") != self.server.service.draft.revision:
                raise ReviewError("stale_draft_revision")
            result = ProfileTransaction(
                self.server.service.project_root,
                self.server.service.records,
                self.server.service.draft,
                self.server.store,
            ).apply()
            result["summary"] = self.server.service.summary()
            self.server.final_result = result
            self.server.stop_event.set()
            self._json(HTTPStatus.OK, result)
        elif self.path == "/api/refresh":
            record_ids = payload.get("record_ids")
            expected_revision = payload.get("expected_revision")
            if not isinstance(record_ids, list):
                raise ReviewError("invalid_refresh_targets")
            if not isinstance(expected_revision, int):
                raise ReviewError("invalid_draft_revision")
            previous_draft = ReviewDraft.from_dict(self.server.service.draft.to_dict())
            previous_records = dict(self.server.service.records)
            previous_clusters = {key: list(value) for key, value in self.server.service.clusters.items()}
            snapshot = self.server.service.refresh(record_ids, expected_revision=expected_revision)
            try:
                self.server.store.save(self.server.service.draft)
            except (SessionError, OSError):
                self.server.service.draft = previous_draft
                self.server.service.records = previous_records
                self.server.service.clusters = previous_clusters
                raise
            self.server.previewed_operations.clear()
            self._json(HTTPStatus.OK, {**snapshot, "gate_tokens": self._gate_tokens()})
        elif self.path == "/api/cancel":
            retained = bool(self.server.service.draft.decisions or self.server.service.draft.deferred)
            if not retained:
                self.server.store.discard()
            result = {
                "status": "cancelled",
                "draft_retained": retained,
                "summary": self.server.service.summary(),
            }
            self.server.final_result = result
            self.server.stop_event.set()
            self._json(HTTPStatus.OK, result)
        elif self.path == "/api/discard":
            self.server.store.discard()
            result = {"status": "discarded"}
            self.server.final_result = result
            self.server.stop_event.set()
            self._json(HTTPStatus.OK, result)
        else:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})


def create_server(
    service: ReviewService,
    store: SessionStore,
    *,
    token: str | None = None,
) -> ReviewHTTPServer:
    server = ReviewHTTPServer(("127.0.0.1", 0), ReviewHandler)
    server.service = service
    server.store = store
    server.token = token or secrets.token_urlsafe(32)
    return server
