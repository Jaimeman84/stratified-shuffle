import streamlit as st
import os
from dotenv import load_dotenv
from typing import List, Optional
import pandas as pd

from models.student import Student
from models.group import Group
from services.group_service import GroupService
from utils.constants import (
    SkillLevel,
    DEFAULT_GROUP_SIZE,
    DEFAULT_ADMIN_PAGE,
    DEFAULT_STUDENT_PAGE
)

# Load environment variables
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")  # Default for development

def init_session_state():
    """Initialize session state variables."""
    if "roster" not in st.session_state:
        st.session_state.roster: List[Student] = []
    if "group_size" not in st.session_state:
        st.session_state.group_size = DEFAULT_GROUP_SIZE
    if "groups" not in st.session_state:
        st.session_state.groups: List[Group] = []

def admin_page():
    """Render the admin page."""
    st.title("Stratified Shuffle - Admin")
    
    # Password protection
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter admin password:", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        return

    # Roster management
    st.header("Roster Management")
    
    # Bulk text input
    st.write("Enter student names (one per line):")
    bulk_names = st.text_area(
        "Student Names",
        height=200,
        help="Enter each student name on a new line",
        label_visibility="collapsed"
    )
    
    if st.button("Add Students"):
        if bulk_names:
            # Split names by newline and filter out empty lines
            names = [name.strip() for name in bulk_names.split("\n") if name.strip()]
            
            # Add new students to roster
            for name in names:
                if not any(s.name == name for s in st.session_state.roster):
                    st.session_state.roster.append(Student(name=name))
            
            st.success(f"Added {len(names)} students to roster")
            st.rerun()

    # Display current roster
    if st.session_state.roster:
        st.subheader("Current Roster")
        responses, total = GroupService.get_response_status(st.session_state.roster)
        st.progress(responses / total, text=f"Responses: {responses}/{total}")
        
        roster_df = pd.DataFrame([
            {
                "Name": s.name,
                "Status": "✅" if s.has_responded else "⏳",
                "Skill Level": f"{s.skill_level.emoji} ({s.skill_level.value}) - {s.skill_level.description}" if s.skill_level else ""
            }
            for s in st.session_state.roster
        ])
        st.dataframe(roster_df, hide_index=True, use_container_width=True)

        if st.button("Clear Roster"):
            st.session_state.roster = []
            st.session_state.groups = []
            st.rerun()

    # Group formation
    st.header("Group Formation")
    st.session_state.group_size = st.number_input(
        "Group Size",
        min_value=2,
        max_value=10,
        value=st.session_state.group_size
    )

    if st.button(
        "Create Groups",
        disabled=not GroupService.validate_responses(st.session_state.roster)
    ):
        try:
            st.session_state.groups = GroupService.create_stratified_groups(
                st.session_state.roster,
                st.session_state.group_size
            )
            st.success("Groups created successfully!")
        except ValueError as e:
            st.error(str(e))

    # Display groups
    if st.session_state.groups:
        st.subheader("Groups")
        
        # Create columns to display groups side by side
        cols = st.columns(min(3, len(st.session_state.groups)))
        
        for idx, group in enumerate(st.session_state.groups, 1):
            # Calculate which column to use
            col_idx = (idx - 1) % len(cols)
            
            with cols[col_idx]:
                st.write(f"#### 🎥 Breakout Room {idx}")
                st.write(f"**{group.name}** {group.skill_emoji} (Avg: {group.average_skill_level:.1f})")
                
                # Create group data
                group_data = [{
                    "Name": f"{member.name}",
                    "Skill Level": f"{member.skill_level.emoji} ({member.skill_level.value}) - {member.skill_level.description}"
                } for member in group.members]
                
                # Display group table
                group_df = pd.DataFrame(group_data)
                st.dataframe(
                    group_df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Name": st.column_config.Column(
                            width="medium"
                        ),
                        "Skill Level": st.column_config.Column(
                            width="large"
                        )
                    }
                )
                st.write("---")

def student_page():
    """Render the student page."""
    st.title("Stratified Shuffle - Student Survey")

    if not st.session_state.roster:
        st.warning("No students in roster yet. Please wait for the admin to add students.")
        return

    # Student selection
    available_students = [
        s.name for s in st.session_state.roster if not s.has_responded
    ]
    
    if not available_students:
        st.success("All students have completed the survey!")
        return

    selected_name = st.selectbox(
        "Select your name:",
        options=available_students
    )

    selected_student = next(
        (s for s in st.session_state.roster if s.name == selected_name),
        None
    )

    if selected_student:
        st.write("### How would you rate your current skill level?")
        
        for level in SkillLevel:
            if st.button(
                f"{level.emoji} {level.description}",
                key=f"skill_{level.name}",
                use_container_width=True
            ):
                selected_student.submit_response(level)
                st.success("Thanks for your response! ✨")
                st.rerun()

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Stratified Shuffle",
        page_icon="🎲",
        layout="wide"
    )

    init_session_state()

    # Page navigation
    page = st.sidebar.radio("Select Page", [DEFAULT_ADMIN_PAGE, DEFAULT_STUDENT_PAGE])
    
    if page == DEFAULT_ADMIN_PAGE:
        admin_page()
    else:
        student_page()

if __name__ == "__main__":
    main() 