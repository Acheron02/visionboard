import tkinter as tk
import json
import os
import hashlib

# --- Database Functions (using a local JSON file) ---
USERS_FILE = "users.json"


def load_user_data():
    """Loads user data from the JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_user_data(data):
    """Saves user data to the JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


# --- Main Application Class ---
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1600x900")
        self.title("VisionBoard")

        self.is_logged_in = False
        self.current_user = None

        # --- Title and Navigation Bar ---
        # A single frame to hold both the title and the navigation buttons
        header_frame = tk.Frame(self, bg="#0D3E5B")
        header_frame.pack(side="top", fill="x")

        # The application title with top and bottom padding and horizontal padding
        title_label = tk.Label(header_frame, text="VisionBoard", font=("Arial", 24, "bold"), bg="#0D3E5B", fg="white")
        title_label.pack(anchor="center", pady=(60, 10), padx=50)

        # A nested frame for the navigation buttons with top and bottom padding and horizontal padding
        nav_buttons_frame = tk.Frame(header_frame, bg="#0D3E5B")
        nav_buttons_frame.pack(anchor="center", pady=(10, 60), padx=50)

        home_button = tk.Button(nav_buttons_frame, text="Home", command=lambda: self._show_home_or_profile(), width=10,
                                height=3, font=("Arial", 12))
        home_button.pack(side="left", padx=5)

        about_button = tk.Button(nav_buttons_frame, text="About", command=lambda: self.show_frame("About"), width=10,
                                 height=3, font=("Arial", 12))
        about_button.pack(side="left", padx=5)

        # --- Content Area ---
        # This is the container for the different pages (Home, Login, Register, etc.)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Home, About, Login, Register, Profile, Camera, History):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        # Reset fields if navigating to Login or Register
        if page_name in ["Login", "Register"]:
            frame.reset_fields()
        frame.tkraise()
        # Update dynamic content on the profile page when it is shown
        if page_name == "Profile":
            frame.update_profile_info()

    def login_user(self, email, password):
        users = load_user_data()
        hashed_password = hash_password(password)
        if email in users and users[email]["password"] == hashed_password:
            self.is_logged_in = True
            self.current_user = {"email": email, **users[email]}
            self.show_frame("Profile")
            print("Login successful.")
            return True
        else:
            print("Invalid email or password.")
            return False

    def logout_user(self):
        self.is_logged_in = False
        self.current_user = None
        self.show_frame("Home")

    def delete_account(self):
        if self.current_user:
            users = load_user_data()
            del users[self.current_user["email"]]
            save_user_data(users)
            self.logout_user()
            print("Account deleted.")

    def _show_home_or_profile(self):
        if self.is_logged_in:
            self.show_frame("Profile")
        else:
            self.show_frame("Home")


class Home(tk.Frame):
    def __init__(self, parent, controller):
        # Set the background color for the main Home frame
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        # Header and welcome labels now have the same background color
        header_label = tk.Label(self, text="Home", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        welcome_label = tk.Label(self, text="Welcome to VisionBoard!", font=("Arial", 16), bg="#02517F", fg="white")
        welcome_label.pack(pady=20)

        # The button container also has the same background color
        button_frame = tk.Frame(self, bg="#02517F")
        button_frame.pack(pady=10)

        # Login button
        login_button = tk.Button(button_frame, text="Login", bg="#029DF7", fg="white",
                                 command=lambda: self.controller.show_frame("Login"),
                                 width=10, height=2, font=("Arial", 12))
        login_button.pack(side="left", padx=10)

        # Register button
        register_button = tk.Button(button_frame, text="Register", bg="#029DF7", fg="white",
                                    command=lambda: self.controller.show_frame("Register"), width=10, height=2,
                                    font=("Arial", 12))
        register_button.pack(side="left", padx=10)


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        # Header for the login form
        header_label = tk.Label(self, text="Login", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        # Error/Success message label
        self.message_label = tk.Label(self, text="", bg="#02517F", fg="red", font=("Arial", 10))
        self.message_label.pack()

        # Email field
        email_label = tk.Label(self, text="Email:", bg="#02517F", fg="white", font=("Arial", 12))
        email_label.pack(pady=(10, 0))
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=(0, 10))

        # Password field
        password_label = tk.Label(self, text="Password:", bg="#02517F", fg="white", font=("Arial", 12))
        password_label.pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=(0, 10))

        # Login button with consistent size
        login_button = tk.Button(self, text="Login", command=self.attempt_login, font=("Arial", 12), bg="#029DF7",
                                 fg="white", width=10, height=2)
        login_button.pack(pady=10)

        # Back button with consistent size
        back_button = tk.Button(self, text="Back to Home", command=lambda: self.controller.show_frame("Home"),
                                font=("Arial", 12), bg="#029DF7", fg="white", width=10, height=2)
        back_button.pack(pady=10)

    def attempt_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.controller.login_user(email, password):
            self.message_label.config(text="")  # Clear message on success
        else:
            self.message_label.config(text="Invalid email or password. Please try again.")

    def reset_fields(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.message_label.config(text="")


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        # Header for the registration form
        header_label = tk.Label(self, text="Register", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        # Error/Success message label
        self.message_label = tk.Label(self, text="", bg="#02517F", fg="red", font=("Arial", 10))
        self.message_label.pack()

        # Email field
        email_label = tk.Label(self, text="Email:", bg="#02517F", fg="white", font=("Arial", 12))
        email_label.pack(pady=(10, 0))
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=(0, 10))

        # Password field
        password_label = tk.Label(self, text="Password:", bg="#02517F", fg="white", font=("Arial", 12))
        password_label.pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=(0, 10))

        # User type selection with a dropdown menu
        options = ("---", "Student", "Teacher")
        self.user_type_var = tk.StringVar(value=options[0])

        user_type_dropdown = tk.OptionMenu(self, self.user_type_var, *options)
        user_type_dropdown.pack()

        # Register button with consistent size
        register_button = tk.Button(self, text="Register", command=self.attempt_register, font=("Arial", 12),
                                    bg="#029DF7", fg="white", width=10, height=2)
        register_button.pack(pady=10)

        # Back button with consistent size
        back_button = tk.Button(self, text="Back to Home", command=lambda: self.controller.show_frame("Home"),
                                font=("Arial", 12), bg="#029DF7", fg="white", width=10, height=2)
        back_button.pack(pady=10)

    def attempt_register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        users = load_user_data()
        if email in users:
            self.message_label.config(text="Email already exists.")
            return

        if not email or not password or user_type == "---":
            self.message_label.config(text="All fields are required.")
            return

        users[email] = {
            "password": hash_password(password),
            "user_type": user_type
        }
        save_user_data(users)
        self.message_label.config(text="Registration successful!", fg="green")
        self.controller.show_frame("Login")

    def reset_fields(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.user_type_var.set("---")
        self.message_label.config(text="")


class Profile(tk.Frame):
    def __init__(self, parent, controller):
        # Set the background color for the main Profile frame
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        # Header and welcome labels now have the same background color
        header_label = tk.Label(self, text="Profile Page", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        content_label = tk.Label(self, text="Welcome to your profile!", font=("Arial", 16), bg="#02517F", fg="white")
        content_label.pack(pady=20)

        self.user_type_label = tk.Label(self, text="", font=("Arial", 14), bg="#02517F", fg="white")
        self.user_type_label.pack(pady=(0, 20))

        # Container for the Camera and History buttons with matching background
        button_frame = tk.Frame(self, bg="#02517F")
        button_frame.pack(pady=10)

        # Camera button with new color and consistent size
        camera_button = tk.Button(button_frame, text="Camera", width=10, height=2, font=("Arial", 12), bg="#029DF7",
                                  fg="white", command=lambda: self.controller.show_frame("Camera"))
        camera_button.pack(side="left", padx=10)

        # History button with new color and consistent size
        history_button = tk.Button(button_frame, text="History", width=10, height=2, font=("Arial", 12), bg="#029DF7",
                                   fg="white", command=lambda: self.controller.show_frame("History"))
        history_button.pack(side="left", padx=10)

        # Logout button with consistent size
        logout_button = tk.Button(self, text="Log Out", width=10, height=2, font=("Arial", 12), bg="#029DF7",
                                  fg="white", command=lambda: self.controller.logout_user())
        logout_button.pack(pady=10)

        # Delete Account button
        delete_button = tk.Button(self, text="Delete", width=10, height=2, font=("Arial", 12), bg="#029DF7", fg="white",
                                  command=lambda: self.controller.delete_account())
        delete_button.pack(pady=10)

    def update_profile_info(self):
        if self.controller.current_user:
            user_type = self.controller.current_user.get("user_type", "N/A")
            self.user_type_label.config(text=f"User Type: {user_type}")
        else:
            self.user_type_label.config(text="")


class Camera(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        header_label = tk.Label(self, text="Camera", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        back_button = tk.Button(self, text="Back to Profile", command=lambda: self.controller.show_frame("Profile"),
                                font=("Arial", 12), bg="#029DF7", fg="white", width=15, height=2)
        back_button.pack(pady=10)


class History(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        header_label = tk.Label(self, text="History", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        back_button = tk.Button(self, text="Back to Profile", command=lambda: self.controller.show_frame("Profile"),
                                font=("Arial", 12), bg="#029DF7", fg="white", width=15, height=2)
        back_button.pack(pady=10)


class About(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#02517F")
        self.controller = controller

        # Header for the about page
        header_label = tk.Label(self, text="About", font=("Arial", 18, "bold"), bg="#02517F", fg="white")
        header_label.pack(pady=(60, 10))

        label = tk.Label(self, text="About Page", font=("Arial", 16), bg="#02517F", fg="white")
        label.pack(pady=10)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
