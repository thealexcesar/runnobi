"""
Runnobi - Ninja Endless Runner

Academic Project - Clean Architecture & Design Patterns
Author: Alex Cesar da Silva
Repo: https://github.com/yourusername/runnobi.git

University: Centro Universitário UNINTER
Discipline: Linguagem de Programação Aplicada
Professor: Vinicius Pozzobon Borin
Course: Análise e Desenvolvimento de Sistemas
Student ID: 3387546
Date: December 7, 2025
"""
import sys
import os

if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets") if not hasattr(sys, "_MEIPASS") else os.path.join(BASE_DIR, "assets")

from src.application.game_manager import GameManager


def main():
    print("RUNNOBI - Ninja Endless Runner")
    print("=" * 50)
    print("Starting at MENU...")
    print("\nControls:")
    print("  SPACE/W/UP        - Jump (double jump available)")
    print("  DOWN/S            - Crouch (slide under obstacles)")
    print("  X/Z/LEFT/RIGHT    - Attack (destroy wooden crates)")
    print("  ESC               - Pause / Return to menu")
    print("\nTips:")
    print("  - Destroy wooden crates for +100 points!")
    print("  - Crouch OR attack to break wooden crates")
    print("  - Use double jump for high obstacles")
    print("  - Crouch under low blockers from ceiling")
    print("  - Speed increases over time!")
    print("=" * 50)
    print("\nStarting game...\n")

    try:
        game = GameManager()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")

    print("\nGame closed successfully!")


if __name__ == "__main__":
    main()

    if os.name == "nt":
        os.system("pause")
