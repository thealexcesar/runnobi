"""Load ninja sprites from individual PNG files."""
import pygame
import os
from typing import Optional, List

class NinjaSpriteLoader:
    """Load ninja sprites from separated PNG files."""

    def __init__(self):
        self. sprites = {}
        self.base_path = self._find_base_path()
        self._load_sprites()

    def _find_base_path(self) -> str:
        possible_paths = [
            'assets/sprites/ninja',
            './assets/sprites/ninja',
            'src/../assets/sprites/ninja',
            os.path.join(os.path.dirname(__file__), '../../../assets/sprites/ninja'),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return 'assets/sprites/ninja'

    def _load_sprites(self):
        animations = {
            'idle': 'adventurer-idle-{:02d}.png',
            'run': 'adventurer-run-{:02d}.png',
            'jump': 'adventurer-jump-{:02d}.png',
            'slide': 'adventurer-slide-{:02d}.png',
            'attack': 'adventurer-attack1-{:02d}.png',
            'dash': 'adventurer-smrslt-{:02d}.png',
            'die': 'adventurer-die-{:02d}.png',
        }

        max_frames = {
            'idle': 4,
            'run': 6,
            'jump': 4,
            'slide': 2,
            'attack': 5,
            'dash': 4,
            'die': 7,
        }

        for anim_name, pattern in animations.items():
            frames = []
            for i in range(max_frames.get(anim_name, 10)):
                filename = pattern.format(i)
                path = os.path.join(self.base_path, filename)

                if os.path.exists(path):
                    sprite = pygame.image.load(path).convert_alpha()
                    frames.append(sprite)
                else:
                    break

            if frames:
                self.sprites[anim_name] = frames

    def get_sprite(self, animation: str, frame: int = 0) -> Optional[pygame. Surface]:
        if animation not in self.sprites:
            return None

        frames = self.sprites[animation]
        if not frames:
            return None

        return frames[frame % len(frames)]

    def has_sprites(self) -> bool:
        return len(self.sprites) > 0
