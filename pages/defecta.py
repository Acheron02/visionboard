import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2


class DefectA(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller
        self.cap = None
        self.imgtk = None  # Store reference here

        # === TOP NAVBAR ===
        navbar = tk.Frame(self, bg="#013B5C")
        navbar.pack(fill="x", pady=(0, 20))

        nav_center = tk.Frame(navbar, bg="#013B5C")
        nav_center.pack(expand=True)

        def make_nav(text, target_page):
            lbl = tk.Label(
                nav_center,
                text=text,
                font=("Arial", 14, "bold"),
                fg="white",
                bg="#013B5C",
                cursor="hand2",
                padx=20,
                pady=10
            )
            lbl.pack(side="left", padx=15)
            lbl.bind("<Button-1>", lambda e: controller.show_frame(target_page))

        make_nav("Defect A", "DefectA")
        make_nav("Defect B", "DefectB")
        make_nav("Components", "Components")

        # === HEADER ===
        header_label = tk.Label(
            self,
            text="Defect A Inspection",
            font=("Arial", 18, "bold"),
            bg="#02517F",
            fg="white"
        )
        header_label.pack(pady=(20, 10))

        # Camera display
        self.video_label = tk.Label(self, bg="#02517F")
        self.video_label.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#02517F")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Open Camera",
            command=self.start_camera,
            font=("Arial", 12),
            bg="#029DF7",
            fg="white",
            width=15,
            height=2
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Stop Camera",
            command=self.stop_camera,
            font=("Arial", 12),
            bg="#FF4C4C",
            fg="white",
            width=15,
            height=2
        ).pack(side="left", padx=10)

    def start_camera(self):
        """Start webcam feed only if logged in."""
        if not self.controller.auth.is_logged_in:
            messagebox.showwarning("Access Denied", "You must log in to use the camera.")
            self.controller.show_frame("Home")  # redirect to login page
            return

        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        """Continuously update camera frames."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                self.imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=self.imgtk)
            self.after(10, self.update_frame)

    def stop_camera(self):
        """Stop webcam feed and clear frame."""
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.config(image="")  # Clear display
