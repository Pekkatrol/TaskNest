import tkinter as tk
from tkinter import messagebox
from tasknest.manager import TaskManager

class TaskApp:

    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Task Nest")

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Add", command=self.add_task)
        self.add_button.pack()

        self.list_frame = tk.Frame(root)
        self.list_frame.pack(pady=10)

        self.listbox = tk.Listbox(self.list_frame, width=50, height=10, selectmode=tk.SINGLE)
        self.listbox.config(exportselection=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.done_button = tk.Button(root, text="Done", command=self.mark_done)
        self.done_button.pack()

        self.delete_button = tk.Button(root, text="Delete", command=self.delete_task)
        self.delete_button.pack()

        self.refresh_tasks()

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        self.tasks = self.manager.get_all_tasks()

        for index, task in enumerate(self.tasks):
            status = "✔" if task["completed"] else "✗"
            self.listbox.insert(tk.END, f"{status} {task['title']}")
        
            if task["completed"]:
                self.listbox.itemconfig(index, fg="gray")
            else:
                self.listbox.itemconfig(index, fg="black")

    def add_task(self):
        title = self.entry.get()
        if title:
            self.manager.add_task(title)
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

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = selection[0]
        task_id = self.tasks[index]["id"]
        self.manager.delete_task(task_id)
        self.refresh_tasks()