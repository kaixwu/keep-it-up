import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import re

class ChartsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        completed = 54
        in_progress = 27
        pending = 13
        total = completed + in_progress + pending
        header = tk.Frame(self, bg="#F2B705", height=80)
        header.pack(fill="x")
        avatar = tk.Canvas(header, width=60, height=60, bg="white", highlightthickness=0)
        avatar.create_oval(5, 5, 55, 55, fill="lightgrey")
        avatar.place(x=20, y=20)
        tk.Label(header, text="Keep It Up, [Name]!", bg="orange", fg="white", font=("Arial", 20, "bold")).place(x=100, y=30)
        logout_btn = tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12), padx=10, pady=5, command=lambda: self.controller.show_frame("LoginPage"))
        logout_btn.place(relx=1.0, x=-20, y=30, anchor="ne")
        nav = tk.Frame(self, bg="orange", pady=10)
        # NAVIGATION BAR
        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')

        # Correct label-to-page mapping
        nav_pages = {
            'Home': 'DashboardPage',
            'All Tasks': 'AllTasksPage',
            'Calendar': 'CalendarPage',
            'History': 'HistoryPage',
            'Charts': 'ChartsPage'
        }

        # Add buttons using .grid() for responsive alignment
        for i, (label, page) in enumerate(nav_pages.items()):
            tk.Button(
                nav,
                text=label,
                font=("Arial", 12),
                width=20,
                command=lambda p=page: self.controller.show_frame(p)
            ).grid(row=0, column=i, padx=5, pady=10, sticky="ew")

            nav.grid_columnconfigure(i, weight=1)  # Make each column expand equally

        body = tk.Frame(self, bg="white")
        body.pack(fill="both", expand=True, padx=20, pady=10)
        pie_frame = tk.Frame(body, bg="white")
        pie_frame.pack(side="left", fill="both", expand=True)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([completed, in_progress, pending], labels=["Completed", "In Progress", "Pending"], colors=["cornflowerblue", "gold", "orangered"], startangle=90, wedgeprops={"edgecolor": "black"})
        ax.axis("equal")
        canvas = FigureCanvasTkAgg(fig, master=pie_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=20, pady=20)
        progress_frame = tk.Frame(body, bg="white", relief="solid", bd=1)
        progress_frame.pack(side="right", fill="y", padx=10, pady=10)
        tk.Label(progress_frame, text="Progress", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        def make_stat(label, value, color):
            f = tk.Frame(progress_frame, bg="lightgrey", bd=1, relief="solid")
            f.pack(padx=10, pady=5, fill="x")
            tk.Label(f, text=label, bg="lightgrey", font=("Arial", 12, "bold")).pack(side="left", padx=10)
            tk.Label(f, text=str(value), bg=color, fg="white", width=5, font=("Arial", 12)).pack(side="right", padx=10)
        make_stat("Completed", completed, "green")
        make_stat("In Progress", in_progress, "orange")
        make_stat("Pending", pending, "brown")
        make_stat("Total Tasks", total, "cornflowerblue")