import tkinter as tk
import json
import os

# ---------------- App Setup ----------------
app = tk.Tk()
app.title("To-Do App with Timer")
app.geometry("500x500")

TASK_FILE = "tasks.json"
timer_running = False
time_left = 0

# ---------------- Task Functions ----------------
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file)

tasks = load_tasks()

# ---------------- Timer Functions ----------------
def start_timer():
    global time_left, timer_running

    if timer_running:
        return

    try:
        minutes = int(timer_entry.get())
        time_left = minutes * 60
    except ValueError:
        timer_label.config(text="Enter minutes")
        return

    timer_running = True
    countdown()

def stop_timer():
    global timer_running
    timer_running = False

def countdown():
    global time_left, timer_running

    if not timer_running:
        return

    if time_left <= 0:
        timer_label.config(text="Time's up!")
        timer_running = False
        return

    mins = time_left // 60
    secs = time_left % 60
    timer_label.config(text=f"{mins:02d}:{secs:02d}")

    time_left -= 1
    app.after(1000, countdown)

# ---------------- UI ----------------
tk.Label(app, text="Add Task").pack(pady=5)

task_entry = tk.Entry(app, width=30)
task_entry.pack()

task_listbox = tk.Listbox(app, width=45, height=8)
task_listbox.pack(pady=10)

for task in tasks:
    task_listbox.insert(tk.END, task)

def add_task():
    task = task_entry.get()
    if task.strip() == "":
        return
    tasks.append(task)
    task_listbox.insert(tk.END, task)
    save_tasks()
    task_entry.delete(0, tk.END)

tk.Button(app, text="Add Task", command=add_task).pack(pady=5)

# ---------------- Timer UI ----------------
tk.Label(app, text="Timer (minutes)").pack(pady=10)

timer_entry = tk.Entry(app, width=10)
timer_entry.pack()

timer_label = tk.Label(app, text="00:00", font=("Arial", 20))
timer_label.pack(pady=5)

tk.Button(app, text="Start Timer", command=start_timer).pack(pady=5)
tk.Button(app, text="Stop Timer", command=stop_timer).pack(pady=5)

# ---------------- Run App ----------------
app.mainloop()
