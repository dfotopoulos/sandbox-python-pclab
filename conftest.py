"""
Pytest configuration and root path resolution for Python Language Mastery Sandbox.
"""

from pathlib import Path
import sys

# Ensure src directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
