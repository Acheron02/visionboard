import tkinter as tk

class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#013B5C")
        self.controller = controller

        label = tk.Label(
            self,
            text="Analyzing image...\nPlease wait",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#013B5C"
        )
        label.pack(expand=True)
