"""
Ninja entity - the player character.

Implements all game interfaces and manages player state, abilities,
and interactions with the game world.
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
    Player character entity with full ability set.

    Implements state machine for animations and behavior.
    Manages parkour mechanics (jump, slide, dash) and combat (slash, shuriken).
    """

    # Constants
    WIDTH = 56
    HEIGHT = 84
    SLIDE_HEIGHT = 50

    JUMP_VELOCITY = -900.0
    DOUBLE_JUMP_VELOCITY = -750.0
    DASH_SPEED_MULTIPLIER = 2.5

    DASH_DURATION = 3.0  # seconds
    DASH_COOLDOWN = 10.0  # seconds
    ATTACK_DURATION = 0.3  # seconds
    SLIDE_DURATION = 0.5  # seconds

    MAX_SHURIKEN = 10
    STARTING_SHURIKEN = 3

    def __init__(self, start_x: float, start_y: float, ground_y: float) -> None:
        """
        Initialize ninja at starting position.

        Args:
            start_x: Initial x position
            start_y: Initial y position  
            ground_y: Y coordinate of ground level
        """
        self._position = Position(start_x, start_y)
        self._velocity = Velocity(0.0, 0.0)
        self._ground_y = ground_y

        self._state = NinjaState.IDLE
        self._active = True
        self._on_ground = True

        # Jump mechanics
        self._can_double_jump = False
        self._has_used_double_jump = False

        # Dash mechanics
        self._is_dashing = False
        self._is_invincible = False
        self._dash_timer = 0.0
        self._dash_cooldown_timer = 0.0

        # Attack mechanics
        self._is_attacking = False
        self._attack_timer = 0.0

        # Slide mechanics
        self._is_sliding = False
        self._slide_timer = 0.0

        # Combat
        self._shuriken_count = self.STARTING_SHURIKEN

        # Score
        self._score = 0
        self._distance = 0.0

        # Rendering
        self._sprite_cache: dict = {}
        self._current_frame = 0
        self._animation_timer = 0.0
        self._animation_speed = 0.1  # seconds per frame

    # IGameEntity implementation

    def get_position(self) -> Position:
        """Get ninja's current position."""
        return self._position

    def get_bounds(self) -> Bounds:
        """
        Get ninja's collision bounds.

        Bounds adjust based on state (sliding has reduced height).
        """
        height = self.SLIDE_HEIGHT if self._is_sliding else self.HEIGHT
        return Bounds(
            self._position.x,
            self._position.y,
            self.WIDTH,
            height
        )

    def is_active(self) -> bool:
        """Check if ninja is active."""
        return self._active and self._state != NinjaState.DEAD

    def deactivate(self) -> None:
        """Deactivate ninja (game over)."""
        self._active = False
        self._state = NinjaState.DEAD

    def jump(self) -> bool:
        """
        Execute jump or double jump.

        Returns:
            True if jump executed, False if not possible
        """
        if self._on_ground:
            self._velocity = Velocity(self._velocity.vx, self.JUMP_VELOCITY)
            self._state = NinjaState.JUMPING
            self._on_ground = False
            self._can_double_jump = True
            self._has_used_double_jump = False
            return True
        elif self._can_double_jump and not self._has_used_double_jump:
            self._velocity = Velocity(self._velocity.vx, self.DOUBLE_JUMP_VELOCITY)
            self._has_used_double_jump = True
            return True
        return False

    def start_slide(self) -> bool:
        """
        Start sliding (must be on ground).

        Returns:
            True if slide started, False if not possible
        """
        if self._on_ground and not self._is_sliding:
            self._is_sliding = True
            self._state = NinjaState.SLIDING
            self._slide_timer = 0.0
            offset = self.HEIGHT - self.SLIDE_HEIGHT  # 84 - 50 = 34
            self._position = Position(self._position.x, self._position.y + offset)
            return True
        return False

    def stop_slide(self) -> None:
        """Stop sliding."""
        if self._is_sliding:
            self._is_sliding = False
            offset = self.HEIGHT - self.SLIDE_HEIGHT  # 34
            self._position = Position(self._position.x, self._position.y - offset)

    def start_dash(self) -> bool:
        """
        Activate shadow dash ability.

        Returns:
            True if dash activated, False if on cooldown
        """
        if self._dash_cooldown_timer <= 0.0 and not self._is_dashing:
            self._is_dashing = True
            self._is_invincible = True
            self._state = NinjaState.DASHING
            self._dash_timer = 0.0
            self._dash_cooldown_timer = self.DASH_COOLDOWN
            return True
        return False

    def refill_dash(self) -> None:
        """Refill dash cooldown (from shadow orb pickup)."""
        self._dash_cooldown_timer = 0.0

    def start_attack(self) -> bool:
        """
        Execute katana slash attack.

        Returns:
            True if attack started, False if already attacking
        """
        if not self._is_attacking:
            self._is_attacking = True
            self._state = NinjaState.ATTACKING
            self._attack_timer = 0.0
            return True
        return False

    def add_shuriken(self, amount: int = 1) -> None:
        """
        Add shuriken ammo.

        Args:
            amount: Number of shuriken to add
        """
        self._shuriken_count = min(self._shuriken_count + amount, self.MAX_SHURIKEN)

    def use_shuriken(self) -> bool:
        """
        Use one shuriken (for throwing).

        Returns:
            True if shuriken available, False if out of ammo
        """
        if self._shuriken_count > 0:
            self._shuriken_count -= 1
            return True
        return False

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

    # ICollidable implementation

    def on_collision(self, other: IGameEntity) -> None:
        """
        Handle collision with another entity.

        Args:
            other: The entity this ninja collided with
        """
        # Collision handling will be managed by game systems
        # This is called by collision detector
        pass

    def can_collide_with(self, other: IGameEntity) -> bool:
        """
        Check if ninja can collide with entity.

        Args:
            other: Entity to check collision with

        Returns:
            True if collision should be checked
        """
        # Ninja collides with everything when active and not invincible
        return self.is_active() and not self._is_invincible

    # IUpdatable implementation

    def update(self, delta_time: float) -> None:
        """
        Update ninja state each frame.

        Args:
            delta_time: Time elapsed since last frame (seconds)
        """
        # Update timers
        self._update_timers(delta_time)

        # Update state based on timers
        self._update_state()

        # Update animation
        self._update_animation(delta_time)

        # Update distance traveled
        self._distance += abs(self._velocity.vx) * delta_time

    def _update_timers(self, delta_time: float) -> None:
        """Update all ability timers."""
        # Dash timer
        if self._is_dashing:
            self._dash_timer += delta_time
            if self._dash_timer >= self.DASH_DURATION:
                self._is_dashing = False
                self._is_invincible = False

        # Dash cooldown
        if self._dash_cooldown_timer > 0.0:
            self._dash_cooldown_timer -= delta_time

        # Attack timer
        if self._is_attacking:
            self._attack_timer += delta_time
            if self._attack_timer >= self.ATTACK_DURATION:
                self._is_attacking = False

        # # Slide timer
        # if self._is_sliding:
        #     self._slide_timer += delta_time
        #     if self._slide_timer >= self.SLIDE_DURATION:
        #         self._is_sliding = False

    def _update_state(self) -> None:
        if self._state == NinjaState.DEAD:
            return

        if self._is_sliding and not self._on_ground:
            self.stop_slide()

        if self._is_dashing:
            self._state = NinjaState.DASHING
        elif self._is_attacking:
            self._state = NinjaState.ATTACKING
        elif self._is_sliding:
            self._state = NinjaState.SLIDING
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
            self._current_frame = (self._current_frame + 1) % 4  # 4 frame cycle

    def set_velocity(self, velocity: Velocity) -> None:
        """
        Set ninja velocity (called by physics engine).

        Args:
            velocity: New velocity
        """
        self._velocity = velocity

    def set_position(self, position: Position) -> None:
        """
        Set ninja position (called by physics engine).

        Args:
            position: New position
        """
        self._position = position

        # Check if on ground
        if position.y >= self._ground_y - self.HEIGHT:
            if not self._on_ground:
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
            # Just landed
            self._can_double_jump = False
            self._has_used_double_jump = False
        self._on_ground = on_ground

    # IRenderable implementation

    def get_sprite(self) -> pygame.Surface:
        """
        Get current sprite based on state.

        Returns:
            Sprite surface to render
        """
        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites

        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites

        if self._state == NinjaState.IDLE:
            return PlaceholderSprites.create_ninja_idle(frame=self._current_frame)
        elif self._state == NinjaState.RUNNING:
            return PlaceholderSprites.create_ninja_run(frame=self._current_frame)
        elif self._state == NinjaState.JUMPING:
            return PlaceholderSprites.create_ninja_jump(
                frame=self._current_frame,
                is_double_jump=self._has_used_double_jump
            )
        elif self._state == NinjaState.SLIDING:
            return PlaceholderSprites.create_ninja_slide(frame=self._current_frame)
        elif self._state == NinjaState.ATTACKING:
            return PlaceholderSprites.create_ninja_attack(frame=self._current_frame)
        elif self._state == NinjaState.DASHING:
            return PlaceholderSprites.create_ninja_dash(frame=self._current_frame)
        else:
            return PlaceholderSprites.create_ninja_idle(frame=0)

    def get_render_position(self) -> Position:
        """
        Get position for rendering.

        Returns:
            Position where sprite should be drawn
        """
        return self._position

    def get_render_layer(self) -> int:
        """
        Get render layer (ninja is always in foreground).

        Returns:
            Layer 10 (high priority)
        """
        return 10

    # Public getters for game systems

    def get_velocity(self) -> Velocity:
        """Get current velocity."""
        return self._velocity

    def get_state(self) -> NinjaState:
        """Get current state."""
        return self._state

    def is_on_ground(self) -> bool:
        """Check if on ground."""
        return self._on_ground

    def is_invincible(self) -> bool:
        """Check if invincible (during dash)."""
        return self._is_invincible

    def get_shuriken_count(self) -> int:
        """Get current shuriken ammo."""
        return self._shuriken_count

    def get_score(self) -> int:
        """Get current score."""
        return self._score

    def get_distance(self) -> float:
        """Get distance traveled."""
        return self._distance

    def get_dash_cooldown_remaining(self) -> float:
        """Get remaining dash cooldown time."""
        return max(0.0, self._dash_cooldown_timer)
