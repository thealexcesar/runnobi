"""
Ninja entity - player character with simplified mechanics.

Implements clean state machine for animations and parkour movement.
Focused gameplay: jump, crouch, and attack wooden obstacles.
"""
import pygame
from typing import Optional
from ..interfaces.i_game_entity import IGameEntity
from ..interfaces.i_collidable import ICollidable
from ..interfaces.i_updatable import IUpdatable
from ..interfaces.i_renderable import IRenderable
from ..value_objects.position import Position
from ..value_objects.velocity import Velocity
from ..value_objects.bounds import Bounds
from .ninja_state import NinjaState


class Ninja(IGameEntity, ICollidable, IUpdatable, IRenderable):
    """
    Player character with parkour and combat abilities.

    Mechanics:
    - Jump and double jump to clear obstacles
    - Crouch to duck under obstacles (and destroy wooden crates)
    - Attack to destroy wooden crates in front
    - Second jump uses special somersault animation

    Follows Single Responsibility: manages only player state and movement.
    Collision and physics handled by external systems.
    """

    # Sprite dimensions (will be scaled by sprite loader)
    BASE_WIDTH = 56
    BASE_HEIGHT = 84
    BASE_CROUCH_HEIGHT = 50

    # Actual dimensions after 1.5x scaling
    WIDTH = int(BASE_WIDTH * 1.5)  # 84px
    HEIGHT = int(BASE_HEIGHT * 1.5)  # 126px
    CROUCH_HEIGHT = int(BASE_CROUCH_HEIGHT * 1.5)  # 75px

    # Physics constants
    JUMP_VELOCITY = -900.0
    DOUBLE_JUMP_VELOCITY = -750.0

    # Ability durations
    ATTACK_DURATION = 0.3  # seconds
    CROUCH_MIN_DURATION = 0.2  # minimum crouch time

    def __init__(self, start_x: float, start_y: float, ground_y: float) -> None:
        """
        Initialize ninja at starting position.

        Args:
            start_x: Initial x position (pixels)
            start_y: Initial y position (pixels)
            ground_y: Y coordinate of ground level
        """
        self._position = Position(start_x, start_y)
        self._velocity = Velocity(0.0, 0.0)
        self._ground_y = ground_y

        # State management
        self._state = NinjaState.IDLE
        self._active = True
        self._on_ground = True

        # Jump mechanics
        self._can_double_jump = False
        self._has_used_double_jump = False

        # Crouch mechanics (uses stand sprite)
        self._is_crouching = False
        self._crouch_timer = 0.0

        # Attack mechanics
        self._is_attacking = False
        self._attack_timer = 0.0

        # Scoring
        self._score = 0
        self._distance = 0.0

        # Animation system
        self._current_frame = 0
        self._animation_timer = 0.0
        self._animation_speed = 0.1  # seconds per frame

    # === IGameEntity Implementation ===

    def get_position(self) -> Position:
        """Get ninja's current position."""
        return self._position

    def get_bounds(self) -> Bounds:
        """
        Get collision bounds (adjusted for crouching).

        Returns smaller hitbox when crouching for dodging low obstacles.
        """
        height = self.CROUCH_HEIGHT if self._is_crouching else self.HEIGHT
        y_offset = self.HEIGHT - height if self._is_crouching else 0

        return Bounds(
            self._position.x,
            self._position.y + y_offset,
            self.WIDTH,
            height
        )

    def is_active(self) -> bool:
        """Check if ninja is active (alive)."""
        return self._active and self._state != NinjaState.DEAD

    def deactivate(self) -> None:
        """Deactivate ninja (death/game over)."""
        self._active = False
        self._state = NinjaState.DEAD

    # === ICollidable Implementation ===

    def on_collision(self, other: IGameEntity) -> None:
        """
        Handle collision with another entity.

        Collision response handled by game systems (GameManager).
        This method satisfies interface requirements.
        """
        pass

    def can_collide_with(self, other: IGameEntity) -> bool:
        """
        Check if ninja can collide with entity.

        Ninja always collides when active (no invincibility mechanic).
        """
        return self.is_active()

    # === IUpdatable Implementation ===

    def update(self, delta_time: float) -> None:
        """
        Update ninja state each frame.

        Args:
            delta_time: Time elapsed since last frame (seconds)
        """
        self._update_timers(delta_time)
        self._update_state()
        self._update_animation(delta_time)
        self._distance += abs(self._velocity.vx) * delta_time

    def _update_timers(self, delta_time: float) -> None:
        """Update all ability timers."""
        # Attack timer
        if self._is_attacking:
            self._attack_timer += delta_time
            if self._attack_timer >= self.ATTACK_DURATION:
                self._is_attacking = False
                self._attack_timer = 0.0

        # Crouch timer (for minimum duration)
        if self._is_crouching:
            self._crouch_timer += delta_time

    def _update_state(self) -> None:
        """
        Update ninja state based on current conditions.

        State machine implementation following State pattern.
        Priority: Dead > Attacking > Crouching > Jumping > Running > Idle
        """
        if self._state == NinjaState.DEAD:
            return

        # Can't crouch while in air
        if self._is_crouching and not self._on_ground:
            self.stop_crouch()

        # State priority order
        if self._is_attacking:
            self._state = NinjaState.ATTACKING
        elif self._is_crouching:
            self._state = NinjaState.CROUCHING
        elif not self._on_ground:
            self._state = NinjaState.JUMPING
        elif self._on_ground:
            self._state = NinjaState.RUNNING
        else:
            self._state = NinjaState.IDLE

    def _update_animation(self, delta_time: float) -> None:
        """Update animation frame."""
        self._animation_timer += delta_time
        if self._animation_timer >= self._animation_speed:
            self._animation_timer = 0.0
            self._current_frame = (self._current_frame + 1) % 6  # 6 frame cycle

    # === IRenderable Implementation ===

    def get_sprite(self) -> pygame.Surface:
        """
        Get current sprite based on state and animation frame.

        Returns:
            Pygame surface with current animation frame
        """
        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites

        # State-based sprite selection
        if self._state == NinjaState.IDLE:
            return PlaceholderSprites.create_ninja_idle(frame=self._current_frame)

        elif self._state == NinjaState.RUNNING:
            return PlaceholderSprites.create_ninja_run(frame=self._current_frame)

        elif self._state == NinjaState.JUMPING:
            # Special case: second jump uses somersault animation
            if self._has_used_double_jump:
                return PlaceholderSprites.create_ninja_somersault(frame=self._current_frame)
            else:
                return PlaceholderSprites.create_ninja_jump(frame=self._current_frame)

        elif self._state == NinjaState.CROUCHING:
            # Use stand sprite for crouching
            return PlaceholderSprites.create_ninja_crouch(frame=self._current_frame)

        elif self._state == NinjaState.ATTACKING:
            return PlaceholderSprites.create_ninja_attack(frame=self._current_frame)

        else:
            # Fallback
            return PlaceholderSprites.create_ninja_idle(frame=0)

    def get_render_position(self) -> Position:
        """Get position for rendering sprite."""
        return self._position

    def get_render_layer(self) -> int:
        """Get render layer (ninja always in foreground)."""
        return 10

    # === Player Actions ===

    def jump(self) -> bool:
        """
        Execute jump or double jump.

        Returns:
            True if jump executed successfully
        """
        if self._on_ground:
            # Ground jump
            self._velocity = Velocity(self._velocity.vx, self.JUMP_VELOCITY)
            self._state = NinjaState.JUMPING
            self._on_ground = False
            self._can_double_jump = True
            self._has_used_double_jump = False
            return True

        elif self._can_double_jump and not self._has_used_double_jump:
            # Double jump (uses somersault animation)
            self._velocity = Velocity(self._velocity.vx, self.DOUBLE_JUMP_VELOCITY)
            self._has_used_double_jump = True
            return True

        return False

    def start_crouch(self) -> bool:
        """
        Start crouching (uses stand sprite).

        Crouching reduces hitbox and destroys wooden crates on contact.

        Returns:
            True if crouch started successfully
        """
        if self._on_ground and not self._is_crouching:
            self._is_crouching = True
            self._state = NinjaState.CROUCHING
            self._crouch_timer = 0.0
            return True
        return False

    def stop_crouch(self) -> None:
        """Stop crouching."""
        if self._is_crouching and self._crouch_timer >= self.CROUCH_MIN_DURATION:
            self._is_crouching = False
            self._crouch_timer = 0.0

    def start_attack(self) -> bool:
        """
        Execute sword slash attack.

        Destroys wooden crates in front of ninja.

        Returns:
            True if attack started successfully
        """
        if not self._is_attacking:
            self._is_attacking = True
            self._state = NinjaState.ATTACKING
            self._attack_timer = 0.0
            return True
        return False

    # === Combat & Scoring ===

    def add_score(self, points: int) -> None:
        """
        Add points to score.

        Args:
            points: Points to add
        """
        self._score += points

    def kill(self) -> None:
        """Kill ninja (game over)."""
        self._state = NinjaState.DEAD
        self._active = False

    # === Physics System Interface ===

    def set_velocity(self, velocity: Velocity) -> None:
        """Set velocity (called by physics engine)."""
        self._velocity = velocity

    def set_position(self, position: Position) -> None:
        """Set position (called by physics engine)."""
        self._position = position

        # Update ground state
        if position.y >= self._ground_y - self.HEIGHT:
            if not self._on_ground:
                # Just landed
                self._on_ground = True
                self._can_double_jump = False
                self._has_used_double_jump = False

    def set_on_ground(self, on_ground: bool) -> None:
        """
        Set ground state (called by physics engine).

        Args:
            on_ground: True if ninja is on ground
        """
        if on_ground and not self._on_ground:
            # Landing - reset double jump
            self._can_double_jump = False
            self._has_used_double_jump = False

        self._on_ground = on_ground

    # === Public Getters ===

    def get_velocity(self) -> Velocity:
        """Get current velocity."""
        return self._velocity

    def get_state(self) -> NinjaState:
        """Get current state."""
        return self._state

    def is_on_ground(self) -> bool:
        """Check if on ground."""
        return self._on_ground

    def is_crouching(self) -> bool:
        """Check if currently crouching."""
        return self._is_crouching

    def is_attacking(self) -> bool:
        """Check if currently attacking."""
        return self._is_attacking and self._attack_timer < self.ATTACK_DURATION

    def get_score(self) -> int:
        """Get current score."""
        return self._score

    def get_distance(self) -> float:
        """Get distance traveled."""
        return self._distance
