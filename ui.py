import datetime
import math
import threading
import tkinter as tk


class JarvisUI:
    def __init__(self, on_command, on_close, on_listen):
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.geometry("900x600")
        self.root.configure(bg="#05070b")
        self.root.protocol("WM_DELETE_WINDOW", on_close)

        self.on_command = on_command
        self.on_listen = on_listen
        self.status = tk.StringVar(value="JARVIS ONLINE")
        self.last_command = tk.StringVar(value="Čakam ...")
        self.response = tk.StringVar(value="Pozdravljen. Reci »Jarvis«.")
        self.clock = tk.StringVar()
        self.date = tk.StringVar()

        tk.Label(
            self.root, text="J A R V I S",
            font=("Segoe UI", 30, "bold"),
            fg="#66e6ff", bg="#05070b"
        ).pack(pady=(28, 4))

        tk.Label(
            self.root, textvariable=self.status,
            font=("Segoe UI", 11, "bold"),
            fg="#7df9ff", bg="#05070b"
        ).pack()

        tk.Label(
            self.root, textvariable=self.clock,
            font=("Segoe UI", 28, "bold"),
            fg="#ffffff", bg="#05070b"
        ).pack(pady=(10, 0))

        tk.Label(
            self.root, textvariable=self.date,
            font=("Segoe UI", 11),
            fg="#8fa6b8", bg="#05070b"
        ).pack()

        self.canvas = tk.Canvas(
            self.root, width=430, height=250,
            bg="#05070b", highlightthickness=0
        )
        self.canvas.pack(pady=5)
        self.angle = 0
        self.animate()
        self.update_clock()

        tk.Label(
            self.root, textvariable=self.last_command,
            font=("Segoe UI", 13), fg="#b9c7d6", bg="#05070b"
        ).pack(pady=5)

        tk.Label(
            self.root, textvariable=self.response,
            font=("Segoe UI", 15), fg="#ffffff", bg="#05070b",
            wraplength=760
        ).pack(pady=12)

        tk.Button(
            self.root, text="🎙  POSLUŠAJ",
            command=self.listen_once,
            font=("Segoe UI", 12, "bold"),
            bg="#0d1820", fg="#66e6ff",
            activebackground="#132b35", activeforeground="#ffffff",
            relief="flat", padx=25, pady=10
        ).pack(pady=5)

    def listen_once(self):
        threading.Thread(target=self.on_listen, daemon=True).start()

    def update_clock(self):
        now = datetime.datetime.now()
        self.clock.set(now.strftime("%H:%M:%S"))
        self.date.set(now.strftime("%A, %d.%m.%Y"))
        self.root.after(1000, self.update_clock)

    def animate(self):
        self.canvas.delete("all")
        cx, cy = 215, 125
        for r in (95, 74, 53, 32):
            self.canvas.create_oval(
                cx-r, cy-r, cx+r, cy+r,
                outline="#123d4a", width=2
            )
        pulse = 30 + int(8 * math.sin(self.angle))
        self.canvas.create_oval(
            cx-pulse, cy-pulse, cx+pulse, cy+pulse,
            outline="#66e6ff", width=4
        )
        self.canvas.create_text(
            cx, cy, text="J",
            fill="#e8fbff", font=("Segoe UI", 32, "bold")
        )
        self.angle += 0.12
        self.root.after(40, self.animate)

    def set_status(self, value):
        self.root.after(0, self.status.set, value)

    def set_command(self, value):
        self.root.after(0, self.last_command.set, value)

    def set_response(self, value):
        self.root.after(0, self.response.set, value)

    def run(self):
        self.root.mainloop()
