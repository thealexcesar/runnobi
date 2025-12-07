# 🥷 RUNNOBI - Ninja Endless Runner

Fast-paced endless runner with parkour and combat mechanics. Academic project demonstrating Clean Architecture, SOLID principles, and Design Patterns.

---

## 🎮 Controls

| Input | Action |
|-------|--------|
| `SPACE` / `W` / `UP` | Jump (double jump in air) |
| `DOWN` / `S` | Crouch (slide under obstacles) |
| `X` / `Z` / `LEFT` / `RIGHT` | Attack (slash to destroy crates) |
| `ESC` | Pause / Return to menu |

---

## 🚧 Obstacles

### Spike (Metal - Indestructible)
- 3 sharp metal points
- **Counter:** Jump over

### Barrier (Stone - Indestructible)
- Tall stone wall with brick pattern
- **Counter:** Jump or double jump

### Low Blocker (Ceiling - Indestructible)
- Solid block from ceiling leaving gap at bottom
- **Counter:** Crouch to pass under

### Wooden Crate (Breakable)
- Brown crate with visible wood grain
- **Counter:** Attack (slash) OR crouch into it
- **Reward:** +100 points when destroyed

---

## 🎯 Mechanics

### Jump System
- **Single Jump:** Press SPACE/W/UP
- **Double Jump:** Press again in mid-air (uses somersault animation)
- Responsive physics with gravity

### Crouch System
- **Hold DOWN/S** to crouch (uses "stand" sprite animation)
- **Hitbox reduced:** 126px → 75px height
- **Destroys wooden crates** on contact
- Pass safely under low blockers

### Attack System
- **Press X/Z/LEFT/RIGHT** to slash with katana
- **Range:** 80 pixels forward
- **Cooldown:** 0.3 seconds
- Destroys wooden crates in range
- Uses "attack1" sprite animation

### Difficulty Progression
- **Speed increase:** +5 px/s per second
- **Starting speed:** 300 px/s
- **Max speed:** 800 px/s (after 3 minutes)

---

## 🏗️ Architecture

### Clean Architecture Layers
```
Infrastructure Layer (Pygame, Input, Rendering, Audio)
         ↓
Application Layer (Game Logic, Physics, Collision)
         ↓
Domain Layer (Entities, Value Objects, Business Rules)
```

### Design Patterns (6 Required ✅)

1. **Factory Pattern** - `ObstacleFactory`, `CollectibleFactory`
2. **State Pattern** - `NinjaState`, `GameState`
3. **Adapter Pattern** - `KeyboardAdapter`
4. **Mediator Pattern** - `GameManager`
5. **Value Object Pattern** - `Position`, `Velocity`, `Bounds`
6. **Proxy Pattern** - `PlaceholderSprites`

### SOLID Principles ✅

- **Single Responsibility:** Each class has one purpose
- **Open/Closed:** Extensible via inheritance
- **Liskov Substitution:** All obstacles interchangeable
- **Interface Segregation:** Focused interfaces (`ICollidable`, `IUpdatable`)
- **Dependency Inversion:** Depends on interfaces, not implementations

---

## 🚀 Getting Started

### Requirements
- Python 3.10+
- Pygame 2.6+

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/runnobi.git
cd runnobi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run game
python src/main.py
```

### Development
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Game States
- **Menu:** Main menu with animated ninja
- **Playing:** Active gameplay
- **Game Over:** Score display with restart option

---

## 🎯 Gameplay Tips

1. **Master double jump** - Essential for high barriers
2. **Crouch early** - Duck before obstacles hit you
3. **Use attack wisely** - Cooldown of 0.3s, plan ahead
4. **Destroy crates** - +100 points each
5. **Watch speed** - Game accelerates over time

---

## 📊 Scoring
```
Action                   Points
──────────────────────────────
Destroy wooden crate     +100
Distance traveled        +1 per meter
```

---

## 🤝 Contributing

This is an academic project. Suggestions welcome via issues or PRs!

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📝 License

MIT License - See LICENSE file

---
