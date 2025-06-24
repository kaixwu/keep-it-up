# main.py
import sys
import os
import database

# Get the directory where main.py is located (your project root)
project_root = os.path.dirname(os.path.abspath(__file__))
# Add this directory to sys.path so Python can find database
if project_root not in sys.path:
    sys.path.append(project_root)

import tkinter as tk
from screens.login import LoginPage
from screens.signup import SignUpPage
from screens.dashboard import DashboardPage
from screens.add_task import AddTaskPage
from screens.edit_task import EditTaskPage
from screens.all_tasks import AllTasksPage
from screens.history import HistoryPage
from screens.charts import ChartsPage
import database # Import your database service file

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keep It Up!")
        self.configure(bg="white")
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))

        self.current_user = None

        self.task_data = []

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)
        self.frames = {}

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        pages = [
            LoginPage, SignUpPage, DashboardPage,
            AddTaskPage, EditTaskPage, AllTasksPage,
            HistoryPage, ChartsPage
        ]

        for F in pages:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "DashboardPage":
            frame.refresh_dashboard()
        elif page_name == "AllTasksPage":
            frame.update_task_display()

    def on_login_success(self, user_data):
        self.current_user = user_data
        print(f"User '{self.current_user['name']}' logged in successfully.")
        self.show_frame("DashboardPage")


if __name__ == "__main__":
    database.init_db()
    app = App()
    app.state("zoomed")
    app.mainloop()