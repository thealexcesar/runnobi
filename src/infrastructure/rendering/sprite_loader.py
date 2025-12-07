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
            'idle': 'adventurer-idle-',
            'run': 'adventurer-run-',
            'jump': 'adventurer-jump-',
            'slide': 'adventurer-slide-',
            'attack': 'adventurer-attack3-',
            'dash': 'adventurer-smrslt-',
            'die': 'adventurer-die-',
            'crouch': 'adventurer-crouch-',
            'hurt': 'adventurer-hurt-',
            'stand': 'adventurer-stand-',
        }

        for anim_name, prefix in animations.items():
            frames = []
            frame_index = 0

            while True:
                filename = f"{prefix}{frame_index:02d}.png"
                path = os.path.join(self.base_path, filename)

                if os.path.exists(path):
                    try:
                        sprite = pygame.image.load(path).convert_alpha()
                        frames.append(sprite)
                        frame_index += 1
                    except:
                        break
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
