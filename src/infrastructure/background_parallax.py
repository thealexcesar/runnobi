"""
Layered background parallax system.
Loads and renders multiple background layers with different scroll speeds.
"""
import pygame
from pathlib import Path
from typing import List, Tuple


class BackgroundLayer:
    """Single parallax background layer."""
    
    def __init__(self, image_path: str, speed_multiplier: float, screen_width: int, screen_height: int):
        """
        Initialize background layer.
        
        Args:
            image_path: Path to layer image
            speed_multiplier: How fast this layer moves (0.0 = static, 1.0 = game speed)
            screen_width: Screen width
            screen_height: Screen height
        """
        self.speed_multiplier = speed_multiplier
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load and scale image
        # Load and scale image
        try:
            original = pygame.image.load(image_path).convert_alpha()
            aspect_ratio = original.get_width() / original.get_height()
            new_height = screen_height
            new_width = int(new_height * aspect_ratio)
            self.image = pygame.transform.scale(original, (new_width, new_height))
        except Exception as e:
            print(f"Failed to load background layer {image_path}: {e}")
            # Fallback: transparent surface
            self.image = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        
        # Position for seamless scrolling
        self.x1 = 0
        self.x2 = screen_width
    
    def update(self, delta_time: float, scroll_speed: float) -> None:
        """
        Update layer position for parallax effect.
        
        Args:
            delta_time: Time elapsed since last frame
            scroll_speed: Base game scroll speed
        """
        # Move both copies of the image
        move_amount = scroll_speed * self.speed_multiplier * delta_time
        self.x1 -= move_amount
        self.x2 -= move_amount
        
        # Reset positions for seamless loop
        if self.x1 <= -self.screen_width:
            self.x1 = self.screen_width
        if self.x2 <= -self.screen_width:
            self.x2 = self.screen_width
    
    def render(self, screen: pygame.Surface) -> None:
        """Render layer to screen."""
        screen.blit(self.image, (int(self.x1), 0))
        screen.blit(self.image, (int(self.x2), 0))


class BackgroundParallax:
    """
    Multi-layer parallax background system.
    
    Renders layered backgrounds with depth effect.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize parallax system.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Base path
        base_path = Path(__file__).parent.parent.parent / 'assets' / 'backgrounds' / 'png'

        # Create layers (back to front, slowest to fastest)
        self.layers: List[BackgroundLayer] = [
            BackgroundLayer(str(base_path / '0.png'), 0.0, screen_width, screen_height),  # Sky (static)
            BackgroundLayer(str(base_path / '1.png'), 0.1, screen_width, screen_height),  # Moon/Sun
            BackgroundLayer(str(base_path / '2.png'), 0.3, screen_width, screen_height),  # Far clouds
            BackgroundLayer(str(base_path / '3.png'), 0.5, screen_width, screen_height),  # Near clouds
        ]
    
    def update(self, delta_time: float, scroll_speed: float) -> None:
        """
        Update all background layers.
        
        Args:
            delta_time: Time elapsed
            scroll_speed: Game scroll speed
        """
        for layer in self.layers:
            layer.update(delta_time, scroll_speed)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render all layers back to front."""
        for layer in self.layers:
            layer.render(screen)
