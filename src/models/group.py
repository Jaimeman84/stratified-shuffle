from dataclasses import dataclass, field
from typing import List
import random
from utils.constants import ADJECTIVES, ANIMALS
from models.student import Student

@dataclass
class Group:
    """
    Represents a group of students.
    
    Attributes:
        name (str): The generated fun name for the group
        members (List[Student]): List of students in the group
    """
    members: List[Student] = field(default_factory=list)
    name: str = field(init=False)

    def __post_init__(self):
        """Generate a random fun name for the group."""
        self.name = f"{random.choice(ADJECTIVES)} {random.choice(ANIMALS)}"

    @property
    def average_skill_level(self) -> float:
        """Calculate the average skill level of the group."""
        if not self.members or not all(m.skill_level for m in self.members):
            return 0.0
        return sum(m.skill_level.value for m in self.members) / len(self.members)
    
    @property
    def skill_emoji(self) -> str:
        """Return emoji representation of the average skill level."""
        avg = self.average_skill_level
        if avg >= 3.5:
            return "🏁"
        elif avg >= 2.5:
            return "🚀"
        elif avg >= 1.5:
            return "⚙️"
        return "🐢"

    def add_member(self, student: Student) -> None:
        """Add a student to the group."""
        self.members.append(student)

    def __str__(self) -> str:
        """String representation of the group."""
        return f"{self.name} {self.skill_emoji} (Avg: {self.average_skill_level:.1f})" 