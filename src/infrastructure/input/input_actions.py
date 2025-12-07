"""
Input actions enumeration.

Defines all possible player actions that can be triggered by input.
Simplified mechanics: jump, crouch, attack, pause.
"""
from enum import Enum, auto


class InputAction(Enum):
    """
    Player input actions for simplified ninja mechanics.

    Maps raw input (keyboard/gamepad) to game actions.
    Used by KeyboardAdapter to decouple input handling from game logic.
    """

    FULLSCREEN = auto()

    JUMP = auto()
    """Jump or double jump action."""

    CROUCH = auto()
    """Crouch to duck under obstacles (uses stand sprite)."""

    ATTACK = auto()
    """Sword slash attack to destroy wooden crates."""

    PAUSE = auto()
    """Pause/unpause game."""

    QUIT = auto()
    """Quit game (close window)."""
