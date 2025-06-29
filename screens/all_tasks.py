import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, date
import database
from utils import get_deadline_color

class AllTasksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.assignment_var = tk.StringVar(value="All")
        self.urgency_var = tk.StringVar(value="Urgent")
        self.selected_date = None
        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg='#F2B705', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        self.task_count_label = tk.Label(header, text="", font=("Arial", 22, "bold"),
                                         bg='#F2B705', fg='white')
        self.task_count_label.place(x=80, y=35)
        tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12),
                  command=lambda: self.controller.show_frame("LoginPage")).place(relx=1.0, x=-20, y=30, anchor="ne")

        # Navbar
        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')
        pages = {'Home': 'DashboardPage', 'All Tasks': 'AllTasksPage', 'History': 'HistoryPage', 'Charts': 'ChartsPage'}
        for i, (label, page) in enumerate(pages.items()):
            tk.Button(nav, text=label, font=("Arial", 12), width=20,
                      command=lambda p=page: self.controller.show_frame(p)).grid(
                row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

        # Main Content Layout
        main = tk.Frame(self, bg="white")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # --- LEFT SIDE (calendar + counters) ---
        left = tk.Frame(main, bg="white")
        left.grid(row=0, column=0, sticky="ns", padx=10)

        self.calendar = Calendar(left)
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_date_selected)
        self.calendar.bind("<<CalendarMonthChanged>>", lambda e: self.clear_calendar_date())

        self.left_summary_frame = tk.Frame(left, bg="white")
        self.left_summary_frame.pack(pady=10, fill="x")
        self.draw_pending_tiles(self.left_summary_frame)

        # --- RIGHT SIDE (filters + task grid) ---
        right = tk.Frame(main, bg="white", bd=2, relief="groove")
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        filter_bar = tk.Frame(right, bg="white")
        filter_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        ttk.Label(filter_bar, text="Category:", background="white").pack(side="left")
        assignment_options = ["All", "Assignment", "Task", "Quiz", "Exam"]
        assignment_menu = ttk.OptionMenu(filter_bar, self.assignment_var,
                                         self.assignment_var.get(), *assignment_options,
                                         command=lambda _: self.update_task_display())
        assignment_menu.pack(side='left', padx=5)

        ttk.Label(filter_bar, text="Urgency:", background="white").pack(side="left")
        urgency_menu = ttk.OptionMenu(filter_bar, self.urgency_var,
                                      self.urgency_var.get(), "Urgent", "Normal", "Low",
                                      command=lambda _: self.update_task_display())
        urgency_menu.pack(side='left', padx=5)

        tk.Button(filter_bar, text="Clear", bg="gray", fg="white", font=("Arial", 10, "bold"),
                  command=self.clear_filters).pack(side="left", padx=10)

        tk.Button(filter_bar, text="➕ Add Task To Do", bg='cornflowerblue', fg='white', width=18,
                  command=lambda: self.controller.show_frame("AddTaskPage")).pack(side='right', padx=10)

        # Scrollable Task Display Area
        self.canvas = tk.Canvas(right, bg="white")
        self.scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        self.task_frame = tk.Frame(self.canvas, bg="white")

        self.task_window = self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.resize_task_frame)

    def resize_task_frame(self, event):
        self.canvas.itemconfig(self.task_window, width=event.width)

    def clear_filters(self):
        self.selected_date = None
        self.assignment_var.set("All")
        self.urgency_var.set("Urgent")
        self.update_task_display()

    def on_calendar_date_selected(self, event):
        self.selected_date = self.calendar.selection_get()
        self.update_task_display()

    def clear_calendar_date(self):
        self.selected_date = None
        self.update_task_display()

    def draw_pending_tiles(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()  # Clear existing tiles

        categories = ["Quiz", "Assignment", "Exam", "Task"]
        category_counts = {cat: 0 for cat in categories}

        for task in self.controller.task_data:
            if not task.get("completed") and task.get("category") in category_counts:
                category_counts[task["category"]] += 1

        for cat in categories:
            frame = tk.Frame(parent, bg="gold", height=40)
            frame.pack(fill="x", padx=5, pady=3)
            frame.pack_propagate(False)
            inner = tk.Frame(frame, bg="white")
            inner.pack(fill="both", expand=True, padx=2, pady=2)
            tk.Label(inner, text=f"[{category_counts[cat]}]", bg="white", font=("Arial", 12, "bold")).pack(side="left",
                                                                                                           padx=5)
            tk.Label(inner, text=f"Pending {cat}", bg="white", font=("Arial", 12)).pack(side="left")

    def refresh_from_db(self):
        if self.controller.current_user:
            user_id = self.controller.current_user["id"]
            self.controller.task_data = database.get_all_tasks(user_id)

            # Force refresh counters
            self.update_task_display()
            self.draw_pending_tiles(self.left_summary_frame)  # ← Ensure correct parent frame

    def filter_tasks(self):
        cat = self.assignment_var.get()
        urg = self.urgency_var.get()
        tasks = self.controller.task_data or []

        # Apply filters
        filtered = [
            t for t in tasks
            if not t.get("completed")
            and (cat == "All" or t["category"] == cat)
            and (not self.selected_date or t["due_date"] == self.selected_date.strftime("%Y-%m-%d"))
        ]

        # Sort by urgency
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
                      command=lambda t=task: self.open_view_details(t)).pack(side="left", padx=2)

    def open_edit(self, task):
        idx = next((i for i, t in enumerate(self.controller.task_data) if t["id"] == task["id"]), None)
        if idx is not None:
            edit = self.controller.frames["EditTaskPage"]
            edit.load_task(task, idx)
            self.controller.show_frame("EditTaskPage")

    def open_view_details(self, task):
        self.controller.frames["TaskDetailsPage"].load_task(task)
        self.controller.show_frame("TaskDetailsPage")
