"""
NinjaState enumeration for player character states.

Defines all possible states the ninja can be in, used for animation
and behavior control.
"""
from enum import Enum, auto


class NinjaState(Enum):
    """
    Enumeration of ninja character states.

    Each state corresponds to different animations and behavior logic.
    State machine ensures ninja can only be in one state at a time.
    """

    IDLE = auto()
    """Standing still on ground."""

    RUNNING = auto()
    """Moving forward on ground."""

    JUMPING = auto()
    """In air, ascending or descending."""

    SLIDING = auto()
    """Sliding under low obstacles with reduced hitbox."""

    ATTACKING = auto()
    """Performing katana slash attack."""

    DASHING = auto()
    """Executing shadow dash with invincibility."""

    DEAD = auto()
    """Ninja has died, game over."""
