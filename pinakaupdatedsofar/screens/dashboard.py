import tkinter as tk
from tkinter import ttk
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.build_header()
        self.build_navbar()
        self.build_main_content()

    def build_header(self):
        header = tk.Frame(self, bg='#F2B705', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header, text="Keep it up, [Name]", font=("Arial", 22, "bold"), bg='#F2B705', fg='white').place(x=10, y=15)
        tk.Label(header, text="emailaddress@domain.com", bg='#F2B705', fg='white').place(x=10, y=50)
        tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12),
                  command=lambda: self.controller.show_frame("LoginPage")).place(relx=1.0, x=-20, y=30, anchor="ne")

    def build_navbar(self):
        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')
        nav_pages = {'Home': 'DashboardPage', 'All Tasks': 'AllTasksPage', 'Calendar': 'CalendarPage', 'History': 'HistoryPage', 'Charts': 'ChartsPage'}
        for i, (label, page) in enumerate(nav_pages.items()):
            tk.Button(nav, text=label, font=("Arial", 12), width=20, command=lambda p=page: self.controller.show_frame(p)).grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

    def build_main_content(self):
        content = tk.Frame(self, bg="white")
        content.pack(fill="both", expand=True)

        self.left_panel = tk.Frame(content, bg="white")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_panel = tk.Frame(content, bg="white")
        self.right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        self.pie_chart_frame = tk.Frame(self.left_panel, bg="white", bd=2, relief="solid")
        self.pie_chart_frame.pack(fill="x", padx=10, pady=10)
        self.draw_pie_chart()

        summary_frame = tk.Frame(self.left_panel, bg="white")
        summary_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.draw_task_summary(parent=summary_frame)

        pending_frame = tk.Frame(self.left_panel, bg="white")
        pending_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.draw_pending_tiles(parent=pending_frame)

    def draw_pie_chart(self):
        for widget in self.pie_chart_frame.winfo_children():
            widget.destroy()

        completed = sum(1 for t in self.controller.task_data if t.get("completed"))
        pending = sum(1 for t in self.controller.task_data if not t.get("completed"))

        fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=100)

        if completed == 0 and pending == 0:
            ax.pie([1], colors=["lightgray"])
        else:
            ax.pie([completed, pending], colors=["green", "brown"])

        ax.axis('equal')
        canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_task_summary(self, parent):
        total = len(self.controller.task_data)
        completed = sum(t.get("completed", False) for t in self.controller.task_data)
        pending = total - completed

        def summary_box(color, count, label):
            frame = tk.Frame(parent, bg=color, height=30)
            frame.pack(fill="x", padx=5, pady=2)
            frame.pack_propagate(False)
            tk.Label(frame, text=f"{count}  {label}", fg="white", bg=color, font=("Arial", 12, "bold")).pack(anchor="w",
                                                                                                             padx=10)
        summary_box("steelblue", total, "All Tasks")
        summary_box("seagreen", completed, "Completed")
        summary_box("firebrick", pending, "Pending")

    def draw_pending_tiles(self, parent):
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

    def build_right_panel(self):
        header_frame = tk.Frame(self.right_panel, bg='#F2B705')
        header_frame.pack(fill='x', pady=5)
        total_tasks = len(self.controller.task_data)
        near_deadline_tasks = len(self.get_tasks_near_deadline())

        tk.Label(header_frame, text=f"{near_deadline_tasks} tasks near deadline", font=("Arial", 12), bg='#F2B705', fg='white').pack(side='left', padx=10)

        tk.Button(header_frame, text="➕ Add Task To Do", bg='cornflowerblue', fg='white', width=18, command=lambda: self.controller.show_frame("AddTaskPage")).pack(side='right', padx=10, pady=5)

        # Scrollable task display
        canvas = tk.Canvas(self.right_panel, bg="white")
        scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=canvas.yview)
        self.task_frame = tk.Frame(canvas, bg="white")

        canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.display_near_deadline_tasks()

    def get_tasks_near_deadline(self):
        today = date.today()
        upcoming = []
        for task in self.controller.task_data:
            if not task.get("completed"):
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                days_left = (due_date - today).days
                if 0 <= days_left <= 3:
                    upcoming.append(task)
        return upcoming

    def display_near_deadline_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        tasks = self.get_tasks_near_deadline()
        for i, task in enumerate(tasks):
            frame = tk.Frame(self.task_frame, bg="#f0f0f0", bd=1, relief="solid", padx=10, pady=5)
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            self.task_frame.grid_columnconfigure(i%2, weight=1)

            color = "darkred"
            tk.Frame(frame, width=10, height=100, bg=color).pack(side="left", fill="y")

            info = tk.Frame(frame, bg="#f0f0f0")
            info.pack(side="left", fill="both", expand=True, padx=10)

            tk.Label(info, text=task['name'], font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
            tk.Label(info, text=f"{task['due_date']}, {task['time']}", bg="#f0f0f0").pack(anchor="w")
            tk.Label(info, text=task['category'], bg="#f0f0f0").pack(anchor="w")

            for sub in task.get("subtasks", []):
                tk.Checkbutton(info, text=sub, bg="#f0f0f0").pack(anchor="w")

            btn_frame = tk.Frame(info, bg="#f0f0f0")
            btn_frame.pack(anchor="e", pady=(5,0))

            tk.Button(btn_frame, text="✔", bg='green', fg='white', width=3, command=lambda t=task: self.mark_done(t)).pack(side="left", padx=2)
            tk.Button(btn_frame, text="✎", bg='cornflowerblue', fg='white', width=3, command=lambda t=task: self.edit_task(t)).pack(side="left", padx=2)
            tk.Button(btn_frame, text="View Details", bg='gold', fg='black', command=lambda: self.controller.show_frame("AllTasksPage")).pack(side="left", padx=2)

    def mark_done(self, task):
        task['completed'] = True
        self.refresh()

    def edit_task(self, task):
        index = self.controller.task_data.index(task)
        self.controller.frames["EditTaskPage"].load_task(task, index)
        self.controller.show_frame("EditTaskPage")

    def refresh(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self.build_left_panel()
        self.build_right_panel()

    def refresh_dashboard(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        self.build_left_panel()
        self.build_right_panel()
