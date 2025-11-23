import tkinter as tk
from auth import AuthManager
from pages.home import Home
from pages.register import Register
from pages.profile import Profile
from pages.about import About
from pages.defecta import DefectA
from pages.defectb import DefectB
from pages.components import Components
from pages.results import DefectResult
from pages.loading import LoadingPage


class VisionBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x900")
        self.title("VisionBoard")
        self.auth = AuthManager()

        # === HEADER BAR ===
        header_frame = tk.Frame(self, bg="#0D3E5B")
        header_frame.pack(side="top", fill="x")

        # App title
        title_label = tk.Label(
            header_frame,
            text="VISIONBOARD",
            font=("Helvetica", 24, "bold"),
            bg="#0D3E5B",
            fg="white"
        )
        title_label.pack(side="left", padx=50, pady=10)

        # Navigation container (center)
        self.nav_frame = tk.Frame(header_frame, bg="#0D3E5B")
        self.nav_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Navigation state
        self.nav_labels = {}
        self.nav_color_default = "white"
        self.nav_color_active = "#00FFFF"

        # === PAGE CONTAINER ===
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # === INITIALIZE PAGES ===
        self.frames = {}
        for F in (
            Home, About, Register, Profile,
            DefectA, DefectB, Components,
            DefectResult, LoadingPage
        ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Setup initial navigation (before login → Home + About)
        self.rebuild_nav([("Home", "Home"), ("About", "About")])

        # Start at Home
        self.show_frame("Home")

    # ---------------- NAV HELPERS ----------------
    def create_nav_label(self, text, page_name):
        """Create and store a single nav label in nav_frame."""
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

    def rebuild_nav(self, items):
        """Rebuild the top navigation bar with given items."""
        for lbl in list(self.nav_labels.values()):
            try:
                lbl.destroy()
            except Exception:
                pass
        self.nav_labels.clear()

        for text, page_name in items:
            self.create_nav_label(text, page_name)

        # Highlight current page if it exists
        cur = None
        for page in self.frames:
            if self.frames[page].winfo_ismapped():
                cur = page
                break
        if cur:
            self._update_nav_active(cur)

    def enable_post_login_nav(self):
        """After login → Profile + About"""
        self.rebuild_nav([("Profile", "Profile"), ("About", "About")])
        self.show_frame("Profile")

    def disable_post_logout_nav(self):
        """After logout → Home + About"""
        self.rebuild_nav([("Home", "Home"), ("About", "About")])
        self.show_frame("Home")

    # ---------------- PAGE NAVIGATION ----------------
    def show_frame(self, page_name):
        """Raise the page and call lifecycle hooks."""
        for f in self.frames.values():
            if hasattr(f, "on_hide"):
                try:
                    f.on_hide()
                except Exception:
                    pass

        frame = self.frames[page_name]

        if page_name == "Register" and hasattr(frame, "reset_fields"):
            frame.reset_fields()
        if page_name == "Profile" and hasattr(frame, "update_profile_info"):
            frame.update_profile_info()
        if hasattr(frame, "on_show"):
            frame.on_show()

        frame.tkraise()
        self._update_nav_active(page_name)

    def _update_nav_active(self, active_page):
        """Highlight the active nav link if present."""
        for page, lbl in list(self.nav_labels.items()):
            try:
                if page == active_page:
                    lbl.config(font=("Helvetica", 12, "bold", "underline"),
                               fg=self.nav_color_active)
                else:
                    lbl.config(font=("Helvetica", 12, "bold"),
                               fg=self.nav_color_default)
            except Exception:
                pass
