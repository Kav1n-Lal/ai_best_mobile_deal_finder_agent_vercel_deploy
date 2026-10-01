import sys
from pathlib import Path

# Adds the root project directory to Python's sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))