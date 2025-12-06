"""Domain interfaces module."""
from .i_game_entity import IGameEntity
from .i_collidable import ICollidable
from .i_updatable import IUpdatable
from .i_renderable import IRenderable

__all__ = [
    'IGameEntity',
    'ICollidable',
    'IUpdatable',
    'IRenderable',
]
