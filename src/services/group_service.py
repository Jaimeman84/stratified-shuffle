from typing import List, Dict
import random
from models.student import Student
from models.group import Group
from utils.constants import SkillLevel, DEFAULT_GROUP_SIZE

class GroupService:
    """Service class for handling group formation logic."""

    @staticmethod
    def create_stratified_groups(students: List[Student], group_size: int = DEFAULT_GROUP_SIZE) -> List[Group]:
        """
        Create balanced groups using stratified round-robin distribution.
        
        Args:
            students (List[Student]): List of students to group
            group_size (int): Target size for each group
            
        Returns:
            List[Group]: List of formed groups
        """
        if not all(student.has_responded for student in students):
            raise ValueError("All students must respond before groups can be formed")

        # Calculate number of groups needed
        num_students = len(students)
        num_groups = max(1, (num_students + group_size - 1) // group_size)
        groups = [Group() for _ in range(num_groups)]

        # Sort students by skill level and shuffle within each level
        students_by_level: Dict[SkillLevel, List[Student]] = {
            level: [] for level in SkillLevel
        }
        
        for student in students:
            if student.skill_level:
                students_by_level[student.skill_level].append(student)

        # Shuffle each skill level group
        for level_group in students_by_level.values():
            random.shuffle(level_group)

        # Distribute students in round-robin fashion, starting with highest skill level
        current_group_idx = 0
        
        # Start with highest skill level and work down
        for level in reversed(list(SkillLevel)):
            level_students = students_by_level[level]
            for student in level_students:
                groups[current_group_idx].add_member(student)
                current_group_idx = (current_group_idx + 1) % num_groups

        return groups

    @staticmethod
    def validate_responses(roster: List[Student]) -> bool:
        """
        Check if all students in the roster have responded.
        
        Args:
            roster (List[Student]): List of students to check
            
        Returns:
            bool: True if all students have responded
        """
        return all(student.has_responded for student in roster)

    @staticmethod
    def get_response_status(roster: List[Student]) -> tuple[int, int]:
        """
        Get the current response status.
        
        Args:
            roster (List[Student]): List of students to check
            
        Returns:
            tuple[int, int]: (number of responses, total roster size)
        """
        responses = sum(1 for student in roster if student.has_responded)
        return responses, len(roster) 