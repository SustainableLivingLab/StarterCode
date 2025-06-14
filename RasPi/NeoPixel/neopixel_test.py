import time
import board
import neopixel

# Configuration
NUM_PIXELS = 30         # Change this to match your NeoPixel count
PIXEL_PIN = board.D18  # GPIO18 is PWM-capable and commonly used
BRIGHTNESS = 0.5       # From 0.0 (off) to 1.0 (max)
ORDER = neopixel.GRB   # NeoPixel color order

# Initialize NeoPixel strip
pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER
)

def color_wipe(color, wait):
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

try:
    print("Testing NeoPixels...")
    while True:
        color_wipe((255, 0, 0), 0.1)  # Red
        color_wipe((0, 255, 0), 0.1)  # Green
        color_wipe((0, 0, 255), 0.1)  # Blue
        color_wipe((255, 255, 255), 0.1)  # White
        pixels.fill((0, 0, 0))  # Turn off
        pixels.show()
        time.sleep(1)
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    print("Stopped.")
