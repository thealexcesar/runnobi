# Runnobi 🥷

Fast-paced ninja endless runner with parkour and combat mechanics

## Description

**Runnobi** is an endless runner where you control a ninja running through an infinite procedurally generated landscape. Use parkour moves (jump, slide) and combat abilities (katana slash, shuriken throw, shadow dash) to avoid obstacles, destroy enemies, and collect coins.

The game gradually increases in speed, creating an intense, skill-based challenge. Only the most skilled players can survive 5+ minutes!

## Features

- **Parkour Mechanics**
  - Jump over obstacles
  - Slide under low barriers
  
- **Combat Abilities**
  - Katana Slash: Destroy nearby enemies with a melee attack
  - Shuriken Throw: Launch projectiles at distant enemies
  - Shadow Dash: Become invincible and dash through obstacles for a short time

- **Progressive Difficulty**
  - Game speed gradually increases over time
  - More challenging as you survive longer
  
- **Scoring System**
  - Score based on distance traveled
  - Collect coins for bonus points
  - Destroy enemies for extra score

## Installation

### Requirements
- Python 3.8 or higher
- pygame 2.5.2 or higher

### Install from source

```bash
# Clone the repository
git clone https://github.com/thealexcesar/runnobi.git
cd runnobi

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## How to Play

### Starting the Game

Run the game using Python:

```bash
python -m runnobi.main
```

Or if installed:

```bash
runnobi
```

### Controls

**Movement:**
- `SPACE` / `UP` / `W` - Jump
- `DOWN` / `S` - Slide

**Combat:**
- `Z` / `J` - Katana Slash (melee attack)
- `X` / `K` - Throw Shuriken (ranged attack)
- `C` / `SHIFT` - Shadow Dash (invincibility dash)

**Other:**
- `P` - Pause game
- `R` - Restart (when game over)
- `ESC` - Quit game

### Gameplay Tips

1. **Master the basics first**: Practice jumping and sliding before using combat abilities
2. **Use Shadow Dash wisely**: It has a 3-second cooldown, save it for emergencies
3. **Destroy enemies for points**: Use katana or shuriken to eliminate flying enemies
4. **Collect coins**: They boost your score and appear at various heights
5. **Watch the speed**: The game gets progressively faster - stay focused!
6. **Survival milestones**: 
   - 1 minute: You're getting the hang of it
   - 3 minutes: You're skilled
   - 5+ minutes: You're a master ninja!

## Game Mechanics

### Player Abilities

- **Jump**: Standard parkour move to clear obstacles
- **Slide**: Duck under obstacles while maintaining speed
- **Katana Slash**: Short-range melee attack with cooldown
- **Shuriken Throw**: Ranged projectile attack with cooldown
- **Shadow Dash**: Brief invincibility with long cooldown (3 seconds)

### Obstacles

- Randomly generated ground obstacles
- Must be jumped over or slid under
- Collision results in game over

### Enemies

- Flying enemies that move at varying speeds
- Can be destroyed with combat abilities
- Collision results in game over (unless shadow dashing)
- Award bonus points when destroyed

### Coins

- Collectible items scattered throughout the level
- Appear at different heights
- Add bonus points to your score

### Difficulty Scaling

- Game speed starts at 8 and gradually increases to maximum of 20
- Speed increase is continuous and automatic
- Creates an increasingly challenging experience

## Development

### Project Structure

```
runnobi/
├── runnobi/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── game.py          # Main game loop and logic
│   ├── player.py        # Player character with abilities
│   ├── entities.py      # Obstacles, enemies, coins
│   └── constants.py     # Game configuration
├── requirements.txt
├── setup.py
├── README.md
└── LICENSE
```

### Running Tests

Currently, the game doesn't have automated tests. Manual testing can be done by running the game.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created by thealexcesar

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Future Enhancements

Possible future additions:
- Power-ups and upgrades
- Different enemy types
- Boss battles
- Leaderboard system
- Sound effects and music
- Multiple environments/themes
- Character customization
