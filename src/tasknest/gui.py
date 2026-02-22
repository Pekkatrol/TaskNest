import tkinter as tk
from tkinter import messagebox
from tasknest.manager import TaskManager

PRIORITY_ICONS = {
    "high": "[HIGH]",
    "medium": "[MED]",
    "low": "[LOW]"
}

class TaskApp:

    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Task Nest")
    
        self.toggle = 0

        title_label = tk.Label(root, text="TaskNest", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)


        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)

        self.entry = tk.Entry(input_frame, width=35)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.priority_var = tk.StringVar(value="low")

        priority_menu = tk.OptionMenu(
            input_frame,
            self.priority_var,
            "low",
            "medium",
            "high"
        )
        priority_menu.config(width=8)
        priority_menu.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(input_frame, text="Add", width=8, command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.list_frame = tk.Frame(root)
        self.list_frame.pack(pady=10)

        self.listbox = tk.Listbox(
            self.list_frame,
            width=50,
            height=12,
            selectmode=tk.SINGLE
        )
        self.listbox.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)

        self.done_button = tk.Button(action_frame, text="Done", width=10, command=self.mark_done)
        self.done_button.pack(side=tk.LEFT, padx=5)

        self.undone_button = tk.Button(action_frame, text="Undone", width=10, command=self.mark_undone)
        self.undone_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(action_frame, text="Delete", width=10, command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.show_button = tk.Button(root, text="Hide completed", command=self.change_toggle)
        self.show_button.pack(pady=5)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)

        all_tasks = self.manager.get_all_tasks()

        if self.toggle == 1:
            self.tasks = [t for t in all_tasks if not t["completed"]]
        else:
            self.tasks = all_tasks

        for index, task in enumerate(self.tasks):
            status = "✔" if task["completed"] else "✗"
            self.listbox.insert(tk.END, f"{status}     {task['title']}     {PRIORITY_ICONS[task["priority"]]}")
            if task["completed"]:
                self.listbox.itemconfig(index, fg="gray")
            else:
                self.listbox.itemconfig(index, fg="black")

    def change_toggle(self):
        self.toggle = 0 if self.toggle == 1 else 1
        self.refresh_tasks()

    def add_task(self):
        priority = self.priority_var.get()

        title = self.entry.get()
        if title:
            self.manager.add_task(title, priority)
            self.entry.delete(0, tk.END)
            self.refresh_tasks()

    def mark_done(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = selection[0]
        task_id = self.tasks[index]["id"]
        self.manager.mark_done(task_id)
        self.refresh_tasks()

    def mark_undone(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = selection[0]
        task_id = self.tasks[index]["id"]
        self.manager.mark_undone(task_id)
        self.refresh_tasks()

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = selection[0]
        task_id = self.tasks[index]["id"]
        self.manager.delete_task(task_id)
        self.refresh_tasks()