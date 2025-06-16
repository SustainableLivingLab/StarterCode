import time
import numpy as np
import pygame

SAMPLE_RATE = 44100
VOLUME = 0.5

def play_tone(frequency, duration_sec):
    if frequency <= 0 or duration_sec <= 0:
        return
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), False)
    wave = np.sin(frequency * 2 * np.pi * t)
    audio = np.ascontiguousarray((wave * 32767 * VOLUME).astype(np.int16))
    sound = pygame.sndarray.make_sound(audio)
    sound.play()
    time.sleep(duration_sec)

if __name__ == "__main__":
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
    try:
        freq = 440  # Hz (A4)
        duration = 2.0  # seconds
        print(f"Playing {freq} Hz for {duration} seconds through 3.5mm jack...")
        play_tone(freq, duration)
    finally:
        pygame.mixer.quit()
