"""Game entities: obstacles, enemies, and coins."""

import pygame
import random
from runnobi.constants import *


class Obstacle:
    """Ground obstacle that the player must avoid."""
    
    def __init__(self, x):
        self.x = x
        self.width = random.randint(OBSTACLE_WIDTH_MIN, OBSTACLE_WIDTH_MAX)
        self.height = random.randint(OBSTACLE_HEIGHT_MIN, OBSTACLE_HEIGHT_MAX)
        self.y = GROUND_Y + PLAYER_HEIGHT - self.height
        self.color = DARK_GRAY
    
    def update(self, speed):
        """Move obstacle to the left."""
        self.x -= speed
    
    def is_off_screen(self):
        """Check if obstacle is off screen."""
        return self.x + self.width < 0
    
    def get_rect(self):
        """Get collision rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw obstacle."""
        pygame.draw.rect(screen, self.color, self.get_rect())
        # Add some detail
        pygame.draw.rect(screen, BLACK, self.get_rect(), 2)


class Enemy:
    """Flying enemy that can be destroyed."""
    
    def __init__(self, x):
        self.x = x
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        # Random height for variety
        self.y = random.randint(GROUND_Y - 200, GROUND_Y - 50)
        self.base_speed = random.randint(-ENEMY_SPEED_VARIATION, ENEMY_SPEED_VARIATION)
        self.destroyed = False
        self.color = RED
    
    def update(self, speed):
        """Move enemy to the left."""
        self.x -= (speed + self.base_speed)
    
    def is_off_screen(self):
        """Check if enemy is off screen."""
        return self.x + self.width < 0
    
    def get_rect(self):
        """Get collision rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw enemy."""
        if not self.destroyed:
            # Enemy body
            pygame.draw.rect(screen, self.color, self.get_rect())
            # Evil eyes
            eye_y = self.y + 15
            pygame.draw.circle(screen, YELLOW, 
                             (int(self.x + 12), eye_y), 5)
            pygame.draw.circle(screen, YELLOW, 
                             (int(self.x + 28), eye_y), 5)
            pygame.draw.circle(screen, BLACK, 
                             (int(self.x + 12), eye_y), 2)
            pygame.draw.circle(screen, BLACK, 
                             (int(self.x + 28), eye_y), 2)


class Coin:
    """Collectible coin for score."""
    
    def __init__(self, x):
        self.x = x
        self.size = COIN_SIZE
        # Random height for variety
        self.y = random.randint(GROUND_Y - 200, GROUND_Y - 50)
        self.collected = False
        self.rotation = 0
    
    def update(self, speed):
        """Move coin to the left and rotate."""
        self.x -= speed
        self.rotation = (self.rotation + 5) % 360
    
    def is_off_screen(self):
        """Check if coin is off screen."""
        return self.x + self.size < 0
    
    def get_rect(self):
        """Get collision rectangle."""
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def draw(self, screen):
        """Draw coin."""
        if not self.collected:
            # Draw spinning coin effect
            pygame.draw.circle(screen, YELLOW, 
                             (int(self.x + self.size // 2), 
                              int(self.y + self.size // 2)), 
                             self.size // 2)
            # Inner circle for depth
            pygame.draw.circle(screen, (255, 200, 0), 
                             (int(self.x + self.size // 2), 
                              int(self.y + self.size // 2)), 
                             self.size // 3)
