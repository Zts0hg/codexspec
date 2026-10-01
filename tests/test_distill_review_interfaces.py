import http.client
import json
import socket
import threading
import time
import webbrowser
from pathlib import Path

import pytest
from typer.testing import CliRunner

import codexspec.distill_review.server as server_module
from codexspec import app
from codexspec.distill_review.domain import ReviewError, ReviewService
from codexspec.distill_review.lease import ReviewLease
from codexspec.distill_review.server import REQUEST_READ_TIMEOUT, ReviewHandler, create_server
from codexspec.distill_review.session import SessionStore
from codexspec.distill_review.terminal import localized_error, run_text_review
from codexspec.distill_review.transaction import ProfileTransaction, TransactionError
from codexspec.i18n import LANGUAGE_ALIASES
from tests.test_distill_review_core import make_profile, write_consolidation_manifest


def request(server, method: str, path: str, *, token: str | None = None, payload=None, origin: str | None = None):
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if origin:
        headers["Origin"] = origin
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps({"schema_version": 1, **payload})
    connection.request(method, path, body=body, headers=headers)
    response = connection.getresponse()
    data = response.read()
    headers_out = dict(response.getheaders())
    connection.close()
    return response.status, headers_out, data


def test_loopback_server_auth_draft_preview_and_cancel(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    store = SessionStore(root)
    server = create_server(service, store, token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    try:
        status, headers, body = request(server, "GET", "/")
        assert status == 200
        assert "default-src 'self'" in headers["Content-Security-Policy"]
        assert b"P-2026" not in body

        assert request(server, "GET", "/api/session")[0] == 401
        status, _, body = request(server, "GET", "/api/session", token="secret")
        assert status == 200
        assert json.loads(body)["records"][0]["id"] == "P-2026-0927-2310d6-1"

        payload = {
            "expected_revision": 0,
            "operation": {"action": "defer", "record_id": "P-2026-0927-2310d6-1"},
        }
        assert request(server, "POST", "/api/draft", token="secret", payload=payload)[0] == 403
        status, _, body = request(server, "POST", "/api/draft", token="secret", payload=payload, origin=origin)
        assert status == 200
        assert json.loads(body)["revision"] == 1
        assert store.load().revision == 1
        preview_payload = {
            "operation": {
                "action": "replace",
                "record_id": "P-2026-0927-2310d6-1",
                "fields": {"claim": "Previewed"},
            }
        }
        status, _, body = request(
            server, "POST", "/api/preview", token="secret", payload=preview_payload, origin=origin
        )
        assert status == 200
        assert "- claim: Previewed" in json.loads(body)["markdown"]
        assert service.draft.revision == 1
        target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
        target.write_text(target.read_text().replace("Original claim", "Concurrent claim"))
        refresh_payload = {"record_ids": ["P-2026-0927-2310d6-1"], "expected_revision": 1}
        status, _, body = request(
            server, "POST", "/api/refresh", token="secret", payload=refresh_payload, origin=origin
        )
        assert status == 200
        refreshed = json.loads(body)
        assert refreshed["draft"]["revision"] == 2
        assert not refreshed["draft"]["deferred"]
        assert refreshed["records"][0]["fields"]["claim"] == "Concurrent claim"
        assert request(server, "POST", "/api/cancel", token="secret", payload={}, origin=origin)[0] == 200
        assert server.final_result["status"] == "cancelled"
        status, _, body = request(server, "POST", "/api/discard", token="secret", payload={}, origin=origin)
        assert status == 409
        assert json.loads(body)["error"] == "session_finished"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_server_rejects_wrong_origin_token_and_stale_revision(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    store = SessionStore(root)
    server = create_server(service, store, token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    payload = {
        "expected_revision": 0,
        "operation": {"action": "defer", "record_id": "P-2026-0927-2310d6-1"},
    }
    try:
        assert request(server, "POST", "/api/draft", token="wrong", payload=payload, origin=origin)[0] == 401
        foreign = request(server, "POST", "/api/draft", token="secret", payload=payload, origin="http://evil.test")
        assert foreign[0] == 403
        assert request(server, "POST", "/api/draft", token="secret", payload=payload, origin=origin)[0] == 200
        status, _, body = request(server, "POST", "/api/draft", token="secret", payload=payload, origin=origin)
        assert status == 409
        assert json.loads(body)["error"] == "stale_draft_revision"
        unsupported = {"schema_version": 99, "expected_revision": 1, "operation": payload["operation"]}
        assert request(server, "POST", "/api/draft", token="secret", payload=unsupported, origin=origin)[0] == 400
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_server_request_body_read_has_timeout() -> None:
    handler = object.__new__(ReviewHandler)

    class Headers:
        @staticmethod
        def get(name: str, default: str = "") -> str:
            return "16" if name == "Content-Length" else default

    class Connection:
        timeout = None

        def settimeout(self, value: float) -> None:
            self.timeout = value

    class TimedOutBody:
        @staticmethod
        def read(length: int) -> bytes:
            raise TimeoutError

    handler.headers = Headers()
    handler.connection = Connection()
    handler.rfile = TimedOutBody()
    with pytest.raises(ReviewError, match="request_timeout"):
        handler._payload()
    assert 0 < handler.connection.timeout <= REQUEST_READ_TIMEOUT


def test_server_request_body_has_absolute_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    handler = object.__new__(ReviewHandler)

    class Headers:
        @staticmethod
        def get(name: str, default: str = "") -> str:
            return "3" if name == "Content-Length" else default

    class Connection:
        timeouts: list[float] = []

        def settimeout(self, value: float) -> None:
            self.timeouts.append(value)

    class TrickleBody:
        reads = 0

        def read1(self, length: int) -> bytes:
            self.reads += 1
            return b"x"

    ticks = iter([0.0, 0.0, 6.0, 11.0])
    monkeypatch.setattr(server_module.time, "monotonic", lambda: next(ticks))
    handler.headers = Headers()
    handler.connection = Connection()
    handler.rfile = TrickleBody()
    with pytest.raises(ReviewError, match="request_timeout"):
        handler._payload()
    assert handler.rfile.reads == 2
    assert handler.connection.timeouts == [10.0, 4.0]


def test_server_deadline_covers_incomplete_request_headers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server_module, "REQUEST_READ_TIMEOUT", 0.15)
    root = make_profile(tmp_path)
    server = create_server(ReviewService.from_project(root), SessionStore(root), token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    client = socket.create_connection(("127.0.0.1", server.server_port), timeout=1)
    try:
        client.sendall(b"GET /api/session HTTP/1.1\r\nHost: 127.0.0.1\r\nX-Slow: ")
        deadline = time.monotonic() + 1
        while server.active_request_count and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.active_request_count == 0
        assert client.recv(1) == b""
    finally:
        client.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_server_caps_concurrent_incomplete_requests(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server_module, "REQUEST_READ_TIMEOUT", 0.25)
    monkeypatch.setattr(server_module, "MAX_CONCURRENT_REQUESTS", 2)
    root = make_profile(tmp_path)
    server = create_server(ReviewService.from_project(root), SessionStore(root), token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    clients = [socket.create_connection(("127.0.0.1", server.server_port), timeout=1) for _ in range(3)]
    try:
        for client in clients:
            client.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nX-Slow: ")
        deadline = time.monotonic() + 0.2
        while server.active_request_count < 2 and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.active_request_count <= 2
    finally:
        for client in clients:
            client.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_server_rolls_back_draft_when_persistence_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    store = SessionStore(root)
    server = create_server(service, store, token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    monkeypatch.setattr(store, "save", lambda draft: (_ for _ in ()).throw(OSError("disk full")))
    payload = {
        "expected_revision": 0,
        "operation": {"action": "defer", "record_id": "P-2026-0927-2310d6-1"},
    }
    try:
        status, _, body = request(server, "POST", "/api/draft", token="secret", payload=payload, origin=origin)
        assert status == 500
        assert json.loads(body) == {"error": "persistence_failed"}
        assert service.draft.revision == 0
        assert not service.draft.deferred
        assert store.load() is None
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_server_rolls_back_refresh_when_persistence_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    store = SessionStore(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "defer", "record_id": record_id})
    store.save(service.draft)
    original_claim = service.records[record_id].fields["claim"]
    target = service.records[record_id].path
    target.write_text(target.read_text().replace("Original claim", "Concurrent claim"), encoding="utf-8")
    server = create_server(service, store, token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    monkeypatch.setattr(store, "save", lambda draft: (_ for _ in ()).throw(OSError("disk full")))
    try:
        status, _, body = request(
            server,
            "POST",
            "/api/refresh",
            token="secret",
            payload={"record_ids": [record_id], "expected_revision": 1},
            origin=origin,
        )
        assert status == 500
        assert json.loads(body) == {"error": "persistence_failed"}
        assert service.draft.revision == 1
        assert service.draft.deferred == [record_id]
        assert service.records[record_id].fields["claim"] == original_claim
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_server_requires_matching_preview_before_staging_revision(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    server = create_server(service, SessionStore(root), token="secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    operation = {
        "action": "replace",
        "record_id": "P-2026-0927-2310d6-1",
        "fields": {"claim": "Previewed final claim"},
    }
    payload = {"expected_revision": 0, "operation": operation}
    try:
        status, _, body = request(server, "POST", "/api/draft", token="secret", payload=payload, origin=origin)
        assert status == 400
        assert json.loads(body)["error"] == "preview_required"
        assert (
            request(
                server,
                "POST",
                "/api/preview",
                token="secret",
                payload={"operation": operation},
                origin=origin,
            )[0]
            == 200
        )
        assert request(server, "POST", "/api/draft", token="secret", payload=payload, origin=origin)[0] == 200
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_terminal_response_failure_still_stops_server(tmp_path: Path, monkeypatch) -> None:
    root = make_profile(tmp_path)
    server = create_server(ReviewService.from_project(root), SessionStore(root), token="secret")
    handler = object.__new__(ReviewHandler)
    handler.server = server
    handler.path = "/api/cancel"

    def broken_response(*args, **kwargs) -> None:
        raise BrokenPipeError("client disconnected")

    monkeypatch.setattr(handler, "_json", broken_response)
    try:
        try:
            handler._dispatch_post({"schema_version": 1})
        except BrokenPipeError:
            pass
        assert server.final_result and server.final_result["status"] == "cancelled"
        assert server.stop_event.is_set()
    finally:
        server.server_close()


def test_frontend_is_offline_and_uses_fragment_bearer() -> None:
    assets = Path("src/codexspec/distill_review/assets")
    html = (assets / "index.html").read_text(encoding="utf-8")
    script = (assets / "app.js").read_text(encoding="utf-8")
    combined = html + script + (assets / "styles.css").read_text(encoding="utf-8")
    assert "https://" not in combined and "http://" not in combined
    assert "location.hash" in script
    assert "history.replaceState" in script
    assert "Authorization" in script and "Bearer" in script
    assert "/api/draft" in script and "/api/apply" in script
    assert "renderConsolidation" in script
    assert "Object.keys(state.clusters)" in script
    assert 't("noProposal"' in script
    assert "field_changes" in script
    assert "state.proposals[record.id]" in script
    assert "record.editable_fields" in script
    assert "state.draft.decisions[record.id]" in script
    assert "staged.field_changes" in script
    assert "renderRecordContext" in script
    assert "formatResult" in script
    assert "previewOperation" in script
    assert "previewMatches" in script
    assert "previewBeforeStage" in script
    assert "formatError" in script
    assert "details.records" in script and "details.failures" in script
    assert "/i18n/" in script
    assert (assets / "i18n/en.json").is_file()
    assert (assets / "i18n/zh-CN.json").is_file()


def test_frontend_and_terminal_catalogs_cover_every_interaction_language() -> None:
    catalog_dir = Path("src/codexspec/distill_review/assets/i18n")
    english = json.loads((catalog_dir / "en.json").read_text(encoding="utf-8"))
    for language in LANGUAGE_ALIASES:
        catalog_path = catalog_dir / f"{language}.json"
        assert catalog_path.is_file(), language
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        assert set(catalog) == set(english), language
        assert catalog["documentTitle"]
        assert catalog["navigationLabel"]
        assert set(catalog["fieldLabels"]) == {
            "title",
            "claim",
            "scope",
            "scope/when",
            "root-cause",
            "workaround",
            "lesson",
            "trigger",
            "action",
            "steps",
            "failure-recovery",
            "evidence.facts",
            "evidence.state",
        }
        assert all(value and value != key for key, value in catalog["fieldLabels"].items())


def test_frontend_connects_field_errors_to_controls_and_moves_focus() -> None:
    assets = Path("src/codexspec/distill_review/assets")
    html = (assets / "index.html").read_text(encoding="utf-8")
    script = (assets / "app.js").read_text(encoding="utf-8")
    assert 'aria-live="polite"' in html and 'tabindex="-1"' in html
    assert "label.htmlFor = id" in script
    assert 'input.setAttribute("aria-invalid", "true")' in script
    assert 'input.setAttribute("aria-describedby", input.dataset.errorId)' in script
    assert "input.focus()" in script
    assert 'document.documentElement.dir = language === "ar" ? "rtl" : "ltr"' in script


def test_text_review_stages_and_applies_with_shared_domain(tmp_path: Path) -> None:
    root = make_profile(tmp_path, verified=True)
    service = ReviewService.from_project(root)
    store = SessionStore(root)
    answers = iter(["v", "y", "a"])
    output: list[str] = []
    result = run_text_review(service, store, input_fn=lambda _: next(answers), output_fn=output.append)
    assert result["status"] == "applied"
    assert "- status: vetted" in next((root / ".codexspec/profile/pitfalls").glob("*.md")).read_text()
    assert any("- status: vetted" in item for item in output)


def test_text_review_does_not_stage_until_final_preview_is_confirmed(tmp_path: Path) -> None:
    root = make_profile(tmp_path, verified=True)
    service = ReviewService.from_project(root)
    store = SessionStore(root)
    answers = iter(["v", "n", "q"])
    result = run_text_review(service, store, input_fn=lambda _: next(answers), output_fn=lambda _: None)
    assert result["status"] == "cancelled"
    assert not service.draft.decisions


def test_text_review_uses_interaction_language_without_changing_record_bytes(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    before = next((root / ".codexspec/profile/pitfalls").glob("*.md")).read_bytes()
    service = ReviewService.from_project(root, interaction_language="zh-CN")
    prompts: list[str] = []

    def answer(prompt: str) -> str:
        prompts.append(prompt)
        return "q"

    result = run_text_review(service, SessionStore(root), input_fn=answer, output_fn=lambda _: None)
    assert result["status"] == "cancelled"
    assert any("通过" in prompt and "停止" in prompt for prompt in prompts)
    assert next((root / ".codexspec/profile/pitfalls").glob("*.md")).read_bytes() == before


def test_text_review_neutralizes_terminal_controls(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(target.read_text().replace("Original claim", "Unsafe \x1b]0;owned\x07 claim"))
    output: list[str] = []
    result = run_text_review(
        ReviewService.from_project(root),
        SessionStore(root),
        input_fn=lambda _: "q",
        output_fn=output.append,
    )
    assert result["status"] == "cancelled"
    rendered = "\n".join(output)
    assert "\x1b" not in rendered and "\x07" not in rendered
    assert "\\x1b" in rendered and "\\x07" in rendered


def test_text_review_returns_structured_transaction_conflict(tmp_path: Path, monkeypatch) -> None:
    root = make_profile(tmp_path, verified=True)

    def fail_apply(self):
        raise TransactionError("hash_conflict: record", records=["record"])

    monkeypatch.setattr(ProfileTransaction, "apply", fail_apply)
    answers = iter(["v", "y", "a"])
    result = run_text_review(
        ReviewService.from_project(root),
        SessionStore(root),
        input_fn=lambda _: next(answers),
        output_fn=lambda _: None,
    )
    assert result["status"] == "conflict"
    assert result["records"] == ["record"]


def test_text_review_can_stop_during_cluster_review_and_retain_draft(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(
        target.read_text().replace(
            "- status: candidate",
            "- consolidation: candidate; cluster: parser-loss\n- status: candidate",
        )
    )
    store = SessionStore(root)
    answers = iter(["s", "q"])
    manifest = write_consolidation_manifest(root, tmp_path / "text-cluster.json")
    result = run_text_review(
        ReviewService.from_project(root, manifest_path=manifest),
        store,
        input_fn=lambda _: next(answers),
        output_fn=lambda _: None,
    )
    assert result["status"] == "cancelled"
    assert store.load() is not None


def test_hidden_cli_reports_nothing_to_review_and_is_not_in_help(tmp_path: Path) -> None:
    root = tmp_path / "project"
    (root / ".codexspec/profile").mkdir(parents=True)
    runner = CliRunner()
    result = runner.invoke(app, ["_distill-review-helper", "--project-root", str(root), "--no-open"])
    assert result.exit_code == 0, result.output
    assert '"status":"nothing_to_review"' in result.output
    assert "_distill-review-helper" not in runner.invoke(app, ["--help"]).output


def test_hidden_cli_rejects_invalid_project_without_creating_runtime_state(tmp_path: Path) -> None:
    root = tmp_path / "not-a-project"
    root.mkdir()
    result = CliRunner().invoke(app, ["_distill-review-helper", "--project-root", str(root), "--no-open"])
    assert result.exit_code == 2
    assert '"error":"invalid_project_root"' in result.output
    assert not (root / ".codexspec").exists()


def test_hidden_cli_explicitly_discards_corrupt_draft(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    store = SessionStore(root)
    store.prepare()
    store.draft_path.write_text('{"schema_version":1,"broken":true}', encoding="utf-8")
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--discard-draft", "--no-open"],
    )
    assert result.exit_code == 0, result.output
    assert '"status":"discarded"' in result.output
    assert not store.draft_path.exists()


def test_hidden_cli_recovers_transaction_before_discarding_draft(tmp_path: Path, monkeypatch) -> None:
    root = make_profile(tmp_path)
    store = SessionStore(root)
    store.save(ReviewService.from_project(root).draft)
    calls: list[str] = []

    def recover(project_root: Path, session_store: SessionStore) -> None:
        assert project_root == root
        assert session_store.project_root == store.project_root
        calls.append("recover")

    original_discard = SessionStore.discard

    def discard(self: SessionStore) -> None:
        calls.append("discard")
        original_discard(self)

    monkeypatch.setattr(ProfileTransaction, "recover", recover)
    monkeypatch.setattr(SessionStore, "discard", discard)
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--discard-draft", "--no-open"],
    )
    assert result.exit_code == 0, result.output
    assert calls == ["recover", "discard"]


def test_hidden_cli_prints_fallback_url_when_browser_launch_raises(tmp_path: Path, monkeypatch) -> None:
    root = make_profile(tmp_path)

    class StoppedServer:
        server_port = 43210
        stop_event = threading.Event()
        final_result = {"status": "cancelled"}

        def __init__(self) -> None:
            self.stop_event.set()

        def server_close(self) -> None:
            return

    monkeypatch.setattr("codexspec.create_server", lambda *args, **kwargs: StoppedServer())
    monkeypatch.setattr(webbrowser, "open", lambda url: (_ for _ in ()).throw(webbrowser.Error("no browser")))
    result = CliRunner().invoke(app, ["_distill-review-helper", "--project-root", str(root)])
    assert result.exit_code == 0, result.output
    assert "http://127.0.0.1:43210/#token=" in result.output
    assert '"status":"cancelled"' in result.output


def test_hidden_cli_localizes_server_start_failure_and_emits_machine_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    (root / ".codexspec/config.yml").write_text("language:\n  interaction: zh-CN\n", encoding="utf-8")
    monkeypatch.setattr("codexspec.create_server", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("bind")))
    result = CliRunner().invoke(app, ["_distill-review-helper", "--project-root", str(root), "--no-open"])
    assert result.exit_code == 2
    lines = [line for line in result.output.splitlines() if line]
    assert "审核校验失败" in "\n".join(lines[:-1])
    assert json.loads(lines[-1]) == {"error": "bind", "status": "invalid_input"}


def test_hidden_cli_localizes_text_carrier_failure_and_emits_machine_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    (root / ".codexspec/config.yml").write_text("language:\n  interaction: zh-CN\n", encoding="utf-8")
    monkeypatch.setattr("codexspec.run_text_review", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("stdin")))
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--mode", "text", "--no-open"],
    )
    assert result.exit_code == 2
    lines = [line for line in result.output.splitlines() if line]
    assert "审核校验失败" in "\n".join(lines[:-1])
    assert json.loads(lines[-1]) == {"error": "stdin", "status": "invalid_input"}


def test_hidden_cli_localizes_human_diagnostic_and_keeps_machine_result(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    config = root / ".codexspec/config.yml"
    config.write_text("language:\n  interaction: zh-CN\n", encoding="utf-8")
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--mode", "invalid"],
    )
    assert result.exit_code == 2
    lines = [line for line in result.output.splitlines() if line]
    assert any("模式" in line for line in lines[:-1])
    assert json.loads(lines[-1]) == {"error": "invalid_mode", "status": "invalid_input"}


def test_hidden_cli_localizes_unmapped_validation_and_preserves_rule_detail(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    config = root / ".codexspec/config.yml"
    config.write_text("language:\n  interaction: zh-CN\n", encoding="utf-8")
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(target.read_text().replace("### P-", "### C-"), encoding="utf-8")
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--no-open"],
    )
    assert result.exit_code == 2
    lines = [line for line in result.output.splitlines() if line]
    human = "\n".join(lines[:-1])
    assert "审核校验失败" in human
    assert "规则: invalid_profile" in human
    assert "详情: category_id_mismatch" in human
    assert json.loads(lines[-1]) == {
        "error": "invalid_profile: category_id_mismatch",
        "status": "invalid_input",
    }


def test_localized_transaction_error_keeps_records_and_each_failure() -> None:
    error = TransactionError(
        "validation_failed: multiple records",
        records=["P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"],
        failures=["hash_conflict: P-2026-0927-2310d6-1", "invalid_status: P-2026-0927-2310d6-2"],
    )
    message = localized_error("zh-CN", error)
    assert "审核校验失败" in message
    assert "详情: multiple records" in message
    assert "相关记录: P-2026-0927-2310d6-1, P-2026-0927-2310d6-2" in message
    assert "失败原因: hash_conflict" in message and "invalid_status" in message


def test_hidden_cli_can_discard_saved_draft_after_target_disappears(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "remove", "record_id": record_id})
    store = SessionStore(root)
    store.save(service.draft)
    service.records[record_id].path.unlink()
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--mode", "text"],
        input="x\n",
    )
    assert result.exit_code == 0, result.output
    assert '"status":"discarded"' in result.output
    assert not store.draft_path.exists()


def test_hidden_cli_text_mode_respects_existing_writer_lease(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    lease = ReviewLease(root)
    lease.acquire({"mode": "html", "url": "http://127.0.0.1:1234/#token=secret"})
    try:
        result = CliRunner().invoke(
            app,
            ["_distill-review-helper", "--project-root", str(root), "--mode", "text"],
        )
    finally:
        lease.release()
    assert result.exit_code == 0, result.output
    assert '"status":"active_session"' in result.output


def test_hidden_cli_text_mode_ends_with_standalone_machine_result(tmp_path: Path) -> None:
    root = make_profile(tmp_path, verified=True)
    result = CliRunner().invoke(
        app,
        ["_distill-review-helper", "--project-root", str(root), "--mode", "text"],
        input="v\ny\na\n",
    )
    assert result.exit_code == 0, result.output
    envelope = json.loads([line for line in result.output.splitlines() if line][-1])
    assert envelope["status"] == "applied"
    assert envelope["summary"]["promoted"] == ["P-2026-0927-2310d6-1"]
