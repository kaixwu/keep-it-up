import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, date

class EditTaskPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.task_index = None
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg="#f5a800", height=80)
        header.pack(fill="x")
        tk.Label(header, text="EDIT TASK",
                 bg="#f5a800",
                 fg="white",
                 font=("Arial", 24, "bold")).pack(pady=20)

        self.content = tk.Frame(self, bg="white")
        self.content.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(self.content, text="Task Name", bg="white", anchor="w").pack(fill="x")
        self.task_name_entry = tk.Entry(self.content, font=("Arial", 12), relief="solid", bd=1)
        self.task_name_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.content, text="Description", bg="white", anchor="w").pack(fill="x")
        self.description_text = tk.Text(self.content, height=6, font=("Arial", 12), relief="solid", bd=1)
        self.description_text.pack(fill="x", pady=(0, 10))

        tk.Label(self.content, text="Task Category", bg="white", anchor="w").pack(fill="x")
        category_options = ["Assignment", "Task", "Quiz", "Exam"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.content, textvariable=self.category_var, values=category_options, state="readonly")
        self.category_dropdown.pack(fill="x", pady=(0, 10))

        tk.Label(self.content, text="Due Date", bg="white", anchor="w").pack(fill="x")
        self.due_date_entry = DateEntry(self.content, font=("Arial", 12), date_pattern='yyyy-mm-dd', mindate=date.today())
        self.due_date_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.content, text="Due Time", bg="white", anchor="w").pack(fill="x")
        time_frame = tk.Frame(self.content, bg="white")
        time_frame.pack(fill="x", pady=(0, 20))

        self.hour_var = tk.StringVar(value='12')
        self.minute_var = tk.StringVar(value='00')
        self.ampm_var = tk.StringVar(value='AM')

        ttk.Spinbox(time_frame, from_=1, to=12, wrap=True, textvariable=self.hour_var, width=5, font=("Arial", 12), justify='center').pack(side='left')
        tk.Label(time_frame, text=":", font=("Arial", 12), bg='white').pack(side='left')
        ttk.Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f", textvariable=self.minute_var, width=5, font=("Arial", 12), justify='center').pack(side='left')
        ttk.Combobox(time_frame, values=['AM', 'PM'], textvariable=self.ampm_var, width=5, font=("Arial", 12), justify='center', state="readonly").pack(side='left', padx=10)

        button_frame = tk.Frame(self.content, bg="white")
        button_frame.pack(pady=10, fill="x")

        tk.Button(button_frame, text="Cancel", bg="darkred", fg="white", font=("Arial", 12, "bold"),
                  command=lambda: self.controller.show_frame("DashboardPage")).pack(side="left", expand=True, fill="x", padx=5)

        tk.Button(button_frame, text="Save Edit", bg="orange", fg="white", font=("Arial", 12, "bold"),
                  command=self.save_edit).pack(side="left", expand=True, fill="x", padx=5)

    def load_task(self, task, index):
        self.task_index = index
        self.task_name_entry.delete(0, 'end')
        self.task_name_entry.insert(0, task["name"])
        self.description_text.delete("1.0", 'end')
        self.description_text.insert("1.0", task["description"])
        self.category_var.set(task["category"])
        self.due_date_entry.set_date(task["due_date"])

        time_str = task["time"]  # e.g., "10:00 AM"
        time_part, ampm = time_str.split()
        hour, minute = time_part.split(":")
        self.hour_var.set(hour)
        self.minute_var.set(minute)
        self.ampm_var.set(ampm)

    def save_edit(self):
        if self.task_index is None:
            messagebox.showerror("Error", "No task loaded.")
            return

        name = self.task_name_entry.get().strip()
        desc = self.description_text.get("1.0", "end").strip()
        category = self.category_var.get().strip()
        date_str = self.due_date_entry.get().strip()
        time = f"{self.hour_var.get()}:{self.minute_var.get()} {self.ampm_var.get()}"

        if not name or not category or not date_str:
            messagebox.showerror("Missing Field", "All fields must be filled out.")
            return

        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        selected_hour = int(self.hour_var.get()) % 12 + (12 if self.ampm_var.get() == 'PM' else 0)
        selected_minute = int(self.minute_var.get())
        selected_datetime = selected_date.replace(hour=selected_hour, minute=selected_minute)
        if selected_datetime < now:
            messagebox.showerror("Invalid Time", "Due time cannot be in the past.")
            return

        updated_task = {
            "name": name,
            "description": desc,
            "category": category,
            "due_date": date_str,
            "time": time,
            "subtasks": self.controller.task_data[self.task_index].get("subtasks", []),
            "completed": self.controller.task_data[self.task_index].get("completed", False)
        }

        self.controller.task_data[self.task_index] = updated_task
        messagebox.showinfo("Success", "Task updated successfully!")
        self.controller.show_frame("AllTasksPage")
        if "AllTasksPage" in self.controller.frames:
            self.controller.frames["AllTasksPage"].update_task_display()
