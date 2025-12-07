"""
Collision detection system using AABB algorithm.

Simple and efficient collision detection for 2D platformer.
"""
from typing import List
from domain.interfaces.i_game_entity import IGameEntity
from domain.entities.ninja import Ninja
from domain.entities.obstacle import Obstacle
from domain.entities.collectible import Collectible


class CollisionDetector:
    """
    AABB collision detection system.

    Detects collisions between ninja and game entities using
    Axis-Aligned Bounding Box algorithm.
    """

    def check_ninja_obstacles(self, ninja: Ninja, obstacles: List[Obstacle]) -> List[Obstacle]:
        """
        Check collisions between ninja and obstacles.

        Args:
            ninja: Ninja entity
            obstacles: List of obstacle entities

        Returns:
            List of obstacles that collided with ninja
        """
        if not ninja.is_active():
            return []

        collisions = []
        ninja_bounds = ninja.get_bounds()

        for obstacle in obstacles:
            if not obstacle.is_active():
                continue

            if not ninja.can_collide_with(obstacle):
                continue

            obstacle_bounds = obstacle.get_bounds()

            if ninja_bounds.intersects(obstacle_bounds):
                collisions.append(obstacle)

        return collisions

    def check_ninja_collectibles(self, ninja: Ninja, collectibles: List[Collectible]) -> List[Collectible]:
        """
        Check collisions between ninja and collectibles.

        Args:
            ninja: Ninja entity
            collectibles: List of collectible entities

        Returns:
            List of collectibles that were collected
        """
        if not ninja.is_active():
            return []

        collected = []
        ninja_bounds = ninja.get_bounds()

        for collectible in collectibles:
            if not collectible.is_active():
                continue

            collectible_bounds = collectible.get_bounds()

            if ninja_bounds.intersects(collectible_bounds):
                collected.append(collectible)

        return collected

    @staticmethod
    def check_collision(entity_a: IGameEntity, entity_b: IGameEntity) -> bool:
        """
        Check if two entities are colliding (generic method).

        Args:
            entity_a: First entity
            entity_b: Second entity

        Returns:
            True if entities are colliding
        """
        if not entity_a.is_active() or not entity_b.is_active():
            return False

        bounds_a = entity_a.get_bounds()
        bounds_b = entity_b.get_bounds()

        return bounds_a.intersects(bounds_b)
