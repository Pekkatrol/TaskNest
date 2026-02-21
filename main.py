import tkinter as tk
from task.gui import TaskApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()