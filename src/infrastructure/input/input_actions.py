"""
Input actions enumeration.

Defines all possible player actions that can be triggered by input.
"""
from enum import Enum, auto


class InputAction(Enum):
    """
    Player input actions.

    Maps raw input (keyboard) to game actions.
    """

    JUMP = auto()
    SLIDE = auto()
    DASH = auto()
    ATTACK = auto()
    PAUSE = auto()
    QUIT = auto()
