import customtkinter as ctk
from tkinter import messagebox
from tasknest.manager import TaskManager

PRIORITY_ICONS = {
    "high": "[HIGH]",
    "medium": "[MED]",
    "low": "[LOW]"
}

ctk.set_appearance_mode("dark")


class TaskNestApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("TaskNest")
        self.geometry("500x450")

        self.manager = TaskManager()
        self.toggle = 0
        self.tasks = []
        self.font_size = 14

        title_label = ctk.CTkLabel(self, text="TaskNest", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Nouvelle tâche...", width=200)
        self.entry.pack(side="left", padx=5, expand=True, fill="x")

        self.priority_var = ctk.StringVar(value="low")
        self.priority_menu = ctk.CTkOptionMenu(input_frame, values=["low", "medium", "high"], variable=self.priority_var, width=100)
        self.priority_menu.pack(side="left", padx=5)

        self.add_button = ctk.CTkButton(input_frame, text="Ajouter", width=80, command=self.add_task)
        self.add_button.pack(side="left", padx=5)

        zoom_frame = ctk.CTkFrame(self)
        zoom_frame.pack(pady=5, padx=20, fill="x")

        zoom_label = ctk.CTkLabel(zoom_frame, text="Zoom:")
        zoom_label.pack(side="left", padx=5)

        self.zoom_minus = ctk.CTkButton(zoom_frame, text="-", width=30, command=self.zoom_out)
        self.zoom_minus.pack(side="left", padx=2)

        self.zoom_label = ctk.CTkLabel(zoom_frame, text="100%", width=50)
        self.zoom_label.pack(side="left", padx=5)

        self.zoom_plus = ctk.CTkButton(zoom_frame, text="+", width=30, command=self.zoom_in)
        self.zoom_plus.pack(side="left", padx=2)

        self.zoom_reset = ctk.CTkButton(zoom_frame, text="Reset", width=50, command=self.zoom_reset_action)
        self.zoom_reset.pack(side="left", padx=10)

        self.listbox = ctk.CTkTextbox(self, height=200, state="disabled", font=ctk.CTkFont(size=self.font_size))
        self.listbox.pack(pady=10, padx=20, fill="both", expand=True)

        action_frame = ctk.CTkFrame(self)
        action_frame.pack(pady=10)

        self.done_button = ctk.CTkButton(action_frame, text="Terminée", width=100, command=self.mark_done)
        self.done_button.pack(side="left", padx=5)

        self.undone_button = ctk.CTkButton(action_frame, text="Non terminée", width=100, command=self.mark_undone)
        self.undone_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(action_frame, text="Supprimer", width=100, fg_color="#e74c3c", command=self.delete_task)
        self.delete_button.pack(side="left", padx=5)

        self.toggle_button = ctk.CTkButton(self, text="Masquer terminées", command=self.change_toggle)
        self.toggle_button.pack(pady=10)

        self.bind("<Control-plus>", lambda e: self.zoom_in())
        self.bind("<Control-minus>", lambda e: self.zoom_out())
        self.bind("<Control-0>", lambda e: self.zoom_reset_action())

        self.refresh_tasks()

    def zoom_in(self):
        if self.font_size < 28:
            self.font_size += 2
            self.update_zoom()

    def zoom_out(self):
        if self.font_size > 8:
            self.font_size -= 2
            self.update_zoom()

    def zoom_reset_action(self):
        self.font_size = 14
        self.update_zoom()

    def update_zoom(self):
        zoom_percent = int((self.font_size / 14) * 100)
        self.zoom_label.configure(text=f"{zoom_percent}%")
        self.listbox.configure(font=ctk.CTkFont(size=self.font_size))

    def refresh_tasks(self):
        all_tasks = self.manager.get_all_tasks() or []

        if self.toggle == 1:
            self.tasks = [t for t in all_tasks if not t["completed"]]
        else:
            self.tasks = all_tasks

        self.listbox.configure(state="normal")
        self.listbox.delete("1.0", "end")

        for task in self.tasks:
            status = "✔" if task["completed"] else "✗"
            priority_key = task['priority'].lower()
            line = f"[{task['id']}] {status}  {task['title']}  {PRIORITY_ICONS[priority_key]}\n"
            self.listbox.insert("end", line)

        self.listbox.configure(state="disabled")

    def add_task(self):
        title = self.entry.get().strip()
        if title:
            priority = self.priority_var.get()
            self.manager.add_task(title, priority)
            self.entry.delete(0, "end")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Attention", "Entrez un titre")

    def get_task_id(self):
        """Demande l'ID de la tâche à l'utilisateur."""
        dialog = ctk.CTkInputDialog(text="ID de la tâche:", title="Sélection")
        result = dialog.get_input()
        if result and result.isdigit():
            task_id = int(result)
            if any(t["id"] == task_id for t in self.tasks):
                return task_id
            else:
                messagebox.showwarning("Attention", "ID invalide")
        return None

    def mark_done(self):
        task_id = self.get_task_id()
        if task_id is not None:
            self.manager.mark_done(task_id)
            self.refresh_tasks()

    def mark_undone(self):
        task_id = self.get_task_id()
        if task_id is not None:
            self.manager.mark_undone(task_id)
            self.refresh_tasks()

    def delete_task(self):
        task_id = self.get_task_id()
        if task_id is not None:
            self.manager.delete_task(task_id)
            self.refresh_tasks()

    def change_toggle(self):
        self.toggle = 0 if self.toggle == 1 else 1
        if self.toggle == 1:
            self.toggle_button.configure(text="Afficher toutes")
        else:
            self.toggle_button.configure(text="Masquer terminées")
        self.refresh_tasks()


def run():
    app = TaskNestApp()
    app.mainloop()


if __name__ == "__main__":
    run()