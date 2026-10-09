"""Platform-independent session rules for the FocusFrame Flet experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Status = Literal["idle", "active", "paused", "completed"]


@dataclass
class Session:
    id: str
    task: str
    duration_seconds: int
    started_at: float | None = None
    end_at: float | None = None
    paused_at: float | None = None
    status: Status = "idle"
    reflection: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "Session":
        return cls(**value)


def create_session(session_id: str, task: str, duration_seconds: int) -> Session:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    clean_task = task.strip()
    if not clean_task:
        raise ValueError("task must not be empty")
    return Session(id=session_id, task=clean_task, duration_seconds=duration_seconds)


def start_session(session: Session, now: float) -> Session:
    if session.status != "idle":
        raise ValueError("Only an idle session can be started")
    session.started_at = now
    session.end_at = now + session.duration_seconds
    session.status = "active"
    return session


def pause_session(session: Session, now: float) -> Session:
    if session.status != "active":
        raise ValueError("Only an active session can be paused")
    session.status = "paused"
    session.paused_at = now
    return session


def resume_session(session: Session, now: float) -> Session:
    if session.status != "paused" or session.paused_at is None or session.end_at is None:
        raise ValueError("Only a paused session can be resumed")
    session.end_at += max(0, now - session.paused_at)
    session.paused_at = None
    session.status = "active"
    return session


def reconcile_session(session: Session, now: float) -> Session:
    if session.status == "active" and session.end_at is not None and now >= session.end_at:
        session.status = "completed"
    return session


def remaining_seconds(session: Session, now: float) -> int:
    if session.status == "idle":
        return session.duration_seconds
    if session.status == "paused" and session.paused_at is not None and session.end_at is not None:
        return max(0, int(session.end_at - session.paused_at + 0.999999))
    if session.status in ("active", "completed") and session.end_at is not None:
        return max(0, int(session.end_at - now + 0.999999))
    return 0
