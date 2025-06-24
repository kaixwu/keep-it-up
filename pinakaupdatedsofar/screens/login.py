import tkinter as tk
from tkinter import messagebox, ttk
# from tkcalendar import Calendar, DateEntry # Not directly used here
# from datetime import datetime, date # Not directly used here
# import pytz # Not directly used here
# import matplotlib.pyplot as plt # Not directly used here
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Not directly used here
# from PIL import Image, ImageTk # Not directly used here
import re
import database # The two dots (..) mean "go up one directory" # Import your database service

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
            return

        user = database.validate_login(email, password)
        if user:
            self.controller.user = {"email": email, "name": "User"}
            self.controller.show_frame("DashboardPage")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def forgot_password(self):
        # Create a new Toplevel window for forgot password
        forgot_window = tk.Toplevel(self.controller)
        forgot_window.title("Forgot Password")
        forgot_window.transient(self.controller) # Make it modal
        forgot_window.grab_set() # Grab focus

        tk.Label(forgot_window, text="Enter your email to reset password:", font=("Arial", 12)).pack(pady=10)
        email_entry = tk.Entry(forgot_window, width=40, font=("Arial", 12))
        email_entry.pack(pady=5)

        def send_reset_link():
            email = email_entry.get().strip()
            if not email:
                messagebox.showwarning("Input Error", "Please enter your email.")
                return

            if not database.email_exists(email):
                messagebox.showerror("Error", "No account found with that email address.")
                return

            # In a real application, you would send an email with a reset link.
            # For this desktop app, we'll implement a direct password reset.
            messagebox.showinfo("Reset Password", f"If an account exists for {email}, you will be prompted to reset your password.")
            forgot_window.destroy() # Close the current window

            # Open a new window for password reset
            self._open_password_reset_window(email)

        tk.Button(forgot_window, text="Reset Password", command=send_reset_link,
                  bg="#FFB800", fg="white", font=("Arial", 12)).pack(pady=10)

        # Center the new window
        forgot_window.update_idletasks()
        x = self.controller.winfo_x() + (self.controller.winfo_width() // 2) - (forgot_window.winfo_width() // 2)
        y = self.controller.winfo_y() + (self.controller.winfo_height() // 2) - (forgot_window.winfo_height() // 2)
        forgot_window.geometry(f"+{x}+{y}")


    def _open_password_reset_window(self, email):
        """Opens a new window for the user to enter a new password."""
        reset_window = tk.Toplevel(self.controller)
        reset_window.title("Set New Password")
        reset_window.transient(self.controller)
        reset_window.grab_set()

        tk.Label(reset_window, text=f"Resetting password for: {email}", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(reset_window, text="New Password:", font=("Arial", 12)).pack(pady=5)
        new_password_entry = tk.Entry(reset_window, width=40, show="*", font=("Arial", 12))
        new_password_entry.pack(pady=5)

        tk.Label(reset_window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
        confirm_new_password_entry = tk.Entry(reset_window, width=40, show="*", font=("Arial", 12))
        confirm_new_password_entry.pack(pady=5)

        def set_new_password():
            new_password = new_password_entry.get()
            confirm_new_password = confirm_new_password_entry.get()

            # Re-use password validation from signup
            if len(new_password) < 8:
                messagebox.showerror("Weak Password", "Password must be at least 8 characters long.")
                return
            if not (any(c.isupper() for c in new_password) and
                    any(c.islower() for c in new_password) and
                    any(c.isdigit() for c in new_password)):
                messagebox.showerror("Weak Password", "Password must contain uppercase, lowercase, and numbers.")
                return
            if new_password != confirm_new_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            # === DATABASE INTEGRATION ===
            if database.update_user_password(email, new_password):
                messagebox.showinfo("Success", "Password has been reset successfully. You can now log in.")
                reset_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to reset password. Please try again.")

        tk.Button(reset_window, text="Set New Password", command=set_new_password,
                  bg="#FFB800", fg="white", font=("Arial", 12)).pack(pady=10)

        reset_window.update_idletasks()
        x = self.controller.winfo_x() + (self.controller.winfo_width() // 2) - (reset_window.winfo_width() // 2)
        y = self.controller.winfo_y() + (self.controller.winfo_height() // 2) - (reset_window.winfo_height() // 2)
        reset_window.geometry(f"+{x}+{y}")