"""Student model: a plain data class with validation and dict conversion."""
import re
from dataclasses import dataclass, asdict

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class ValidationError(ValueError):
    """Raised when student data fails validation."""


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    email: str
    course: str

    def __post_init__(self):
        self.validate()

    def validate(self):
        """Validate all fields; raise ValidationError on the first problem."""
        if not str(self.student_id).strip():
            raise ValidationError("Student ID cannot be empty.")
        if not str(self.name).strip():
            raise ValidationError("Name cannot be empty.")
        try:
            self.age = int(self.age)
        except (TypeError, ValueError):
            raise ValidationError("Age must be a whole number.")
        if not 5 <= self.age <= 100:
            raise ValidationError("Age must be between 5 and 100.")
        if not EMAIL_PATTERN.match(str(self.email)):
            raise ValidationError("Email format is invalid.")
        if not str(self.course).strip():
            raise ValidationError("Course cannot be empty.")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            email=data["email"],
            course=data["course"],
        )

    def __str__(self):
        return (f"[{self.student_id}] {self.name} | Age: {self.age} | "
                f"{self.email} | Course: {self.course}")
