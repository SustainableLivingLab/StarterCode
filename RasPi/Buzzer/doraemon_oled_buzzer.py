import RPi.GPIO as GPIO
import time
from doreamon import melody

# --- Buzzer Setup ---
BUZZER_PIN = 12  # BCM numbering
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 440)

tempo = 120  # BPM
whole_note_duration = (60 / tempo) * 4  # in seconds

try:
    pwm.start(50)
    for freq, divider in melody:
        if freq == 0:
            pwm.ChangeDutyCycle(0)  # Rest
        else:
            pwm.ChangeFrequency(freq)
            pwm.ChangeDutyCycle(50)
        duration = whole_note_duration / abs(divider)
        time.sleep(duration)
    pwm.stop()
finally:
    GPIO.cleanup()
