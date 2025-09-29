import tkinter as tk

class Register(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1E1E2F")
        self.controller = controller

        # === HEADER ===
        header_label = tk.Label(
            self,
            text="Create an Account",
            font=("Helvetica", 22, "bold"),
            bg="#1E1E2F",
            fg="white"
        )
        header_label.pack(pady=(40, 10))

        subtitle_label = tk.Label(
            self,
            text="Join VisionBoard to inspect your PCBs with ease.",
            font=("Helvetica", 14),
            bg="#1E1E2F",
            fg="#A9A9B8"
        )
        subtitle_label.pack(pady=(0, 20))

        # === MESSAGE LABEL (for errors/success) ===
        self.message_label = tk.Label(
            self,
            text="",
            bg="#1E1E2F",
            fg="red",
            font=("Helvetica", 11)
        )
        self.message_label.pack()

        # === FORM FRAME ===
        form_frame = tk.Frame(self, bg="#1E1E2F")
        form_frame.pack(pady=20)

        # Standard sizes
        input_width = 30
        input_ipady = 7  # vertical height

        # Username label and entry
        tk.Label(form_frame, text="Username", font=("Helvetica", 12),
                 bg="#1E1E2F", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=input_width,
                                       bg="#2C2C3E", fg="white", insertbackground="white", relief="flat")
        self.username_entry.pack(pady=(0, 10), ipady=input_ipady)

        # Email label and entry
        tk.Label(form_frame, text="Email", font=("Helvetica", 12),
                 bg="#1E1E2F", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        self.email_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=input_width,
                                    bg="#2C2C3E", fg="white", insertbackground="white", relief="flat")
        self.email_entry.pack(pady=(0, 10), ipady=input_ipady)

        # Password label and entry
        tk.Label(form_frame, text="Password", font=("Helvetica", 12),
                 bg="#1E1E2F", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=input_width, show="*",
                                       bg="#2C2C3E", fg="white", insertbackground="white", relief="flat")
        self.password_entry.pack(pady=(0, 10), ipady=input_ipady)

        # User Type label
        tk.Label(form_frame, text="User Type", font=("Helvetica", 12),
                bg="#1E1E2F", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))

        # Dropdown frame
        dropdown_frame = tk.Frame(form_frame, bg="#2C2C3E", width=input_width)
        dropdown_frame.pack(pady=(0, 20))

        options = ("Role", "Student", "Teacher")
        self.user_type_var = tk.StringVar(value=options[0])
        dropdown = tk.OptionMenu(dropdown_frame, self.user_type_var, *options)
        dropdown.config(
            bg="#2C2C3E",
            fg="gray",
            font=("Helvetica", 12),
            relief="flat",
            bd=0,
            highlightthickness=0,
            width=input_width-4,
            anchor="w"
        )
        dropdown["menu"].config(bg="#2C2C3E", fg="white", font=("Helvetica", 11))
        dropdown.pack(fill="x", ipady=input_ipady-4)

        # === REGISTER BUTTON ===
        register_btn = tk.Button(
            self,
            text="Register",
            command=self.attempt_register,
            bg="#3B82F6", fg="white",
            activebackground="#2563EB", activeforeground="white",
            relief="flat", font=("Helvetica", 13, "bold"),
            width=15, height=2, bd=0
        )
        register_btn.pack(pady=(0, 10))

        # === LOGIN LINK TEXT (centered) ===
        link_frame = tk.Frame(self, bg="#1E1E2F")
        link_frame.pack()

        tk.Label(link_frame,
                 text="Already have an account?",
                 font=("Helvetica", 11),
                 bg="#1E1E2F",
                 fg="white").pack(side="left")

        login_link = tk.Label(link_frame,
                              text=" Login",
                              font=("Helvetica", 11, "underline"),
                              bg="#1E1E2F",
                              fg="#3B82F6",
                              cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: controller.show_frame("Home"))

    # === REGISTER LOGIC ===
    def attempt_register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        if not username or not email or not password or user_type == "Role":
            self.message_label.config(text="All fields are required.", fg="red")
            return

        # ✅ Pass username into auth.register
        success, message = self.controller.auth.register(username, email, password, user_type)
        if success:
            self.message_label.config(text=message, fg="green")
            self.controller.show_frame("Home")
        else:
            self.message_label.config(text=message, fg="red")

    def reset_fields(self):
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.user_type_var.set("Role")
        self.message_label.config(text="")
