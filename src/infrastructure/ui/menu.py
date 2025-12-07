"""
Main menu system for Runnobi.
Handles menu rendering and user interaction.
"""
import pygame
from pathlib import Path

from infrastructure.rendering.sprite_placeholder import PlaceholderSprites


class MainMenu:
    """Main menu screen with Start button."""

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize main menu.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Pixel font (cross-platform path)
        # Pixel font (cross-platform path)
        font_path = Path(
            __file__).parent.parent.parent.parent / 'assets' / 'fonts' / 'Press_Start_2P' / 'PressStart2P-Regular.ttf'
        try:
            self.title_font = pygame.font.Font(str(font_path), 36)
            self.button_font = pygame.font.Font(str(font_path), 24)
            self.subtitle_font = pygame.font.Font(str(font_path), 16)
        except:
            print(f"Failed to load font: {font_path}")
            self.title_font = pygame.font.Font(None, 48)
            self.button_font = pygame.font.Font(None, 32)
            self.subtitle_font = pygame.font.Font(None, 24)

        # Colors
        self.bg_color = (20, 25, 35)
        self.title_color = (220, 50, 50)
        self.button_color = (200, 50, 50)
        self.button_hover_color = (255, 80, 80)
        self.text_color = (255, 255, 255)

        # Button setup
        button_width = 250
        button_height = 70
        self.start_button_rect = pygame.Rect(
            (screen_width - button_width) // 2, 420,
            button_width,
            button_height
        )
        self.button_hovered = False

        # Ninja sprite animation (IDLE loop)
        self.ninja_frame = 0
        self.ninja_animation_timer = 0.0
        self.ninja_animation_speed = 0.15
        self.ninja_x = screen_width // 2 - 42
        self.ninja_y = 220

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle menu events.

        Args:
            event: Pygame event

        Returns:
            True if Start button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.button_hovered = self.start_button_rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.button_hovered:
                return True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return True

        return False

    def update(self, delta_time: float) -> None:
        """
        Update menu animations.

        Args:
            delta_time: Time elapsed since last frame (seconds)
        """
        self.ninja_animation_timer += delta_time
        if self.ninja_animation_timer >= self.ninja_animation_speed:
            self.ninja_animation_timer = 0.0
            self.ninja_frame = (self.ninja_frame + 1) % 4  # 4 idle frames

    def render(self, screen: pygame.Surface) -> None:
        """
        Render the menu.

        Args:
            screen: Pygame surface to render on
        """
        # Background
        screen.fill(self.bg_color)

        # Animated ninja sprite (IDLE)
        ninja_sprite = PlaceholderSprites.create_ninja_idle(frame=self.ninja_frame)
        screen.blit(ninja_sprite, (self.ninja_x, self.ninja_y))

        # Title
        title_text = self.title_font.render("RUN:NOBI", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)

        # Subtitle
        # subtitle_text = self.subtitle_font.render("ðŸ¥· Ninja Endless Runner", True, self.text_color)
        # subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3 + 60))
        # screen.blit(subtitle_text, subtitle_rect)

        # Start button
        button_color = self.button_hover_color if self.button_hovered else self.button_color
        pygame.draw.rect(screen, button_color, self.start_button_rect, border_radius=10)
        pygame.draw.rect(screen, self.text_color, self.start_button_rect, 3, border_radius=10)

        # Start button text
        start_text = self.button_font.render("START", True, self.text_color)
        start_rect = start_text.get_rect(center=self.start_button_rect.center)
        screen.blit(start_text, start_rect)

        # Instructions
        instructions = [
            "Controls:",
            "SPACE - Jump (double jump!) | DOWN - Crouch",
            "X/Z - Attack (destroy wooden crates)",
            "",
            "💡 Wooden crates are breakable and give points!",
            "Game speed increases over time!"
        ]

        y_offset = self.screen_height - 180
        for instruction in instructions:
            text = self.subtitle_font.render(instruction, True, (150, 150, 150))
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30
