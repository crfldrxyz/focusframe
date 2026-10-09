"""Flet UI prototype for FocusFrame.

The session engine is independent of Flet; the UI only renders and persists it.
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid

import flet as ft

from markdown_export import export_markdown
from session_engine import (
    Session,
    create_session,
    pause_session,
    reconcile_session,
    remaining_seconds,
    resume_session,
    start_session,
)

SESSION_KEY = "focusframe.flet.session.v1"
DURATION_KEY = "focusframe.flet.default_minutes.v1"


def format_time(seconds: int) -> str:
    minutes, seconds = divmod(max(0, seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"


async def main(page: ft.Page):
    page.title = "FocusFrame — Flet experiment"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F6F4EF"
    page.padding = 24
    page.window_min_width = 360
    page.window_min_height = 620

    prefs = ft.SharedPreferences()
    stored_session = await prefs.get(SESSION_KEY)
    stored_minutes = await prefs.get(DURATION_KEY)
    try:
        session = Session.from_dict(json.loads(stored_session)) if stored_session else None
    except (ValueError, TypeError, KeyError):
        session = None

    if session:
        reconcile_session(session, time.time())

    title = ft.Text("Make room for one thing.", size=30, weight=ft.FontWeight.W_600, color="#20231F")
    subtitle = ft.Text(
        "A quiet space for focused work. One task, one session.",
        size=14,
        color="#6F756D",
    )
    task_input = ft.TextField(
        label="What will you focus on?",
        hint_text="e.g. Draft the first paragraph",
        border_radius=12,
        filled=True,
        bgcolor="#FFFFFF",
        border_color="#E2E2D9",
        text_size=15,
    )
    duration_input = ft.Dropdown(
        label="Session length",
        value=str(stored_minutes or "25"),
        options=[
            ft.DropdownOption(key="5", text="5 minutes"),
            ft.DropdownOption(key="15", text="15 minutes"),
            ft.DropdownOption(key="25", text="25 minutes"),
            ft.DropdownOption(key="45", text="45 minutes"),
            ft.DropdownOption(key="60", text="60 minutes"),
        ],
        width=180,
    )
    timer = ft.Text("25:00", size=64, weight=ft.FontWeight.W_600, color="#20231F")
    status = ft.Text("Ready when you are.", size=14, color="#6F756D")
    reflection = ft.TextField(
        label="A short reflection (optional)",
        hint_text="What did you notice or complete?",
        multiline=True,
        min_lines=2,
        max_lines=4,
        border_radius=12,
        filled=True,
        bgcolor="#FFFFFF",
        border_color="#E2E2D9",
    )
    export_preview = ft.TextField(
        label="Markdown export preview",
        multiline=True,
        min_lines=5,
        max_lines=9,
        read_only=True,
        visible=False,
        border_radius=12,
    )

    async def persist():
        if session:
            await prefs.set(SESSION_KEY, json.dumps(session.to_dict()))
        await prefs.set(DURATION_KEY, int(duration_input.value or "25"))

    def refresh():
        nonlocal session
        now = time.time()
        if session:
            reconcile_session(session, now)
            timer.value = format_time(remaining_seconds(session, now))
            reflection.value = session.reflection
            task_input.value = session.task
            duration_input.value = str(session.duration_seconds // 60)
            if session.status == "active":
                status.value = "You're in a focus session."
            elif session.status == "paused":
                status.value = "Paused. Pick up when you're ready."
            elif session.status == "completed":
                status.value = "Session complete. Take a breath."
            else:
                status.value = "Ready when you are."
        else:
            timer.value = format_time(int(duration_input.value or "25") * 60)
            status.value = "Ready when you are."
        page.update()

    async def start_click(e):
        nonlocal session
        try:
            if session and session.status in ("active", "paused"):
                status.value = "Finish or complete the current session first."
                page.update()
                return
            session = create_session(
                str(uuid.uuid4()),
                task_input.value or "",
                int(duration_input.value or "25") * 60,
            )
            start_session(session, time.time())
            export_preview.visible = False
            await persist()
            refresh()
        except ValueError as error:
            status.value = str(error)
            page.update()

    async def pause_resume_click(e):
        if not session:
            return
        now = time.time()
        if session.status == "active":
            pause_session(session, now)
        elif session.status == "paused":
            resume_session(session, now)
        await persist()
        refresh()

    async def finish_click(e):
        if not session:
            return
        session.status = "completed"
        session.end_at = min(session.end_at or time.time(), time.time())
        session.paused_at = None
        session.reflection = reflection.value or ""
        await persist()
        refresh()

    async def reflection_change(e):
        if session:
            session.reflection = reflection.value or ""
            await persist()

    async def export_click(e):
        if not session:
            status.value = "Complete a session before exporting."
            page.update()
            return
        session.reflection = reflection.value or ""
        export_preview.value = export_markdown(session)
        export_preview.visible = True
        await persist()
        page.update()

    async def copy_click(e):
        if not export_preview.value:
            await export_click(e)
        if export_preview.value:
            await ft.Clipboard().set(export_preview.value)
            status.value = "Markdown copied to clipboard."
            page.update()

    start_button = ft.Button("Start focus", on_click=start_click)
    pause_button = ft.OutlinedButton("Pause / resume", on_click=pause_resume_click)
    finish_button = ft.OutlinedButton("Finish session", on_click=finish_click)
    export_button = ft.OutlinedButton("Prepare Markdown", on_click=export_click)
    copy_button = ft.OutlinedButton("Copy Markdown", on_click=copy_click)

    page.add(
        ft.SafeArea(
            content=ft.Container(
                width=680,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=18,
                    controls=[
                        ft.Container(height=8),
                        ft.Text("FOCUSFRAME  /  FLET LAB", size=11, weight=ft.FontWeight.BOLD, color="#7C806F"),
                        title,
                        subtitle,
                        ft.Container(
                            padding=20,
                            border_radius=18,
                            bgcolor="#FFFFFF",
                            border=ft.Border.all(1, "#E8E6DE"),
                            content=ft.Column(
                                spacing=16,
                                controls=[
                                    task_input,
                                    ft.Row([duration_input], wrap=True),
                                    ft.Divider(color="#ECEAE3"),
                                    ft.Container(
                                        alignment=ft.Alignment.CENTER,
                                        padding=ft.Padding.symmetric(vertical=12),
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=6,
                                            controls=[timer, status],
                                        ),
                                    ),
                                    ft.Row([start_button, pause_button, finish_button], wrap=True),
                                    ft.Divider(color="#ECEAE3"),
                                    reflection,
                                    ft.Row([export_button, copy_button], wrap=True),
                                    export_preview,
                                ],
                            ),
                        ),
                        ft.Text(
                            "Experimental build. Session timing is timestamp-based; verify offline and lifecycle behavior on real devices before drawing conclusions.",
                            size=12,
                            color="#7A7E75",
                        ),
                    ],
                ),
            )
        )
    )

    refresh()

    async def ticker():
        while True:
            await asyncio.sleep(1)
            if session and session.status == "active":
                before = session.status
                reconcile_session(session, time.time())
                if session.status != before:
                    await persist()
                refresh()

    page.run_task(ticker)


if __name__ == "__main__":
    ft.run(main)
