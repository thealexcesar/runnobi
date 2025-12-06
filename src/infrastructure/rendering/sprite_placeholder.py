"""
Placeholder sprite system using pygame primitives.

Temporary sprites using shapes that match exact dimensions of final sprites.
Allows immediate development without asset dependencies.
"""
import pygame
from typing import Dict


class PlaceholderSprites:
    """Generates placeholder sprites using pygame drawing primitives."""
    NINJA_BODY = (30, 30, 40)
    NINJA_SCARF = (220, 50, 50)
    OBSTACLE_COLOR = (100, 60, 40)
    SPIKE_COLOR = (150, 150, 150)
    COIN_COLOR = (255, 215, 0)
    SHURIKEN_COLOR = (200, 200, 210)
    BREAKABLE_COLOR = (139, 90, 43)

    @staticmethod
    def create_ninja_idle(width: int = 56, height: int = 84) -> pygame.Surface:
        """Create ninja idle sprite placeholder."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        head_radius = int(width * 0.25)
        head_y = int(height * 0.15)
        pygame.draw.circle(surface, PlaceholderSprites.NINJA_BODY, (width // 2, head_y), head_radius)

        eye_y = head_y - 2
        pygame.draw.circle(surface, (255, 255, 255), (width // 2 - 6, eye_y), 3)
        pygame.draw.circle(surface, (255, 255, 255), (width // 2 + 6, eye_y), 3)

        body_rect = pygame.Rect(width // 4, int(height * 0.28), width // 2, int(height * 0.5))
        pygame.draw.rect(surface, PlaceholderSprites.NINJA_BODY, body_rect, border_radius=4)

        leg_width = width // 5
        leg_height = int(height * 0.22)
        left_leg = pygame.Rect(width // 3 - 5, int(height * 0.78), leg_width, leg_height)
        right_leg = pygame.Rect(width // 2 + 5, int(height * 0.78), leg_width, leg_height)
        pygame.draw.rect(surface, PlaceholderSprites.NINJA_BODY, left_leg, border_radius=3)
        pygame.draw.rect(surface, PlaceholderSprites.NINJA_BODY, right_leg, border_radius=3)

        scarf_points = [(width // 2, int(height * 0.25)), (width - 5, int(height * 0.35)),
                        (width // 2 + 5, int(height * 0.4))]
        pygame.draw.polygon(surface, PlaceholderSprites.NINJA_SCARF, scarf_points)

        return surface

    @staticmethod
    def create_ninja_run(width: int = 56, height: int = 84, frame: int = 0) -> pygame.Surface:
        """Create ninja running animation frame."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        base = PlaceholderSprites.create_ninja_idle(width, height)
        surface.blit(base, (0, 0))

        offset = (frame % 2) * 2 - 1
        scarf_points = [(width // 2, int(height * 0.25)), (width - 8 - offset * 3, int(height * 0.30)),
                        (width - 5 - offset * 5, int(height * 0.38))]
        pygame.draw.polygon(surface, PlaceholderSprites.NINJA_SCARF, scarf_points)

        return surface

    @staticmethod
    def create_ninja_jump(width: int = 56, height: int = 84) -> pygame.Surface:
        """Create ninja jumping sprite."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        head_radius = int(width * 0.25)
        head_y = int(height * 0.2)
        pygame.draw.circle(surface, PlaceholderSprites.NINJA_BODY, (width // 2, head_y), head_radius)
        pygame.draw.circle(surface, (255, 255, 255), (width // 2 - 6, head_y - 2), 3)
        pygame.draw.circle(surface, (255, 255, 255), (width // 2 + 6, head_y - 2), 3)

        body_rect = pygame.Rect(width // 4, int(height * 0.35), width // 2, int(height * 0.45))
        pygame.draw.rect(surface, PlaceholderSprites.NINJA_BODY, body_rect, border_radius=4)

        pygame.draw.circle(surface, PlaceholderSprites.NINJA_BODY, (width // 3, int(height * 0.85)), 8)
        pygame.draw.circle(surface, PlaceholderSprites.NINJA_BODY, (2 * width // 3, int(height * 0.82)), 8)

        scarf_points = [(width // 2, int(height * 0.3)), (width - 5, int(height * 0.2)),
                        (width - 8, int(height * 0.28))]
        pygame.draw.polygon(surface, PlaceholderSprites.NINJA_SCARF, scarf_points)

        return surface

    @staticmethod
    def create_ninja_slide(width: int = 56, height: int = 50) -> pygame.Surface:
        """Create ninja sliding sprite (reduced height hitbox)."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.circle(surface, PlaceholderSprites.NINJA_BODY, (width // 3, height // 3), 10)
        pygame.draw.circle(surface, (255, 255, 255), (width // 3 - 4, height // 3 - 2), 2)
        pygame.draw.circle(surface, (255, 255, 255), (width // 3 + 4, height // 3 - 2), 2)

        body_rect = pygame.Rect(width // 4, height // 2, int(width * 0.6), height // 3)
        pygame.draw.rect(surface, PlaceholderSprites.NINJA_BODY, body_rect, border_radius=4)

        scarf_points = [(width // 4, height // 2), (5, height // 3), (8, height // 2 + 5)]
        pygame.draw.polygon(surface, PlaceholderSprites.NINJA_SCARF, scarf_points)

        return surface

    @staticmethod
    def create_ninja_attack(width: int = 70, height: int = 84) -> pygame.Surface:
        """Create ninja attack sprite with katana."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        base = PlaceholderSprites.create_ninja_idle(56, height)
        surface.blit(base, (0, 0))

        sword_start = (50, int(height * 0.4))
        sword_end = (width - 5, int(height * 0.3))
        pygame.draw.line(surface, (200, 200, 220), sword_start, sword_end, 3)
        pygame.draw.circle(surface, (255, 255, 100), sword_end, 4)

        return surface

    @staticmethod
    def create_ninja_dash(width: int = 56, height: int = 84) -> pygame.Surface:
        """Create ninja dash sprite with transparency."""
        surface = PlaceholderSprites.create_ninja_idle(width, height)
        surface.set_alpha(180)
        return surface

    @staticmethod
    def create_obstacle_spike(width: int = 40, height: int = 50) -> pygame.Surface:
        """Create spike obstacle."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        points = [(width // 2, 5), (width - 5, height - 5), (5, height - 5)]
        pygame.draw.polygon(surface, PlaceholderSprites.SPIKE_COLOR, points)
        pygame.draw.polygon(surface, (100, 100, 100), points, 2)
        return surface

    @staticmethod
    def create_obstacle_barrier(width: int = 56, height: int = 80) -> pygame.Surface:
        """Create barrier obstacle."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, PlaceholderSprites.OBSTACLE_COLOR, (10, 0, width - 20, height), border_radius=4)
        for i in range(0, height, 15):
            pygame.draw.line(surface, (80, 50, 30), (12, i), (width - 12, i), 1)
        return surface

    @staticmethod
    def create_obstacle_low_barrier(width: int = 56, height: int = 40) -> pygame.Surface:
        """Create low barrier obstacle (must slide under)."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, PlaceholderSprites.OBSTACLE_COLOR, (10, 0, width - 20, height), border_radius=4)
        for i in range(0, height, 12):
            pygame.draw.line(surface, (80, 50, 30), (12, i), (width - 12, i), 1)
        return surface

    @staticmethod
    def create_breakable_crate(width: int = 56, height: int = 56) -> pygame.Surface:
        """Create breakable crate."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, PlaceholderSprites.BREAKABLE_COLOR, (5, 5, width - 10, height - 10), border_radius=3)
        pygame.draw.line(surface, (80, 50, 20), (15, 15), (width - 15, height - 15), 3)
        pygame.draw.line(surface, (80, 50, 20), (width - 15, 15), (15, height - 15), 3)
        return surface

    @staticmethod
    def create_coin(radius: int = 12) -> pygame.Surface:
        """Create coin collectible."""
        size = radius * 2 + 4
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(surface, PlaceholderSprites.COIN_COLOR, center, radius)
        pygame.draw.circle(surface, (255, 235, 100), center, radius - 3)
        pygame.draw.circle(surface, PlaceholderSprites.COIN_COLOR, center, radius - 6)
        return surface

    @staticmethod
    def create_shuriken(size: int = 24) -> pygame.Surface:
        """Create shuriken collectible/projectile."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        points = []
        for i in range(8):
            angle = i * 45
            radius = (size // 2 - 2) if i % 2 == 0 else (size // 4)
            x = center[0] + int(radius * pygame.math.Vector2(1, 0).rotate(angle).x)
            y = center[1] + int(radius * pygame.math.Vector2(1, 0).rotate(angle).y)
            points.append((x, y))
        pygame.draw.polygon(surface, PlaceholderSprites.SHURIKEN_COLOR, points)
        pygame.draw.circle(surface, (150, 150, 160), center, 4)
        return surface

    @staticmethod
    def create_shadow_orb(radius: int = 16) -> pygame.Surface:
        """Create shadow orb collectible."""
        size = radius * 2 + 4
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(surface, (100, 50, 150), center, radius)
        pygame.draw.circle(surface, (150, 100, 200), center, radius - 4)
        pygame.draw.circle(surface, (200, 150, 255), center, radius - 8)
        return surface

    @staticmethod
    def create_background_layer(width: int, height: int, layer: int) -> pygame.Surface:
        """
        Create parallax background layer placeholder.

        Args:
            width: Layer width
            height: Layer height
            layer: Layer number (0=far, 3=near)
        """
        surface = pygame.Surface((width, height))

        if layer == 0:
            for y in range(height):
                color_value = int(140 + (y / height) * 60)
                color = (color_value, color_value + 40, color_value + 60)
                pygame.draw.line(surface, color, (0, y), (width, y))
        elif layer == 1:
            surface.fill((100, 120, 140))
            for i in range(0, width, 200):
                points = [(i, height), (i + 100, height // 2), (i + 200, height)]
                pygame.draw.polygon(surface, (80, 90, 110), points)
        elif layer == 2:
            surface.fill((60, 80, 100))
            surface.set_alpha(180)
            for i in range(0, width, 150):
                pygame.draw.rect(surface, (40, 60, 40), (i + 60, height - 100, 30, 100))
                pygame.draw.circle(surface, (50, 80, 50), (i + 75, height - 100), 40)
        else:
            surface.fill((40, 60, 40))

        return surface


class SpriteCache:
    """
    Cache for generated placeholder sprites.

    Implements simple caching to improve performance.
    """

    def __init__(self):
        """Initialize empty sprite cache."""
        self._cache: Dict[str, pygame.Surface] = {}

    def get_or_create(self, key: str, creator_func, *args, **kwargs) -> pygame.Surface:
        """Get sprite from cache or create and cache it."""
        if key not in self._cache:
            self._cache[key] = creator_func(*args, **kwargs)
        return self._cache[key]

    def clear(self) -> None:
        """Clear all cached sprites."""
        self._cache.clear()
