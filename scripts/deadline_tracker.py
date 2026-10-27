"""Track assignment deadlines using a simple command-line interface."""

import argparse
import json
from datetime import date
from pathlib import Path


DEFAULT_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def parse_date(value):
    """Read a date in YYYY-MM-DD format or show a helpful CLI error."""
    try:
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Use a valid date in YYYY-MM-DD format")


def load_tasks(file_path):
    """Load saved tasks; return an empty list for a new tracker."""
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(file_path, tasks):
    """Save tasks so they are available on the next run."""
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)


def add_task(tasks, title, due_date):
    """Add a new assignment and return its ID."""
    if not title.strip():
        raise ValueError("Task title cannot be empty")
    task_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({
        "id": task_id,
        "title": title.strip(),
        "due": due_date.isoformat(),
        "done": False,
    })
    return task_id


def show_tasks(tasks, include_done=False):
    """Print saved assignments in order of their deadlines."""
    visible = [task for task in tasks if include_done or not task["done"]]
    if not visible:
        print("No assignments to show.")
        return
    print(f"{'ID':<5} {'Due date':<12} {'Status':<14} Title")
    print("-" * 62)
    for task in sorted(visible, key=lambda item: item["due"]):
        status = "Done" if task["done"] else "Pending"
        print(f"{task['id']:<5} {task['due']:<12} {status:<14} {task['title']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Track university assignment deadlines")
    parser.add_argument("--data-file", type=Path, default=DEFAULT_FILE,
                        help="location of the saved JSON file")
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="add an assignment")
    add_parser.add_argument("title", help="assignment name (in quotes if needed)")
    add_parser.add_argument("due", type=parse_date, help="deadline: YYYY-MM-DD")

    list_parser = commands.add_parser("list", help="list assignments")
    list_parser.add_argument("--all", action="store_true", help="include finished tasks")

    args = parser.parse_args(argv)
    try:
        tasks = load_tasks(args.data_file)
        if args.command == "add":
            task_id = add_task(tasks, args.title, args.due)
            save_tasks(args.data_file, tasks)
            print(f"Added assignment #{task_id}: {args.title.strip()}")
        elif args.command == "list":
            show_tasks(tasks, include_done=args.all)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
