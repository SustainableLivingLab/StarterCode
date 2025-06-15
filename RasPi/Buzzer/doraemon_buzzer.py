import RPi.GPIO as GPIO
import time
from doraemon import melody, REST, tempo

# --- Buzzer Setup ---
BUZZER_PIN = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 440)

# --- Timing ---
whole_note_duration = (60 / tempo) * 4

def play_tone(frequency, duration_sec):
    if frequency == REST:
        pwm.ChangeDutyCycle(0)
        time.sleep(duration_sec)
    else:
        pwm.ChangeFrequency(frequency)
        pwm.ChangeDutyCycle(50)
        time.sleep(duration_sec)
        pwm.ChangeDutyCycle(0)
        time.sleep(0.02)

try:
    pwm.start(0)
    for note, divider in melody:
        duration = whole_note_duration / abs(divider)
        if divider < 0:
            duration *= 1.5
        play_tone(note, duration * 0.9)
        time.sleep(duration * 0.1)
finally:
    pwm.stop()
    GPIO.cleanup()
