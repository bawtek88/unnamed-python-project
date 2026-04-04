from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from html import escape
from typing import Callable
import logging

import pygame
import pygame_gui


@dataclass
class DebugCommandContext:
    get_fps: Callable[[], float]
    log: Callable[[str], None]
    

class InGameLogHandler(logging.Handler):
    def __init__(self, sink: Callable[[str], None]):
        super().__init__()
        self.sink = sink
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.sink(self.format(record))
        except Exception:
            pass  # Avoid crashing the game if logging fails


class DebugCommandRegistry:
    def __init__(self):
        self._commands: dict[str, Callable[[list[str], DebugCommandContext], None]] = {}

    def register(self, name: str, handler: Callable[[list[str], DebugCommandContext], None]) -> None:
        self._commands[name.lower()] = handler

    def names(self) -> list[str]:
        return sorted(self._commands.keys())

    def run(self, raw: str, ctx: DebugCommandContext) -> None:
        parts = raw.strip().split()
        if not parts:
            return
        name = parts[0].lower()
        args = parts[1:]

        handler = self._commands.get(name)
        if handler is None:
            ctx.log("Unknown command. Type 'help'.")
            return
        handler(args, ctx)


class DebugConsole:
    def __init__(
        self,
        manager: pygame_gui.UIManager,
        screen_size: tuple[int, int],
        command_registry: DebugCommandRegistry,
        max_lines: int = 300,
        start_visible: bool = False,
        margin: int = 16,
        panel_height: int = 260,
    ):
        self._manager = manager
        self._registry = command_registry
        self._lines = deque(maxlen=max_lines)
        self.visible = start_visible
        self._last_fps = 0.0
        self._history: list[str] = []
        self._history_index: int | None = None
        self._history_draft = ""

        width, height = screen_size
        panel_rect = pygame.Rect(
            margin,
            height - panel_height - margin,
            width - (margin * 2),
            panel_height,
        )

        self.window = pygame_gui.elements.UIWindow(
            rect=panel_rect,
            manager=self._manager,
            window_display_title="Debug Console",
            object_id="#debug_console_window",
            resizable=False,
        )

        content_w = panel_rect.width - 20
        content_h = panel_rect.height - 60

        self.output_box = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(8, 8, content_w, content_h - 12),
            manager=self._manager,
            container=self.window,
            object_id="#debug_console_output",
        )

        self.input_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(8, content_h + 4, content_w, 32),
            manager=self._manager,
            container=self.window,
            object_id="#debug_console_input",
        )

        if not self.visible:
            self.window.hide()
        else:
            self.input_line.focus()
            
    def set_fps_snapshot(self, fps: float) -> None:
        self._last_fps = fps

    def toggle(self) -> None:
        self.visible = not self.visible
        if self.visible:
            self.window.show()
            self.prepare_input_for_open()
        else:
            self.window.hide()

    def prepare_input_for_open(self) -> None:
        self.input_line.set_text("")
        self.input_line.focus()

    def push_line(self, text: str) -> None:
        self._lines.append(escape(text))
        self._refresh_output()

    def attach_logger(self, logger: logging.Logger) -> InGameLogHandler:
        handler = InGameLogHandler(self.push_line)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        return handler

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == self.input_line:
            raw = event.text.strip()
            if raw:
                self.push_line("> " + raw)
                
                if not self._history or self._history[-1] != raw:
                    self._history.append(raw)
                self._history_index = None
                self._history_draft = ""
                
                ctx = DebugCommandContext(get_fps=lambda: self._last_fps, log=self.push_line)
                self._registry.run(raw, ctx)
            self.input_line.set_text("")
            self.input_line.focus()

    def is_toggle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return False
        if event.key == pygame.K_BACKQUOTE:
            return True
        return getattr(event, "unicode", "") == "~"

    def _refresh_output(self) -> None:
        self.output_box.set_text("<br>".join(self._lines))
    
    def process_history_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.KEYDOWN:
            return False
        if not self.visible:
            return False

        if event.key == pygame.K_UP:
            self._history_up()
            return True
        if event.key == pygame.K_DOWN:
            self._history_down()
            return True
        return False

    def _history_up(self) -> None:
        if not self._history:
            return

        if self._history_index is None:
            self._history_draft = self.input_line.get_text()
            self._history_index = len(self._history) - 1
        elif self._history_index > 0:
            self._history_index -= 1

        self.input_line.set_text(self._history[self._history_index])
        self.input_line.focus()

    def _history_down(self) -> None:
        if self._history_index is None:
            return

        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self.input_line.set_text(self._history[self._history_index])
        else:
            self._history_index = None
            self.input_line.set_text(self._history_draft)

        self.input_line.focus()

    # Clear console output
    def clear(self) -> None:
        self._lines.clear()
        self._refresh_output()
    