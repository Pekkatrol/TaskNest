from tasknest.gui import TaskApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()