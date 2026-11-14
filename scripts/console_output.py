"""Terminal output of the scripts of the pack: steps, states, a spinner and a summary box.

Colour and animation only when the output is a terminal that understands ANSI; with ``NO_COLOR``,
``TERM=dumb`` or a redirected output, the same lines come out as plain text.
"""

import contextlib
import itertools
import os
import sys
import threading

# Palette, symbols and timing: the only literals of the output.
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_RED = "\033[31m"
ANSI_CYAN = "\033[36m"
ANSI_BLUE = "\033[34m"
ANSI_CLEAR_LINE = "\r\033[2K"
ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"

STATE_DONE = "done"
STATE_SKIPPED = "skipped"
STATE_CHANGED = "changed"
STATE_WARNING = "warning"
STATE_ERROR = "error"
# (symbol with colour, plain symbol, colour) of each state.
STATE_STYLES = {
    STATE_DONE: ("✔", "[ok]", ANSI_GREEN),
    STATE_SKIPPED: ("○", "[--]", ANSI_DIM),
    STATE_CHANGED: ("●", "[~~]", ANSI_BLUE),
    STATE_WARNING: ("▲", "[!!]", ANSI_YELLOW),
    STATE_ERROR: ("✖", "[xx]", ANSI_RED),
}
SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
SPINNER_INTERVAL_SECONDS = 0.08
BOX_HORIZONTAL = "─"
BOX_VERTICAL = "│"
BOX_CORNERS = ("╭", "╮", "╰", "╯")
PLAIN_BOX_EDGE = "="
NO_COLOR_VARIABLE = "NO_COLOR"
DUMB_TERMINAL = "dumb"
WINDOWS_ENABLE_VIRTUAL_TERMINAL = 0x0004
WINDOWS_STANDARD_ERROR_HANDLE = -12


def enable_windows_ansi():
    """Turn on ANSI escapes in a Windows console; False when the console cannot."""
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(WINDOWS_STANDARD_ERROR_HANDLE)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | WINDOWS_ENABLE_VIRTUAL_TERMINAL))
    except (AttributeError, OSError):
        return False


def supports_color(stream, environment=None):
    """Colour and animation need a terminal that understands ANSI and no NO_COLOR."""
    environment = os.environ if environment is None else environment
    if environment.get(NO_COLOR_VARIABLE) is not None or environment.get("TERM") == DUMB_TERMINAL:
        return False
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    return enable_windows_ansi() if os.name == "nt" else True


class Console:
    """Lines of a script: a banner, numbered steps, one state per line, a spinner and a summary."""

    def __init__(self, stream=None, color=None, spinner_interval=SPINNER_INTERVAL_SECONDS):
        self.stream = stream or sys.stderr
        self.color = supports_color(self.stream) if color is None else color
        self.spinner_interval = spinner_interval

    def paint(self, text, *styles):
        return f"{''.join(styles)}{text}{ANSI_RESET}" if self.color and styles else text

    def write(self, text):
        self.stream.write(text + "\n")
        self.stream.flush()

    def banner(self, title, subtitle=""):
        self.write(self.paint(title, ANSI_BOLD, ANSI_CYAN))
        if subtitle:
            self.write(self.paint(subtitle, ANSI_DIM))

    def step(self, index, total, title):
        self.write("")
        self.write(self.paint(f"[{index}/{total}] ", ANSI_BOLD) + self.paint(title, ANSI_BOLD))

    def state(self, state, message):
        symbol, plain_symbol, color = STATE_STYLES[state]
        prefix = self.paint(symbol, color) if self.color else plain_symbol
        self.write(f"  {prefix} {message}")

    @contextlib.contextmanager
    def spinner(self, message):
        """Animate ``message`` while the block runs; plain mode prints it once. The line is always cleared."""
        if not self.color:
            self.write(f"  ... {message}")
            yield
            return
        stop = threading.Event()

        def animate():
            for frame in itertools.cycle(SPINNER_FRAMES):
                self.stream.write(f"{ANSI_CLEAR_LINE}  {self.paint(frame, ANSI_CYAN)} {message}")
                self.stream.flush()
                if stop.wait(self.spinner_interval):
                    return

        self.stream.write(ANSI_HIDE_CURSOR)
        thread = threading.Thread(target=animate, daemon=True)
        thread.start()
        try:
            yield
        finally:
            stop.set()
            thread.join()
            self.stream.write(ANSI_CLEAR_LINE + ANSI_SHOW_CURSOR)
            self.stream.flush()

    def summary(self, title, lines, succeeded):
        """A box with the result and what to do next."""
        color = ANSI_GREEN if succeeded else ANSI_RED
        width = max(len(line) for line in [title] + lines) + 2
        self.write("")
        if not self.color:
            self.write(PLAIN_BOX_EDGE * width)
            self.write(f" {title}")
            for line in lines:
                self.write(f" {line}")
            self.write(PLAIN_BOX_EDGE * width)
            return
        top_left, top_right, bottom_left, bottom_right = BOX_CORNERS
        self.write(self.paint(top_left + BOX_HORIZONTAL * width + top_right, color))
        for index, line in enumerate([title] + lines):
            text = self.paint(line.ljust(width - 1), ANSI_BOLD) if index == 0 else line.ljust(width - 1)
            self.write(f"{self.paint(BOX_VERTICAL, color)} {text}{self.paint(BOX_VERTICAL, color)}")
        self.write(self.paint(bottom_left + BOX_HORIZONTAL * width + bottom_right, color))

    def failure(self, message):
        """One clear line for an error that ends the script."""
        prefix = self.paint("error:", ANSI_BOLD, ANSI_RED) if self.color else "error:"
        self.write(f"{prefix} {message}")
