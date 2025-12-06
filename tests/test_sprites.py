"""
Quick test script to visualize placeholder sprites.

Run this to see all placeholder sprites before integrating into game.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
from infrastructure.rendering.sprite_placeholder import PlaceholderSprites


def main():
    """Display all placeholder sprites in a grid."""
    pygame.init()

    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("🥷 Runnobi - Placeholder Sprites Preview")

    clock = pygame.time.Clock()

    sprites = {
        "Ninja Idle": PlaceholderSprites.create_ninja_idle(),
        "Ninja Run 0": PlaceholderSprites.create_ninja_run(frame=0),
        "Ninja Run 1": PlaceholderSprites.create_ninja_run(frame=1),
        "Ninja Jump": PlaceholderSprites.create_ninja_jump(),
        "Ninja Slide": PlaceholderSprites.create_ninja_slide(),
        "Ninja Attack": PlaceholderSprites.create_ninja_attack(),
        "Ninja Dash": PlaceholderSprites.create_ninja_dash(),
        "Spike": PlaceholderSprites.create_obstacle_spike(),
        "Barrier": PlaceholderSprites.create_obstacle_barrier(),
        "Low Barrier": PlaceholderSprites.create_obstacle_low_barrier(),
        "Crate": PlaceholderSprites.create_breakable_crate(),
        "Coin": PlaceholderSprites.create_coin(),
        "Shuriken": PlaceholderSprites.create_shuriken(),
        "Shadow Orb": PlaceholderSprites.create_shadow_orb(),
    }

    print("🥷 Runnobi Sprite Viewer")
    print("=" * 50)
    print(f"Loaded {len(sprites)} placeholder sprites")
    print("Close window to exit (ESC or X)")
    print("=" * 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((200, 220, 240))

        title_font = pygame.font.Font(None, 36)
        title = title_font.render("RUNNOBI - Placeholder Sprites", True, (50, 50, 50))
        screen.blit(title, (250, 20))

        x, y = 80, 80
        for name, sprite in sprites.items():
            screen.blit(sprite, (x, y))

            font = pygame.font.Font(None, 18)
            text = font.render(name, True, (0, 0, 0))
            screen.blit(text, (x - 10, y + sprite.get_height() + 8))

            x += 180
            if x > 750:
                x = 80
                y += 150

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("\n✅ Sprite viewer closed")


if __name__ == "__main__":
    main()
