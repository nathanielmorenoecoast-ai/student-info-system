"""Command-line interface for the Student Information System.

Run from the project root:  python -m src.main
"""
import sys

from src.models.student import ValidationError
from src.services.student_service import (
    DuplicateStudentError, StudentNotFoundError, StudentService)
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger

MENU = """
===== {title} =====
1. Add student
2. View all students
3. View one student
4. Update student
5. Delete student
6. Search students
7. Export to CSV
0. Exit
"""


def prompt(text):
    return input(text).strip()


def add_student(service):
    student = service.add_student(
        prompt("Student ID: "), prompt("Name: "), prompt("Age: "),
        prompt("Email: "), prompt("Course: "))
    print(f"Added: {student}")


def view_all(service):
    students = service.list_students()
    if not students:
        print("No students on record.")
    for s in students:
        print(s)


def view_one(service):
    print(service.get_student(prompt("Student ID: ")))


def update_student(service):
    sid = prompt("Student ID to update: ")
    print(f"Current: {service.get_student(sid)}")
    print("Leave a field blank to keep its current value.")
    updated = service.update_student(
        sid, name=prompt("New name: "), age=prompt("New age: "),
        email=prompt("New email: "), course=prompt("New course: "))
    print(f"Updated: {updated}")


def delete_student(service):
    sid = prompt("Student ID to delete: ")
    service.get_student(sid)  # fail early if it does not exist
    if prompt(f"Delete {sid}? (y/n): ").lower() == "y":
        service.delete_student(sid)
        print("Deleted.")
    else:
        print("Cancelled.")


def search_students(service):
    results = service.search(prompt("Search keyword: "))
    print(f"{len(results)} result(s)")
    for s in results:
        print(s)


def main():
    config = load_config()
    logger = setup_logger(config["log_file"], config["log_level"])
    service = StudentService(config["data_file"])
    logger.info("Application started")

    def export_csv(svc):
        print(f"Exported to {svc.export_csv(config['export_file'])}")

    actions = {
        "1": add_student, "2": view_all, "3": view_one,
        "4": update_student, "5": delete_student, "6": search_students,
        "7": export_csv,
    }

    while True:
        print(MENU.format(title=config["app_name"]))
        try:
            choice = prompt("Choose an option: ")
        except EOFError:  # input stream closed (e.g. piped input ended)
            return 0
        if choice == "0":
            logger.info("Application exited")
            print("Goodbye!")
            return 0
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Try again.")
            continue
        try:
            action(service)
        except (ValidationError, DuplicateStudentError, StudentNotFoundError) as exc:
            print(f"Error: {exc}")          # expected, user-fixable problems
        except OSError as exc:
            logger.error("File error: %s", exc)
            print("A file error occurred. Check the log for details.")
        except Exception:                    # last-resort safety net
            logger.exception("Unexpected error")
            print("Something went wrong. Details were written to the log.")


if __name__ == "__main__":
    sys.exit(main())
