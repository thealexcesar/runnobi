"""
Runnobi - Ninja Endless Runner
Main entry point for the game.

Academic project demonstrating clean architecture, SOLID principles,
and design patterns in game development.
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
    print("  SPACE/ENTER - Start game / Jump (double jump available)")
    print("  DOWN/S      - Crouch (slide under obstacles)")
    print("  X/Z         - Katana Attack (destroy breakables for points)")
    print("  ESC         - Return to menu / Quit")
    print("\n💡 Tips:")
    print("  - Destroy breakable crates to score points!")
    print("  - Chain destructions for combo multipliers!")
    print("  - Crouch OR attack to break wooden crates")
    print("=" * 50)
    print("\nStarting game.. .\n")

    game = GameManager()
    game.run()

    print("\n✅ Game closed successfully!")


if __name__ == "__main__":
    main()
