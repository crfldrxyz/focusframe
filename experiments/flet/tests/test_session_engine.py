from session_engine import (
    create_session,
    pause_session,
    reconcile_session,
    remaining_seconds,
    resume_session,
    start_session,
)


def test_start_uses_timestamps_as_source_of_truth():
    session = start_session(create_session("a", "Write", 600), 1000)
    assert session.started_at == 1000
    assert session.end_at == 1600
    assert remaining_seconds(session, 1250) == 350


def test_pause_and_resume_preserve_remaining_time():
    session = start_session(create_session("b", "Read", 600), 1000)
    pause_session(session, 1200)
    assert remaining_seconds(session, 1500) == 400
    resume_session(session, 1500)
    assert session.end_at == 1900
    assert remaining_seconds(session, 1500) == 400


def test_expired_active_session_reconciles_to_completed():
    session = start_session(create_session("c", "Plan", 60), 100)
    reconcile_session(session, 160)
    assert session.status == "completed"
    assert remaining_seconds(session, 160) == 0


def test_task_must_not_be_empty():
    try:
        create_session("d", "   ", 60)
    except ValueError as error:
        assert "task" in str(error)
    else:
        raise AssertionError("Expected an empty task to be rejected")
