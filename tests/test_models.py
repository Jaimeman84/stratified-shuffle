import pytest
from src.models.student import Student
from src.models.group import Group
from src.utils.constants import SkillLevel

def test_student_creation():
    """Test student creation with different parameters."""
    # Test with required parameters only
    student = Student(name="John Doe")
    assert student.name == "John Doe"
    assert student.email is None
    assert student.skill_level is None
    assert not student.has_responded

    # Test with all parameters
    student = Student(
        name="Jane Doe",
        email="jane@example.com",
        skill_level=SkillLevel.ADVANCED,
        has_responded=True
    )
    assert student.name == "Jane Doe"
    assert student.email == "jane@example.com"
    assert student.skill_level == SkillLevel.ADVANCED
    assert student.has_responded

def test_student_response_submission():
    """Test student response submission logic."""
    student = Student(name="John Doe")
    
    # Test successful submission
    student.submit_response(SkillLevel.INTERMEDIATE)
    assert student.skill_level == SkillLevel.INTERMEDIATE
    assert student.has_responded

    # Test duplicate submission prevention
    with pytest.raises(ValueError):
        student.submit_response(SkillLevel.ADVANCED)

def test_student_string_representation():
    """Test student string representation with and without skill level."""
    student = Student(name="John Doe")
    assert str(student) == "John Doe"

    student.submit_response(SkillLevel.NOVICE)
    assert str(student) == f"John Doe {SkillLevel.NOVICE.emoji}"

def test_group_creation():
    """Test group creation and name generation."""
    group = Group()
    assert group.members == []
    assert isinstance(group.name, str)
    assert len(group.name.split()) == 2  # Should be "Adjective Animal"

def test_group_member_management():
    """Test adding members to a group."""
    group = Group()
    student = Student(name="John Doe")
    student.submit_response(SkillLevel.ADVANCED)
    
    group.add_member(student)
    assert len(group.members) == 1
    assert group.members[0] == student

def test_group_average_skill_level():
    """Test group average skill level calculation."""
    group = Group()
    
    # Empty group should have 0 average
    assert group.average_skill_level == 0.0

    # Add students with different skill levels
    students = [
        Student(name="Student 1", skill_level=SkillLevel.NOVICE, has_responded=True),
        Student(name="Student 2", skill_level=SkillLevel.ADVANCED, has_responded=True),
        Student(name="Student 3", skill_level=SkillLevel.INTERMEDIATE, has_responded=True)
    ]
    
    for student in students:
        group.add_member(student)

    expected_avg = (1 + 3 + 2) / 3  # NOVICE=1, ADVANCED=3, INTERMEDIATE=2
    assert group.average_skill_level == expected_avg

def test_group_skill_emoji():
    """Test group skill emoji based on average level."""
    group = Group()
    
    # Empty group
    assert group.skill_emoji == "🐢"

    # Add expert students
    students = [
        Student(name=f"Student {i}", skill_level=SkillLevel.EXPERT, has_responded=True)
        for i in range(3)
    ]
    for student in students:
        group.add_member(student)
    
    assert group.skill_emoji == "🏁"  # Should show expert emoji for high average 