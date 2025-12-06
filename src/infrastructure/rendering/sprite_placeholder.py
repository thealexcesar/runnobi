"""Placeholder sprites with real sprite loading."""
import pygame
from typing import Optional

_ninja_loader = None


def _get_ninja_loader():
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

    NINJA_COLOR = (30, 30, 40)
    NINJA_SCARF = (220, 50, 50)
    WIDTH = 70
    HEIGHT = int(WIDTH * 1.5)

    @staticmethod
    def _get_real_sprite(animation: str, frame: int, width: int, height: int) -> Optional[pygame.Surface]:
        loader = _get_ninja_loader()
        if loader:
            sprite = loader.get_sprite(animation, frame)
            if sprite:
                return pygame.transform.scale(sprite, (width, height))
        return None

    @staticmethod
    def _create_fallback(width: int, height: int) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, width, height))
        return surf

    @staticmethod
    def create_ninja_idle(width: int = WIDTH, height: int = HEIGHT, frame: int = 0) -> pygame.Surface:
        sprite = PlaceholderSprites._get_real_sprite('idle', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_slide(width: int = WIDTH, height: int = 50, frame: int = 0) -> pygame.Surface:
        sprite = PlaceholderSprites._get_real_sprite('slide', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_run(width: int = WIDTH, height: int = HEIGHT, frame: int = 0) -> pygame.Surface:
        sprite = PlaceholderSprites._get_real_sprite('run', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_jump(width: int = WIDTH, height: int = HEIGHT, frame: int = 0, is_double_jump: bool = False) -> pygame. Surface:
        sprite = PlaceholderSprites._get_real_sprite('jump', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_attack(width: int = 70, height: int = HEIGHT, frame: int = 0) -> pygame.Surface:
        sprite = PlaceholderSprites._get_real_sprite('attack', frame, width, height)
        return sprite if sprite else PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_ninja_dash(width: int = WIDTH, height: int = HEIGHT, frame: int = 0) -> pygame.Surface:
        sprite = PlaceholderSprites._get_real_sprite('dash', frame, width, height)
        if sprite:
            sprite. set_alpha(180)
            return sprite
        return PlaceholderSprites._create_fallback(width, height)

    @staticmethod
    def create_obstacle_spike(width: int = 40, height: int = 60) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        points = [(width//2, 5), (width-5, height-5), (5, height-5)]
        pygame.draw.polygon(surf, (150, 150, 150), points)
        return surf

    @staticmethod
    def create_obstacle_barrier(width: int = WIDTH, height: int = 100) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (100, 60, 40), (10, 0, width-20, height))
        return surf

    @staticmethod
    def create_breakable_crate(width: int = WIDTH, height: int = 70) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (139, 90, 43), (5, 5, width-10, height-10))
        pygame.draw.line(surf, (80, 50, 20), (15, 15), (width-15, height-15), 3)
        return surf

    @staticmethod
    def create_coin(radius: int = 12) -> pygame.Surface:
        size = radius * 2 + 4
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size//2, size//2)
        pygame.draw. circle(surf, (255, 215, 0), center, radius)
        return surf
