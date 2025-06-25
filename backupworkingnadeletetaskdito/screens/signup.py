import tkinter as tk
import database
from tkinter import messagebox
import re

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)

        # === LEFT PANEL (Branding) ===
        left_panel = tk.Frame(main_frame, bg="#FFB800", width=450)
        left_panel.pack(side="left", fill="both")

        branding_container = tk.Frame(left_panel, bg="#FFB800")
        branding_container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(branding_container, text="SIGN UP!",
                 font=("Arial", 48, "bold"),
                 fg="white",
                 bg="#FFB800").pack(anchor="w")
        tk.Label(branding_container, text="Create an account and Keep It Up!",
                 font=("Arial", 12),
                 fg="white",
                 bg="#FFB800",
                 pady=10).pack(anchor="w")

        # === RIGHT PANEL (Form) ===
        right_panel = tk.Frame(main_frame, bg="white")
        right_panel.pack(side="left", fill="both", expand=True)

        form_container = tk.Frame(right_panel, bg="white", width=480)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        font_label = ("Arial", 14)
        font_entry = ("Arial", 14)

        def add_field(label_text, show=None):
            row = tk.Frame(form_container, bg="white")
            row.pack(fill="x", pady=10)

            tk.Label(row, text=label_text,
                     font=font_label,
                     bg="white",
                     anchor="w",
                     width=18).pack(side="left")
            entry = tk.Entry(row, font=font_entry,
                             relief="solid",
                             bd=1,
                             show=show,
                             width=35)
            entry.pack(side="left", ipady=6)
            return entry

        self.entry_email = add_field("Email Address")
        self.entry_name = add_field("Name")
        self.entry_password = add_field("Password", show="*")
        self.entry_confirm = add_field("Confirm Password", show="*")

        # === CREATE ACCOUNT BUTTON ===
        create_btn = tk.Button(
            form_container,
            text="Create Account",
            bg="#FFB800",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="flat",
            bd=0,
            width=46,
            padx=20,
            pady=10,
            command=self.create_account
        )
        create_btn.pack(pady=(20, 10), anchor="center")

        # === FOOTER ===
        footer = tk.Frame(form_container, bg="white")
        footer.pack(pady=(10, 0))

        tk.Label(footer, text="Already have an account?",
                 font=("Arial", 12),
                 bg="white").pack(side="left", padx=(0, 5))
        login_link = tk.Label(footer, text="Log In",
                              font=("Arial", 12),
                              fg="#FFB800",
                              bg="white",
                              cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.controller.show_frame("LoginPage"))

    def create_account(self):
        email = self.entry_email.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_password.get().strip()
        confirm = self.entry_confirm.get().strip()

        if not email or not name or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if database.email_exists(email):
            messagebox.showerror("Error", "Email already registered.")
            return

        database.create_user(email, password, name)
        messagebox.showinfo("Success", "Account created successfully!")
        self.controller.show_frame("LoginPage")
