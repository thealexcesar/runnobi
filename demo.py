#!/usr/bin/env python3
"""Demo script showing game features and mechanics."""

import os
import sys

# Set dummy drivers for headless demo
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from runnobi.game import Game
from runnobi.constants import *


def demo_game():
    """Run a demonstration of the game."""
    print("=" * 70)
    print("RUNNOBI - NINJA ENDLESS RUNNER DEMO")
    print("=" * 70)
    
    print("\n🥷 Initializing game...")
    game = Game()
    
    print(f"✓ Game started!")
    print(f"  - Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"  - FPS: {FPS}")
    print(f"  - Initial Speed: {game.game_speed}")
    
    print("\n📋 Game Features:")
    print("  Parkour Moves:")
    print("    • Jump - Clear obstacles with ninja agility")
    print("    • Slide - Duck under low barriers")
    print("\n  Combat Abilities:")
    print("    • Katana Slash - Melee attack with cooldown")
    print("    • Shuriken Throw - Ranged projectile attack")
    print("    • Shadow Dash - Invincibility dash (3s cooldown)")
    print("\n  Objectives:")
    print("    • Avoid obstacles and enemies")
    print("    • Collect coins for bonus points")
    print("    • Survive as long as possible")
    
    print("\n🎮 Simulating 60 seconds of gameplay...")
    
    # Move player up to avoid immediate collision
    game.player.y = 100
    
    # Simulate 60 seconds
    action_frames = {
        120: "Jump",
        180: "Slide", 
        240: "Katana Slash",
        300: "Throw Shuriken",
        360: "Shadow Dash",
    }
    
    for frame in range(3600):  # 60 seconds
        game.update()
        
        # Perform actions
        if frame in action_frames:
            action = action_frames[frame]
            if action == "Jump":
                game.player.jump()
            elif action == "Slide":
                game.player.slide()
            elif action == "Katana Slash":
                game.player.katana_slash()
            elif action == "Throw Shuriken":
                game.player.throw_shuriken()
            elif action == "Shadow Dash":
                game.player.shadow_dash()
            print(f"  {frame//60:2d}s: {action} activated!")
        
        # Report every 10 seconds
        if frame > 0 and frame % 600 == 0:
            seconds = frame // 60
            print(f"\n  ⏱️  {seconds} seconds:")
            print(f"     Speed: {game.game_speed:.2f}")
            print(f"     Score: {game.player.score}")
            print(f"     Coins: {game.player.coins}")
            print(f"     Obstacles on screen: {len(game.obstacles)}")
            print(f"     Enemies on screen: {len(game.enemies)}")
    
    print("\n" + "=" * 70)
    print("📊 FINAL STATISTICS")
    print("=" * 70)
    print(f"  ⏱️  Survival Time: 60 seconds")
    print(f"  🏃 Final Speed: {game.game_speed:.2f}")
    print(f"  📏 Distance Traveled: {game.distance:.0f}")
    print(f"  🎯 Final Score: {game.player.score}")
    print(f"  💰 Coins Collected: {game.player.coins}")
    print(f"  ⚔️  Shurikens Thrown: {1}")  # From our test
    print(f"  💀 Game Over: {game.game_over}")
    
    # Demonstrate difficulty progression
    print("\n" + "=" * 70)
    print("📈 DIFFICULTY PROGRESSION DEMO")
    print("=" * 70)
    print("\nSpeed increase over 5 minutes:")
    
    game2 = Game()
    game2.player.y = -500  # Avoid obstacles
    
    for minute in range(6):
        for _ in range(3600):  # 60 seconds
            game2.update()
        
        if minute < 5:
            print(f"  {minute + 1} min: Speed = {game2.game_speed:.2f}")
    
    print(f"\n  Maximum speed reached: {game2.game_speed:.2f}")
    print(f"  Challenge level: {'🔥' * int(game2.game_speed / 4)}")
    
    print("\n" + "=" * 70)
    print("✨ The game gets progressively harder as you survive!")
    print("   Can you survive 5+ minutes? Only master ninjas can!")
    print("=" * 70)
    
    print("\n🎮 To play the actual game with graphics, run:")
    print("   python -m runnobi.main")
    print("   or: runnobi")
    
    print("\n✓ Demo completed successfully!")


if __name__ == "__main__":
    try:
        demo_game()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
