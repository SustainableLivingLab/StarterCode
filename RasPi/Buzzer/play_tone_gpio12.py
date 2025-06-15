import RPi.GPIO as GPIO
import time

# Pin configuration
BUZZER_PIN = 12  # BCM numbering

# Tone frequencies (Hz)
TONE_FREQS = [262, 294, 330, 349, 392, 440, 494, 523]  # C4, D4, E4, F4, G4, A4, B4, C5

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 440)  # Default to 440Hz


def play_tone(frequency, duration=0.5):
    pwm.ChangeFrequency(frequency)
    pwm.start(50)  # 50% duty cycle
    time.sleep(duration)
    pwm.stop()
    time.sleep(0.05)

try:
    print("Playing tones on GPIO 12...")
    for freq in TONE_FREQS:
        play_tone(freq, 0.4)
    print("Done.")
finally:
    pwm.stop()
    GPIO.cleanup()
