import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
import pytz
from PIL import Image, ImageTk
from utils import get_deadline_color

class AllTasksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.assignment_var = tk.StringVar(value="All")
        self.urgency_var = tk.StringVar(value="Urgent")


        self.build_ui()

    def build_ui(self):
        self.header = tk.Frame(self, bg='#F2B705', height=80)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)
        self.task_count_label = tk.Label(self.header, text="", font=("Arial", 22, "bold"), bg='#F2B705', fg='white')
        self.task_count_label.place(x=80, y=35)
        tk.Button(self.header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12), padx=10, pady=5,
                  command=lambda: self.controller.show_frame("LoginPage")).place(relx=1.0, x=-20, y=30, anchor="ne")

        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')
        nav_pages = {'Home': 'DashboardPage', 'All Tasks': 'AllTasksPage', 'Calendar': 'CalendarPage', 'History': 'HistoryPage', 'Charts': 'ChartsPage'}
        for i, (label, page) in enumerate(nav_pages.items()):
            tk.Button(nav, text=label, font=("Arial", 12), width=20, command=lambda p=page: self.controller.show_frame(p)).grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

        filters = tk.Frame(self, bg='#FFE482')
        filters.pack(fill='x')
        assignment_options = ["All", "Assignment", "Task", "Quiz", "Exam"]
        assignment_menu = ttk.OptionMenu(filters, self.assignment_var, self.assignment_var.get(), *assignment_options, command=lambda _: self.update_task_display())
        assignment_menu.config(width=15)
        assignment_menu.pack(side='left', padx=5, pady=5)
        urgency_menu = ttk.OptionMenu(filters, self.urgency_var, self.urgency_var.get(), "Urgent", "Normal", "Low", command=lambda _: self.update_task_display())
        urgency_menu.config(width=12)
        urgency_menu.pack(side='left', padx=5, pady=5)
        tk.Button(filters, text="➕ Add Task To Do", bg='cornflowerblue', fg='white', width=18,
                  command=lambda: self.controller.show_frame("AddTaskPage")).pack(side='right', padx=10, pady=5)

        self.main = tk.Frame(self, bg="white")
        self.main.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.main, bg="white")
        self.scrollbar = ttk.Scrollbar(self.main, orient="vertical", command=self.canvas.yview)
        self.task_frame = tk.Frame(self.canvas, bg="white")

        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.update_task_display)

        self.update_task_display()


    def filter_tasks(self):
        category = self.assignment_var.get()
        urgency = self.urgency_var.get()

        tasks = getattr(self.controller, "task_data", [])
        filtered = [t for t in tasks if not t.get("completed") and (category == "All" or t["category"] == category)]

        def sort_key(task):
            days_left = (datetime.strptime(task["due_date"], "%Y-%m-%d").date() - date.today()).days
            return days_left

        if urgency == "Low":
            filtered.sort(key=sort_key, reverse=True)  # farthest deadline first
        else:
            filtered.sort(key=sort_key)  # soonest deadline first

        return filtered

    def edit_task(self, task, index):
        edit_page = self.controller.frames["EditTaskPage"]
        edit_page.load_task(task, index)
        self.controller.show_frame("EditTaskPage")

    def update_task_display(self, event=None):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        filtered_tasks = self.filter_tasks()
        self.task_count_label.config(text=f"{len(filtered_tasks)} tasks")

        width = self.canvas.winfo_width()
        column_count = max(1, width // 300)

        for index, task in enumerate(filtered_tasks):
            col = index % column_count
            row = index // column_count

            frame = tk.Frame(self.task_frame, bg="#f0f0f0", bd=1, relief="solid", padx=10, pady=5)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.task_frame.grid_columnconfigure(col, weight=1)

            color = get_deadline_color(task["due_date"])
            tk.Frame(frame, width=10, height=100, bg=color).pack(side="left", fill="y")

            inner = tk.Frame(frame, bg="#f0f0f0")
            inner.pack(fill="both", expand=True, padx=10)

            tk.Label(inner, text=task['name'], font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
            tk.Label(inner, text=f"{task['due_date']}, {task['time']}", bg="#f0f0f0").pack(anchor="w")
            tk.Label(inner, text=f"{task['category']}", bg="#f0f0f0").pack(anchor="w")

            subtask_vars = []
            for sub in task['subtasks']:
                var = tk.BooleanVar()
                tk.Checkbutton(inner, text=sub, bg="#f0f0f0", variable=var).pack(anchor="w")
                subtask_vars.append(var)

            btns = tk.Frame(inner, bg="#f0f0f0")
            btns.pack(anchor="e")

            def complete_action(task=task, vars=subtask_vars):
                if not all(v.get() for v in vars):
                    if not messagebox.askyesno("Confirm", "Some subtasks are not completed. Mark main task as done?"):
                        return
                task['completed'] = True
                self.update_task_display()

            tk.Button(btns, text="✔", bg='green', fg='white', width=3, command=complete_action).pack(side='left', padx=2)
            tk.Button(btns, text="✎", bg='cornflowerblue', fg='white', width=3,
                      command=lambda t=task, i=index: self.edit_task(t, i)).pack(side='left', padx=2)
            tk.Button(btns, text="View Details", bg='gold', fg='black',
                      command=lambda: self.controller.show_frame("AllTasksPage")).pack(side='left', padx=2)
