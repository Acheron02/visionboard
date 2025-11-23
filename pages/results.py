import customtkinter as ctk
from PIL import Image, ImageTk
import json
import os


class DefectResult(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#02517F")
        self.controller = controller
        self.image_path = None
        self.result_path = None
        self.imgtk = None

        # ---------------- Grid configuration ----------------
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---------------- Top navbar + header ----------------
        top_frame = ctk.CTkFrame(self, fg_color="#02517F")
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        # Navbar
        navbar = ctk.CTkFrame(top_frame, fg_color="#013B5C")
        navbar.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 10))

        nav_center = ctk.CTkFrame(navbar, fg_color="#013B5C")
        nav_center.pack(expand=True)

        def make_nav(text, target_page):
            lbl = ctk.CTkLabel(
                nav_center,
                text=text,
                font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                fg_color="#013B5C",
                text_color="white",
                cursor="hand2"
            )
            lbl.pack(side="left", padx=15)
            lbl.bind("<Button-1>", lambda e: controller.show_frame(target_page))

        make_nav("Defect Group A", "DefectA")
        make_nav("Defect Group B", "DefectB")
        make_nav("Components Detection", "Components")

        # Header
        header_label = ctk.CTkLabel(
            top_frame,
            text="Detection Result",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            fg_color="#02517F",
            text_color="white"
        )
        header_label.grid(row=1, column=0, pady=(10, 10))

        # ---------------- Content frame (image + report side by side) ----------------
        content_frame = ctk.CTkFrame(self, fg_color="#02517F")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        content_frame.grid_columnconfigure(0, weight=2)  # left takes more space
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Image display (left)
        self.image_label = ctk.CTkLabel(
            content_frame,
            text="Processed image will appear here",
            fg_color="white",
            corner_radius=10
        )
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Right side (legend + results)
        right_frame = ctk.CTkFrame(content_frame, fg_color="#02517F")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.grid_rowconfigure(1, weight=1)  # result box expands

        # --- Legend Box ---
        legend_frame = ctk.CTkFrame(right_frame, fg_color="white", corner_radius=10)
        legend_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        legend_title = ctk.CTkLabel(
            legend_frame,
            text="Legend:",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            text_color="black"
        )
        legend_title.pack(anchor="w", padx=10, pady=(5, 2))

        legends = [
            ("A", "Broken Traces", "#FF0000"),
            ("B", "Short Circuits", "#00AA00"),
            ("C", "90 Degree Angle", "#0000FF"),
        ]
        for letter, desc, color in legends:
            row = ctk.CTkFrame(legend_frame, fg_color="white")
            row.pack(anchor="w", padx=10, pady=2, fill="x")

            color_box = ctk.CTkLabel(row, text=" ", width=15, height=15, fg_color=color, corner_radius=3)
            color_box.pack(side="left", padx=(0, 5))

            text_label = ctk.CTkLabel(
                row,
                text=f"{letter} = {desc}",
                font=ctk.CTkFont(family="Arial", size=12),
                text_color="black"
            )
            text_label.pack(side="left")

        # --- Result text ---
        self.result_label = ctk.CTkTextbox(
            right_frame,
            width=400,
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="white",
            corner_radius=10
        )
        self.result_label.grid(row=1, column=0, sticky="nsew")
        self.result_label.configure(state="disabled")

        # Back button
        self.back_btn = ctk.CTkButton(
            self,
            text="Back",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            fg_color="#029DF7",
            text_color="white",
            width=150,
            height=40,
            command=self.go_back
        )
        self.back_btn.grid(row=2, column=0, pady=20)

        # Bind resize event
        self.image_label.bind("<Configure>", self._resize_image)

    def set_paths(self, image_path, result_path):
        self.image_path = image_path
        self.result_path = result_path
        self.load_result()

    def load_result(self):
        # Load processed image
        if self.image_path and os.path.exists(self.image_path):
            try:
                self.original_img = Image.open(self.image_path)
                self._resize_image()
                self.image_label.configure(text="")
            except Exception:
                self.image_label.configure(text="Processed image not available")
        else:
            self.image_label.configure(text="Processed image not available")

        # Load detection results
        self.result_label.configure(state="normal")
        self.result_label.delete("1.0", "end")

        result_text = ""
        if self.result_path and os.path.exists(self.result_path):
            try:
                with open(self.result_path, "r") as f:
                    data = json.load(f)

                if data:
                    result_lines = [
                        f"{d.get('id', '?')} - {d.get('class', 'unknown')} ({d.get('confidence', 0)*100:.1f}%)"
                        for d in data
                    ]
                    result_text = "\n".join(result_lines)
                else:
                    result_text = "No detections found."
            except Exception:
                result_text = "Error reading results."
        else:
            result_text = "No results file found."

        self.result_label.insert("1.0", result_text)
        self.result_label.configure(state="disabled")

    def _resize_image(self, event=None):
        """Resize image dynamically to fit inside the left frame."""
        if hasattr(self, "original_img"):
            w, h = self.image_label.winfo_width(), self.image_label.winfo_height()
            if w > 10 and h > 10:  # avoid errors before layout stabilizes
                resized = self.original_img.copy()
                resized.thumbnail((w-10, h-10))  # small margin
                self.imgtk = ImageTk.PhotoImage(resized)
                self.image_label.configure(image=self.imgtk)

    def go_back(self):
        if self.controller:
            self.controller.show_frame("DefectA")
