import tkinter as tk
from auth import AuthManager
from pages.home import Home
from pages.register import Register
from pages.profile import Profile
from pages.about import About
from pages.defecta import DefectA
from pages.defectb import DefectB
from pages.components import Components


class VisionBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x900")
        self.title("VisionBoard")
        self.auth = AuthManager()

        # === HEADER BAR (Modern Style) ===
        header_frame = tk.Frame(self, bg="#0D3E5B")
        header_frame.pack(side="top", fill="x")

        # App title on the left
        title_label = tk.Label(
            header_frame,
            text="VISIONBOARD",
            font=("Helvetica", 24, "bold"),
            bg="#0D3E5B",
            fg="white"
        )
        title_label.pack(side="left", padx=50, pady=10)

        # Navigation links container centered
        self.nav_frame = tk.Frame(header_frame, bg="#0D3E5B")
        self.nav_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Nav state
        self.nav_labels = {}
        self.nav_color_default = "white"
        self.nav_color_active = "#00FFFF"

        # Only show these by default
        self.create_nav_label("Home", "Home")
        self.create_nav_label("About", "About")

        # === PAGE CONTAINER ===
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # === INITIALIZE PAGES ===
        self.frames = {}
        for F in (Home, About, Register, Profile, DefectA, DefectB, Components):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def create_nav_label(self, text, page_name):
        """Create and store nav label in header nav frame."""
        lbl = tk.Label(
            self.nav_frame,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg="#0D3E5B",
            fg=self.nav_color_default,
            cursor="hand2"
        )
        lbl.pack(side="left", padx=15)
        lbl.bind("<Button-1>", lambda e: self.show_frame(page_name))
        self.nav_labels[page_name] = lbl
        return lbl

    def enable_post_login_nav(self):
        """Show Defect A, Defect B, Components nav links after login."""
        if "DefectA" not in self.nav_labels:
            self.create_nav_label("Defect A", "DefectA")
            self.create_nav_label("Defect B", "DefectB")
            self.create_nav_label("Components", "Components")

    def show_frame(self, page_name):
        """Raise the page and update nav active style."""
        frame = self.frames[page_name]
        if page_name == "Register":
            frame.reset_fields()
        if page_name == "Profile":
            frame.update_profile_info()
        frame.tkraise()
        self._update_nav_active(page_name)

    def _update_nav_active(self, active_page):
        """Highlight the active page with color and underline."""
        for page, lbl in self.nav_labels.items():
            if page == active_page:
                lbl.config(font=("Helvetica", 12, "bold", "underline"),
                           fg=self.nav_color_active)
            else:
                lbl.config(font=("Helvetica", 12, "bold"),
                           fg=self.nav_color_default)

    def _show_home_or_profile(self):
        """Go to Profile if logged in, else Home (with login form)."""
        if self.auth.is_logged_in:
            self.show_frame("Profile")
        else:
            self.show_frame("Home")
