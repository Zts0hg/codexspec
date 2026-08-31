"""Tests for renewable auto-dev ownership."""

import threading
from pathlib import Path

import pytest

from codexspec.automation import AutoDevOwnership, OwnershipError, locate_repository
from tests.automation_test_support import make_repo


def test_only_one_live_owner_and_normal_release(tmp_path: Path) -> None:
    context = locate_repository(make_repo(tmp_path / "project"))

    def clock() -> float:
        return 100.0

    ownership = AutoDevOwnership(context, clock=clock, stale_after=60)
    token = ownership.acquire()
    with pytest.raises(OwnershipError, match="already_running"):
        ownership.acquire()
    ownership.assert_owner(token)
    ownership.renew(token)
    ownership.release(token)
    assert ownership.acquire() != token


def test_stale_owner_is_reclaimed_and_old_token_is_fenced(tmp_path: Path) -> None:
    context = locate_repository(make_repo(tmp_path / "project"))
    now = [100.0]
    ownership = AutoDevOwnership(context, clock=lambda: now[0], stale_after=10)
    old = ownership.acquire()
    now[0] = 111.0
    new = ownership.acquire()
    assert new != old
    with pytest.raises(OwnershipError, match="lost_ownership"):
        ownership.assert_owner(old)
    ownership.assert_owner(new)


def test_guard_prevents_stale_takeover_during_repository_mutation(tmp_path: Path) -> None:
    context = locate_repository(make_repo(tmp_path / "project"))
    now = [100.0]
    ownership = AutoDevOwnership(context, clock=lambda: now[0], stale_after=10)
    token = ownership.acquire()
    outcome: list[str] = []

    def contend() -> None:
        try:
            ownership.acquire()
        except OwnershipError as exc:
            outcome.append(exc.code)

    with ownership.guard(token):
        now[0] = 111.0
        contender = threading.Thread(target=contend)
        contender.start()
        # The contender must fail immediately (never wait behind the guard) and
        # must not reclaim the stale-dated ownership while a mutation is live.
        contender.join(timeout=5)
        assert not contender.is_alive()

    assert outcome == ["already_running"]
    ownership.assert_owner(token)


def test_acquire_reports_busy_immediately_while_owner_lock_is_held(tmp_path: Path) -> None:
    context = locate_repository(make_repo(tmp_path / "project"))
    ownership = AutoDevOwnership(context, clock=lambda: 100.0, stale_after=60)
    token = ownership.acquire()
    with ownership.guard(token):
        # The owner lock is held by guard(); acquire must fail fast instead of
        # blocking until the mutation finishes (REQ-018: exit immediately).
        with pytest.raises(OwnershipError, match="already_running"):
            ownership.acquire()
    ownership.assert_owner(token)
