# utils.py
from datetime import datetime, date

def get_deadline_color(due_date_str):
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        days_left = (due_date - date.today()).days
        if days_left <= 2:
            return "red"
        elif days_left == 3:
            return "darkred"
        elif 4 <= days_left <= 5:
            return "chocolate"
        elif 6 <= days_left <= 7:
            return "gold"
        else:
            return "green"
    except:
        return "gray"