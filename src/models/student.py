from dataclasses import dataclass
from typing import Optional
from utils.constants import SkillLevel

@dataclass
class Student:
    """
    Represents a student in the system.
    
    Attributes:
        name (str): The student's name
        email (Optional[str]): The student's email (optional)
        skill_level (Optional[SkillLevel]): The student's self-reported skill level
        has_responded (bool): Whether the student has submitted their skill level
    """
    name: str
    email: Optional[str] = None
    skill_level: Optional[SkillLevel] = None
    has_responded: bool = False

    def submit_response(self, skill_level: SkillLevel) -> None:
        """
        Submit the student's skill level response.
        
        Args:
            skill_level (SkillLevel): The chosen skill level
        """
        if self.has_responded:
            raise ValueError(f"Student {self.name} has already submitted a response")
        
        self.skill_level = skill_level
        self.has_responded = True

    def __str__(self) -> str:
        """String representation with emoji if skill level is set."""
        if self.skill_level:
            return f"{self.name} {self.skill_level.emoji}"
        return self.name 