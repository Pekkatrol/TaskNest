import argparse
from task.manager import TaskManager

def run():
    parser = argparse.ArgumentParser(description="Task Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")

    subparsers.add_parser("list")

    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add":
        manager.add_task(args.title)
    elif args.command == "list":
        manager.list_tasks()
    elif args.command == "done":
        manager.mark_done(args.id)
    elif args.command == "delete":
        manager.delete_task(args.id)
    else:
        parser.print_help()