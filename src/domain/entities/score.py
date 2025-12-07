"""
Score management system.
Handles score tracking and breakable destruction rewards.
"""

class ScoreManager:
    """Manages player score based on breakable destruction."""

    # Points awarded for different actions
    POINTS_PER_BREAKABLE = 100
    COMBO_MULTIPLIER = 1.5
    COMBO_TIME_WINDOW = 2.0  # seconds

    def __init__(self):
        """Initialize score manager."""
        self.score = 0
        self.combo_count = 0
        self.last_destruction_time = 0.
        0
        self.total_breakables_destroyed = 0

    def reset(self) -> None:
        """Reset score and stats."""
        self.score = 0
        self.combo_count = 0
        self.last_destruction_time = 0.
        0
        self.total_breakables_destroyed = 0

    def on_breakable_destroyed(self, current_time: float) -> int:
        """
        Handle breakable destruction and award points.

        Args:
            current_time: Current game time in seconds

        Returns:
            Points awarded for this destruction
        """
        # Check if within combo window
        time_since_last = current_time - self.last_destruction_time

        if time_since_last <= self.COMBO_TIME_WINDOW and self.combo_count > 0:
            # Continue combo
            self.combo_count += 1
        else:
            # Start new combo
            self.combo_count = 1

        # Calculate points with combo multiplier
        base_points = self.POINTS_PER_BREAKABLE
        if self.combo_count > 1:
            points = int(base_points * (1 + (self.combo_count - 1) * 0.5))
        else:
            points = base_points

        self.score += points
        self.total_breakables_destroyed += 1
        self.last_destruction_time = current_time

        return points

    def get_score(self) -> int:
        """Get current score."""
        return self.score

    def get_combo(self) -> int:
        """Get current combo count."""
        return self.combo_count

    def get_total_destroyed(self) -> int:
        """Get total breakables destroyed."""
        return self.total_breakables_destroyed
