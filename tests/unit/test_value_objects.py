"""
Unit tests for domain value objects.

Tests immutability, methods, and edge cases for Position, Velocity, and Bounds.
"""
import pytest
from src.domain.value_objects.position import Position
from src.domain.value_objects.velocity import Velocity
from src.domain.value_objects.bounds import Bounds


class TestPosition:
    """Test suite for Position value object."""

    def test_create_position(self):
        """Position should be created with x and y coordinates."""
        pos = Position(10.0, 20.0)
        assert pos.x == 10.0
        assert pos.y == 20.0

    def test_position_as_tuple(self):
        """Position should convert to tuple."""
        pos = Position(5.0, 15.0)
        assert pos.as_tuple() == (5.0, 15.0)

    def test_position_distance(self):
        """Position should calculate distance to another position."""
        pos1 = Position(0.0, 0.0)
        pos2 = Position(3.0, 4.0)
        assert pos1.distance_to(pos2) == 5.0

    def test_position_translate(self):
        """Position translate should create new position."""
        pos = Position(10.0, 20.0)
        new_pos = pos.translate(5.0, -10.0)
        assert new_pos.x == 15.0
        assert new_pos.y == 10.0
        assert pos.x == 10.0  # Original unchanged (immutable)

    def test_position_equality(self):
        """Positions with same coordinates should be equal."""
        pos1 = Position(10.0, 20.0)
        pos2 = Position(10.0, 20.0)
        pos3 = Position(10.0, 21.0)
        assert pos1 == pos2
        assert pos1 != pos3

    def test_position_hashable(self):
        """Position should be hashable for use in sets."""
        pos1 = Position(10.0, 20.0)
        pos2 = Position(10.0, 20.0)
        pos_set = {pos1, pos2}
        assert len(pos_set) == 1

    def test_position_repr(self):
        """Position should have readable string representation."""
        pos = Position(10.0, 20.0)
        assert "Position" in repr(pos)
        assert "10.0" in repr(pos)


class TestVelocity:
    """Test suite for Velocity value object."""

    def test_create_velocity(self):
        """Velocity should be created with vx and vy components."""
        vel = Velocity(5.0, 10.0)
        assert vel.vx == 5.0
        assert vel.vy == 10.0

    def test_velocity_as_tuple(self):
        """Velocity should convert to tuple."""
        vel = Velocity(3.0, 4.0)
        assert vel.as_tuple() == (3.0, 4.0)

    def test_velocity_magnitude(self):
        """Velocity should calculate magnitude (speed)."""
        vel = Velocity(3.0, 4.0)
        assert vel.magnitude() == 5.0

    def test_velocity_scale(self):
        """Velocity scale should create new scaled velocity."""
        vel = Velocity(10.0, 20.0)
        scaled = vel.scale(0.5)
        assert scaled.vx == 5.0
        assert scaled.vy == 10.0
        assert vel.vx == 10.0  # Original unchanged (immutable)

    def test_velocity_add(self):
        """Velocity add should create new summed velocity."""
        vel1 = Velocity(10.0, 5.0)
        vel2 = Velocity(3.0, 2.0)
        result = vel1.add(vel2)
        assert result.vx == 13.0
        assert result.vy == 7.0
        assert vel1.vx == 10.0  # Original unchanged

    def test_velocity_apply_gravity(self):
        """Velocity should apply gravity to vertical component."""
        vel = Velocity(10.0, 0.0)
        gravity = 980.0  # pixels per second squared
        delta_time = 0.016  # ~60 FPS
        new_vel = vel.apply_gravity(gravity, delta_time)
        assert new_vel.vx == 10.0
        assert new_vel.vy == pytest.approx(15.68, rel=0.01)

    def test_velocity_equality(self):
        """Velocities with same components should be equal."""
        vel1 = Velocity(10.0, 20.0)
        vel2 = Velocity(10.0, 20.0)
        vel3 = Velocity(10.0, 21.0)
        assert vel1 == vel2
        assert vel1 != vel3

    def test_velocity_hashable(self):
        """Velocity should be hashable for use in sets."""
        vel1 = Velocity(10.0, 20.0)
        vel2 = Velocity(10.0, 20.0)
        vel_set = {vel1, vel2}
        assert len(vel_set) == 1


class TestBounds:
    """Test suite for Bounds value object."""

    def test_create_bounds(self):
        """Bounds should be created with x, y, width, height."""
        bounds = Bounds(10.0, 20.0, 50.0, 30.0)
        assert bounds.x == 10.0
        assert bounds.y == 20.0
        assert bounds.width == 50.0
        assert bounds.height == 30.0

    def test_bounds_edges(self):
        """Bounds should calculate edge coordinates correctly."""
        bounds = Bounds(10.0, 20.0, 50.0, 30.0)
        assert bounds.left == 10.0
        assert bounds.right == 60.0
        assert bounds.top == 20.0
        assert bounds.bottom == 50.0

    def test_bounds_center(self):
        """Bounds should calculate center coordinates."""
        bounds = Bounds(10.0, 20.0, 50.0, 30.0)
        assert bounds.center_x == 35.0
        assert bounds.center_y == 35.0

    def test_bounds_as_tuple(self):
        """Bounds should convert to tuple."""
        bounds = Bounds(10.0, 20.0, 50.0, 30.0)
        assert bounds.as_tuple() == (10.0, 20.0, 50.0, 30.0)

    def test_bounds_translate(self):
        """Bounds translate should create new translated bounds."""
        bounds = Bounds(10.0, 20.0, 50.0, 30.0)
        new_bounds = bounds.translate(5.0, -10.0)
        assert new_bounds.x == 15.0
        assert new_bounds.y == 10.0
        assert new_bounds.width == 50.0
        assert new_bounds.height == 30.0
        assert bounds.x == 10.0  # Original unchanged (immutable)

    def test_bounds_intersects_true(self):
        """Bounds should detect intersection with overlapping bounds."""
        bounds1 = Bounds(0.0, 0.0, 50.0, 50.0)
        bounds2 = Bounds(25.0, 25.0, 50.0, 50.0)
        assert bounds1.intersects(bounds2)
        assert bounds2.intersects(bounds1)

    def test_bounds_intersects_false(self):
        """Bounds should not detect intersection with non-overlapping bounds."""
        bounds1 = Bounds(0.0, 0.0, 50.0, 50.0)
        bounds2 = Bounds(100.0, 100.0, 50.0, 50.0)
        assert not bounds1.intersects(bounds2)

    def test_bounds_intersects_edge_touching(self):
        """Bounds touching at edge should not intersect."""
        bounds1 = Bounds(0.0, 0.0, 50.0, 50.0)
        bounds2 = Bounds(50.0, 0.0, 50.0, 50.0)
        assert not bounds1.intersects(bounds2)

    def test_bounds_contains_point_inside(self):
        """Bounds should detect point inside."""
        bounds = Bounds(10.0, 10.0, 50.0, 50.0)
        assert bounds.contains_point(30.0, 30.0)

    def test_bounds_contains_point_outside(self):
        """Bounds should detect point outside."""
        bounds = Bounds(10.0, 10.0, 50.0, 50.0)
        assert not bounds.contains_point(100.0, 100.0)

    def test_bounds_contains_point_on_edge(self):
        """Bounds should include points on edges."""
        bounds = Bounds(10.0, 10.0, 50.0, 50.0)
        assert bounds.contains_point(10.0, 10.0)
        assert bounds.contains_point(60.0, 60.0)

    def test_bounds_equality(self):
        """Bounds with same values should be equal."""
        bounds1 = Bounds(10.0, 20.0, 50.0, 30.0)
        bounds2 = Bounds(10.0, 20.0, 50.0, 30.0)
        bounds3 = Bounds(10.0, 20.0, 50.0, 31.0)
        assert bounds1 == bounds2
        assert bounds1 != bounds3

    def test_bounds_hashable(self):
        """Bounds should be hashable for use in sets."""
        bounds1 = Bounds(10.0, 20.0, 50.0, 30.0)
        bounds2 = Bounds(10.0, 20.0, 50.0, 30.0)
        bounds_set = {bounds1, bounds2}
        assert len(bounds_set) == 1
