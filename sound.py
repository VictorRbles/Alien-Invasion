import pygame
from pygame import mixer

class SoundEffects:
    """A class to manage sound files in game"""
    
    def __init__(self):
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound("Sounds/Sounds_laser.ogg")
        self.laser_sound.set_volume(1)
        self.sound_track = pygame.mixer.Sound("Sounds/Sounds_music.ogg")
        self.sound_track.set_volume(1)
        self.explosion = pygame.mixer.Sound("Sounds/Sounds_explosion.ogg")
        self.explosion.set_volume(1)


    def play_laser_clip(self):
        """Method to play laser sound effect"""
        self.laser_sound.play()

    def play_music_clip(self):
        """Method to play background sound"""
        self.sound_track.play(-1)

    def play_explosion_clip(self):
        """Method to play explosion sound effect"""
        self.explosion.play()