import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import re

#Log In Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.configure(bg="white")

        # Main container with two sections: left (branding) and right (form)
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)

        # Left panel
        left_panel = tk.Frame(main_frame, bg="#FFB800", width=450)
        left_panel.pack(side="left", fill="both")

        branding_container = tk.Frame(left_panel, bg="#FFB800")
        branding_container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(branding_container, text="KEEP IT\nUP!",
                 font=("Arial", 48, "bold"),
                 fg="white",
                 bg="#FFB800",
                 justify="left").pack(anchor="w")
        tk.Label(branding_container, text="We’re Here To Remind You Everyday!",
                 font=("Arial", 12),
                 fg="white",
                 bg="#FFB800").pack(anchor="w", pady=(10, 0))

        # Right panel
        right_panel = tk.Frame(main_frame, bg="white")
        right_panel.pack(side="left", fill="both", expand=True)

        # Container to center all form elements in the right panel
        form_container = tk.Frame(right_panel, bg="white")
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        # Email Label and Entry
        (tk.Label(form_container,
                 text="Email Address",
                 font=("Arial", 14),
                 bg="white",
                 anchor="w").pack(fill="x", pady=(0, 5)))

        self.entry_email = tk.Entry(form_container, font=("Arial", 14),
                                    relief="solid",
                                    bd=1,
                                    width=50)
        self.entry_email.pack(fill="x", pady=(0, 20), ipady=8)

        # Password Label and Entry
        tk.Label(form_container, text="Password",
                 font=("Arial", 14),
                 bg="white",
                 anchor="w").pack(fill="x", pady=(0, 5))

        self.entry_password = tk.Entry(form_container, font=("Arial", 14),
                                       relief="solid",
                                       bd=1,
                                       show="*",
                                       width=50)
        self.entry_password.pack(fill="x", pady=(0, 10), ipady=8)

        # Forgot Password
        tk.Button(form_container, text="Forgot Password?",
                  font=("Arial", 12),
                  fg="#FFB800",
                  bg="white",
                  bd=0,
                  command=self.forgot_password).pack(anchor="e", pady=(0, 20))

        # Log In Button
        tk.Button(form_container, text="Log In",
                  font=("Arial", 16),
                  bg="#FFB800",
                  fg="white",
                  height=2,
                  bd=0,
                  command=self.login).pack(fill="x", pady=(0, 20))

        # Sign Up Footer
        footer_frame = tk.Frame(form_container, bg="white")
        footer_frame.pack()
        tk.Label(footer_frame, text="Don’t have an account?",
                 font=("Arial", 12), bg="white").pack(side="left")
        tk.Button(footer_frame, text="Sign Up",
                  font=("Arial", 12),
                  fg="#FFB800",
                  bg="white",
                  bd=0,
                  command=lambda: self.controller.show_frame("SignUpPage")).pack(side="left")

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
        else:
            self.controller.user = {"email": email, "name": "User"}
            self.controller.show_frame("DashboardPage")

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Password recovery not implemented yet.")
