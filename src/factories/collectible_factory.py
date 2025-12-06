"""
Simple collectible factory for creating collectibles.

Factory pattern for collectible creation (MVP version).
"""
from typing import Literal
from ..domain.entities.collectible import Collectible
from ..domain.entities.coin import Coin

CollectibleType = Literal['coin']


class CollectibleFactory:
    """
    Simple factory for creating collectibles.

    Creates collectible instances based on type string.
    """

    @staticmethod
    def create(collectible_type: CollectibleType, x: float, y: float, scroll_speed: float) -> Collectible:
        """
        Create collectible at position.

        Args:
            collectible_type: Type of collectible to create
            x: X position
            y: Y position
            scroll_speed: World scroll speed

        Returns:
            Created collectible instance
        """
        if collectible_type == 'coin':
            return Coin(x, y, scroll_speed)
        else:
            raise ValueError(f"Unknown collectible type: {collectible_type}")
