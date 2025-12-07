"""
Ninja state enumeration for state machine.

Defines all possible states for the ninja character.
Simplified mechanics: no dash, no shuriken.
"""
from enum import Enum, auto


class NinjaState(Enum):
    """
    Ninja character states for state machine implementation.

    Each state corresponds to different animations and behavior.
    State transitions managed by Ninja class following State pattern.
    """

    IDLE = auto()
    """Standing still on ground (not used during gameplay, default state)."""

    RUNNING = auto()
    """Moving forward on ground (main gameplay state)."""

    JUMPING = auto()
    """In air - ascending or descending (includes double jump)."""

    CROUCHING = auto()
    """Crouching with reduced hitbox (uses stand sprite animation)."""

    ATTACKING = auto()
    """Performing sword slash attack to destroy wooden crates."""

    DEAD = auto()
    """Ninja has died - game over state."""
