"""
Physics constants for game simulation.

Tuned values for 60 FPS gameplay with responsive feel.
"""

# Gravity (pixels per second squared)
GRAVITY = 2000.0

# Terminal velocity (max fall speed)
MAX_FALL_SPEED = 1200.0

# Ground friction (for sliding)
GROUND_FRICTION = 0.8

# Air resistance (slight drag in air)
AIR_RESISTANCE = 0.98

# World scroll speed (base speed)
BASE_SCROLL_SPEED = 300.0  # pixels per second

# Speed increase per second (difficulty progression)
SPEED_INCREASE_RATE = 5.0  # pixels per second per second
