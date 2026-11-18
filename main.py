"""Launcher for Complexity Class Explorer.

Provides interactive exploration of P (Merge Sort), NP (Subset Sum),
Undecidable (Halting Problem), and Cryptography (RSA & Password Hashing),
as well as automated benchmarking and theoretical concepts.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.interactive_explorer import main_interactive_menu


def main():
    try:
        main_interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExecution interrupted. Exiting Complexity Class Explorer.")
        sys.exit(0)


if __name__ == "__main__":
    main()
