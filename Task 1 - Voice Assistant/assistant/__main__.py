"""
Alternate entry: from the project root (folder that contains main.py), run:

    python -m assistant

Loads the same code path as ``python main.py`` after clearing ``assistant/__pycache__``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

_pkg = Path(__file__).resolve().parent
_root = _pkg.parent
_pyc = _pkg / "__pycache__"
if _pyc.is_dir():
    for f in _pyc.glob("*.pyc"):
        try:
            f.unlink()
        except OSError:
            pass

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

if __name__ == "__main__":
    import main as _main

    _main.main()
