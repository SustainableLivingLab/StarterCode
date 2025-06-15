import os
import sys
import tty
import termios
import select
import time
import statistics
import colorsys
import board
import neopixel
from hx711 import HX711
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1107
from PIL import Image, ImageDraw, ImageFont

# ┌──── WIRING CONNECTIONS ────┐
# HX711 Load Cell Amplifier:
# | Signal      | Wire Color | Grove HX711 Pin | Raspberry Pi Pin | Notes                 |
# | ----------- | ---------- | --------------- | ---------------- | --------------------- |
# | **DOUT**    | White      | `DOUT`          | GPIO **6**       | Data out from HX711   |
# | **PD_SCK**  | Yellow     | `SCK`           | GPIO **5**       | Clock signal          |
# | **VCC**     | Red        | `VCC`           | 3.3V             | Power (safe at 3.3V)  |
# | **GND**     | Black      | `GND`           | GND              | Ground                |
#
# OLED Display (SH1107 128x128):
# | Pin         | Raspberry Pi Pin | Notes                    |
# | ----------- | ---------------- | ------------------------ |
# | **VCC**     | 3.3V             | Power                    |
# | **GND**     | GND              | Ground                   |
# | **SDA**     | GPIO 2 (SDA1)    | I2C Data line            |
# | **SCL**     | GPIO 3 (SCL1)    | I2C Clock line           |
#
# NeoPixel Strip:
# | Pin         | Raspberry Pi Pin | Notes                    |
# | ----------- | ---------------- | ------------------------ |
# | **VCC/5V**  | 5V               | Power (external PSU recommended for >10 LEDs) |
# | **GND**     | GND              | Ground                   |
# | **DIN**     | GPIO **18**      | Data input (PWM capable) |
#
# Load Cell (connects to HX711):
# | Wire Color  | HX711 Terminal | Notes                    |
# | ----------- | -------------- | ------------------------ |
# | **Red**     | E+             | Excitation positive      |
# | **Black**   | E-             | Excitation negative      |
# | **White**   | A-             | Signal negative          |
# | **Green**   | A+             | Signal positive          |

# ┌──── Terminal Setup ────┐
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
tty.setcbreak(fd)

# ┌──── Hardware Setup ────┐
# HX711 Load Cell
hx = HX711(6, 5)  # DOUT = GPIO6, SCK = GPIO5
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(210.0)  # Adjust after calibration
hx.reset()
hx.tare()

# OLED Display (SH1107 with luma.oled)
serial = i2c(port=1, address=0x3C)  # I2C port 1, address 0x3C (detected via i2cdetect)
oled = sh1107(serial, width=128, height=128, rotate=2)  # rotate=2 for 180 degrees

# NeoPixel Strip
NUM_PIXELS = 30
PIXEL_PIN = board.D18
BRIGHTNESS = 0.5
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)

# ┌──── Configuration ─────┐
MAX_WEIGHT = 1000.0  # Maximum weight for color mapping (grams)
MIN_WEIGHT = 0.0     # Minimum weight for color mapping

# ┌──── Functions ─────────┐
def clear_screen():
    os.system("clear")

def average_weight(samples=5):
    return statistics.mean([hx.get_weight(1) for _ in range(samples)])

def key_pressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def print_header():
    clear_screen()
    print("═══════════════════════════════════════")
    print("    Weight Display Demo with NeoPixel")
    print("═══════════════════════════════════════")
    print("Controls:")
    print("  [t] → Tare (zero scale)")
    print("  [c] → Calibrate with known weight")
    print("  [q] → Quit")
    print("═══════════════════════════════════════\n")

def update_oled(weight):
    """Update OLED display with current weight in 7-segment style font"""
    with canvas(oled) as draw:
        # Try to load a 7-segment style font, fall back to monospace if not available
        try:
            # Try 7-segment or digital display font (common locations)
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 28)
        except:
            try:
                # Fall back to a monospace font which looks more digital
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 28)
            except:
                try:
                    # Another monospace option
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 28)
                except:
                    # Use default font if no system fonts available
                    font = ImageFont.load_default()
        
        # Format weight text with one decimal place, use monospace-friendly format
        weight_text = f"{weight:6.1f}g"  # 6 characters wide for consistent spacing
        
        # Get text dimensions for centering
        bbox = draw.textbbox((0, 0), weight_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate center position
        x = (oled.width - text_width) // 2
        y = (oled.height - text_height) // 2
        
        # Draw the weight text centered
        draw.text((x, y), weight_text, font=font, fill="white")

def weight_to_hue(weight):
    """Convert weight to hue value (0-1) for rainbow colors"""
    # Normalize weight to 0-1 range
    normalized = max(0, min(1, (weight - MIN_WEIGHT) / (MAX_WEIGHT - MIN_WEIGHT)))
    # Map to hue (0 = red, 0.33 = green, 0.66 = blue, 1 = red again)
    return normalized * 0.8  # Use 0.8 to avoid wrapping back to red too quickly

def update_neopixels(weight):
    """Update NeoPixel colors based on weight"""
    hue = weight_to_hue(weight)
    
    # Create rainbow effect with weight-based base hue
    for i in range(NUM_PIXELS):
        # Create rainbow by varying hue across pixels
        pixel_hue = (hue + (i / NUM_PIXELS) * 0.3) % 1.0
        rgb = colorsys.hsv_to_rgb(pixel_hue, 1.0, 1.0)
        # Convert to 0-255 range
        color = tuple(int(c * 255) for c in rgb)
        pixels[i] = color
    
    pixels.show()

def show_progress(message, duration=2):
    print(f"{message}", end="", flush=True)
    for _ in range(duration * 2):
        print(".", end="", flush=True)
        time.sleep(0.25)
    print()

# ┌──── Startup ───────────┐
print_header()
update_oled(0.0)

# ┌──── Main Loop ─────────┐
try:
    while True:
        # Read weight
        weight = average_weight()
        
        # Update displays
        print(f"\rWeight: {weight:.2f} g | Hue: {weight_to_hue(weight):.3f}      ", end="", flush=True)
        update_oled(weight)
        update_neopixels(weight)
        
        # Power management for HX711
        hx.power_down()
        hx.power_up()
        time.sleep(0.3)
        
        # Check for keyboard input
        if key_pressed():
            key = sys.stdin.read(1)
            
            if key == 't':
                # Tare operation
                with canvas(oled) as draw:
                    font = ImageFont.load_default()
                    draw.text((30, 50), "Taring...", font=font, fill="white")
                
                pixels.fill((255, 255, 0))  # Yellow during tare
                pixels.show()
                
                show_progress("Taring")
                hx.tare()
                
                print_header()
                
            elif key == 'c':
                # Calibration operation
                with canvas(oled) as draw:
                    font = ImageFont.load_default()
                    draw.text((10, 30), "Calibration", font=font, fill="white")
                    draw.text((15, 50), "Place known", font=font, fill="white")
                    draw.text((15, 70), "weight then", font=font, fill="white")
                    draw.text((15, 90), "press Enter", font=font, fill="white")
                
                pixels.fill((0, 255, 255))  # Cyan during calibration
                pixels.show()
                
                print("\nCalibration Mode:")
                print("1. Place known weight on scale")
                print("2. Press Enter when ready")
                input()
                
                try:
                    known_weight = float(input("Enter known weight in grams: "))
                    
                    with canvas(oled) as draw:
                        font = ImageFont.load_default()
                        draw.text((20, 50), "Calibrating...", font=font, fill="white")
                    
                    show_progress("Calibrating")
                    raw = average_weight()
                    ref_unit = (raw - hx.get_offset()) / known_weight
                    hx.set_reference_unit(ref_unit)
                    
                    print_header()
                    print(f"Calibrated! New reference unit: {ref_unit:.2f}")
                    time.sleep(2)
                    
                except ValueError:
                    print("Invalid weight entered. Calibration cancelled.")
                    time.sleep(2)
                    print_header()
                    
            elif key == 'q':
                print("\nShutting down...")
                break

finally:
    # Cleanup
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    pixels.fill((0, 0, 0))  # Turn off NeoPixels
    pixels.show()
    with canvas(oled) as draw:
        font = ImageFont.load_default()
        draw.text((40, 50), "Goodbye!", font=font, fill="white")
    time.sleep(1)
    oled.cleanup()  # Clear display
    print("\nGoodbye!")