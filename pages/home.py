import tkinter as tk

class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1E1E2F")
        self.controller = controller

        # === HEADER ===
        header_label = tk.Label(
            self,
            text="VisionBoard",
            font=("Helvetica", 22, "bold"),
            bg="#1E1E2F",
            fg="white"
        )
        header_label.pack(pady=(40, 10))

        subtitle_label = tk.Label(
            self,
            text="Inspect your fabricated PCBs with ease.",
            font=("Helvetica", 14),
            bg="#1E1E2F",
            fg="#A9A9B8"
        )
        subtitle_label.pack(pady=(0, 30))

        # === LOGIN FORM ===
        form_frame = tk.Frame(self, bg="#1E1E2F")
        form_frame.pack(pady=20)

        # Username/Email label on top
        tk.Label(form_frame, text="Username/Email", font=("Helvetica", 12),
                 bg="#1E1E2F", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30,
                                  bg="#2C2C3E", fg="white", insertbackground="white", relief="flat")
        username_entry.pack(pady=(0, 10), ipady=5)

        # Password label on top
        tk.Label(form_frame, text="Password", font=("Helvetica", 12),
                 bg="#1E1E2F", fg="white", anchor="w").pack(anchor="w", pady=(0, 2))
        password_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30, show="*",
                                  bg="#2C2C3E", fg="white", insertbackground="white", relief="flat")
        password_entry.pack(pady=(0, 20), ipady=5)

        # === LOGIN FUNCTION ===
        def login_action(event=None):
            controller.show_frame("Profile")

        # === LOGIN BUTTON (centered) ===
        login_btn = tk.Button(
            self,
            text="Login",
            command=login_action,
            bg="#3B82F6", fg="white",
            activebackground="#2563EB", activeforeground="white",
            relief="flat", font=("Helvetica", 13, "bold"),
            width=15, height=2, bd=0
        )
        login_btn.pack(pady=(0, 15))

        # Bind Enter key
        self.bind_all("<Return>", login_action)

        # === REGISTER LINK (centered under button) ===
        link_frame = tk.Frame(self, bg="#1E1E2F")
        link_frame.pack()

        tk.Label(link_frame,
                 text="Don't have an account?",
                 font=("Helvetica", 11),
                 bg="#1E1E2F",
                 fg="white").pack(side="left")

        register_link = tk.Label(link_frame,
                                 text=" Register",
                                 font=("Helvetica", 11, "underline"),
                                 bg="#1E1E2F",
                                 fg="#3B82F6",
                                 cursor="hand2")
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: controller.show_frame("Register"))
