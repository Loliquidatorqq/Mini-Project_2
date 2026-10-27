# Student Deadline Tracker

A small Python command-line tool for tracking university assignment deadlines.
Students often have several assignments with different submission dates. This
script stores a list of tasks, calculates how many days are left, highlights
late assignments, and lets the user mark finished work. It replaces checking
deadlines manually in a notebook or spreadsheet.

**Mini-Project 2: Programming** — Introduction to Artificial Intelligence Practical Tools

## Requirements

- Python 3.9 or newer
- A terminal (Command Prompt, PowerShell, Bash, or another shell)
- No third-party libraries or internet connection

## How to run

1. Download or clone this repository and open a terminal in its folder.
2. Run the commands below. On Windows, use `python`; on macOS/Linux, use
   `python3` if `python` is not available.

**Add an assignment** (put multi-word titles in quotation marks):

```bash
python scripts/deadline_tracker.py add "Mini-Project 2" 2026-10-28
python scripts/deadline_tracker.py add "Statistics homework" 2026-11-05
```

**See unfinished assignments**, sorted by due date:

```bash
python scripts/deadline_tracker.py list
```

The status is calculated automatically from the computer's current date:
`In 3d` (three days left), `Due today`, or `Overdue 2d` (two days late).

**Check urgent assignments** (overdue and due in the next 7 days):

```bash
python scripts/deadline_tracker.py upcoming
```

To change the time window, for example to 14 days:

```bash
python scripts/deadline_tracker.py upcoming --days 14
```

**Mark an assignment as completed** (use its ID from `list`):

```bash
python scripts/deadline_tracker.py done 1
```

**Show completed assignments too:**

```bash
python scripts/deadline_tracker.py list --all
```

**Show command help:**

```bash
python scripts/deadline_tracker.py --help
```

### Example of the console output

The numbers below are illustrative; the displayed status changes with the date.

```text
ID    Due date     Status         Title
--------------------------------------------------------------
1     2026-10-28   In 1d          Mini-Project 2
2     2026-11-05   In 9d          Statistics homework
```

## Where the data is stored

The script creates `tasks.json` in the repository folder on the first `add`.
Data is saved after each change, so assignments remain available after the
program closes. This file is in `.gitignore` because it contains personal task
data; it should not be uploaded to GitHub.

You can choose a different data file by putting `--data-file` **before** a
command:

```bash
python scripts/deadline_tracker.py --data-file example.json add "Exam" 2026-12-15
```

## Input checks

- Deadlines must be real dates in `YYYY-MM-DD` format.
- Assignment titles cannot be blank.
- An unknown task ID causes an error instead of modifying another task.
- A negative `--days` value is rejected.
- If the JSON file is unreadable or contains invalid JSON, the program reports
  an error instead of silently replacing the file.

## How to test

From the repository folder, run:

```bash
python -m unittest discover -s tests -v
```

The tests check saving/loading, validation, marking work as finished,
upcoming/overdue deadlines, and error handling.

## Project files

```text
student-deadline-tracker/
├── scripts/
│   └── deadline_tracker.py   # Python console program
├── tests/
│   └── test_deadline_tracker.py  # Automated checks
├── .gitignore               # Keeps local task data out of Git
├── AI_WORKFLOW.md           # Notes on the AI-assisted development process
└── README.md                # This guide
```

## AI and Git workflow

AI assistance was used to draft the Python functions, review errors, create
basic tests, and prepare this README. The script and tests were run in a
terminal, and a failing test for overdue tasks was used to identify and fix a
bug. See [AI_WORKFLOW.md](AI_WORKFLOW.md) for the development notes.

Git version history is visible using:

```bash
git log --oneline
```

The commits show the original script, new commands, a test suite, a bug fix,
and the documentation.
