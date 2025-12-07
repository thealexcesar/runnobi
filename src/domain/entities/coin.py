"""Coin collectible - adds score points."""
import pygame

from domain.entities import Collectible
from domain.interfaces import IGameEntity


class Coin(Collectible):
    """Coin that adds 10 points to score."""

    SIZE = 24
    POINTS = 10

    def __init__(self, x: float, y: float, scroll_speed: float) -> None:
        """Initialize coin at position."""
        super().__init__(x, y, self.SIZE, self.SIZE, scroll_speed)

    def on_collision(self, other: IGameEntity) -> None:
        """Collect coin and add points."""
        self.collect()

    def get_sprite(self) -> pygame.Surface:
        """Get coin sprite."""
        from infrastructure.rendering.sprite_placeholder import PlaceholderSprites
        return PlaceholderSprites.create_coin()

    def get_points(self) -> int:
        """Get points value."""
        return self.POINTS
