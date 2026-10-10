"""Unit tests for the student model and service.

Run with either:  python -m unittest discover -s tests -t .   or   pytest -v
"""
import json
import os
import tempfile
import unittest

from src.models.student import Student, ValidationError
from src.services.student_service import (
    DuplicateStudentError, StudentNotFoundError, StudentService)


class StudentServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "students.json")
        self.service = StudentService(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def add_sample(self, sid="S001"):
        return self.service.add_student(
            sid, "Juan Dela Cruz", 20, "juan@example.com", "BSIT")

    def test_add_and_get(self):
        self.add_sample()
        self.assertEqual(self.service.get_student("S001").name, "Juan Dela Cruz")

    def test_duplicate_id_rejected(self):
        self.add_sample()
        with self.assertRaises(DuplicateStudentError):
            self.add_sample()

    def test_update_keeps_blank_fields(self):
        self.add_sample()
        updated = self.service.update_student("S001", name="", course="BSCS")
        self.assertEqual(updated.name, "Juan Dela Cruz")
        self.assertEqual(updated.course, "BSCS")

    def test_delete(self):
        self.add_sample()
        self.service.delete_student("S001")
        with self.assertRaises(StudentNotFoundError):
            self.service.get_student("S001")

    def test_persistence(self):
        self.add_sample()
        reloaded = StudentService(self.path)
        self.assertEqual(reloaded.get_student("S001").email, "juan@example.com")

    def test_validation_errors(self):
        with self.assertRaises(ValidationError):
            Student("S1", "Bad Email", 20, "not-an-email", "BSIT")
        with self.assertRaises(ValidationError):
            Student("S1", "Too Young", 2, "a@b.co", "BSIT")

    def test_search_and_export(self):
        self.add_sample()
        self.assertEqual(len(self.service.search("bsit")), 1)
        out = self.service.export_csv(os.path.join(self.tmp.name, "out.csv"))
        with open(out, encoding="utf-8") as f:
            self.assertIn("Juan Dela Cruz", f.read())

    def test_corrupt_file_recovery(self):
        with open(self.path, "w") as f:
            f.write("{not valid json")
        service = StudentService(self.path)
        self.assertEqual(service.list_students(), [])
        self.assertTrue(os.path.exists(self.path + ".corrupt"))
        with open(self.path) as f:
            self.assertEqual(json.load(f), [])


if __name__ == "__main__":
    unittest.main()
