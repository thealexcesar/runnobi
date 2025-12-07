# 🥷 RUNNOBI - Core Mechanics (Simplified)

## 🎮 Player Controls

| Input | Action | Description |
|-------|--------|-------------|
| `SPACE` / `J` | Jump | Jump over obstacles (double jump available) |
| `DOWN` / `K` | Crouch | Duck under obstacles (uses "stand" animation 0-5) |
| `DOWN` / `K` | Attack (Ground) | When crouched, destroys wooden crates |
| `X` / `Z` | Attack (Sword) | Slash forward to destroy wooden crates |
| `ESC` / `P` | Pause | Pause game |

## 🥷 Ninja Abilities

### 1. Jump & Double Jump
- **Cooldown:** None
- **Use:** Jump over high obstacles
- **Mechanic:**
  - Press `SPACE`/`J` once to jump
  - Press again in mid-air for double jump
  - **Second jump uses "smrslt" sprite animation**
- **Physics:** Gravity applies, responsive controls

### 2. Crouch (Stand Sprite)
- **Cooldown:** None
- **Use:** Duck under low obstacles
- **Mechanic:**
  - Hold `DOWN`/`K` to crouch
  - Uses "adventurer-stand-" animation (frames 0-5)
  - Hitbox reduces from 84px → 50px height
  - **Also destroys wooden crates when touching them**
- **Duration:** As long as button is held

### 3. Sword Attack
- **Cooldown:** 0.3 seconds
- **Use:** Destroy wooden crates in front of player
- **Mechanic:**
  - Press `X`/`Z` to slash
  - Uses "adventurer-attack1-" animation
  - Destroys all wooden crates in 80px radius
  - Awards +5 points per crate destroyed
- **Range:** 80 pixels forward

## 🚧 Obstacles

### Spike (Instant Death)
- **Material:** Metal
- **Height:** 50px
- **Behavior:** Cannot be destroyed
- **Counter:** Jump over
- **Spawn Rate:** Common

### High Barrier
- **Material:** Stone
- **Height:** 100px
- **Behavior:** Solid, cannot be destroyed
- **Counter:** Jump or double jump over
- **Spawn Rate:** Common

### Wooden Crate (Breakable)
- **Material:** Wood
- **Height:** 56px
- **Behavior:** Can be destroyed
- **Counter:**
  - Slash with sword (attack)
  - Crouch into it (stand sprite)
  - Jump over it
- **Spawn Rate:** Medium
- **Reward:** Sometimes drops coins
- **Visual:** Clearly wooden appearance

## 💎 Collectibles

### Coin
- **Value:** +10 points
- **Spawn:** Common, appears in clusters
- **Visual:** Gold spinning circle
- **Behavior:** Collected on touch

## 📊 Scoring System

```
Action                    Points
─────────────────────────────────
Coin collected            +10
Destroy wooden crate      +5
Survive 10 seconds        +50
Survive 30 seconds        +100
Survive 1 minute          +200
```

## ⚙️ Difficulty Progression

### Speed Curve
```
Time      Speed (px/s)    Difficulty
──────────────────────────────────
0:00      300            Easy
0:30      400            Medium
1:00      500            Hard
2:00      650            Very Hard
3:00+     800            Extreme
```

### Obstacle Density
- Speed increases gradually (5 px/s per second)
- Spawn interval: 1.5 - 3.0 seconds (random)
- Fair difficulty curve for 3-5 minute runs

## 🎯 Design Philosophy

**Simplified Mechanics:**
- ❌ No shuriken throw (removed complexity)
- ❌ No shadow dash (removed invincibility mechanic)
- ✅ Clear distinction: Stone/Metal = indestructible, Wood = breakable
- ✅ Crouch serves dual purpose: dodge + attack
- ✅ Focus on timing and reflexes over complex combos

**Player Experience:**
- "Easy to learn, hard to master"
- Clear visual feedback
- Responsive controls
- Fair challenge progression
- Quick retry loop ("one more run!")
