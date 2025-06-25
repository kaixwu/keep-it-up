import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
import database
from utils import get_deadline_color

class AllTasksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.assignment_var = tk.StringVar(value="All")
        self.urgency_var = tk.StringVar(value="Urgent")
        self.build_ui()

    def build_ui(self):
        self.header = tk.Frame(self, bg='#F2B705', height=80)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)
        self.task_count_label = tk.Label(self.header, text="", font=("Arial", 22, "bold"),
                                         bg='#F2B705', fg='white')
        self.task_count_label.place(x=80, y=35)
        tk.Button(self.header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12),
                  padx=10, pady=5,
                  command=lambda: self.controller.show_frame("LoginPage")).place(
            relx=1.0, x=-20, y=30, anchor="ne")

        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')
        nav_pages = {'Home': 'DashboardPage', 'All Tasks': 'AllTasksPage',
                     'Calendar': 'CalendarPage', 'History': 'HistoryPage', 'Charts': 'ChartsPage'}
        for i, (label, page) in enumerate(nav_pages.items()):
            tk.Button(nav, text=label, font=("Arial", 12), width=20,
                      command=lambda p=page: self.controller.show_frame(p)).grid(
                row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

        filters = tk.Frame(self, bg='#FFE482')
        filters.pack(fill='x')
        assignment_options = ["All", "Assignment", "Task", "Quiz", "Exam"]
        assignment_menu = ttk.OptionMenu(filters, self.assignment_var,
                                         self.assignment_var.get(), *assignment_options,
                                         command=lambda _: self.update_task_display())
        assignment_menu.config(width=15)
        assignment_menu.pack(side='left', padx=5, pady=5)

        urgency_menu = ttk.OptionMenu(filters, self.urgency_var,
                                      self.urgency_var.get(), "Urgent", "Normal", "Low",
                                      command=lambda _: self.update_task_display())
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
        self.task_frame.bind("<Configure>",
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.update_task_display)

    def refresh_from_db(self):
        if self.controller.current_user:
            user_id = self.controller.current_user["id"]
            self.controller.task_data = database.get_all_tasks(user_id)
            self.update_task_display()

    def filter_tasks(self):
        cat = self.assignment_var.get()
        urg = self.urgency_var.get()
        tasks = self.controller.task_data or []
        filtered = [t for t in tasks if not t.get("completed") and (cat == "All" or t["category"] == cat)]

        def days_left(task):
            return (datetime.strptime(task["due_date"], "%Y-%m-%d").date() - date.today()).days

        filtered.sort(key=days_left, reverse=(urg == "Low"))
        return filtered

    def update_task_display(self, event=None):
        for w in self.task_frame.winfo_children():
            w.destroy()

        tasks = self.filter_tasks()
        self.task_count_label.config(text=f"{len(tasks)} tasks")

        width = self.canvas.winfo_width() or self.canvas.winfo_reqwidth()
        cols = max(1, width // 300)

        for idx, task in enumerate(tasks):
            row, col = divmod(idx, cols)
            frame = tk.Frame(self.task_frame, bg="#f0f0f0", bd=1, relief="solid", padx=10, pady=5)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.task_frame.grid_columnconfigure(col, weight=1)

            color = get_deadline_color(task["due_date"])
            tk.Frame(frame, width=10, height=100, bg=color).pack(side="left", fill="y")

            inner = tk.Frame(frame, bg="#f0f0f0")
            inner.pack(fill="both", expand=True, padx=10)
            tk.Label(inner, text=task['name'], font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
            tk.Label(inner, text=f"{task['due_date']}, {task['time']}", bg="#f0f0f0").pack(anchor="w")
            tk.Label(inner, text=task['category'], bg="#f0f0f0").pack(anchor="w")

            vars_list = []
            for sub in task.get('subtasks', []):
                var = tk.BooleanVar()
                tk.Checkbutton(inner, text=sub, bg="#f0f0f0", variable=var).pack(anchor="w")
                vars_list.append(var)

            btns = tk.Frame(inner, bg="#f0f0f0")
            btns.pack(anchor="e", pady=(5, 0))

            def complete_action(t=task, vars=vars_list):
                if vars and not all(v.get() for v in vars):
                    if not messagebox.askyesno("Confirm", "Some subtasks are not completed. Mark as done?"):
                        return
                database.update_task_completion(t["id"], True)
                self.refresh_from_db()
                self.controller.frames["DashboardPage"].refresh_dashboard()

            def delete_action(t=task):
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{t['name']}'?"):
                    database.delete_task(t["id"])
                    self.refresh_from_db()
                    self.controller.frames["DashboardPage"].refresh_dashboard()

            tk.Button(btns, text="✔", bg='green', fg='white', width=3,
                      font=("Arial", 11, "bold"), relief="raised", command=complete_action).pack(side="left", padx=2)
            tk.Button(btns, text="✎", bg='cornflowerblue', fg='white', width=3,
                      font=("Arial", 11, "bold"), relief="raised", command=lambda t=task: self.open_edit(t)).pack(side="left", padx=2)
            tk.Button(btns, text="🗑", bg='brown', fg='white', width=3,
                      font=("Arial", 11, "bold"), relief="raised", command=delete_action).pack(side="left", padx=2)
            tk.Button(btns, text="View Details", bg='gold', fg='black',
                      font=("Arial", 11, "bold"), relief="raised",
                      command=lambda: self.controller.show_frame("AllTasksPage")).pack(side="left", padx=2)

    def open_edit(self, task):
        idx = next((i for i, t in enumerate(self.controller.task_data) if t["id"] == task["id"]), None)
        if idx is not None:
            edit = self.controller.frames["EditTaskPage"]
            edit.load_task(task, idx)
            self.controller.show_frame("EditTaskPage")
