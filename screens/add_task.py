import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date, datetime
import database

class AddTaskPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.subtasks = []
        self.build_ui()

    def build_ui(self):
        left_panel = tk.Frame(self, bg='#FFB800', width=450)
        left_panel.pack(side='left', fill='both')
        left_panel.pack_propagate(False)

        tk.Button(
            left_panel, text="←", font=("Arial", 20, "bold"),
            bg='white', fg='black', relief='solid', bd=1, width=2,
            command=self.go_back
        ).pack(padx=20, pady=20, anchor='nw')

        tk.Label(
            left_panel, text="ADD TASK",
            font=("Arial", 28, "bold"),
            bg='#FFB800', fg='white'
        ).place(relx=0.5, rely=0.5, anchor='center')

        right_panel = tk.Frame(self, bg='white')
        right_panel.pack(side='left', fill='both', expand=True)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        form = tk.Frame(right_panel, bg='white')
        form.grid(row=0, column=0, padx=20, pady=20)

        label_font = ("Arial", 12)
        entry_font = ("Arial", 11)

        tk.Label(form, text="Task Name", font=label_font, bg='white')\
            .grid(row=0, column=0, sticky='w', padx=5, pady=(0, 2))
        self.task_name_entry = tk.Entry(form, font=entry_font, width=40)
        self.task_name_entry.grid(row=0, column=1, pady=(0, 2), sticky='w')

        tk.Label(form, text="Description", font=label_font, bg='white')\
            .grid(row=1, column=0, sticky='nw', padx=5, pady=(0, 2))
        self.description_text = tk.Text(form, font=entry_font, width=38, height=4)
        self.description_text.grid(row=1, column=1, pady=(0, 2), sticky='w')

        tk.Label(form, text="Subtasks", font=label_font, bg='white')\
            .grid(row=2, column=0, sticky='nw', padx=5, pady=(5, 2))
        tk.Button(form, text="Add Subtask", bg='#FFB800', fg='white',
                  font=entry_font, width=20, command=self.add_subtask)\
            .grid(row=2, column=1, sticky='w', pady=(5, 2))

        self.subtask_container = tk.Frame(form, bg='white', bd=1, relief='solid')
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

        tk.Label(form, text="Task Category", font=label_font, bg='white')\
            .grid(row=5, column=0, sticky='w', padx=5, pady=(5, 2))
        self.task_category = ttk.Combobox(form,
                                          values=["Assignment", "Task", "Quiz", "Exam"],
                                          font=entry_font, width=38, state="readonly")
        self.task_category.grid(row=5, column=1, sticky='w', pady=(5, 2))

        tk.Label(form, text="Due Date", font=label_font, bg='white')\
            .grid(row=6, column=0, sticky='w', padx=5, pady=(0, 2))
        self.due_date = DateEntry(form, font=entry_font, width=25, date_pattern='yyyy-mm-dd',
                                  mindate=date.today())
        self.due_date.grid(row=6, column=1, sticky='w', pady=(0, 2))

        tk.Label(form, text="Due Time", font=label_font, bg='white')\
            .grid(row=7, column=0, sticky='w', padx=5, pady=(0, 5))
        time_frame = tk.Frame(form, bg='white')
        time_frame.grid(row=7, column=1, sticky='w', pady=(0, 5))
        self.hour_var = tk.StringVar(value='12')
        self.minute_var = tk.StringVar(value='00')
        self.ampm_var = tk.StringVar(value='AM')
        ttk.Spinbox(time_frame, from_=1, to=12, wrap=True,
                    textvariable=self.hour_var,
                    width=5, font=entry_font, justify='center').pack(side='left')
        tk.Label(time_frame, text=":", font=entry_font, bg='white').pack(side='left')
        ttk.Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f",
                    textvariable=self.minute_var,
                    width=5, font=entry_font, justify='center').pack(side='left')
        ttk.Combobox(time_frame,
                     values=['AM', 'PM'],
                     textvariable=self.ampm_var,
                     width=5,
                     font=entry_font,
                     state="readonly").pack(side='left', padx=10)

        button_frame = tk.Frame(form, bg='white')
        button_frame.grid(row=8, column=1, sticky='e', pady=(10, 10))
        tk.Button(button_frame, text="Cancel", bg='darkred', fg='white',
                  font=("Arial", 12), width=12, height=1,
                  command=self.cancel_task).pack(side='left', padx=5)
        tk.Button(button_frame, text="Add Task", bg='#FFB800', fg='white',
                  font=("Arial", 12), width=12, height=1,
                  command=self.save_task).pack(side='left', padx=5)

    def go_back(self):
        self.controller.show_frame("DashboardPage")

    def cancel_task(self):
        self.clear_form()
        self.controller.show_frame("DashboardPage")

    def add_subtask(self):
        subtask_row = tk.Frame(self.subtask_frame, bg='white', pady=2)
        subtask_row.pack(fill='x', padx=5, pady=2)

        entry = tk.Entry(subtask_row, font=("Arial", 11), width=30)
        entry.pack(side='left', padx=(0, 10), fill='x', expand=True)
        tk.Button(subtask_row, text="Remove", bg='darkred', fg='white',
                  font=("Arial", 10), width=8,
                  command=lambda r=subtask_row, e=entry: self.remove_subtask(r, e)).pack(side='right')
        self.subtasks.append(entry)

    def remove_subtask(self, row, entry):
        self.subtasks.remove(entry)
        row.destroy()

    def save_task(self):
        name = self.task_name_entry.get().strip()
        desc = self.description_text.get("1.0", "end").strip()
        category = self.task_category.get().strip()
        date_str = self.due_date.get().strip()
        time = f"{self.hour_var.get()}:{self.minute_var.get()} {self.ampm_var.get()}"
        subtasks = [entry.get().strip() for entry in self.subtasks if entry.get().strip()]
        notif_days = int(self.notify_days.get())
        notif_hours = int(self.notify_hours.get())

        if not name:
            messagebox.showerror("Missing Field", "Task name is required.")
            return
        if not category:
            messagebox.showerror("Missing Field", "Please select a task category.")
            return

        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        selected_hour = (int(self.hour_var.get()) % 12) + (12 if self.ampm_var.get() == 'PM' else 0)
        selected_datetime = selected_date.replace(hour=selected_hour,
                                                  minute=int(self.minute_var.get()))
        if selected_datetime < now:
            messagebox.showerror("Invalid Time", "Due time cannot be in the past.")
            return

        task = {
            "name": name,
            "description": desc,
            "category": category,
            "due_date": date_str,
            "time": time,
            "subtasks": subtasks,
            "completed": False,
            "notify_days": notif_days,
            "notify_hours": notif_hours,
        }

        if not self.controller.current_user:
            messagebox.showerror("Not Logged In", "You must be logged in to add a task.")
            return

        user_id = self.controller.current_user["id"]
        database.add_task(user_id, task)

        messagebox.showinfo("Success", f"Task '{name}' added successfully!")
        self.clear_form()
        self.controller.show_frame("AllTasksPage")

        # Refresh AllTasksPage
        if "AllTasksPage" in self.controller.frames:
            self.controller.frames["AllTasksPage"].refresh_from_db()
        if "DashboardPage" in self.controller.frames:
            self.controller.frames["DashboardPage"].refresh_dashboard()

    def clear_form(self):
        self.task_name_entry.delete(0, 'end')
        self.description_text.delete("1.0", 'end')
        self.task_category.set('')
        self.due_date.set_date(date.today())
        self.hour_var.set('12')
        self.minute_var.set('00')
        self.ampm_var.set('AM')
        for w in self.subtask_frame.winfo_children():
            w.destroy()
        self.subtasks.clear()
