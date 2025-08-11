from enum import Enum

class SkillLevel(Enum):
    NOVICE = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

    @property
    def emoji(self):
        return SKILL_EMOJIS[self]

    @property
    def description(self):
        return SKILL_DESCRIPTIONS[self]

SKILL_EMOJIS = {
    SkillLevel.NOVICE: "🐢",
    SkillLevel.INTERMEDIATE: "⚙️",
    SkillLevel.ADVANCED: "🚀",
    SkillLevel.EXPERT: "🏁"
}

SKILL_DESCRIPTIONS = {
    SkillLevel.NOVICE: "I'm stalling a bit",
    SkillLevel.INTERMEDIATE: "I'm shifting gears",
    SkillLevel.ADVANCED: "I'm cruising",
    SkillLevel.EXPERT: "I'm in the fast lane"
}

# Fun team name components
ADJECTIVES = [
    "Quantum", "Async", "Binary", "Cosmic", "Digital",
    "Epic", "Fuzzy", "Galactic", "Hyper", "Infinite"
]

ANIMALS = [
    "Koalas", "Otters", "Pandas", "Dragons", "Foxes",
    "Wolves", "Eagles", "Tigers", "Lions", "Bears"
]

# Default configuration
DEFAULT_GROUP_SIZE = 5
DEFAULT_ADMIN_PAGE = "admin"
DEFAULT_STUDENT_PAGE = "student" 