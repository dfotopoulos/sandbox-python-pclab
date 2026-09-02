"""
Root test package with automatic sys.path resolution.
"""

from pathlib import Path
import sys

_src_dir = Path(__file__).resolve().parent.parent / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))
