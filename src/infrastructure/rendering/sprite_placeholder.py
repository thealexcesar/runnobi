"""
Sprite placeholder system with real sprite loading and scaling.

Loads sprites from individual PNG files and applies 1.5x scaling
for better visibility. Falls back to colored rectangles if sprites missing.
"""
import pygame
from typing import Optional


# Global sprite loader instance (lazy loaded)
_ninja_loader = None

# Sprite scaling factor for better visibility
SPRITE_SCALE = 1.5


def _get_ninja_loader():
    """
    Get or create ninja sprite loader instance.

    Lazy initialization pattern - loader created on first use.
    """
    global _ninja_loader
    if _ninja_loader is None:
        try:
            from .sprite_loader import NinjaSpriteLoader
            _ninja_loader = NinjaSpriteLoader()
            if not _ninja_loader.has_sprites():
                _ninja_loader = False
        except Exception as e:
            print(f"Sprite loader error: {e}")
            _ninja_loader = False

    return _ninja_loader if _ninja_loader else None


class PlaceholderSprites:
    """
    Sprite management with scaling and fallback system.

    Attempts to load real sprites from PNG files, scales them up for
    better visibility, and falls back to colored rectangles if missing.

    Follows Proxy pattern: provides interface to sprite loading system.
    """

    # Fallback colors
    NINJA_COLOR = (30, 30, 40)
    NINJA_SCARF = (220, 50, 50)
    NINJA_WIDTH = 90
    NINJA_HEIGHT = int(NINJA_WIDTH * 1.5)

    @staticmethod
    def _get_real_sprite(animation: str, frame: int, width: int, height: int) -> Optional[pygame.Surface]:
        """
        Load and scale real sprite from files.

        Args:
            animation: Animation name (idle, run, jump, etc.)
            frame: Frame number
            width: Target width after scaling
            height: Target height after scaling

        Returns:
            Scaled sprite surface or None if not found
        """
        loader = _get_ninja_loader()
        if loader:
            sprite = loader.get_sprite(animation, frame)
            if sprite:
                # Scale sprite for better visibility
                return pygame.transform.scale(sprite, (width, height))
        return None

    @staticmethod
    def _create_fallback(width: int, height: int) -> pygame.Surface:
        """
        Create fallback colored rectangle.

        Args:
            width: Rectangle width
            height: Rectangle height

        Returns:
            Colored rectangle surface
        """
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, width, height))
        return surf

    # === Ninja Sprites (Scaled 1.5x) ===

    @staticmethod
    def create_ninja_idle(width: int = NINJA_WIDTH, height: int = NINJA_HEIGHT, frame: int = 0) -> pygame.Surface:
        """
        Create ninja idle sprite.

        Args:
            width: Sprite width (default 84 = 56 * 1.5)
            height: Sprite height (default NINJA_HEIGHT = 84 * 1.5)
            frame: Animation frame

        Returns:
            Idle animation sprite
        """
        sprite = PlaceholderSprites._get_real_sprite('idle', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_run(width: int = NINJA_WIDTH, height: int = NINJA_HEIGHT, frame: int = 0) -> pygame.Surface:
        """
        Create ninja running sprite.

        Returns:
            Running animation sprite
        """
        sprite = PlaceholderSprites._get_real_sprite('run', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_jump(width: int = NINJA_WIDTH, height: int = NINJA_HEIGHT, frame: int = 0) -> pygame.Surface:
        """
        Create ninja jumping sprite (first jump).

        Returns:
            Jump animation sprite
        """
        sprite = PlaceholderSprites._get_real_sprite('jump', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_somersault(width: int = NINJA_WIDTH, height: int = NINJA_HEIGHT, frame: int = 0) -> pygame.Surface:
        """
        Create ninja somersault sprite (second jump).

        Uses 'adventurer-smrslt-' animation for double jump.

        Returns:
            Somersault animation sprite
        """
        # Use smrslt animation for second jump
        sprite = PlaceholderSprites._get_real_sprite('smrslt', frame, width, height)
        if not sprite:
            # Try alternate name
            sprite = PlaceholderSprites._get_real_sprite('dash', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_crouch(width: int = NINJA_WIDTH, height: int = 75, frame: int = 0) -> pygame.Surface:
        """
        Create ninja crouching sprite.

        Uses 'adventurer-stand-' animation (frames 0-5).

        Args:
            width: Sprite width
            height: Sprite height
            frame: Animation frame (0-5)

        Returns:
            Crouching animation sprite
        """
        sprite = PlaceholderSprites._get_real_sprite('stand', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_attack(width: int = NINJA_WIDTH, height: int = NINJA_HEIGHT, frame: int = 0) -> pygame.Surface:
        """
        Create ninja attack sprite.

        Uses 'adventurer-attack1-' animation.

        Args:
            width: Sprite width (wider for sword swing)
            height: Sprite height

        Returns:
            Attack animation sprite
        """
        # Try attack1 first (primary attack animation)
        sprite = PlaceholderSprites._get_real_sprite('attack', frame, width, height)
        if not sprite:
            sprite = PlaceholderSprites._get_real_sprite('attack1', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    # === Obstacle Sprites (Scaled 1.5x) ===

    @staticmethod
    def create_obstacle_spike(width: int = 60, height: int = 75) -> pygame.Surface:
        """
        Create spike obstacle sprite (metal, indestructible).

        Args:
            width: Spike width (scaled)
            height: Spike height (scaled)

        Returns:
            Spike sprite
        """
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        # Gray metallic spike
        points = [(width//2, 5), (width-5, height-5), (5, height-5)]
        pygame.draw.polygon(surf, (150, 150, 150), points)
        pygame.draw.polygon(surf, (100, 100, 100), points, 2)  # Outline
        return surf

    @staticmethod
    def create_obstacle_barrier(width: int = 120, height: int = 150) -> pygame.Surface:
        """
        Create barrier obstacle sprite (stone, indestructible).

        Args:
            width: Barrier width (scaled)
            height: Barrier height (scaled)

        Returns:
            Barrier sprite
        """
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        # Stone barrier (gray)
        pygame.draw.rect(surf, (120, 120, 120), (10, 0, width-20, height))
        pygame.draw.rect(surf, (80, 80, 80), (10, 0, width-20, height), 3)
        return surf

    @staticmethod
    def create_breakable_crate(width: int = 100, height: int = 100) -> pygame.Surface:
        """
        Create wooden crate sprite (wood, breakable).

        CLEARLY wooden appearance with brown color and visible grain.

        Args:
            width: Crate width (scaled)
            height: Crate height (scaled)

        Returns:
            Wooden crate sprite
        """
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        # Brown wooden crate
        wood_color = (139, 90, 43)  # Brown
        dark_wood = (101, 67, 33)   # Darker brown for planks

        # Main crate body
        pygame.draw.rect(surf, wood_color, (5, 5, width-10, height-10))

        # Wooden planks (horizontal lines)
        for i in range(3):
            y = 15 + i * (height // 3)
            pygame.draw.line(surf, dark_wood, (10, y), (width-10, y), 3)

        # Vertical planks
        for i in range(2):
            x = 20 + i * (width // 2)
            pygame.draw.line(surf, dark_wood, (x, 10), (x, height-10), 3)

        # Border
        pygame.draw.rect(surf, dark_wood, (5, 5, width-10, height-10), 4)

        return surf

    # === Collectible Sprites (Scaled 1.5x) ===

    @staticmethod
    def create_coin(radius: int = 18) -> pygame.Surface:
        """
        Create coin collectible sprite.

        Args:
            radius: Coin radius (scaled: 12 * 1.5 = 18)

        Returns:
            Coin sprite
        """
        size = radius * 2 + 4
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size//2, size//2)

        # Gold coin
        pygame.draw.circle(surf, (255, 215, 0), center, radius)
        pygame.draw.circle(surf, (218, 165, 32), center, radius, 3)

        return surf
