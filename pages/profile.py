import tkinter as tk

class Profile(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller

        # === TOP NAVBAR (hidden until login) ===
        self.navbar = tk.Frame(self, bg="#013B5C")

        self.nav_center = tk.Frame(self.navbar, bg="#013B5C")
        self.nav_center.pack(expand=True)

        self.nav_links = {}  # store references so we can hide/show later

        def make_nav(text, target_page):
            lbl = tk.Label(
                self.nav_center,
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
            self.nav_links[text] = lbl

        # Create nav items (but don’t pack navbar until login)
        make_nav("Defect A", "DefectA")
        make_nav("Defect B", "DefectB")
        make_nav("Components", "Components")

        # === PAGE HEADER ===
        self.header_label = tk.Label(
            self,
            text="Profile Page",
            font=("Arial", 18, "bold"),
            bg="#02517F",
            fg="white"
        )
        self.header_label.pack(pady=(40, 10))

        # Username
        self.username_label = tk.Label(
            self,
            text="",
            font=("Arial", 16, "bold"),
            bg="#02517F",
            fg="white"
        )
        self.username_label.pack(pady=5)

        # User Role
        self.user_type_label = tk.Label(
            self,
            text="",
            font=("Arial", 14),
            bg="#02517F",
            fg="white"
        )
        self.user_type_label.pack(pady=(0, 20))

        # === HISTORY SECTION ===
        history_label = tk.Label(
            self,
            text="History",
            font=("Arial", 16, "bold"),
            bg="#02517F",
            fg="white"
        )
        history_label.pack(pady=(10, 5))

        self.history_list = tk.Listbox(
            self,
            width=60,
            height=10,
            font=("Arial", 12),
            bg="#013B5C",
            fg="white",
            selectbackground="#029DF7",
            relief="flat"
        )
        self.history_list.pack(pady=10)

        # Logout button
        tk.Button(
            self,
            text="Log Out",
            width=12,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#029DF7",
            fg="white",
            command=lambda: [self.controller.auth.logout(),
                             self.controller._show_home_or_profile()]
        ).pack(pady=15)

    def update_profile_info(self):
        """Update profile info dynamically when page is shown."""
        if self.controller.auth.current_user:
            username = self.controller.auth.current_user.get("username", "Unknown User")
            user_type = self.controller.auth.current_user.get("user_type", "N/A")
            self.username_label.config(text=f"Username: {username}")
            self.user_type_label.config(text=f"Role: {user_type}")

            # Pack navbar above Profile header
            self.navbar.pack(fill="x", pady=(0, 20), before=self.header_label)

            # Example: populate history
            self.history_list.delete(0, tk.END)
            sample_history = [
                "Checked PCB - 2025-09-25",
                "Inspected Defect A - 2025-09-26"
            ]
            for item in sample_history:
                self.history_list.insert(tk.END, item)
        else:
            self.username_label.config(text="Username: Guest")
            self.user_type_label.config(text="Role: N/A")
            self.history_list.delete(0, tk.END)

            # Hide navbar if not logged in
            self.navbar.pack_forget()
