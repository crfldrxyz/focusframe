"""Markdown export for the FocusFrame Flet experiment."""

from .session_engine import Session


def export_markdown(session: Session) -> str:
    task = session.task.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    reflection = session.reflection.strip()
    result = [
        "# FocusFrame Session",
        "",
        f"**Task:** {task}",
        f"**Planned duration:** {session.duration_seconds // 60} minutes",
        f"**Status:** {session.status}",
    ]
    if reflection:
        result.extend(["", "## Reflection", "", reflection])
    return "\n".join(result) + "\n"
