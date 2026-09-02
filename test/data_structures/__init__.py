"""
Test package for data_structures.
"""

from pathlib import Path
import sys

_src_dir = Path(__file__).resolve().parent.parent.parent / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))
