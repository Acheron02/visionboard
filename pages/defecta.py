import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import time
import json
import threading
import numpy as np
from typing import Optional
from predict import analyze_image  # your YOLO analyze_image function
from db import save_user_history  # Make sure this is imported

class DefectA(tk.Frame):
    """
    Restyled DefectA to match the visual design of DefectB
    (colors, navbar, header, layout). Keeps original DefectA
    functionality: open camera, capture -> analyze (threaded),
    save image and JSON summary, and navigate to results page.
    """
    def __init__(self, parent: tk.Widget, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller

        self.cap: Optional[cv2.VideoCapture] = None
        self.current_frame: Optional[np.ndarray] = None
        self.imgtk: Optional[ImageTk.PhotoImage] = None

        # Grid config: camera row expands
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---------------- Top navbar + header ----------------
        top_frame = tk.Frame(self, bg="#02517F")
        top_frame.grid(row=0, column=0, sticky="ew")

        navbar = tk.Frame(top_frame, bg="#013B5C")
        navbar.pack(fill="x", pady=(0, 10))
        nav_center = tk.Frame(navbar, bg="#013B5C")
        nav_center.pack(expand=True)

        def make_nav(text: str, target_page: str):
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

        # ---------------- Camera display ----------------
        self.video_label = tk.Label(self, bg="#02517F")
        self.video_label.grid(row=1, column=0, sticky="nsew", pady=10, padx=20)

        # ---------------- Buttons ----------------
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

        self.capture_btn = tk.Button(
            button_frame,
            text="Capture & Analyze",
            command=self.capture_image,
            font=("Arial", 12),
            bg="#029DF7",
            fg="white",
            width=18,
            height=2,
            state="disabled"
        )
        self.capture_btn.pack(side="left", padx=10)

    # ---------------- Camera methods ----------------
    def start_camera(self) -> None:
        """Open the webcam and start preview. Enable capture button."""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Linux (Raspberry Pi)

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            if not self.cap.isOpened():
                self.cap.release()
                self.cap = None
                messagebox.showerror("Camera Error", "No camera detected. Please connect a camera.")
                return

            self.capture_btn.config(state="normal")
            self.open_btn.config(text="Close Camera", command=self.stop_camera)
            self.update_frame()

    def update_frame(self) -> None:
        """Continuously read frames and update the label."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)

                self.imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.config(image=self.imgtk)

            self.after(33, self.update_frame)  # ~30 FPS

    def capture_image(self) -> None:
        """Trigger threaded analysis of the current frame (keeps UI responsive)."""
        if self.current_frame is not None:
            threading.Thread(target=self._analyze_image_thread, daemon=True).start()
        else:
            messagebox.showerror("Error", "No frame captured.")

    def _analyze_image_thread(self) -> None:
        """Save a copy, run YOLO analyze_image, save summary JSON, and show results."""
        frame = self.current_frame
        if frame is None:
            return

        try:
            save_dir = "captured_images/defectA"
            os.makedirs(save_dir, exist_ok=True)

            # Get current user email
            user = getattr(self.controller.auth, "current_user", None)
            email = user.get("email") if user else "guest@example.com"

            timestamp = int(time.time())
            filename = f"{email}_{timestamp}.jpg"
            filepath = os.path.join(save_dir, filename)

            small_img = cv2.resize(frame, (640, 480))
            cv2.imwrite(filepath, small_img)

            processed_path, summary = analyze_image(filepath)

            summary_dir = "processed_results/defectA"
            os.makedirs(summary_dir, exist_ok=True)
            summary_path = os.path.join(summary_dir, f"summary_{filename}.json")
            with open(summary_path, "w") as f:
                json.dump(summary.get("detections", summary), f)

            # Save detection to user history
            record = {
                "name": f"DefectA Capture {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}",
                "image_path": processed_path,
                "summary_path": summary_path,
                "timestamp": timestamp
            }
            save_user_history(email, record)

            # Show result page
            result_page = self.controller.frames.get("DefectResult")
            if result_page:
                result_page.set_paths(processed_path, summary_path)

            self.controller.show_frame("DefectResult")

        except Exception as e:
            messagebox.showerror("Prediction Error", f"Failed to analyze image:\n{e}")

    def stop_camera(self) -> None:
        """Stop camera preview and reset buttons/UI pieces."""
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

        self.video_label.config(image="")
        self.imgtk = None
        self.open_btn.config(text="Open Camera", command=self.start_camera)
        self.capture_btn.config(state="disabled")

    def on_hide(self) -> None:
        """Call this when the frame is hidden to ensure the camera is released."""
        self.stop_camera()
