import tkinter as tk
import ctypes
import ctypes.wintypes

class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Clicker")
        self.root.geometry("280x250")
        self.root.attributes("-topmost", True)

        self.running = False
        self.click_count = 0
        self.start_pos = None
        self.move_tolerance = 10
        self.countdown_job = None

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 16),
            bg="lightgray",
            width=20
        )
        self.status_label.pack(pady=10)

        self.counter_label = tk.Label(self.root, text="Clicks: 0", font=("Arial", 12))
        self.counter_label.pack()

        self.start_button = tk.Button(
            self.root, text="Start", command=self.start,
            width=15, height=2, font=("Arial", 11)
        )
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.root, text="Stop", command=self.stop,
            width=15, height=2, font=("Arial", 11), state="disabled"
        )
        self.stop_button.pack(pady=5)

        self.interval = tk.Scale(
            self.root,
            from_=100,
            to=5000,
            orient="horizontal",
            label="Click interval (ms)",
            length=220
        )
        self.interval.set(2000)
        self.interval.pack(pady=10)

        self.root.mainloop()

    def get_mouse_pos(self):
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def do_click(self):
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # left down
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # left up

    def has_mouse_moved(self):
        current_x, current_y = self.get_mouse_pos()
        start_x, start_y = self.start_pos
        return (
            abs(current_x - start_x) > self.move_tolerance or
            abs(current_y - start_y) > self.move_tolerance
        )

    def set_status(self, text, color):
        self.status_label.config(text=text, bg=color)

    def start(self):
        if self.running:
            return

        self.running = True
        self.click_count = 0
        self.counter_label.config(text="Clicks: 0")
        self.start_pos = self.get_mouse_pos()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.click_cycle()

    def stop(self, message="Stopped"):
        self.running = False

        if self.countdown_job is not None:
            self.root.after_cancel(self.countdown_job)
            self.countdown_job = None

        self.set_status(message, "red")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def click_cycle(self):
        if not self.running:
            return

        if self.has_mouse_moved():
            self.stop("Stopped - Mouse Moved")
            return

        self.set_status("CLICKING", "lime")
        self.do_click()
        self.click_count += 1
        self.counter_label.config(text=f"Clicks: {self.click_count}")

        interval_ms = self.interval.get()
        self.root.after(120, lambda: self.wait_countdown(interval_ms - 120))

    def wait_countdown(self, remaining_ms):
        if not self.running:
            return

        if self.has_mouse_moved():
            self.stop("Stopped - Mouse Moved")
            return

        if remaining_ms <= 0:
            self.click_cycle()
            return

        seconds = remaining_ms / 1000
        self.set_status(f"WAITING {seconds:.1f}s", "yellow")

        step = 100  # update every 0.1 second
        self.countdown_job = self.root.after(step, lambda: self.wait_countdown(remaining_ms - step))


AutoClicker()
