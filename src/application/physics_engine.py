"""
Physics engine for game simulation.

Handles gravity, velocity updates, and ground collision for ninja.
Simple implementation focused on responsive 2D platformer feel.
"""
from domain.entities import Ninja
from domain.value_objects.velocity import Velocity
from domain.value_objects.position import Position
from application.physics_constants import (
    GRAVITY,
    MAX_FALL_SPEED,
    GROUND_FRICTION,
    AIR_RESISTANCE,
)

class PhysicsEngine:
    """
    Simple 2D physics engine for ninja movement.

    Applies gravity, updates velocity, and handles ground collision.
    Designed for responsive platformer feel at 60 FPS.
    """

    def __init__(self, ground_y: float) -> None:
        """
        Initialize physics engine.

        Args:
            ground_y: Y coordinate of ground level
        """
        self._ground_y = ground_y

    def update(self, ninja: Ninja, delta_time: float) -> None:
        """
        Update ninja physics for one frame.

        Args:
            ninja: Ninja entity to update
            delta_time: Time elapsed since last frame (seconds)
        """
        current_vel = ninja.get_velocity()
        current_pos = ninja.get_position()

        # Apply gravity if in air
        if not ninja.is_on_ground():
            new_vel = current_vel.apply_gravity(GRAVITY, delta_time)

            # Clamp to terminal velocity
            if new_vel.vy > MAX_FALL_SPEED:
                new_vel = Velocity(new_vel.vx, MAX_FALL_SPEED)

            # Apply air resistance
            new_vel = Velocity(
                new_vel.vx * AIR_RESISTANCE,
                new_vel.vy
            )
        else:
            # On ground - apply friction
            new_vel = Velocity(
                current_vel.vx * GROUND_FRICTION,
                current_vel.vy
            )

        # Update velocity
        ninja.set_velocity(new_vel)

        # Update position based on velocity
        dx = new_vel.vx * delta_time
        dy = new_vel.vy * delta_time
        new_pos = current_pos.translate(dx, dy)

        # Check ground collision
        if new_pos.y >= self._ground_y - ninja.HEIGHT:
            # Snap to ground
            new_pos = Position(new_pos.x, self._ground_y - ninja.HEIGHT)
            ninja.set_on_ground(True)
            # Stop vertical velocity
            ninja.set_velocity(Velocity(new_vel.vx, 0.0))
        else:
            ninja.set_on_ground(False)

        # Update position
        ninja.set_position(new_pos)

    def get_ground_y(self) -> float:
        """Get ground level Y coordinate."""
        return self._ground_y
