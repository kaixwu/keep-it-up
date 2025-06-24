import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import re

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # main layout frame
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)

        # === LEFT PANEL (Yellow Branding) ===
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
        password = self.entry_password.get()
        confirm_password = self.entry_confirm.get()

        # === VALIDATION ===
        if not email or not name or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Basic email format check using regex
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_pattern, email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        # Name should be alphabetic and at least 2 characters
        if len(name) < 2 or not all(c.isalpha() or c.isspace() for c in name):
            messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")
            return

        # Password should be strong enough (min 6 chars, contains digit and letter)
        if len(password) < 6:
            messagebox.showerror("Weak Password", "Password must be at least 6 characters long.")
            return
        if not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            messagebox.showerror("Weak Password", "Password must contain both letters and numbers.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # === SUCCESS ===
        messagebox.showinfo("Success", "Account created successfully!")
        self.controller.show_frame("LoginPage")
