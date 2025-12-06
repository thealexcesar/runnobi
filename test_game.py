#!/usr/bin/env python3
"""Test script to verify game functionality."""

import os
import sys

# Set dummy drivers for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from runnobi.game import Game
from runnobi.player import Player
from runnobi.entities import Obstacle, Enemy, Coin
from runnobi.constants import *


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    print("✓ All modules imported successfully")


def test_player_abilities():
    """Test player abilities."""
    print("\nTesting player abilities...")
    player = Player()
    
    # Test jump
    assert player.is_on_ground
    player.jump()
    assert player.velocity_y == JUMP_STRENGTH
    assert player.is_jumping
    print("✓ Jump ability works")
    
    # Reset player
    player = Player()
    
    # Test slide
    player.slide()
    assert player.is_sliding
    assert player.slide_timer == SLIDE_DURATION
    print("✓ Slide ability works")
    
    # Test katana
    player.katana_slash()
    assert player.katana_active
    assert player.katana_timer == KATANA_COOLDOWN
    print("✓ Katana slash works")
    
    # Test shuriken
    player.throw_shuriken()
    assert len(player.shurikens) == 1
    print("✓ Shuriken throw works")
    
    # Test shadow dash
    player.shadow_dash()
    assert player.shadow_dashing
    assert player.shadow_dash_invincible
    print("✓ Shadow dash works")


def test_entities():
    """Test game entities."""
    print("\nTesting entities...")
    
    obstacle = Obstacle(500)
    assert obstacle.x == 500
    assert obstacle.y == GROUND_Y + PLAYER_HEIGHT - obstacle.height
    print("✓ Obstacle creation works")
    
    enemy = Enemy(600)
    assert enemy.x == 600
    assert not enemy.destroyed
    print("✓ Enemy creation works")
    
    coin = Coin(700)
    assert coin.x == 700
    assert not coin.collected
    print("✓ Coin creation works")


def test_game_mechanics():
    """Test game mechanics."""
    print("\nTesting game mechanics...")
    
    game = Game()
    assert game.game_speed == INITIAL_GAME_SPEED
    assert game.player is not None
    print("✓ Game initialization works")
    
    # Simulate some frames
    for _ in range(60):
        game.update()
    
    assert game.frames == 60
    assert game.distance > 0
    print("✓ Game update loop works")
    
    # Test speed progression
    game2 = Game()
    game2.player.y = -500  # Move player away from obstacles
    for _ in range(18000):  # 5 minutes
        game2.update()
    
    assert game2.game_speed >= MAX_GAME_SPEED - 0.1
    print("✓ Speed progression works")


def test_collision_detection():
    """Test collision detection."""
    print("\nTesting collision detection...")
    
    game = Game()
    
    # Force collision with obstacle
    obstacle = Obstacle(game.player.x)
    obstacle.y = game.player.y
    game.obstacles.append(obstacle)
    game.check_collisions()
    
    assert game.game_over
    print("✓ Obstacle collision detection works")
    
    # Test enemy collision
    game2 = Game()
    enemy = Enemy(game2.player.x)
    enemy.y = game2.player.y
    game2.enemies.append(enemy)
    game2.check_collisions()
    
    assert game2.game_over
    print("✓ Enemy collision detection works")
    
    # Test coin collection
    game3 = Game()
    coin = Coin(game3.player.x)
    coin.y = game3.player.y
    game3.coins.append(coin)
    initial_coins = game3.player.coins
    game3.check_collisions()
    
    assert coin.collected
    assert game3.player.coins == initial_coins + 1
    print("✓ Coin collection works")


def main():
    """Run all tests."""
    print("=" * 60)
    print("RUNNOBI GAME TEST SUITE")
    print("=" * 60)
    
    try:
        test_imports()
        test_player_abilities()
        test_entities()
        test_game_mechanics()
        test_collision_detection()
        
        print("\n" + "=" * 60)
        print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
