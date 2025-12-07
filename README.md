# 🥷 RUNNOBI - Ninja Endless Runner

Fast-paced ninja endless runner with parkour and combat mechanics.

**Academic Project:** Demonstrating Clean Architecture, SOLID principles, and Design Patterns in Python game development.

---

## 🎮 Game Features

### Core Gameplay
- **Endless Runner:** Auto-scrolling world with increasing difficulty
- **Parkour Mechanics:** Jump and double jump over obstacles
- **Combat System:** Slash wooden crates with your katana
- **Crouching:** Duck under low obstacles (also destroys wooden crates!)
- **Score System:** Collect coins and destroy crates for points

### Controls

| Input | Action |
|-------|--------|
| `SPACE` / `J` / `W` / `UP` | Jump (press again for double jump) |
| `DOWN` / `K` / `S` | Crouch (duck under obstacles, destroy wood) |
| `X` / `Z` | Attack (sword slash destroys wooden crates) |
| `ESC` / `P` | Pause |

### Obstacles
- **Spike** (Metal) - Cannot be destroyed, must jump over
- **Barrier** (Stone) - Cannot be destroyed, must jump over
- **Wooden Crate** (Wood) - Can be destroyed with attack or crouch

### Collectibles
- **Coins** - Collect for +10 points

---

## 🏗️ Architecture

### Clean Architecture Layers

```
┌─────────────────────────────────────┐
│     Infrastructure Layer            │
│  (Pygame, Input, Rendering, I/O)    │
├─────────────────────────────────────┤
│     Application Layer                │
│  (Game Logic, Physics, Collision)   │
├─────────────────────────────────────┤
│     Domain Layer                     │
│  (Entities, Value Objects, Rules)   │
└─────────────────────────────────────┘
```

### Design Patterns Implemented

1. **Factory Pattern** - `ObstacleFactory`, `CollectibleFactory`
   - Creates game entities without exposing creation logic
   - Easy to add new obstacle/collectible types

2. **State Pattern** - `NinjaState` enum
   - Manages ninja animations and behavior
   - Clean state transitions

3. **Adapter Pattern** - `KeyboardAdapter`
   - Converts pygame input to game actions
   - Decouples input handling from game logic

4. **Mediator Pattern** - `GameManager`
   - Coordinates all game systems
   - Reduces coupling between systems

5. **Value Object Pattern** - `Position`, `Velocity`, `Bounds`
   - Immutable objects for game state
   - Ensures data consistency

6. **Proxy Pattern** - `PlaceholderSprites`
   - Lazy loading of sprite resources
   - Fallback system for missing sprites

### SOLID Principles

- **Single Responsibility:** Each class has one clear purpose
- **Open/Closed:** Entities extensible via inheritance
- **Liskov Substitution:** All obstacles/collectibles interchangeable
- **Interface Segregation:** Focused interfaces (ICollidable, IUpdatable, etc.)
- **Dependency Inversion:** Depends on interfaces, not implementations

---

## 📁 Project Structure

```
runnobi/
├── src/
│   ├── domain/                 # Core business logic
│   │   ├── entities/          # Game entities (Ninja, Obstacles)
│   │   ├── interfaces/        # Entity contracts
│   │   └── value_objects/     # Immutable value types
│   ├── application/           # Application services
│   │   ├── physics_engine.py # Physics simulation
│   │   ├── collision_detector.py # Collision detection
│   │   └── game_manager.py   # Main coordinator
│   ├── infrastructure/        # External interfaces
│   │   ├── input/            # Input handling
│   │   └── rendering/        # Sprite system
│   └── factories/            # Entity factories
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
└── assets/                   # Sprites and resources
```

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- Pygame 2.0+

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/runnobi.git
cd runnobi

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

---

## 🎯 Game Mechanics

### Jump System
- **First Jump:** Press SPACE to jump
- **Double Jump:** Press SPACE again in mid-air for higher jump
- **Animation:** Second jump uses somersault animation

### Crouch System (NEW!)
- **Hold DOWN:** Crouch using "stand" sprite animation
- **Reduced Hitbox:** Height 126px → 75px (can fit under obstacles)
- **Destroys Wood:** Touching wooden crates while crouching destroys them!

### Attack System
- **Sword Slash:** Press X or Z to attack
- **Range:** 80 pixels forward
- **Effect:** Destroys wooden crates in range
- **Cooldown:** 0.3 seconds

### Difficulty Progression
- **Speed Increase:** +5 px/s per second
- **Starting Speed:** 300 px/s
- **Max Speed:** 800 px/s (at 3+ minutes)

---

## 📚 Documentation

- **[Core Mechanics](docs/mechanics.md)** - Detailed gameplay mechanics
- **[Design Document](notes/design.md)** - Architecture and patterns
- **[Tasks](notes/todo.md)** - Development roadmap

---

## 🧪 Testing

### Unit Tests
- Value objects (Position, Velocity, Bounds)
- Entity behavior
- Collision detection logic

### Integration Tests
- Physics + Collision integration
- Input + Game Manager integration
- Full gameplay loop

---

## 🎨 Sprite System

### Sprite Loading
1. **Real Sprites:** Loads from individual PNG files
2. **Scaling:** Applies 1.5x scale for better visibility
3. **Fallback:** Colored rectangles if sprites missing

### Sprite Animations

| Animation | Frames | Sprite Files |
|-----------|--------|--------------|
| Idle | 4 | `adventurer-idle-00.png` to `-03.png` |
| Run | 6 | `adventurer-run-00.png` to `-05.png` |
| Jump | 3 | `adventurer-jump-00.png` to `-02.png` |
| Crouch | 6 | `adventurer-stand-00.png` to `-05.png` |
| Attack | 4 | `adventurer-attack1-00.png` to `-03.png` |
| Somersault | 4 | `adventurer-smrslt-00.png` to `-03.png` |

---

## 🤝 Contributing

This is an academic project, but suggestions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 🏆 Academic Requirements

### Design Patterns (6 Required) ✅
1. ✅ Factory Pattern
2. ✅ State Pattern
3. ✅ Adapter Pattern
4. ✅ Mediator Pattern
5. ✅ Value Object Pattern
6. ✅ Proxy Pattern

### SOLID Principles ✅
- ✅ Single Responsibility
- ✅ Open/Closed
- ✅ Liskov Substitution
- ✅ Interface Segregation
- ✅ Dependency Inversion

### Clean Architecture ✅
- ✅ Domain Layer (entities, value objects)
- ✅ Application Layer (use cases, services)
- ✅ Infrastructure Layer (frameworks, I/O)

---

## 🎮 Gameplay Tips

1. **Master Double Jump:** Essential for high barriers
2. **Crouch Early:** Duck under obstacles before they hit you
3. **Destroy Wood:** Crouching into crates destroys them (+5 points)
4. **Attack Forward:** Use sword to clear path ahead
5. **Collect Coins:** Every point counts for high score!
6. **Speed Management:** Game gets faster - stay focused!

---

## 🐛 Known Issues

- None currently! 🎉

---

## 📧 Contact

**Author:** [Your Name]  
**Email:** [your.email@example.com]  
**Project Link:** [https://github.com/yourusername/runnobi](https://github.com/yourusername/runnobi)

---

**Made with ❤️ and ☕ for academic excellence**
