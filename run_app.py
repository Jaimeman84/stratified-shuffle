import os
import sys

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, src_path)

if __name__ == "__main__":
    os.system(f"streamlit run {os.path.join(src_path, 'app.py')}") 