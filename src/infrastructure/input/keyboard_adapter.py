"""
Keyboard input adapter.

Adapter pattern: converts pygame keyboard events to game actions.
"""
import pygame
from typing import Set
from .input_actions import InputAction


class KeyboardAdapter:
    """
    Keyboard input adapter using Adapter pattern.

    Converts pygame keyboard input to game-agnostic InputActions.
    Allows easy remapping and future gamepad support.
    """

    # Default key mapping
    DEFAULT_KEY_MAP = {
        pygame.K_SPACE: InputAction.JUMP,
        pygame.K_UP: InputAction.JUMP,
        pygame.K_w: InputAction.JUMP,

        pygame.K_DOWN: InputAction.SLIDE,
        pygame.K_s: InputAction.SLIDE,

        pygame.K_LSHIFT: InputAction.DASH,
        pygame.K_RSHIFT: InputAction.DASH,

        pygame.K_x: InputAction.ATTACK,
        pygame.K_z: InputAction.ATTACK,

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
        Update input state.

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
        Handle pygame event for special cases.

        Args:
            event: Pygame event
        """
        if event.type == pygame.QUIT:
            self._just_pressed_actions.add(InputAction.QUIT)

    def is_action_pressed(self, action: InputAction) -> bool:
        """
        Check if action is currently being held down.

        Args:
            action: Action to check

        Returns:
            True if action is currently pressed
        """
        return action in self._pressed_actions

    def is_action_just_pressed(self, action: InputAction) -> bool:
        """
        Check if action was just pressed this frame.

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
