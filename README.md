# Stratified Shuffle

A Streamlit application for creating balanced groups based on skill levels. Perfect for classroom settings, workshops, or any scenario requiring balanced team formation. Optimized for Zoom breakout rooms.

## Features

- **Admin Panel**:
  - Simple bulk student roster management (paste multiple names at once)
  - Monitor response status with progress bar
  - Configure group sizes
  - Generate and shuffle balanced groups
  - Clear roster functionality
  - Password protected admin access

- **Student Survey**:
  - Simple one-click skill level selection
  - Duplicate submission prevention
  - Instant feedback
  - Four skill levels with fun descriptions:
    - 🐢 (1) - I'm stalling a bit (Novice)
    - ⚙️ (2) - I'm shifting gears (Intermediate)
    - 🚀 (3) - I'm cruising (Advanced)
    - 🏁 (4) - I'm in the fast lane (Expert)

- **Smart Group Formation**:
  - Stratified distribution of skill levels
  - Balanced group sizes
  - Fun team names with emojis
  - Visual skill level indicators
  - Organized by Zoom breakout room numbers
  - Clear group display with detailed skill information
  - Average skill level display per group

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stratified-shuffle.git
   cd stratified-shuffle
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   ADMIN_PASSWORD=your_secure_password
   ```

5. Run the application:
   ```bash
   python run_app.py
   ```

## Usage

1. **Admin Setup**:
   - Access the admin page and log in
   - Paste student names in the text area (one per line)
   - Click "Add Students" to populate the roster
   - Monitor student responses in real-time

2. **Student Response**:
   - Students select their name from the dropdown
   - Choose their skill level with one click
   - Receive immediate confirmation

3. **Group Formation**:
   - Set desired group size
   - Click "Create Groups" when all responses are in
   - View groups organized by Zoom breakout room numbers
   - Each group shows:
     - Room number and fun team name
     - Average skill level
     - Member list with detailed skill information

## Project Structure

```
stratified-shuffle/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py        # Student data model
│   │   └── group.py          # Group data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── group_service.py  # Group formation logic
│   └── utils/
│       ├── __init__.py
│       └── constants.py      # Application constants
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Testing

Run tests using pytest:
```bash
pytest tests/
```

---
Created by Jaime Mantilla, MSIT + AI  
Last Updated: 08/2025