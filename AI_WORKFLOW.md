# AI-assisted development notes

These notes describe the development process for Mini-Project 2. They are a
summary of the AI-assisted work, not a verbatim transcript of the chat.

## 1. Task definition

Create a simple Python console tool that helps a university student manage
assignment deadlines. The main benefit is that the program automatically
calculates time remaining, flags overdue work, and saves tasks between runs.
Use Python's standard library and keep the interface suitable for beginners.

## 2. Code generation and first run

The assistant drafted `scripts/deadline_tracker.py` with the `add` and `list`
commands. The code was executed in a terminal with a sample assignment, and
JSON persistence and the list output were checked.

A second version added `done` and `upcoming` and calculated the deadline status
using `datetime.date`.

## 3. Debugging: a real issue

A set of tests was created with Python's built-in `unittest` module. The first
complete test run had **7 passed, 1 failed**. The failing test was:

`test_upcoming_includes_overdue_tasks`

The problem was the condition in `show_upcoming`:

```python
0 <= days_until(task, today) <= days
```

A negative number of days means an assignment is already overdue. This
condition incorrectly excluded it from the urgent list. The condition was
corrected to:

```python
days_until(task, today) <= days
```

The initial tests were run again after the correction: **8 passed, 0 failed**.

## 4. Additional review and debugging

During a second review, the original eight tests passed. Manual checks then
found another problem: `tasks.json` could contain well-formed JSON with the
wrong structure, such as `{}` or `[42]`. Some commands crashed with a Python
traceback rather than giving a clear error. Three more automated tests were
added to reproduce these cases, including invalid fields and duplicate IDs.
The JSON loading function was updated to validate saved records first and
leave the file unchanged when they are not valid.

After the fix, **11 tests passed, 0 failed**. This second debugging cycle is
also recorded in Git as separate test, fix, and documentation commits.

## 5. Documentation and version control

The README explains the everyday problem, software requirements, exact
commands, example output, data storage, and tests. Git commits preserve the
steps of implementation, testing, debugging, and documentation.

## 6. What to check yourself before submission

Run the script locally, add one of your own deadlines, inspect `list` and
`upcoming`, mark the task completed, and check that `tasks.json` changes.
Then run the automated tests. Verify the public GitHub repository includes
`README.md` and several commits rather than only uploaded files.
