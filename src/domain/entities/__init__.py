"""Domain entities module."""
from .ninja import Ninja
from .ninja_state import NinjaState
from .obstacle import Obstacle
from .spike import Spike
from .barrier import Barrier
from .low_barrier import LowBarrier
from .breakable_crate import BreakableCrate
from .collectible import Collectible
from .coin import Coin

__all__ = [
    'Ninja',
    'NinjaState',
    'Obstacle',
    'Spike',
    'Barrier',
    'LowBarrier',
    'BreakableCrate',
    'Collectible',
    'Coin',
]
