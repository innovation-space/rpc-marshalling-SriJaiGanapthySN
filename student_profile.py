from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class StudentProfile:
    name: str
    id: int
    grades: List[int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "id": self.id,
            "grades": self.grades
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "StudentProfile":
        return StudentProfile(
            name=data["name"],
            id=data["id"],
            grades=data["grades"]
        )

    def __str__(self) -> str:
        return f"StudentProfile(name='{self.name}', id={self.id}, grades={self.grades})"
