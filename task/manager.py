from task.storage import load_tasks, save_tasks

class TaskManager:

    def add_task(self, title):
        tasks = load_tasks()
        task_id = len(tasks) + 1

        tasks.append({
            "id": task_id,
            "title": title,
            "completed": False
        })
        save_tasks(tasks)
        print(f"Task added: {title}")
    
    def list_task(self):
        tasks = load_tasks()

        if not tasks:
            print("No task.")
            return
        
        for task in tasks:
            status = "Done" if task["completed"] else "Not Done"
            print(f"{task['id']} - [{status}] {task['title']}")

    def mark_done(self, task_id):
        tasks = load_tasks()

        for task in tasks:
            if (task['id'] == task_id):
                task['completed'] = True
                save_tasks(tasks)
                print("Task completed.")
                return
        
        print("Task not found.")

    def delete_task(self, task_id):
        tasks = load_tasks()
        tasks = [task for task in tasks if (task['id'] != task_id)]

        save_tasks(tasks)
        print("Task deleted.")