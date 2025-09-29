import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import time
import json
from predict import analyze_image  # Your YOLO analyze_image function

# ==================== DefectA Page ====================
class DefectA(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller
        self.cap = None
        self.current_frame = None
        self.imgtk = None  # Keep reference to avoid GC

        # Screen dimensions
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.reserved_h = 200
        self.cam_w = self.screen_w
        self.cam_h = self.screen_h - self.reserved_h

        # Grid config
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---------------- Top navbar + header ----------------
        top_frame = tk.Frame(self, bg="#02517F")
        top_frame.grid(row=0, column=0, sticky="ew")

        navbar = tk.Frame(top_frame, bg="#013B5C")
        navbar.pack(fill="x", pady=(0, 10))
        nav_center = tk.Frame(navbar, bg="#013B5C")
        nav_center.pack(expand=True)

        def make_nav(text, target_page):
            lbl = tk.Label(
                nav_center, text=text, font=("Arial", 14, "bold"),
                fg="white", bg="#013B5C", cursor="hand2", padx=20, pady=10
            )
            lbl.pack(side="left", padx=15)
            lbl.bind("<Button-1>", lambda e: controller.show_frame(target_page))

        make_nav("Defect Group A", "DefectA")
        make_nav("Defect Group B", "DefectB")
        make_nav("Components Detection", "Components")

        header_label = tk.Label(
            top_frame, text="Defect Group A Inspection",
            font=("Arial", 18, "bold"), bg="#02517F", fg="white"
        )
        header_label.pack(pady=(10, 10))

        # ---------------- Camera display ----------------
        self.video_label = tk.Label(self, bg="white")
        self.video_label.grid(row=1, column=0, sticky="nsew", pady=10, padx=20)

        # ---------------- Buttons ----------------
        button_frame = tk.Frame(self, bg="#02517F")
        button_frame.grid(row=2, column=0, pady=20)

        self.open_btn = tk.Button(
            button_frame, text="Open Camera", font=("Arial", 12),
            bg="#029DF7", fg="white", width=15, height=2, command=self.start_camera
        )
        self.open_btn.pack(side="left", padx=10)

        self.capture_btn = tk.Button(
            button_frame, text="Capture & Analyze", font=("Arial", 12),
            bg="#029DF7", fg="white", width=15, height=2,
            command=self.capture_image, state="disabled"
        )
        self.capture_btn.pack(side="left", padx=10)

    # ---------------- Camera Methods ----------------
    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Camera Error", "No camera detected.")
                self.cap = None
                return

            self.capture_btn.config(state="normal")
            self.open_btn.config(text="Close Camera", command=self.stop_camera)
            self.update_frame()

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Maintain aspect ratio
                h, w, _ = frame_rgb.shape
                aspect_ratio = w / h
                new_h = self.cam_h
                new_w = int(new_h * aspect_ratio)
                if new_w > self.cam_w:
                    new_w = self.cam_w
                    new_h = int(new_w / aspect_ratio)

                frame_resized = cv2.resize(frame_rgb, (new_w, new_h))
                img = Image.fromarray(frame_resized)
                self.imgtk = ImageTk.PhotoImage(img)
                self.video_label.config(image=self.imgtk)

            self.after(33, self.update_frame)

    def capture_image(self):
        if self.current_frame is not None:
            # Save original image
            save_dir = "captured_images/defectA"
            os.makedirs(save_dir, exist_ok=True)
            username = getattr(self.controller.auth, "username", "guest").lower()
            timestamp = int(time.time())
            filename = f"{username}_{timestamp}.jpg"
            filepath = os.path.join(save_dir, filename)
            cv2.imwrite(filepath, self.current_frame)

            try:
                # Run YOLO analyze_image
                processed_path, summary = analyze_image(filepath)

                # Save summary to JSON
                summary_dir = "processed_results/defectA"
                os.makedirs(summary_dir, exist_ok=True)
                summary_path = os.path.join(summary_dir, f"summary_{filename}.json")
                with open(summary_path, "w") as f:
                    json.dump(summary["detections"], f)

                # Pass paths to results page
                result_page = self.controller.frames["DefectResult"]
                result_page.set_paths(processed_path, summary_path)

                # Switch to results page
                self.controller.show_frame("DefectResult")

            except Exception as e:
                messagebox.showerror("Prediction Error", f"Failed to analyze image:\n{e}")

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.config(image="")
        self.imgtk = None
        self.open_btn.config(text="Open Camera", command=self.start_camera)
        self.capture_btn.config(state="disabled")

    def on_hide(self):
        self.stop_camera()