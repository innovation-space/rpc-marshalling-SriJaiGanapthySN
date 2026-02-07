from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class StudentProfile:
    name: str
    id: int
    grades: List[int]

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "id": self.id, "grades": self.grades}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StudentProfile":
        return StudentProfile(d["name"], d["id"], d["grades"])
