"""
Game state enumeration.

Defines possible game states for state machine.
"""
from enum import Enum, auto


class GameState(Enum):
    """
    Game state enumeration.

    States:
        PLAYING: Game is running
        PAUSED: Game is paused
        GAME_OVER: Player died
    """
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
