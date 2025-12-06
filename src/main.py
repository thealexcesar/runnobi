"""
Runnobi - Ninja Endless Runner
Main entry point for the game.

Academic project demonstrating clean architecture, SOLID principles,
and design patterns in game development.
"""
from src.application.game_manager import GameManager


def main():
    """
    Main game entry point.

    Initializes game systems and starts the main loop.
    """
    print("RUNNOBI - Ninja Endless Runner")
    print("=" * 50)
    print("Controls:")
    print("  SPACE/W/UP  - Jump (press again for double jump)")
    print("  DOWN/S      - Slide")
    print("  SHIFT       - Shadow Dash (invincibility)")
    print("  X/Z         - Katana Attack")
    print("  ESC/P       - Pause")
    print("=" * 50)
    print("\nStarting game...")

    game = GameManager()
    game.run()

    print("\n✅ Game closed successfully!")


if __name__ == "__main__":
    main()