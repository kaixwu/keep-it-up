# taskDetails.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date

class TaskDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.task = None
        self.build_ui()

    def build_ui(self):
        # Left panel
        self.left_panel = tk.Frame(self, bg='#FFB800', width=450)
        self.left_panel.pack(side='left', fill='both')
        self.left_panel.pack_propagate(False)

        tk.Button(
            self.left_panel, text="←", font=("Arial", 20, "bold"),
            bg='white', fg='black', relief='solid', bd=1, width=2,
            command=lambda: self.controller.show_frame("DashboardPage")
        ).pack(padx=20, pady=20, anchor='nw')

        self.days_left_label = tk.Label(
            self.left_panel, text="", font=("Arial", 28, "bold"),
            bg='#FFB800', fg='white'
        )
        self.days_left_label.place(relx=0.5, rely=0.5, anchor='center')

        # Right panel
        right_panel = tk.Frame(self, bg='white')
        right_panel.pack(side='left', fill='both', expand=True)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        self.form = tk.Frame(right_panel, bg='white')
        self.form.grid(row=0, column=0, padx=20, pady=20)

        label_font = ("Arial", 12)
        entry_font = ("Arial", 11)

        def readonly_entry(row, label, var):
            tk.Label(self.form, text=label, font=label_font, bg='white')\
                .grid(row=row, column=0, sticky='w', padx=5, pady=(0, 2))
            entry = tk.Entry(self.form, font=entry_font, width=40, state='readonly', textvariable=var)
            entry.grid(row=row, column=1, pady=(0, 2), sticky='w')
            return entry

        self.name_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()

        readonly_entry(0, "Task Name", self.name_var)

        tk.Label(self.form, text="Description", font=label_font, bg='white')\
            .grid(row=1, column=0, sticky='nw', padx=5, pady=(0, 2))
        self.description_text = tk.Text(self.form, font=entry_font, width=38, height=4, state="disabled")
        self.description_text.grid(row=1, column=1, pady=(0, 2), sticky='w')

        tk.Label(self.form, text="Subtasks", font=label_font, bg='white')\
            .grid(row=2, column=0, sticky='nw', padx=5, pady=(5, 2))

        self.subtask_container = tk.Frame(self.form, bg='white', bd=1, relief='solid')
        self.subtask_container.grid(row=3, column=1, sticky='ew', pady=(0, 10))
        self.subtask_canvas = tk.Canvas(self.subtask_container, height=100, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.subtask_container, orient="vertical", command=self.subtask_canvas.yview)
        self.subtask_frame = tk.Frame(self.subtask_canvas, bg='white')
        self.subtask_frame.bind(
            "<Configure>",
            lambda e: self.subtask_canvas.configure(scrollregion=self.subtask_canvas.bbox("all"))
        )
        self.subtask_canvas.create_window((0, 0), window=self.subtask_frame, anchor='nw')
        self.subtask_canvas.configure(yscrollcommand=scrollbar.set)
        self.subtask_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        readonly_entry(4, "Task Category", self.category_var)
        readonly_entry(5, "Due Date", self.date_var)
        readonly_entry(6, "Due Time", self.time_var)

    def load_task(self, task):
        self.task = task
        self.name_var.set(task["name"])
        self.desc_var.set(task["description"])
        self.category_var.set(task["category"])
        self.date_var.set(task["due_date"])
        self.time_var.set(task["time"])

        self.description_text.config(state='normal')
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", task["description"])
        self.description_text.config(state='disabled')

        # Days left
        today = date.today()
        due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        days_left = (due - today).days
        if days_left >= 0:
            self.days_left_label.config(text=f"Days left: {days_left}")
        else:
            self.days_left_label.config(text="Overdue!")

        # Subtasks
        for w in self.subtask_frame.winfo_children():
            w.destroy()

        for subtask in task.get("subtasks", []):
            subtask_label = tk.Label(self.subtask_frame, text=f"• {subtask}", bg='white', font=("Arial", 11), anchor='w')
            subtask_label.pack(anchor='w', padx=5, pady=2)
