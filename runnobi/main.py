"""Main entry point for Runnobi game."""

import sys
from runnobi.game import Game


def main():
    """Start the game."""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
        sys.exit(0)
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
