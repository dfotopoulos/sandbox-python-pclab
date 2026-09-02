"""
Pytest configuration for test suite and sys.path resolution.
"""

from pathlib import Path
import sys

# Ensure src directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
