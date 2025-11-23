import tkinter as tk
from tkinter import messagebox
import json
import os
from db import load_user_history

class Profile(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(0, weight=1)

        # Top navbar + header
        top_frame = tk.Frame(self, bg="#02517F")
        top_frame.grid(row=0, column=0, sticky="ew")
        navbar = tk.Frame(top_frame, bg="#013B5C")
        navbar.pack(fill="x", pady=(0, 10))
        nav_center = tk.Frame(navbar, bg="#013B5C")
        nav_center.pack(expand=True)

        def make_nav(text: str, target_page: str):
            lbl = tk.Label(nav_center, text=text, font=("Arial", 14, "bold"),
                           fg="white", bg="#013B5C", cursor="hand2", padx=20, pady=10)
            lbl.pack(side="left", padx=15)
            lbl.bind("<Button-1>", lambda e: controller.show_frame(target_page))

        make_nav("Defect Group A", "DefectA")
        make_nav("Defect Group B", "DefectB")
        make_nav("Components Detection", "Components")

        header_label = tk.Label(top_frame, text="User Profile", font=("Arial", 18, "bold"),
                                bg="#02517F", fg="white")
        header_label.pack(pady=(10, 10))

        # Profile Info
        self.info_frame = tk.Frame(self, bg="#02517F")
        self.info_frame.grid(row=1, column=0, pady=20, sticky="nsew")
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.username_label = tk.Label(self.info_frame, text="Username: ", font=("Arial", 14),
                                       bg="#02517F", fg="white")
        self.username_label.pack(pady=5)
        self.email_label = tk.Label(self.info_frame, text="Email: ", font=("Arial", 14),
                                    bg="#02517F", fg="white")
        self.email_label.pack(pady=5)

        # Detection History
        history_label = tk.Label(self, text="Detection History", font=("Arial", 16, "bold"),
                                 bg="#02517F", fg="white")
        history_label.grid(row=2, column=0, pady=(10, 5))

        self.history_box = tk.Listbox(self, font=("Arial", 12), bg="#013B5C", fg="white",
                                      selectbackground="#029DF7", activestyle="none")
        self.history_box.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.history_box.bind("<Double-Button-1>", self.open_selected_history)

        self.history_data = []

        # Logout button
        logout_btn = tk.Button(self, text="Logout", command=self.logout,
                               font=("Arial", 12, "bold"), bg="red", fg="white",
                               width=12, height=2)
        logout_btn.grid(row=4, column=0, pady=20)

        # Refresh history every 2 seconds
        self.after(2000, self.refresh_history)

    def update_profile_info(self):
        user = getattr(self.controller.auth, "current_user", None)
        username = user.get("username", "Guest") if user else "Guest"
        email = user.get("email", "N/A") if user else "N/A"
        self.username_label.config(text=f"Username: {username}")
        self.email_label.config(text=f"Email: {email}")

    def refresh_history(self):
        """Load user's detection history and update Listbox."""
        user = getattr(self.controller.auth, "current_user", None)
        if user:
            email = user.get("email")
            if email:
                history_list = load_user_history(email)
                # Sort newest first
                history_list.sort(key=lambda r: r.get("timestamp", 0), reverse=True)

                self.history_box.delete(0, tk.END)
                self.history_data.clear()
                for record in history_list:
                    # Show only if both processed image and summary exist
                    if os.path.exists(record.get("image_path", "")) and os.path.exists(record.get("summary_path", "")):
                        self.history_box.insert(tk.END, record["name"])
                        self.history_data.append(record)

        self.after(2000, self.refresh_history)

    def open_selected_history(self, event=None):
        """Open selected history item in DefectResult page."""
        idx = self.history_box.curselection()
        if not idx:
            return
        idx = idx[0]
        record = self.history_data[idx]

        if not (os.path.exists(record.get("image_path", "")) and os.path.exists(record.get("summary_path", ""))):
            # Remove invalid entry
            email = getattr(self.controller.auth.current_user, "email", None)
            if email:
                self.history_data.pop(idx)
                self.history_box.delete(idx)
                os.makedirs("user_history", exist_ok=True)
                history_file = os.path.join("user_history", f"{email}.json")
                with open(history_file, "w") as f:
                    json.dump(self.history_data, f, indent=4)
            return

        # Load image + summary into DefectResult page
        result_page = self.controller.frames.get("DefectResult")
        if result_page:
            result_page.set_paths(record["image_path"], record["summary_path"])
            result_page.current_image = result_page.imgtk
            self.controller.show_frame("DefectResult")

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            self.controller.auth.logout()
            self.controller.disable_post_logout_nav()
            self.controller.show_frame("Home")
