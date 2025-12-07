"""
Audio manager for music and sound effects.

Handles loading and playing background music and SFX.
"""
import pygame
from pathlib import Path
from typing import Optional


class AudioManager:
    """
    Centralized audio system.
    
    Manages background music and sound effects with volume control.
    """

    def __init__(self):
        """Initialize pygame mixer and load audio files."""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Volume settings
        self.music_volume = 0.4
        self.sfx_volume = 0.6

        # Base path (project root) - works on Windows and Linux
        self.base_path = Path(__file__).parent.parent.parent.parent

        # Music tracks
        self.music_tracks = {
            'menu': str(self.base_path / 'assets' / 'sounds' / 'music' / 'menu.mp3'),
            'game': str(self.base_path / 'assets' / 'sounds' / 'music' / 'game.mp3'),
            'game_over': str(self.base_path / 'assets' / 'sounds' / 'music' / 'game-over.mp3')
        }
        
        # Sound effects
        self.sfx = {}
        self._load_sfx()
        
        # Current track
        self.current_track: Optional[str] = None

    def _load_sfx(self) -> None:
        """Load all sound effects into memory."""
        sfx_files = {
            'jump': str(self.base_path / 'assets' / 'sounds' / 'sfx' / 'jump.mp3'),
            'attack': str(self.base_path / 'assets' / 'sounds' / 'sfx' / 'attack.wav'),
            'stand': str(self.base_path / 'assets' / 'sounds' / 'sfx' / 'stand.wav')
        }

        for name, path in sfx_files.items():
            try:
                if Path(path).exists():
                    self.sfx[name] = pygame.mixer.Sound(path)
                    self.sfx[name].set_volume(self.sfx_volume)
                else:
                    print(f"SFX not found: {path}")
            except Exception as e:
                print(f"Failed to load SFX {name}: {e}")
    
    def play_music(self, track_name: str, loop: bool = True) -> None:
        """
        Play background music track.
        
        Args:
            track_name: Track identifier ('menu', 'game', 'game_over')
            loop: Whether to loop the music
        """
        if track_name == self.current_track and pygame.mixer.music.get_busy():
            return
        
        track_path = self.music_tracks.get(track_name)
        if not track_path:
            print(f"Music track not found: {track_name}")
            return
        
        if not Path(track_path).exists():
            print(f"Music file not found: {track_path}")
            return
        
        try:
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_track = track_name
        except Exception as e:
            print(f"Failed to play music {track_name}: {e}")
    
    def stop_music(self) -> None:
        """Stop background music."""
        pygame.mixer.music.stop()
        self.current_track = None
    
    def play_sfx(self, sfx_name: str) -> None:
        """
        Play sound effect.
        
        Args:
            sfx_name: SFX identifier ('jump', 'attack', 'stand')
        """
        if sfx_name in self.sfx:
            self.sfx[sfx_name].play()
    
    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume: float) -> None:
        """Set SFX volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sfx.values():
            sound.set_volume(self.sfx_volume)
