from markdown_export import export_markdown
from session_engine import create_session


def test_export_includes_task_status_and_reflection():
    session = create_session("x", "Write the outline", 1500)
    session.status = "completed"
    session.reflection = "Finished the first section."
    markdown = export_markdown(session)
    assert "**Task:** Write the outline" in markdown
    assert "**Status:** completed" in markdown
    assert "Finished the first section." in markdown


def test_export_escapes_markdown_brackets_in_task():
    session = create_session("y", "[Draft] a title", 300)
    assert r"\\[Draft\\] a title" in export_markdown(session)
