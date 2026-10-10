"""Student service: business logic and JSON persistence (CRUD + extras)."""
import csv
import json
import logging
import os

from src.models.student import Student, ValidationError

logger = logging.getLogger("sis")


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(Exception):
    """Raised when adding a student whose ID already exists."""


class StudentService:
    def __init__(self, data_file):
        self.data_file = data_file
        self.students = {}
        self._load()

    # ---------- persistence ----------
    def _load(self):
        """Load students from JSON. Recovers from missing/corrupt files."""
        if not os.path.exists(self.data_file):
            logger.warning("Data file missing; starting empty: %s", self.data_file)
            self._save()
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            for rec in records:
                student = Student.from_dict(rec)
                self.students[student.student_id] = student
            logger.info("Loaded %d students", len(self.students))
        except (json.JSONDecodeError, KeyError, TypeError, ValidationError) as exc:
            # Advanced error recovery: back up the bad file, start fresh.
            backup = self.data_file + ".corrupt"
            os.replace(self.data_file, backup)
            logger.error("Corrupt data file (%s). Backed up to %s", exc, backup)
            self.students = {}
            self._save()

    def _save(self):
        """Write all students to JSON (atomic write to avoid partial files)."""
        os.makedirs(os.path.dirname(self.data_file) or ".", exist_ok=True)
        tmp = self.data_file + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self.students.values()], f, indent=2)
            os.replace(tmp, self.data_file)
        except OSError as exc:
            logger.error("Failed to save data: %s", exc)
            raise

    # ---------- CRUD ----------
    def add_student(self, student_id, name, age, email, course):
        if student_id in self.students:
            raise DuplicateStudentError(f"Student ID '{student_id}' already exists.")
        student = Student(student_id, name, age, email, course)  # validates
        self.students[student_id] = student
        self._save()
        logger.info("Added student %s", student_id)
        return student

    def get_student(self, student_id):
        try:
            return self.students[student_id]
        except KeyError:
            raise StudentNotFoundError(f"Student '{student_id}' not found.")

    def list_students(self):
        return sorted(self.students.values(), key=lambda s: s.student_id)

    def update_student(self, student_id, **fields):
        """Update only the provided, non-empty fields."""
        current = self.get_student(student_id)
        data = current.to_dict()
        data.update({k: v for k, v in fields.items() if v not in (None, "")})
        updated = Student.from_dict(data)  # re-validates
        self.students[student_id] = updated
        self._save()
        logger.info("Updated student %s", student_id)
        return updated

    def delete_student(self, student_id):
        self.get_student(student_id)  # raises if missing
        del self.students[student_id]
        self._save()
        logger.info("Deleted student %s", student_id)

    # ---------- bonus features ----------
    def search(self, keyword):
        """Case-insensitive search across name, course, email and ID."""
        kw = keyword.lower().strip()
        return [s for s in self.list_students()
                if kw in s.name.lower() or kw in s.course.lower()
                or kw in s.email.lower() or kw in s.student_id.lower()]

    def export_csv(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["student_id", "name", "age", "email", "course"])
            writer.writeheader()
            for s in self.list_students():
                writer.writerow(s.to_dict())
        logger.info("Exported %d students to %s", len(self.students), path)
        return path
