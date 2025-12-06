"""
Bounds value object representing rectangular collision boundaries.

Immutable value object for AABB (Axis-Aligned Bounding Box) collision detection,
ensuring collision calculations remain consistent.
"""
from typing import Tuple


class Bounds:
    """
    Immutable 2D bounding box value object.

    Represents an axis-aligned bounding box for collision detection.
    Immutability ensures collision state remains predictable.
    """
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initialize bounds with position and dimensions.

        Args:
            x: Left edge x-coordinate
            y: Top edge y-coordinate
            width: Box width
            height: Box height
        """
        self._x = float(x)
        self._y = float(y)
        self._width = float(width)
        self._height = float(height)

    @property
    def x(self) -> float:
        """Get left edge x-coordinate."""
        return self._x

    @property
    def y(self) -> float:
        """Get top edge y-coordinate."""
        return self._y

    @property
    def width(self) -> float:
        """Get box width."""
        return self._width

    @property
    def height(self) -> float:
        """Get box height."""
        return self._height

    @property
    def left(self) -> float:
        """Get left edge x-coordinate."""
        return self._x

    @property
    def right(self) -> float:
        """Get right edge x-coordinate."""
        return self._x + self._width

    @property
    def top(self) -> float:
        """Get top edge y-coordinate."""
        return self._y

    @property
    def bottom(self) -> float:
        """Get bottom edge y-coordinate."""
        return self._y + self._height

    @property
    def center_x(self) -> float:
        """Get center x-coordinate."""
        return self._x + self._width / 2

    @property
    def center_y(self) -> float:
        """Get center y-coordinate."""
        return self._y + self._height / 2

    def as_tuple(self) -> Tuple[float, float, float, float]:
        """
        Convert bounds to tuple representation.

        Returns:
            Tuple of (x, y, width, height)
        """
        return (self._x, self._y, self._width, self._height)

    def translate(self, dx: float, dy: float) -> 'Bounds':
        """
        Create new bounds translated by given offsets.

        Args:
            dx: Horizontal offset
            dy: Vertical offset

        Returns:
            New Bounds instance at translated position
        """
        return Bounds(self._x + dx, self._y + dy, self._width, self._height)

    def intersects(self, other: 'Bounds') -> bool:
        """
        Check if this bounds intersects with another bounds (AABB collision).

        Args:
            other: Other bounds to check collision with

        Returns:
            True if bounds intersect, False otherwise
        """
        return (self.left < other.right and
                self.right > other.left and
                self.top < other.bottom and
                self.bottom > other.top)

    def contains_point(self, x: float, y: float) -> bool:
        """
        Check if a point is inside this bounds.

        Args:
            x: Point x-coordinate
            y: Point y-coordinate

        Returns:
            True if point is inside bounds, False otherwise
        """
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    def __eq__(self, other: object) -> bool:
        """Check equality with another bounds."""
        if not isinstance(other, Bounds):
            return False
        return (self._x == other.x and
                self._y == other.y and
                self._width == other.width and
                self._height == other.height)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Bounds(x={self._x}, y={self._y}, w={self._width}, h={self._height})"

    def __hash__(self) -> int:
        """Make Bounds hashable for use in sets/dicts."""
        return hash((self._x, self._y, self._width, self._height))
