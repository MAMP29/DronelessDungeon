# Lista de canciones
import os
import random

import pygame

songs = ['8-bit-dungeon-251388.mp3', 'ruins-168316.mp3', 'ruins-of-huja-291401.mp3', 'waiting-time-175800.mp3']
# Crear una copia para manejar la reproducción no repetitiva
available_songs = songs.copy()
# Variable para controlar si la música está silenciada
is_muted = False
# Volumen original para restaurar después del silencio
original_volume = 0.5  # 50% del volumen


def play_random_song():
    global available_songs
    # Si no quedan canciones disponibles, recargar la lista
    if not available_songs:
        available_songs = songs.copy()

    # Seleccionar una canción aleatoria de las disponibles
    song = random.choice(available_songs)
    available_songs.remove(song)  # Remover para no repetir

    # Cargar y reproducir la canción
    pygame.mixer.music.load(os.path.join('assets/music/', song))
    pygame.mixer.music.set_volume(original_volume)
    pygame.mixer.music.play()

def toggle_mute():
    global is_muted
    if is_muted:
        # Restaurar el volumen
        pygame.mixer.music.set_volume(original_volume)
        is_muted = False
    else:
        # Silenciar la música
        pygame.mixer.music.set_volume(0.0)
        is_muted = True
    return is_muted

def skip_song():
    # Detener la canción actual y reproducir la siguiente
    pygame.mixer.music.stop()
    play_random_song()