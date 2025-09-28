import tkinter as tk

class About(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller

        # Header
        header_label = tk.Label(self, text="About", font=("Arial", 18, "bold"),
                                bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        # Body text
        label = tk.Label(
            self,
            text="VisionBoard is a simple Tkinter-based app demo with login, registration, "
                 "and profile management.",
            font=("Arial", 14), bg="#02517F", fg="white", wraplength=800, justify="center"
        )
        label.pack(pady=20)

        # Back button
        tk.Button(
            self, text="Back to Home",
            command=lambda: self.controller.show_frame("Home"),
            font=("Arial", 12), bg="#029DF7", fg="white", width=15, height=2
        ).pack(pady=20)
