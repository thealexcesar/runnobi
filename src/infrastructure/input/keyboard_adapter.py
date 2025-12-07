"""
Keyboard input adapter using Adapter pattern.

Converts pygame keyboard events to game-agnostic InputActions.
Allows easy remapping and future gamepad support without changing game code.
"""
import pygame
from typing import Set

from infrastructure.input import InputAction


class KeyboardAdapter:
    """
    Keyboard input adapter implementing Adapter pattern.

    Converts pygame keyboard input to game-agnostic InputActions.
    Benefits:
    - Easy key remapping
    - Input agnostic game code
    - Future gamepad support possible
    - Cleaner separation of concerns
    """

    # Default key mapping (can be customized)
    DEFAULT_KEY_MAP = {
        # Jump
        pygame.K_SPACE: InputAction.JUMP,
        pygame.K_UP: InputAction.JUMP,
        pygame.K_w: InputAction.JUMP,
        pygame.K_j: InputAction.JUMP,

        # Crouch (uses stand sprite)
        pygame.K_DOWN: InputAction.CROUCH,
        pygame.K_s: InputAction.CROUCH,
        pygame.K_k: InputAction.CROUCH,

        # Attack (sword slash)
        pygame.K_x: InputAction.ATTACK,
        pygame.K_z: InputAction.ATTACK,
        pygame.K_LEFT: InputAction.ATTACK,
        pygame.K_RIGHT: InputAction.ATTACK,

        # Pause
        pygame.K_ESCAPE: InputAction.PAUSE,
        pygame.K_p: InputAction.PAUSE,
    }

    def __init__(self) -> None:
        """Initialize keyboard adapter with default key mapping."""
        self._key_map = self.DEFAULT_KEY_MAP.copy()
        self._pressed_actions: Set[InputAction] = set()
        self._just_pressed_actions: Set[InputAction] = set()

    def update(self) -> None:
        """
        Update input state for current frame.

        Call once per frame before checking actions.
        Clears just_pressed actions from previous frame.
        """
        self._just_pressed_actions.clear()

        # Check currently pressed keys
        pressed_keys = pygame.key.get_pressed()
        current_actions = set()

        for key, action in self._key_map.items():
            if pressed_keys[key]:
                current_actions.add(action)

                # If not in previous frame, it's "just pressed"
                if action not in self._pressed_actions:
                    self._just_pressed_actions.add(action)

        self._pressed_actions = current_actions

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame event for special cases (e.g., window close).

        Args:
            event: Pygame event
        """
        if event.type == pygame.QUIT:
            self._just_pressed_actions.add(InputAction.QUIT)

    def is_action_pressed(self, action: InputAction) -> bool:
        """
        Check if action is currently being held down.

        Use for continuous actions (e.g., holding crouch).

        Args:
            action: Action to check

        Returns:
            True if action is currently pressed
        """
        return action in self._pressed_actions

    def is_action_just_pressed(self, action: InputAction) -> bool:
        """
        Check if action was just pressed this frame.

        Use for single-tap actions (e.g., jump, attack).

        Args:
            action: Action to check

        Returns:
            True if action was pressed this frame (not previous frame)
        """
        return action in self._just_pressed_actions

    def get_just_pressed_actions(self) -> Set[InputAction]:
        """
        Get all actions pressed this frame.

        Returns:
            Set of actions that were just pressed
        """
        return self._just_pressed_actions.copy()
