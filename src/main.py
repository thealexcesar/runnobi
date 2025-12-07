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
from application.game_manager import GameManager


def main():
    """
    Main game entry point.

    Initializes game systems and starts the main loop.
    """
    print("🥷 RUNNOBI - Ninja Endless Runner")
    print("=" * 50)
    print("🎮 Starting at MENU...")
    print("\nControls:")
    print("  SPACE/W/UP        - Jump (double jump available)")
    print("  DOWN/S            - Crouch (slide under obstacles)")
    print("  X/Z/LEFT/RIGHT    - Attack (destroy wooden crates)")
    print("  ESC               - Pause / Return to menu")
    print("\n💡 Tips:")
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
        print("\n⚠️  Game interrupted by user")

    print("\n✅ Game closed successfully!")


if __name__ == "__main__":
    main()