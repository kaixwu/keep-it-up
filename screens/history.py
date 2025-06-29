import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import database

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.sort_order = tk.StringVar(value="recent")
        self.selected_date = None
        self.build_ui()

    def build_ui(self):
        # Header
        self.header_frame = tk.Frame(self, bg="#F2B705", height=80)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(self.header_frame, text="History", fg="white", font=("Arial", 22, "bold"), bg="#F2B705")
        self.header_label.place(x=25, y=35)
        tk.Button(self.header_frame, text="Log Out", bg="darkred", fg="white", font=("Arial", 12),
                  command=lambda: self.controller.show_frame("LoginPage")).place(relx=1.0, x=-20, y=30, anchor="ne")

        # Navbar
        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')
        pages = {'Home': 'DashboardPage', 'All Tasks': 'AllTasksPage',
                   'History': 'HistoryPage', 'Charts': 'ChartsPage'}
        for i, (label, page) in enumerate(pages.items()):
            tk.Button(nav, text=label, font=("Arial", 12), width=20,
                      command=lambda p=page: self.controller.show_frame(p))\
                .grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

        # Main layout
        main = tk.Frame(self, bg="white")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # Left panel (calendar + summary)
        left = tk.Frame(main, bg="white")
        left.grid(row=0, column=0, sticky="ns")
        self.calendar = Calendar(left)
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_date_selected)
        self.calendar.bind("<<CalendarMonthChanged>>", lambda e: self.clear_calendar_date())

        self.summary_frame = tk.Frame(left, bg="white", bd=2, relief="groove")
        self.summary_frame.pack(pady=10, fill="x")
        self.summary_label = tk.Label(self.summary_frame, font=("Arial", 10), anchor="w", bg="white", justify="left")
        self.summary_label.pack(padx=10, pady=10)
        self.progress = ttk.Progressbar(self.summary_frame, length=200)
        self.progress.pack(padx=10, pady=5)

        # Right panel (task display)
        right = tk.Frame(main, bg="white", bd=2, relief="groove")
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # Filter bar
        filter_bar = tk.Frame(right, bg="white")
        filter_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        tk.Label(filter_bar, text="Tasks on", font=("Arial", 16, "bold"), bg="white").pack(side="left")
        self.month_menu = ttk.Combobox(filter_bar,
            values=["All"] + [datetime(2025, m, 1).strftime("%B") for m in range(1, 13)], state="readonly")
        self.month_menu.set("All")
        self.month_menu.pack(side="left", padx=5)
        self.month_menu.bind("<<ComboboxSelected>>", lambda e: self.update_task_widgets())

        self.year_menu = ttk.Combobox(filter_bar, values=[str(y) for y in range(2023, 2031)], state="readonly")
        self.year_menu.set(str(datetime.now().year))
        self.year_menu.pack(side="left")
        self.year_menu.bind("<<ComboboxSelected>>", lambda e: self.update_task_widgets())

        # ✅ Clear Button
        tk.Button(filter_bar, text="Clear", bg="gray", fg="white", font=("Arial", 10, "bold"),
                  command=self.clear_filters).pack(side="left", padx=10)

        tk.Radiobutton(filter_bar, text="Oldest", variable=self.sort_order, value="oldest",
                       bg="white", command=self.update_task_widgets).pack(side="right")
        tk.Radiobutton(filter_bar, text="Most Recent", variable=self.sort_order, value="recent",
                       bg="white", command=self.update_task_widgets).pack(side="right")

        # Scrollable task area
        self.task_canvas = tk.Canvas(right, bg="white")
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.task_canvas.yview)
        self.task_frame = tk.Frame(self.task_canvas, bg="white")
        self.task_window = self.task_canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.task_canvas.configure(yscrollcommand=scrollbar.set)

        self.task_canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.task_frame.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))
        self.task_canvas.bind("<Configure>", self.resize_task_frame)

    def show(self):
        self.update_task_widgets()

    def resize_task_frame(self, event):
        self.task_canvas.itemconfig(self.task_window, width=event.width)

    def clear_filters(self):
        self.selected_date = None
        self.month_menu.set("All")
        self.year_menu.set(str(datetime.now().year))
        self.header_label.config(text="History")
        self.update_task_widgets()

    def clear_calendar_date(self):
        self.selected_date = None
        self.header_label.config(text="History")
        self.update_task_widgets()

    def on_calendar_date_selected(self, event):
        self.selected_date = self.calendar.selection_get()
        formatted_date = self.selected_date.strftime("%B %d, %Y")
        self.header_label.config(text=f"Tasks on {formatted_date}")
        self.update_task_widgets()

    def update_task_widgets(self):
        if not self.controller.current_user:
            return

        user_id = self.controller.current_user["id"]
        all_tasks = database.get_all_tasks(user_id)
        completed_tasks = [t for t in all_tasks if t.get("completed")]

        if self.selected_date:
            completed_tasks = [t for t in completed_tasks if t["due_date"] == self.selected_date.strftime("%Y-%m-%d")]
        else:
            selected_month = self.month_menu.get()
            selected_year = int(self.year_menu.get())
            if selected_month != "All":
                month_index = datetime.strptime(selected_month, "%B").month
                completed_tasks = [t for t in completed_tasks
                                   if datetime.strptime(t["due_date"], "%Y-%m-%d").year == selected_year and
                                   datetime.strptime(t["due_date"], "%Y-%m-%d").month == month_index]
            else:
                completed_tasks = [t for t in completed_tasks
                                   if datetime.strptime(t["due_date"], "%Y-%m-%d").year == selected_year]

        completed_tasks.sort(key=lambda t: datetime.strptime(t["due_date"], "%Y-%m-%d"),
                             reverse=(self.sort_order.get() == "recent"))

        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in completed_tasks:
            frame = tk.Frame(self.task_frame, bg="#f2f2f2", bd=1, relief="solid")
            frame.pack(fill="x", expand=True, pady=5, padx=10)
            frame.grid_columnconfigure(0, weight=1)

            tk.Label(frame, text=f"{task['name']}\n{task['due_date']}, {task['time']}\n{task['category']}",
                     font=("Arial", 11), bg="#f2f2f2", justify="left", anchor="w")\
                .grid(row=0, column=0, sticky="w", padx=10, pady=10)

            btns = tk.Frame(frame, bg="#f2f2f2")
            btns.grid(row=0, column=1, sticky="e", padx=10, pady=10)

            tk.Button(btns, text="↩ Restore", bg="seagreen", fg="white", font=("Arial", 10, "bold"),
                      command=lambda t=task: self.restore_task(t)).pack(side="left", padx=5)

            tk.Button(btns, text="🗑 Delete", bg="firebrick", fg="white", font=("Arial", 10, "bold"),
                      command=lambda t=task: self.delete_permanently(t)).pack(side="left", padx=5)

        total = len(completed_tasks)
        self.summary_label.config(text=f"\n\u2022 {total} Completed Task(s)")
        self.progress['maximum'] = total if total else 1
        self.progress['value'] = total

    def restore_task(self, task):
        database.update_task_completion(task["id"], False)
        self.controller.task_data = database.get_all_tasks(self.controller.current_user["id"])
        self.update_task_widgets()
        self.controller.frames["DashboardPage"].refresh_dashboard()
        self.controller.frames["AllTasksPage"].refresh_from_db()

    def delete_permanently(self, task):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete '{task['name']}'?"):
            database.delete_task(task["id"])
            self.controller.task_data = database.get_all_tasks(self.controller.current_user["id"])
            self.update_task_widgets()
            self.controller.frames["DashboardPage"].refresh_dashboard()
            self.controller.frames["AllTasksPage"].refresh_from_db()
