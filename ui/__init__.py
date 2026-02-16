import os, sys
import time
import termios
import tty
import select

from ui.object import Object, TextObject


class TUI:
    def __init__(self):
        self.lines = 0
        self.columns = 0

        self.logo = Object.from_txt(os.path.join("ui", "components", "logo.txt"))

        self.enable_raw()

        self.enable_alt_screen()
        self.hide_cursor()
        self.clear_scrollback()

        try:
            self.mainloop()
        finally:
            self.disable_raw()
            self.show_cursor()
            self.disable_alt_screen()
        pass

    def disable_alt_screen(self):
        print("\033[?1049l", end="")

    def show_cursor(self):
        print("\033[?25h", end="")

    def enable_alt_screen(self):
        print("\033[?1049h", end="")

    def hide_cursor(self):
        print("\033[?25l", end="")

    def clear_scrollback(self):
        print("\033[3J", end="")

    def enable_raw(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)

    def disable_raw(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def check_resize(self):
        dimentions = os.get_terminal_size()
        new_lines, new_columns = dimentions.lines, dimentions.columns
        if new_lines != self.lines or new_columns != self.columns:
            return True
        return False

    def handle_resize(self):
        dimentions = os.get_terminal_size()
        self.lines = dimentions.lines
        self.columns = dimentions.columns

    def get_key(self):
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch += sys.stdin.read(2)  # read next 2 chars
            return ch
        return None

    def clear_screen(self):
        print("\033[H\033[J", end="")

    def build_frame(self):

        frame = Object(height=self.lines, width=self.columns)

        screen_dimentions = TextObject(
            f"{self.lines}x{self.columns}",
            x=self.columns // 2,
            y=self.lines - 1,
            anchor="mm",
        )

        frame.compose(self.logo)
        frame.compose(screen_dimentions)

        return frame

    def mainloop(self):
        running = True
        dirty = True

        while running:
            if self.check_resize():
                dirty = True

                self.handle_resize()

            key = self.get_key()
            if key:
                dirty = True

                if key == "q":
                    running = False
                else:
                    print(f"Pressed: {repr(key)}")

            if dirty:
                print("\033[H\033[J", end="")
                print(self.build_frame(), end="")
                dirty = False

            time.sleep(0.016)
