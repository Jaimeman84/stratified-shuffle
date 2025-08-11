import pytest
from src.models.student import Student
from src.services.group_service import GroupService
from src.utils.constants import SkillLevel

def create_test_students():
    """Helper function to create a list of test students with responses."""
    students = [
        Student(name="Expert 1", skill_level=SkillLevel.EXPERT, has_responded=True),
        Student(name="Expert 2", skill_level=SkillLevel.EXPERT, has_responded=True),
        Student(name="Advanced 1", skill_level=SkillLevel.ADVANCED, has_responded=True),
        Student(name="Advanced 2", skill_level=SkillLevel.ADVANCED, has_responded=True),
        Student(name="Intermediate 1", skill_level=SkillLevel.INTERMEDIATE, has_responded=True),
        Student(name="Intermediate 2", skill_level=SkillLevel.INTERMEDIATE, has_responded=True),
        Student(name="Novice 1", skill_level=SkillLevel.NOVICE, has_responded=True),
        Student(name="Novice 2", skill_level=SkillLevel.NOVICE, has_responded=True),
    ]
    return students

def test_validate_responses():
    """Test response validation logic."""
    # All responded
    students = create_test_students()
    assert GroupService.validate_responses(students) is True

    # Mixed responses
    students.append(Student(name="No Response"))
    assert GroupService.validate_responses(students) is False

def test_get_response_status():
    """Test response status calculation."""
    students = create_test_students()
    responses, total = GroupService.get_response_status(students)
    assert responses == 8
    assert total == 8

    # Add non-responder
    students.append(Student(name="No Response"))
    responses, total = GroupService.get_response_status(students)
    assert responses == 8
    assert total == 9

def test_create_stratified_groups():
    """Test group creation with stratification."""
    students = create_test_students()
    
    # Test with group size of 4 (should create 2 groups)
    groups = GroupService.create_stratified_groups(students, group_size=4)
    assert len(groups) == 2
    
    # Verify each group has 4 members
    assert all(len(group.members) == 4 for group in groups)
    
    # Verify skill distribution (each group should have mix of levels)
    for group in groups:
        skill_levels = [member.skill_level for member in group.members]
        assert len(set(skill_levels)) > 1  # Should have multiple skill levels

def test_create_stratified_groups_uneven():
    """Test group creation with non-uniform group sizes."""
    students = create_test_students()
    
    # Test with group size of 3 (should create 3 groups, one smaller)
    groups = GroupService.create_stratified_groups(students, group_size=3)
    assert len(groups) == 3
    
    # Verify group sizes are within ±1 of target
    group_sizes = [len(group.members) for group in groups]
    assert all(2 <= size <= 3 for size in group_sizes)
    assert sum(group_sizes) == len(students)

def test_create_stratified_groups_validation():
    """Test group creation validation."""
    students = create_test_students()
    
    # Add a student without response
    students.append(Student(name="No Response"))
    
    # Should raise ValueError when not all students have responded
    with pytest.raises(ValueError):
        GroupService.create_stratified_groups(students)

def test_create_stratified_groups_single_group():
    """Test group creation with small number of students."""
    students = create_test_students()[:3]  # Take only 3 students
    
    groups = GroupService.create_stratified_groups(students, group_size=5)
    assert len(groups) == 1
    assert len(groups[0].members) == 3

def test_create_stratified_groups_skill_order():
    """Test that higher skill levels are distributed first."""
    students = create_test_students()
    groups = GroupService.create_stratified_groups(students, group_size=4)
    
    # First student in each group should be Expert or Advanced
    first_students_levels = [group.members[0].skill_level for group in groups]
    assert all(level in (SkillLevel.EXPERT, SkillLevel.ADVANCED) for level in first_students_levels) 