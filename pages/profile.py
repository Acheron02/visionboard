import tkinter as tk

class Profile(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#02517F")
        self.controller = controller

        # Header
        header_label = tk.Label(self, text="Profile Page", font=("Arial", 18, "bold"),
                                bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        # Welcome text
        content_label = tk.Label(self, text="Welcome to your profile!",
                                 font=("Arial", 16), bg="#02517F", fg="white")
        content_label.pack(pady=20)

        # Dynamic user type display
        self.user_type_label = tk.Label(self, text="", font=("Arial", 14),
                                        bg="#02517F", fg="white")
        self.user_type_label.pack(pady=(0, 20))

        # Buttons container
        button_frame = tk.Frame(self, bg="#02517F")
        button_frame.pack(pady=10)

        # Camera button
        tk.Button(
            button_frame, text="Camera", width=10, height=2,
            font=("Arial", 12), bg="#029DF7", fg="white",
            command=lambda: self.controller.show_frame("Camera")
        ).pack(side="left", padx=10)

        # History button
        tk.Button(
            button_frame, text="History", width=10, height=2,
            font=("Arial", 12), bg="#029DF7", fg="white",
            command=lambda: self.controller.show_frame("History")
        ).pack(side="left", padx=10)

        # Logout button
        tk.Button(
            self, text="Log Out", width=10, height=2,
            font=("Arial", 12), bg="#029DF7", fg="white",
            command=self.controller.auth.logout
        ).pack(pady=10)

        # Delete Account button
        tk.Button(
            self, text="Delete", width=10, height=2,
            font=("Arial", 12), bg="#029DF7", fg="white",
            command=self.delete_account
        ).pack(pady=10)

    def update_profile_info(self):
        """Update profile info dynamically when page is shown."""
        if self.controller.auth.current_user:
            user_type = self.controller.auth.current_user.get("user_type", "N/A")
            self.user_type_label.config(text=f"User Type: {user_type}")
        else:
            self.user_type_label.config(text="")

    def delete_account(self):
        """Delete account and redirect to Home."""
        self.controller.auth.delete_account()
        self.controller.show_frame("Home")
