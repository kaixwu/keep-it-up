import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# --- PAGE CLASSES ---

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg="#FFB800", height=120)
        header.pack(fill="x")
        tk.Label(header, text="KEEP IT UP!", font=("Arial", 56, "bold"), bg="#FFB800", fg="white").pack(pady=(40, 10))
        tk.Label(header, text="We’re Here To Remind You Everyday!", font=("Arial", 22), bg="#FFB800", fg="white").pack()
        tk.Label(self, text="", bg="white").pack(pady=5)
        form_container = tk.Frame(self, bg="white")
        form_container.pack()
        form_frame = tk.Frame(form_container, bg="white")
        form_frame.grid(row=0, column=0, padx=40, pady=20)
        tk.Label(form_frame, text="Email Address", font=("Arial", 20), bg="white", width=15, anchor="e").grid(row=0, column=0, padx=10, pady=15)
        self.entry_email = tk.Entry(form_frame, font=("Arial", 18), bd=0, relief="flat")
        self.entry_email.grid(row=0, column=1, padx=10, pady=15)
        tk.Label(form_frame, text="Password", font=("Arial", 20), bg="white", width=15, anchor="e").grid(row=1, column=0, padx=10, pady=15)
        self.entry_password = tk.Entry(form_frame, font=("Arial", 18), bd=0, relief="flat", show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=15)
        tk.Button(self, text="Forgot Password?", font=("Arial", 16), fg="#FFB800", bd=0, bg="white", command=self.forgot_password).pack(pady=(5, 25))
        tk.Button(self, text="Log In", font=("Arial", 20), bg="#FFB800", fg="white", width=25, height=2, bd=0, command=self.login).pack(pady=10)
        footer = tk.Frame(self, bg="white")
        footer.pack(pady=30)
        tk.Label(footer, text="Don’t have an account?", font=("Arial", 16), bg="white").pack(side="left")
        tk.Button(footer, text="Sign Up", font=("Arial", 16), fg="#FFB800", bd=0, bg="white", command=lambda: self.controller.show_frame("SignUpPage")).pack(side="left")

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

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header_frame = tk.Frame(self, bg="#FFB800", height=120)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="SIGN UP", font=("Arial", 40, "bold"), fg="white", bg="#FFB800").pack(pady=(25, 0))
        tk.Label(header_frame, text="Create an account", font=("Arial", 14), fg="white", bg="#FFB800").pack()
        content_frame = tk.Frame(self, bg="white")
        content_frame.pack(expand=True)
        form_frame = tk.Frame(content_frame, bg="white")
        form_frame.pack()
        font_label = ("Arial", 15)
        font_entry = ("Arial", 15)
        def add_field_side_by_side(label_text, show=None):
            row = tk.Frame(form_frame, bg="white")
            row.pack(pady=12, padx=100)
            label = tk.Label(row, text=label_text, font=font_label, bg="white", anchor="w", width=18)
            label.pack(side="left")
            entry = tk.Entry(row, font=font_entry, width=35, relief="solid", bd=1, show=show)
            entry.pack(side="left", ipady=6, padx=5)
            entry.configure(highlightbackground="#ccc", highlightthickness=1, relief="flat")
            return entry
        self.entry_email = add_field_side_by_side("Email Address")
        self.entry_name = add_field_side_by_side("Name")
        self.entry_password = add_field_side_by_side("Password", show="*")
        self.entry_confirm = add_field_side_by_side("Confirm Password", show="*")
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=(25, 10))
        create_btn = tk.Button(
            btn_frame,
            text="Create Account",
            bg="#FFB800",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=10,
            relief="flat",
            bd=0,
            highlightthickness=0,
            command=self.create_account
        )
        create_btn.pack(ipady=3)
        create_btn.configure(borderwidth=0)
        footer_frame = tk.Frame(form_frame, bg="white")
        footer_frame.pack(pady=(20, 10))
        inner_footer = tk.Frame(footer_frame, bg="white")
        inner_footer.pack()
        tk.Label(inner_footer, text="Already have an account?", font=("Arial", 12), bg="white").pack(side="left", padx=(0, 5))
        login_link = tk.Label(inner_footer, text="Log In", font=("Arial", 12), fg="#FFB800", bg="white", cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.controller.show_frame("LoginPage"))

    def create_account(self):
        email = self.entry_email.get()
        name = self.entry_name.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm.get()
        if not email or not name or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        else:
            messagebox.showinfo("Success", "Account created successfully!")
            self.controller.show_frame("LoginPage")

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg='#F2B705', height=80)
        header.pack(fill='x')
        user_frame = tk.Frame(header, bg='#F2B705')
        user_frame.pack(side='left', padx=20, pady=10)
        tk.Label(user_frame, text="Welcome, [Name]", font=("Arial", 20, "bold"), bg='#F2B705', fg='white').pack(anchor='w')
        tk.Label(user_frame, text="emailaddress@domain.com", bg='#F2B705', fg='white').pack(anchor='w')
        tk.Button(header, text="Log Out", bg='#B30000', fg='white', width=10, height=2, command=lambda: self.controller.show_frame("LoginPage")).pack(side='right', padx=20, pady=10)
        main = tk.Frame(self)
        main.pack(fill='both', expand=True)
        left_panel = tk.Frame(main, width=250, bg='white')
        left_panel.pack(side='left', fill='y')
        tk.Button(left_panel, text="➕ Add Task To Do", bg='orange', fg='white', font=("Arial", 12), command=lambda: self.controller.show_frame("AddTaskPage")).pack(pady=10, padx=10, fill='x')
        tk.Label(left_panel, text="[Days] days left!\n[Task Name]\n[Due Date]", bg='green', fg='white', font=("Arial", 10), justify='left').pack(pady=10, padx=10, fill='x')
        tk.Button(left_panel, text="View Details", bg='gold', fg='black', command=lambda: self.controller.show_frame("AllTasksPage")).pack(pady=5, padx=20)
        tk.Label(left_panel, text="Weekly Progress", font=("Arial", 12)).pack(pady=(20, 5))
        tk.Label(left_panel, text="[Tasks Done]/[Total Weekly Task]", font=("Arial", 8)).pack()
        progress = ttk.Progressbar(left_panel, length=200, value=0)
        progress.pack(pady=5)
        tk.Label(left_panel, text="Calendar", fg='red', font=("Arial", 14, "bold")).pack(pady=(20, 5))
        cal = Calendar(left_panel, selectmode='day', year=date.today().year, month=date.today().month, day=date.today().day, date_pattern='yyyy-mm-dd')
        cal.pack(pady=10)
        right_panel = tk.Frame(main, bg='white')
        right_panel.pack(side='left', fill='both', expand=True)
        task_header = tk.Frame(right_panel, bg='#F2B705')
        task_header.pack(fill='x')
        tk.Label(task_header, text="[Count] tasks near deadline", font=("Arial", 16, "bold"), bg='#F2B705', fg='white').pack(side='left', padx=20)
        tk.Button(task_header, text="View All", bg='gold', command=lambda: self.controller.show_frame("AllTasksPage")).pack(side='right', padx=10, pady=5)
        for color in ['darkred', 'darkred', 'chocolate', 'gold']:
            self.create_task(right_panel, color)

    def create_task(self, parent, urgency_color):
        frame = tk.Frame(parent, bg='#f0f0f0', bd=1, relief='solid', padx=10, pady=5)
        frame.pack(padx=10, pady=5, fill='x')
        tk.Canvas(frame, width=20, height=20, bg=urgency_color).pack(side='left', padx=5)
        info = tk.Frame(frame, bg='#f0f0f0')
        info.pack(side='left', fill='x', expand=True)
        tk.Label(info, text="Task Name", font=("Arial", 12, "bold"), bg='#f0f0f0').pack(anchor='w')
        tk.Label(info, text="[Due Date], [Time]", bg='#f0f0f0').pack(anchor='w')
        tk.Label(info, text="[Task Category]", bg='#f0f0f0').pack(anchor='w')
        tk.Button(frame, text="✔", bg='green', fg='white', width=3).pack(side='left', padx=5)
        tk.Button(frame, text="✎", bg='cornflowerblue', fg='white', width=3, command=lambda: self.controller.show_frame("EditTaskPage")).pack(side='left', padx=5)
        tk.Button(frame, text="View Details", bg='gold', fg='black', command=lambda: self.controller.show_frame("AllTasksPage")).pack(side='left', padx=5)

class AddTaskPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg='#FFB800', height=150)
        header.pack(fill='x')
        tk.Label(header, text="ADD TASK", font=("Arial", 40, "bold"), bg='#FFB800', fg='white').pack(pady=30)
        form_frame = tk.Frame(self, padx=60, pady=30)
        form_frame.pack(fill='both', expand=True)
        label_font = ("Arial", 18)
        entry_font = ("Arial", 16)
        tk.Label(form_frame, text="Task Name", font=label_font, anchor='w').grid(row=0, column=0, sticky='w', pady=10)
        self.task_name_entry = tk.Entry(form_frame, width=60, font=entry_font)
        self.task_name_entry.grid(row=0, column=1, pady=10)
        tk.Label(form_frame, text="Description", font=label_font, anchor='nw').grid(row=1, column=0, sticky='nw', pady=10)
        self.description_text = tk.Text(form_frame, width=55, height=10, font=entry_font)
        self.description_text.grid(row=1, column=1, pady=10)
        tk.Label(form_frame, text="Task Category", font=label_font).grid(row=2, column=0, sticky='w', pady=10)
        self.task_category = ttk.Combobox(form_frame, values=["Work", "Study", "Personal", "Others"], width=58, font=entry_font)
        self.task_category.grid(row=2, column=1, pady=10)
        tk.Label(form_frame, text="Due Date", font=label_font).grid(row=3, column=0, sticky='w', pady=10)
        self.due_date = DateEntry(form_frame, width=56, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', font=entry_font)
        self.due_date.grid(row=3, column=1, pady=10)
        tk.Label(form_frame, text="Due Time", font=label_font).grid(row=4, column=0, sticky='w', pady=10)
        time_frame = tk.Frame(form_frame)
        time_frame.grid(row=4, column=1, pady=10, sticky='w')
        self.hour_var = tk.StringVar(value='12')
        self.minute_var = tk.StringVar(value='00')
        self.ampm_var = tk.StringVar(value='AM')
        hour_spinbox = ttk.Spinbox(time_frame, from_=1, to=12, wrap=True, textvariable=self.hour_var, width=5, font=entry_font, justify='center')
        hour_spinbox.pack(side='left')
        tk.Label(time_frame, text=":", font=entry_font).pack(side='left')
        minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f", textvariable=self.minute_var, width=5, font=entry_font, justify='center')
        minute_spinbox.pack(side='left')
        ampm_menu = ttk.Combobox(time_frame, values=['AM', 'PM'], textvariable=self.ampm_var, width=5, font=entry_font, justify='center')
        ampm_menu.pack(side='left', padx=10)
        tk.Label(form_frame, text="Time Zone", font=label_font).grid(row=5, column=0, sticky='w', pady=10)
        self.timezone_combobox = ttk.Combobox(form_frame, values=pytz.all_timezones, width=58, font=entry_font)
        self.timezone_combobox.grid(row=5, column=1, pady=10)
        self.timezone_combobox.set("Asia/Manila")
        button_frame = tk.Frame(self, pady=30)
        button_frame.pack()
        small_btn_font = ("Arial", 14)
        tk.Button(button_frame, text="Cancel", bg='darkred', fg='white', width=13, height=2, font=small_btn_font, command=lambda: self.controller.show_frame("DashboardPage")).pack(side='left', padx=40)
        tk.Button(button_frame, text="Add Task", bg='#FFB800', fg='white', width=13, height=2, font=small_btn_font, command=lambda: self.controller.show_frame("DashboardPage")).pack(side='left', padx=40)

class EditTaskPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg="#f5a800", height=80)
        header.pack(fill="x")
        tk.Label(header, text="EDIT TASK", bg="#f5a800", fg="white", font=("Arial", 24, "bold")).pack(pady=20)
        content = tk.Frame(self, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(content, text="Task Name", bg="white", anchor="w").pack(fill="x")
        self.task_name_entry = tk.Entry(content, font=("Arial", 12), relief="solid", bd=1)
        self.task_name_entry.pack(fill="x", pady=(0, 10))
        tk.Label(content, text="Description", bg="white", anchor="w").pack(fill="x")
        self.description_text = tk.Text(content, height=6, font=("Arial", 12), relief="solid", bd=1)
        self.description_text.pack(fill="x", pady=(0, 10))
        tk.Label(content, text="Task Category", bg="white", anchor="w").pack(fill="x")
        category_options = ["Assignment", "Project", "Exam", "Others"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(content, textvariable=self.category_var, values=category_options, state="readonly")
        self.category_dropdown.pack(fill="x", pady=(0, 10))
        tk.Label(content, text="Due Date", bg="white", anchor="w").pack(fill="x")
        date_frame = tk.Frame(content, bg="white")
        date_frame.pack(fill="x", pady=(0, 10))
        tk.Label(date_frame, text="📅", bg="white", font=("Arial", 12)).pack(side="left")
        self.due_date_entry = tk.Entry(date_frame, font=("Arial", 12), relief="solid", bd=1)
        self.due_date_entry.pack(fill="x", padx=5)
        tk.Label(content, text="Due Time", bg="white", anchor="w").pack(fill="x")
        time_frame = tk.Frame(content, bg="white")
        time_frame.pack(fill="x", pady=(0, 20))
        tk.Label(time_frame, text="⏰", bg="white", font=("Arial", 12)).pack(side="left")
        self.due_time_entry = tk.Entry(time_frame, font=("Arial", 12), relief="solid", bd=1)
        self.due_time_entry.pack(fill="x", padx=5)
        button_frame = tk.Frame(content, bg="white")
        button_frame.pack(pady=10, fill="x")
        cancel_btn = tk.Button(button_frame, text="Cancel", bg="darkred", fg="white", font=("Arial", 12, "bold"), command=lambda: self.controller.show_frame("DashboardPage"))
        cancel_btn.pack(side="left", expand=True, fill="x", padx=5)
        save_btn = tk.Button(button_frame, text="Save Edit", bg="orange", fg="white", font=("Arial", 12, "bold"), command=lambda: messagebox.showinfo("Saved", "Task has been updated."))
        save_btn.pack(side="left", expand=True, fill="x", padx=5)

class AllTasksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg="#f5a800", height=80)
        header.pack(fill="x")
        tk.Canvas(header, width=60, height=60, bg="white").place(x=10, y=10)
        tk.Label(header, text="[Total Tasks] Total Tasks", bg="#f5a800", font=("Arial", 20, "bold")).place(x=80, y=25)
        tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 10, "bold"), width=10, command=lambda: self.controller.show_frame("LoginPage")).place(relx=1.0, x=-100, y=25, anchor="ne")
        nav = tk.Frame(self, bg="white")
        nav.pack(pady=10)
        tk.Button(nav, text="All Tasks", width=15, command=lambda: self.controller.show_frame("AllTasksPage")).pack(side="left", padx=5)
        tk.Button(nav, text="Calendar", width=15, command=lambda: self.controller.show_frame("HistoryPage")).pack(side="left", padx=5)
        tk.Button(nav, text="History", width=15, command=lambda: self.controller.show_frame("HistoryPage")).pack(side="left", padx=5)
        tk.Button(nav, text="Charts", width=15, command=lambda: self.controller.show_frame("ChartsPage")).pack(side="left", padx=5)
        filters = tk.Frame(self, bg="white")
        filters.pack(pady=10)
        assignment_menu = tk.OptionMenu(filters, tk.StringVar(value="Assignment"), "Assignment", "Project", "Exam")
        assignment_menu.config(bg="#f5a800", fg="black", font=("Arial", 10, "bold"), width=12)
        assignment_menu.pack(side="left", padx=5)
        urgent_menu = tk.OptionMenu(filters, tk.StringVar(value="Urgent"), "Urgent", "Normal", "Low")
        urgent_menu.config(bg="#f5a800", fg="black", font=("Arial", 10, "bold"), width=12)
        urgent_menu.pack(side="left", padx=5)
        tk.Label(filters, text="7 tasks\n4 urgent", font=("Arial", 10)).pack(side="left", padx=10)
        tk.Button(filters, text="Add Task To Do", bg="orange", fg="white", font=("Arial", 10, "bold"), width=15, command=lambda: self.controller.show_frame("AddTaskPage")).pack(side="left", padx=5)
        task_section = tk.Frame(self, bg="white")
        task_section.pack(fill="both", expand=True, padx=10, pady=10)
        for color in ["red", "darkred", "orange", "gold"]:
            self.create_task(task_section, color, "Task Name")
        legend = tk.Frame(self, bg="white")
        legend.pack(side="bottom", pady=10)

    def create_task(self, frame, color, name="[Task Name]", due="[Due Date], [Time]", category="[Category]"):
        task_frame = tk.Frame(frame, bd=2, relief="groove", bg="white")
        task_frame.pack(fill="x", padx=5, pady=7)
        inner = tk.Frame(task_frame, bg="white")
        inner.pack(fill="x", padx=10, pady=5)
        circle = tk.Canvas(inner, width=30, height=30, bg="white", highlightthickness=0)
        circle.create_oval(5, 5, 25, 25, fill=color)
        circle.grid(row=0, column=0, rowspan=3, padx=5)
        tk.Label(inner, text=name, font=("Arial", 12, "bold"), bg="white").grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(inner, text=due, font=("Arial", 9), bg="white").grid(row=1, column=1, sticky="w", padx=10)
        tk.Label(inner, text=category, font=("Arial", 9), bg="white").grid(row=2, column=1, sticky="w", padx=10)
        button_frame = tk.Frame(inner, bg="white")
        button_frame.grid(row=0, column=2, rowspan=3, sticky="e", padx=10)
        tk.Button(button_frame, text="✓", bg="green", fg="white", width=3).pack(side="left", padx=3)
        tk.Button(button_frame, text="✎", bg="cornflowerblue", fg="white", width=3, command=lambda: self.controller.show_frame("EditTaskPage")).pack(side="left", padx=3)
        tk.Button(button_frame, text="View Details", bg="orange", fg="white", command=lambda: self.controller.show_frame("EditTaskPage")).pack(side="left", padx=3)

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg="#FDB813", height=100)
        header.pack(fill="x")
        profile = tk.Canvas(header, width=60, height=60, bg="#FDB813", highlightthickness=0)
        profile.create_oval(5, 5, 55, 55, fill="white")
        profile.place(x=20, y=20)
        tk.Label(header, text="[Total Tasks] Completed Tasks", bg="#FDB813", fg="white", font=("Arial", 22, "bold")).place(x=100, y=35)
        tk.Button(header, text="Log Out", bg="red", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="flat", command=lambda: self.controller.show_frame("LoginPage")).place(relx=0.93, y=30)
        nav = tk.Frame(self, bg="#FDB813")
        nav.pack(fill="x")
        for i, name in enumerate(["All Tasks", "Calendar", "History", "Charts"]):
            tk.Button(nav, text=name, font=("Arial", 12), bg="white", fg="black", width=15, relief="groove", bd=2, command=lambda n=name: self.controller.show_frame(n.replace(' ', '')+"Page")).grid(row=0, column=i, padx=20, pady=8)
        main = tk.Frame(self, bg="white")
        main.pack(padx=20, pady=10, fill="both", expand=True)
        left_frame = tk.Frame(main, bd=2, relief="groove", padx=15, pady=10)
        left_frame.grid(row=0, column=0, sticky="n")
        month_nav = tk.Frame(left_frame)
        month_nav.pack()
        tk.Label(month_nav, text="◄", font=("Arial", 20)).grid(row=0, column=0, padx=5)
        tk.Label(month_nav, text="JUNE 2025", font=("Arial", 18, "bold"), fg="red").grid(row=0, column=1, padx=5)
        tk.Label(month_nav, text="►", font=("Arial", 20)).grid(row=0, column=2, padx=5)
        calendar = Calendar(left_frame, selectmode="day", year=2025, month=6, day=1)
        calendar.pack(pady=10)
        right_frame = tk.Frame(main, bd=2, relief="groove", padx=15, pady=10)
        right_frame.grid(row=0, column=1, sticky="n")
        tk.Label(right_frame, text="Tasks on June 2025", font=("Arial", 18, "bold")).pack(anchor="w")
        sort_var = tk.IntVar()
        radio_frame = tk.Frame(right_frame)
        radio_frame.pack(anchor="w", pady=5)
        tk.Radiobutton(radio_frame, text="Most Recent", variable=sort_var, value=1).pack(side="left")
        tk.Radiobutton(radio_frame, text="Most Recent", variable=sort_var, value=2).pack(side="left")
        task_canvas = tk.Canvas(right_frame, width=600, height=430)
        task_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=task_canvas.yview)
        task_container = tk.Frame(task_canvas)
        task_container.bind("<Configure>", lambda e: task_canvas.configure(scrollregion=task_canvas.bbox("all")))
        task_canvas.create_window((0, 0), window=task_container, anchor="nw")
        task_canvas.configure(yscrollcommand=task_scrollbar.set)
        task_canvas.pack(side="left", fill="both", expand=True)
        task_scrollbar.pack(side="right", fill="y")
        sample_tasks = [
            {"name": "Task Name", "date": "June 10, 2025", "time": "10:00 AM", "category": "Work"},
            {"name": "Task Name", "date": "June 15, 2025", "time": "2:00 PM", "category": "Study"},
            {"name": "Task Name", "date": "June 18, 2025", "time": "5:00 PM", "category": "Personal"},
        ]
        for task in sample_tasks:
            box = tk.Frame(task_container, bg="#F5F5F5", bd=2, relief="groove", padx=10, pady=5)
            box.pack(pady=5, fill="x")
            tk.Label(box, text=task["name"], font=("Arial", 12, "bold"), bg="#F5F5F5").pack(anchor="w")
            tk.Label(box, text=f"[{task['date']}], [{task['time']}]\n[{task['category']}]", font=("Arial", 10), bg="#F5F5F5", justify="left").pack(anchor="w")
            tk.Button(box, text="View Details", bg="#FDB813", fg="black", font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5, width=12, command=lambda: self.controller.show_frame("EditTaskPage")).pack(anchor="e", pady=5)

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
        header = tk.Frame(self, bg="orange", height=100)
        header.pack(fill="x")
        avatar = tk.Canvas(header, width=60, height=60, bg="white", highlightthickness=0)
        avatar.create_oval(5, 5, 55, 55, fill="lightgrey")
        avatar.place(x=20, y=20)
        tk.Label(header, text="Keep It Up, [Name]!", bg="orange", fg="white", font=("Arial", 20, "bold")).place(x=100, y=30)
        logout_btn = tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12), padx=10, pady=5, command=lambda: self.controller.show_frame("LoginPage"))
        logout_btn.place(relx=1.0, x=-20, y=30, anchor="ne")
        nav = tk.Frame(self, bg="orange", pady=10)
        nav.pack(fill="x")
        nav_buttons = ["All Tasks", "Calendar", "History", "Charts"]
        for text in nav_buttons:
            tk.Button(nav, text=text, bg="white", font=("Arial", 12, "bold"), padx=20, pady=8, relief="solid", bd=1, command=lambda t=text: self.controller.show_frame(t.replace(' ', '')+"Page")).pack(side="left", padx=20)
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

# --- MAIN APP CONTROLLER ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keep It Up!")
        self.configure(bg="white")
        self.attributes('-fullscreen', True)  # Starts in fullscreen
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))  # Press Esc to exit fullscreen
        self.user = None
        self.tasks = []
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)
        self.frames = {}

        # Allow the page frames to expand fully
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (LoginPage, SignUpPage, DashboardPage, AddTaskPage, EditTaskPage, AllTasksPage, HistoryPage, ChartsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginPage")
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# --- RUN APP ---

if __name__ == "__main__":
    app = App()
    app.mainloop()