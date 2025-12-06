"""
Position value object representing 2D coordinates.

Immutable value object following DDD principles to encapsulate position logic
and ensure position data integrity throughout the application.
"""
from typing import Tuple


class Position:
    """
    Immutable 2D position value object.

    Represents a point in 2D space with x and y coordinates. Once created,
    position values cannot be modified (immutability ensures data consistency).
    """
    def __init__(self, x: float, y: float) -> None:
        """
        Initialize position with x and y coordinates.

        Args:
            x: Horizontal coordinate
            y: Vertical coordinate
        """
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        """Get x coordinate."""
        return self._x

    @property
    def y(self) -> float:
        """Get y coordinate."""
        return self._y

    def as_tuple(self) -> Tuple[float, float]:
        """
        Convert position to tuple representation.

        Returns:
            Tuple of (x, y) coordinates
        """
        return (self._x, self._y)

    def distance_to(self, other: 'Position') -> float:
        """
        Calculate Euclidean distance to another position.

        Args:
            other: Target position

        Returns:
            Distance in pixels
        """
        dx = self._x - other.x
        dy = self._y - other.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def translate(self, dx: float, dy: float) -> 'Position':
        """
        Create new position translated by given offsets.

        Args:
            dx: Horizontal offset
            dy: Vertical offset

        Returns:
            New Position instance at translated coordinates
        """
        return Position(self._x + dx, self._y + dy)

    def __eq__(self, other: object) -> bool:
        """Check equality with another position."""
        if not isinstance(other, Position):
            return False
        return self._x == other.x and self._y == other.y

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Position(x={self._x}, y={self._y})"

    def __hash__(self) -> int:
        """Make Position hashable for use in sets/dicts."""
        return hash((self._x, self._y))
