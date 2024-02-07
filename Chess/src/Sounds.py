import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

    def load_sound(self, sound_file):
        sound_path = os.path.join(f"{os.getcwd()}/sounds/", sound_file)
        return pygame.mixer.Sound(sound_path)

    def play_sound(self, sound):
        sound.play()
        pygame.time.delay(self.get_sound_duration(sound))

    def play_music(self, music_file, loops=-1, volume=1.0):
        music_path = f"{os.getcwd()}/sounds/{music_file}"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def get_sound_duration(self, sound):
        return sound.get_length() * 1000
