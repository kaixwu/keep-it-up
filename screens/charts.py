import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class ChartsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg="#F2B705", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Keep it up!", font=("Arial", 22, "bold"), bg="#F2B705", fg="white").pack(side="left", padx=20)
        tk.Button(header, text="Log Out", bg="darkred", fg="white", font=("Arial", 12),
                  command=lambda: self.controller.show_frame("LoginPage")).pack(side="right", padx=20, pady=20)

        # Navigation Bar
        nav = tk.Frame(self, bg="#F2B705")
        nav.pack(fill="x")
        nav_pages = {
            'Home': 'DashboardPage',
            'All Tasks': 'AllTasksPage',
            'History': 'HistoryPage',
            'Charts': 'ChartsPage'
        }
        for i, (label, page) in enumerate(nav_pages.items()):
            tk.Button(nav, text=label, font=("Arial", 12), width=20,
                      command=lambda p=page: self.controller.show_frame(p)).grid(
                row=0, column=i, padx=5, pady=10, sticky="ew")
            nav.grid_columnconfigure(i, weight=1)

        # Main Content Frame
        main = tk.Frame(self, bg="white")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # Left: Bar Chart
        self.left_panel = tk.Frame(main, bg="white", bd=2, relief="groove")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Right: Pie Chart
        self.right_panel = tk.Frame(main, bg="white", bd=2, relief="groove")
        self.right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def show(self):
        self.refresh_charts()

    def refresh_charts(self):
        for w in self.left_panel.winfo_children():
            w.destroy()
        for w in self.right_panel.winfo_children():
            w.destroy()

        task_data = self.controller.task_data

        # Category color scheme
        cat_colors = {
            "Quiz": "orangered",
            "Assignment": "purple",
            "Task": "cornflowerblue",
            "Exam": "yellowgreen",
            "Completed": "gold"
        }
        categories = ["Quiz", "Assignment", "Task", "Exam"]

        # ===== BAR CHART: Total per category (all tasks) =====
        total_counter = Counter(t["category"] for t in task_data)
        values = [total_counter[cat] for cat in categories]

        fig1, ax1 = plt.subplots(figsize=(4.5, 4), dpi=100)
        ax1.bar(categories, values, color=[cat_colors[c] for c in categories])
        ax1.set_ylabel("Count")
        ax1.set_title("Total Tasks by Category")

        canvas1 = FigureCanvasTkAgg(fig1, master=self.left_panel)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        # Counters under bar chart
        bar_count_frame = tk.Frame(self.left_panel, bg="white")
        bar_count_frame.pack(fill="x", pady=5)

        def stat_box(parent, count, text, bg):
            frame = tk.Frame(parent, bg=bg)
            frame.pack(fill="x", pady=2, padx=20)
            tk.Label(frame, text=f"{count} {text}", bg=bg, fg="white",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=10)

        stat_box(bar_count_frame, total_counter["Quiz"], "Total Quizzes", cat_colors["Quiz"])
        stat_box(bar_count_frame, total_counter["Assignment"], "Total Assignment", cat_colors["Assignment"])
        stat_box(bar_count_frame, total_counter["Task"], "Total Tasks", cat_colors["Task"])
        stat_box(bar_count_frame, total_counter["Exam"], "Total Exam", cat_colors["Exam"])

        # ===== PIE CHART: Completed + Pending (by category) =====
        completed = sum(1 for t in task_data if t.get("completed"))
        pending_counts = {cat: 0 for cat in categories}
        for t in task_data:
            if not t.get("completed") and t["category"] in pending_counts:
                pending_counts[t["category"]] += 1

        pie_labels = []
        pie_values = []
        pie_colors = []

        if completed > 0:
            pie_labels.append(f"{completed} Completed")
            pie_values.append(completed)
            pie_colors.append(cat_colors["Completed"])

        for cat in categories:
            if pending_counts[cat] > 0:
                pie_labels.append(f"{pending_counts[cat]} Pending {cat}")
                pie_values.append(pending_counts[cat])
                pie_colors.append(cat_colors[cat])

        fig2, ax2 = plt.subplots(figsize=(4.5, 4), dpi=100)
        if pie_values:
            ax2.pie(pie_values, labels=pie_labels, colors=pie_colors,
                    startangle=90, wedgeprops={"edgecolor": "black"})
        else:
            ax2.pie([1], colors=["lightgrey"])

        ax2.axis("equal")
        canvas2 = FigureCanvasTkAgg(fig2, master=self.right_panel)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

        # Counters under pie chart
        pie_count_frame = tk.Frame(self.right_panel, bg="white")
        pie_count_frame.pack(fill="x", pady=5)

        def pie_stat_box(parent, count, label, bg):
            frame = tk.Frame(parent, bg=bg)
            frame.pack(fill="x", pady=2, padx=20)
            tk.Label(frame, text=f"{count} {label}", bg=bg, fg="white",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=10)

        if completed:
            pie_stat_box(pie_count_frame, completed, "Completed", cat_colors["Completed"])
        for cat in categories:
            count = pending_counts[cat]
            if count:
                pie_stat_box(pie_count_frame, count, f"Pending {cat}", cat_colors[cat])
