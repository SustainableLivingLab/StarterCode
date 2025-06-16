import time
import numpy as np
import pygame
from doraemon import melody, REST, tempo

# --- Constants ---
SAMPLE_RATE = 44100
VOLUME = 0.5
whole_note_duration = (60 / tempo) * 4

# pygame.mixer.init() will be called in the main execution block

def play_tone(frequency, duration_sec):
    if frequency == REST:
        time.sleep(duration_sec)
        return
    
    if duration_sec <= 0: # Prevent issues with zero or negative duration
        return

    num_samples = int(SAMPLE_RATE * duration_sec)
    if num_samples == 0: # If duration is too short for any samples
        time.sleep(duration_sec) # Still respect the intended rest duration
        return

    t = np.linspace(0, duration_sec, num_samples, False)
    wave = np.sin(frequency * 2 * np.pi * t)
    audio = np.ascontiguousarray((wave * 32767 * VOLUME).astype(np.int16))
    sound = pygame.sndarray.make_sound(audio)
    sound.play() # Play the sound once
    time.sleep(duration_sec) # Allow the sound to play for its duration

def play_melody():
    print("Playing Doraemon theme song... Press Ctrl+C to stop")
    try:
        while True:
            for note, divider in melody:
                duration = whole_note_duration / abs(divider)
                if divider < 0: # Dotted note
                    duration *= 1.5
            
                # Play the note for 90% of its duration
                play_tone(note, duration * 0.9)
                # Rest for the remaining 10% (staccato effect)
                time.sleep(duration * 0.1)
            time.sleep(10) # Pause 10 seconds before repeating
            
    except KeyboardInterrupt:
        print("\nPlayback stopped by user.")

if __name__ == "__main__":
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
    try:
        play_melody()
    finally:
        pygame.mixer.quit()