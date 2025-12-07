"""
Simple obstacle factory for creating obstacles.

Factory pattern for obstacle creation without complex pooling (MVP version).
"""
from typing import Literal

from domain.entities.low_blocker import LowBlocker
from domain.entities.obstacle import Obstacle
from domain.entities.spike import Spike
from domain.entities.barrier import Barrier
from domain.entities.breakable_crate import BreakableCrate


ObstacleType = Literal['spike', 'barrier', 'low_barrier', 'crate']


class ObstacleFactory:
    """
    Simple factory for creating obstacles.

    Creates obstacle instances based on type string.
    """

    @staticmethod
    def create(obstacle_type: ObstacleType, x: float, ground_y: float, scroll_speed: float) -> Obstacle:
        """
        Create obstacle at position.

        Args:
            obstacle_type: Type of obstacle to create
            x: X position
            ground_y: Ground level Y coordinate
            scroll_speed: World scroll speed

        Returns:
            Created obstacle instance
        """
        if obstacle_type == 'spike':
            return Spike(x, ground_y - Spike.HEIGHT, scroll_speed)
        elif obstacle_type == 'barrier':
            return Barrier(x, ground_y - Barrier.HEIGHT, scroll_speed)
        elif obstacle_type == 'crate':
            return BreakableCrate(x, ground_y - BreakableCrate.HEIGHT, scroll_speed)
        elif obstacle_type == 'low_blocker':
            return LowBlocker(x, ground_y, scroll_speed)
        else:
            raise ValueError(f"Unknown obstacle type: {obstacle_type}")

