import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.current_date = datetime(2025, 6, 1)

        self.tasks = [
            {"name": "April Task", "date": datetime(2025, 4, 15, 14), "category": "School", "status": "done"},
            {"name": "June Task", "date": datetime(2025, 6, 10, 10), "category": "Work", "status": "pending"}
        ]

        self.sort_order = tk.StringVar(value="recent")
        self.build_ui()
        self.update_task_widgets()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg="#F2B705", height=80)
        header.pack(fill="x")
        tk.Label(header, text="History", fg="white", font=("Arial", 22, "bold"), bg="#F2B705").place(x=25, y=35)
        logout_btn = tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12), padx=10, pady=5,
                               command=lambda: self.controller.show_frame("LoginPage"))
        logout_btn.place(relx=1.0, x=-20, y=30, anchor="ne")

        # Navigation Bar
        nav = tk.Frame(self, bg='#F2B705')
        nav.pack(fill='x')

        nav_pages = {
            'Home': 'DashboardPage',
            'All Tasks': 'AllTasksPage',
            'Calendar': 'CalendarPage',
            'History': 'HistoryPage',
            'Charts': 'ChartsPage'
        }

        for i, (label, page) in enumerate(nav_pages.items()):
            tk.Button(
                nav,
                text=label,
                font=("Arial", 12),
                width=20,
                command=lambda p=page: self.controller.show_frame(p)
            ).grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

        # Main Content
        main = tk.Frame(self, bg="white")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # Left Panel
        left = tk.Frame(main, bg="white")
        left.grid(row=0, column=0, sticky="ns")

        self.calendar = Calendar(left, year=self.current_date.year, month=self.current_date.month, day=1)
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarDisplayed>>", lambda e: self.update_task_widgets())
        self.calendar.bind("<<CalendarMonthChanged>>", lambda e: self.update_task_widgets())

        self.summary_frame = tk.Frame(left, bg="white", bd=2, relief="groove")
        self.summary_frame.pack(pady=10, fill="x")
        self.summary_label = tk.Label(self.summary_frame, justify="left", font=("Arial", 10), anchor="w", bg="white")
        self.summary_label.pack(padx=10, pady=10)
        self.progress = ttk.Progressbar(self.summary_frame, length=200)
        self.progress.pack(padx=10, pady=5)

        # Right Panel
        right = tk.Frame(main, bg="white", bd=2, relief="groove")
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # Filter Bar
        filter_bar = tk.Frame(right, bg="white")
        filter_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        tk.Label(filter_bar, text="Tasks on", font=("Arial", 16, "bold"), bg="white").pack(side="left")
        self.month_menu = ttk.Combobox(filter_bar, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], state="readonly")
        self.month_menu.set(self.current_date.strftime("%B"))
        self.month_menu.pack(side="left", padx=5)
        self.month_menu.bind("<<ComboboxSelected>>", lambda e: self.update_task_widgets())

        self.year_menu = ttk.Combobox(filter_bar, values=[str(y) for y in range(2023, 2031)], state="readonly")
        self.year_menu.set(str(self.current_date.year))
        self.year_menu.pack(side="left")
        self.year_menu.bind("<<ComboboxSelected>>", lambda e: self.update_task_widgets())

        tk.Radiobutton(filter_bar, text="Oldest", variable=self.sort_order, value="oldest", bg="white", command=self.update_task_widgets).pack(side="right")
        tk.Radiobutton(filter_bar, text="Most Recent", variable=self.sort_order, value="recent", bg="white", command=self.update_task_widgets).pack(side="right")

        # Task Display Area
        self.task_canvas = tk.Canvas(right, bg="white")
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.task_canvas.yview)
        self.task_frame = tk.Frame(self.task_canvas, bg="white")
        self.task_canvas.bind("<Configure>", self.resize_task_frame)

        self.task_window = self.task_canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.task_canvas.configure(yscrollcommand=scrollbar.set)

        self.task_canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.task_frame.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))

    def resize_task_frame(self, event):
        canvas_width = event.width
        self.task_canvas.itemconfig(self.task_window, width=canvas_width)

    def update_task_widgets(self):
        # Update task list and summary based on selected date/month/year
        month_name = self.month_menu.get()
        year_val = int(self.year_menu.get())
        month_index = datetime.strptime(month_name, "%B").month
        self.current_date = datetime(year_val, month_index, 1)

        tasks_this_month = [t for t in self.tasks if t['date'].year == year_val and t['date'].month == month_index]
        tasks_this_month.sort(key=lambda x: x['date'], reverse=(self.sort_order.get() == 'recent'))

        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in tasks_this_month:
            frame = tk.Frame(self.task_frame, bg="#f2f2f2", bd=1, relief="solid")
            frame.pack(fill="x", expand=True, pady=5, padx=10)
            frame.grid_columnconfigure(0, weight=1)  # Make text column expandable

            # Text section on the left
            text = tk.Label(
                frame,
                text=f"{task['name']}\n{task['date'].strftime('%B %d, %Y')}, {task['date'].strftime('%I:%M %p')}\n{task['category']}",
                font=("Arial", 11),
                bg="#f2f2f2",
                justify="left",
                anchor="w"
            )
            text.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            # View Details button on the right
            btn = tk.Button(frame, text="View Details", bg="#FDB813", font=("Arial", 10, "bold"), padx=10, pady=5)
            btn.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        total = len(tasks_this_month)
        done = sum(1 for t in tasks_this_month if t['status'] == 'done')
        pending = total - done
        self.summary_label.config(text=f"\n\u2022 {total} Total Tasks\n\u2022 {done} Done\n\u2022 {pending} Pending")
        self.progress['maximum'] = total if total else 1
        self.progress['value'] = done
