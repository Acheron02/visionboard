import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import time


class DefectA(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller
        self.cap = None
        self.imgtk = None  
        self.current_frame = None  # store last frame for capture

        # === Screen dimensions for resizing ===
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()

        # Reserve some height for nav/header/buttons
        self.reserved_h = 200  
        self.cam_w = self.screen_w
        self.cam_h = self.screen_h - self.reserved_h

        # === Grid config ===
        self.grid_rowconfigure(1, weight=1)   # camera row expands
        self.grid_columnconfigure(0, weight=1)

        # === TOP NAVBAR + HEADER (row 0) ===
        top_frame = tk.Frame(self, bg="#02517F")
        top_frame.grid(row=0, column=0, sticky="ew")

        navbar = tk.Frame(top_frame, bg="#013B5C")
        navbar.pack(fill="x", pady=(0, 10))

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

        make_nav("Defect Group A", "DefectA")
        make_nav("Defect Group B", "DefectB")
        make_nav("Components Detection", "Components")

        header_label = tk.Label(
            top_frame,
            text="Defect Group A Inspection",
            font=("Arial", 18, "bold"),
            bg="#02517F",
            fg="white"
        )
        header_label.pack(pady=(10, 10))

        # === Camera display (row 1) ===
        self.video_label = tk.Label(self, bg="#02517F")
        self.video_label.grid(row=1, column=0, sticky="nsew", pady=10)

        # === Buttons (row 2) ===
        button_frame = tk.Frame(self, bg="#02517F")
        button_frame.grid(row=2, column=0, pady=20)

        self.open_btn = tk.Button(
            button_frame,
            text="Open Camera",
            command=self.start_camera,
            font=("Arial", 12),
            bg="#029DF7",
            fg="white",
            width=15,
            height=2
        )
        self.open_btn.pack(side="left", padx=10)

        self.stop_btn = tk.Button(
            button_frame,
            text="Stop Camera",
            command=self.stop_camera,
            font=("Arial", 12),
            bg="#FF4C4C",
            fg="white",
            width=15,
            height=2
        )
        self.stop_btn.pack(side="left", padx=10)

    def start_camera(self):
        """Start webcam feed only if logged in."""
        if not self.controller.auth.is_logged_in:
            messagebox.showwarning("Access Denied", "You must log in to use the camera.")
            self.controller.show_frame("Home")
            return

        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

        # Change "Open Camera" button to "Capture Image"
        self.open_btn.config(text="Capture Image", command=self.capture_image)

        self.update_frame()

    def update_frame(self):
        """Continuously update camera frames."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()  # keep original BGR for saving
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # --- Maintain aspect ratio ---
                h, w, _ = frame_rgb.shape
                aspect_ratio = w / h

                # fit height first
                new_h = self.cam_h
                new_w = int(new_h * aspect_ratio)

                if new_w > self.cam_w:  # too wide, fit width instead
                    new_w = self.cam_w
                    new_h = int(new_w / aspect_ratio)

                frame_resized = cv2.resize(frame_rgb, (new_w, new_h))

                img = Image.fromarray(frame_resized)
                self.imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=self.imgtk)

            self.after(33, self.update_frame)  # ~30 fps

    def capture_image(self):
        """Capture current frame and save with username in lowercase."""
        if self.current_frame is not None:
            # Ensure folder exists
            save_dir = "captured_images"
            os.makedirs(save_dir, exist_ok=True)

            # Get username from auth system
            username = getattr(self.controller.auth, "username", "guest").lower()

            # Unique filename with timestamp
            filename = f"{username}_{int(time.time())}.jpg"
            filepath = os.path.join(save_dir, filename)

            cv2.imwrite(filepath, self.current_frame)
            messagebox.showinfo("Image Saved", f"Image saved as {filepath}")

    def stop_camera(self):
        """Stop webcam feed and reset button."""
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.config(image="")  # Clear display

        # Reset button text
        self.open_btn.config(text="Open Camera", command=self.start_camera)

    def on_hide(self):
        """Called when frame is hidden. Stop the camera automatically."""
        self.stop_camera()
