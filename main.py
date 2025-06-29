# main.py
import sys
import os
import tkinter as tk
import database

from screens.login import LoginPage
from screens.signup import SignUpPage
from screens.dashboard import DashboardPage
from screens.add_task import AddTaskPage
from screens.edit_task import EditTaskPage
from screens.all_tasks import AllTasksPage
from screens.history import HistoryPage
from screens.charts import ChartsPage
from screens.taskDetails import TaskDetailsPage

# Initialize the database
database.init_db()


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

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        pages = [
            LoginPage, SignUpPage, DashboardPage,
            AddTaskPage, EditTaskPage, AllTasksPage,
            HistoryPage, ChartsPage, TaskDetailsPage
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
            frame.refresh_from_db()
        elif page_name == "HistoryPage":
            frame.show()
        elif page_name == "ChartsPage":
            frame.show()

    def on_login_success(self, user_data):
        self.current_user = user_data
        print(f"User '{self.current_user['name']}' logged in successfully.")

        # Load tasks for the user
        self.task_data = database.get_all_tasks(user_data["id"])

        # Refresh every page that supports refresh_from_db or refresh_dashboard
        for frame in self.frames.values():
            if hasattr(frame, "refresh_from_db"):
                frame.refresh_from_db()
            if hasattr(frame, "refresh_dashboard"):
                frame.refresh_dashboard()

        self.show_frame("DashboardPage")


if __name__ == "__main__":
    app = App()
    app.state("zoomed")
    app.mainloop()
