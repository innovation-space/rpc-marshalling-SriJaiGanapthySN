"""
Student Profile Model

This module defines the StudentProfile class used for RPC communication.
The marshalling/unmarshalling logic is handled by the marshalling layer.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class StudentProfile:
    """
    Represents a student's profile with their grades.
    
    Attributes:
        name: Student's full name (string)
        id: Student's unique identifier (integer)
        grades: List of student's grades (list of integers)
    """
    name: str
    id: int
    grades: List[int]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert StudentProfile object to a dictionary for marshalling.
        
        Returns:
            Dictionary representation of the StudentProfile
        """
        return {
            "name": self.name,
            "id": self.id,
            "grades": self.grades
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "StudentProfile":
        """
        Create a StudentProfile object from a dictionary (unmarshalling).
        
        Args:
            data: Dictionary containing name, id, and grades
            
        Returns:
            A new StudentProfile instance
        """
        return StudentProfile(
            name=data["name"],
            id=data["id"],
            grades=data["grades"]
        )

    def __str__(self) -> str:
        return f"StudentProfile(name='{self.name}', id={self.id}, grades={self.grades})"
