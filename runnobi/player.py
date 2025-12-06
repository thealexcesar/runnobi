"""Player class for the ninja character."""

import pygame
from runnobi.constants import *


class Player:
    """Ninja player with parkour and combat abilities."""
    
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = GROUND_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.is_sliding = False
        self.slide_timer = 0
        self.is_on_ground = True
        
        # Combat abilities
        self.katana_active = False
        self.katana_timer = 0
        self.katana_cooldown_timer = 0
        
        self.shurikens = []
        self.shuriken_cooldown_timer = 0
        
        self.shadow_dashing = False
        self.shadow_dash_timer = 0
        self.shadow_dash_cooldown_timer = 0
        self.shadow_dash_invincible = False
        
        # Stats
        self.coins = 0
        self.score = 0
        
    def jump(self):
        """Make the ninja jump."""
        if self.is_on_ground and not self.is_sliding:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.is_on_ground = False
    
    def slide(self):
        """Make the ninja slide."""
        if self.is_on_ground and not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = SLIDE_DURATION
    
    def katana_slash(self):
        """Activate katana slash."""
        if self.katana_cooldown_timer == 0:
            self.katana_active = True
            self.katana_timer = KATANA_COOLDOWN
            self.katana_cooldown_timer = KATANA_COOLDOWN
    
    def throw_shuriken(self):
        """Throw a shuriken."""
        if self.shuriken_cooldown_timer == 0:
            shuriken_y = self.y + self.height // 2
            self.shurikens.append({
                'x': self.x + self.width,
                'y': shuriken_y,
                'size': 15
            })
            self.shuriken_cooldown_timer = SHURIKEN_COOLDOWN
    
    def shadow_dash(self):
        """Activate shadow dash ability."""
        if self.shadow_dash_cooldown_timer == 0:
            self.shadow_dashing = True
            self.shadow_dash_timer = SHADOW_DASH_DURATION
            self.shadow_dash_cooldown_timer = SHADOW_DASH_COOLDOWN
            self.shadow_dash_invincible = True
    
    def update(self):
        """Update player state."""
        # Apply gravity
        if not self.is_on_ground:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y
        
        # Check if landed
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.velocity_y = 0
            self.is_jumping = False
            self.is_on_ground = True
        
        # Handle sliding
        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False
                self.slide_timer = 0
        
        # Handle katana
        if self.katana_timer > 0:
            self.katana_timer -= 1
            if self.katana_timer == 0:
                self.katana_active = False
        
        if self.katana_cooldown_timer > 0:
            self.katana_cooldown_timer -= 1
        
        # Handle shuriken cooldown
        if self.shuriken_cooldown_timer > 0:
            self.shuriken_cooldown_timer -= 1
        
        # Update shurikens
        for shuriken in self.shurikens[:]:
            shuriken['x'] += SHURIKEN_SPEED
            if shuriken['x'] > SCREEN_WIDTH + 50:
                self.shurikens.remove(shuriken)
        
        # Handle shadow dash
        if self.shadow_dashing:
            self.shadow_dash_timer -= 1
            if self.shadow_dash_timer <= 0:
                self.shadow_dashing = False
                self.shadow_dash_invincible = False
        
        if self.shadow_dash_cooldown_timer > 0:
            self.shadow_dash_cooldown_timer -= 1
    
    def get_rect(self):
        """Get player collision rectangle."""
        if self.is_sliding:
            # Smaller hitbox when sliding
            return pygame.Rect(self.x, self.y + self.height // 2, 
                             self.width, self.height // 2)
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_katana_rect(self):
        """Get katana slash collision rectangle."""
        if self.katana_active:
            return pygame.Rect(self.x + self.width, self.y, 
                             KATANA_RANGE, self.height)
        return None
    
    def draw(self, screen):
        """Draw the player on screen."""
        player_rect = self.get_rect()
        
        # Draw player with different color when shadow dashing
        if self.shadow_dashing:
            # Purple semi-transparent effect
            s = pygame.Surface((player_rect.width, player_rect.height))
            s.set_alpha(128)
            s.fill(PURPLE)
            screen.blit(s, (player_rect.x, player_rect.y))
        else:
            # Normal ninja (dark color)
            pygame.draw.rect(screen, BLACK, player_rect)
        
        # Draw ninja details
        if not self.shadow_dashing:
            # Head band
            pygame.draw.rect(screen, RED, 
                           (player_rect.x + 5, player_rect.y + 10, 
                            player_rect.width - 10, 8))
            
            # Eyes
            eye_y = player_rect.y + 20
            pygame.draw.circle(screen, WHITE, 
                             (player_rect.x + 15, eye_y), 4)
            pygame.draw.circle(screen, WHITE, 
                             (player_rect.x + 35, eye_y), 4)
        
        # Draw katana slash effect
        if self.katana_active:
            katana_rect = self.get_katana_rect()
            s = pygame.Surface((katana_rect.width, katana_rect.height))
            s.set_alpha(128)
            s.fill(YELLOW)
            screen.blit(s, (katana_rect.x, katana_rect.y))
            pygame.draw.line(screen, YELLOW, 
                           (katana_rect.x, katana_rect.y + katana_rect.height // 2),
                           (katana_rect.x + katana_rect.width, 
                            katana_rect.y + katana_rect.height // 2), 3)
        
        # Draw shurikens
        for shuriken in self.shurikens:
            pygame.draw.circle(screen, GRAY, 
                             (int(shuriken['x']), int(shuriken['y'])), 
                             shuriken['size'] // 2)
            # Shuriken star effect
            size = shuriken['size']
            x, y = int(shuriken['x']), int(shuriken['y'])
            pygame.draw.line(screen, WHITE, (x - size//2, y), (x + size//2, y), 2)
            pygame.draw.line(screen, WHITE, (x, y - size//2), (x, y + size//2), 2)
