import os
import sys
import tty
import termios
import select
import time
import statistics
from hx711 import HX711

# ┌──── Terminal Setup ────┐
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
tty.setcbreak(fd)

# ┌──── HX711 Setup ───────┐
hx = HX711(6, 5)  # DOUT = GPIO6, SCK = GPIO5
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(210.0)  # Adjust after calibration
hx.reset()
hx.tare()

# ┌──── Functions ─────────┐
def clear_screen():
    os.system("clear")

def average_weight(samples=10):
    return statistics.mean([hx.get_weight(1) for _ in range(samples)])

def key_pressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def print_header():
    clear_screen()
    print("HX711 ready. Press:")
    print("  [t] → Tare")
    print("  [c] → Calibrate with known weight")
    print("  [q] → Quit\n")

def show_progress(message, duration=2):
    print(f"{message}", end="", flush=True)
    for _ in range(duration * 2):  # prints over ~2s
        print(".", end="", flush=True)
        time.sleep(0.25)
    print()

# ┌──── Startup UI ────────┐
print_header()

# ┌──── Main Loop ─────────┐
try:
    while True:
        weight = average_weight()
        print(f"\rWeight: {weight:.2f} g      ", end="", flush=True)

        hx.power_down()
        hx.power_up()
        time.sleep(0.5)

        if key_pressed():
            key = sys.stdin.read(1)
            if key == 't':
                show_progress("Taring")
                hx.tare()
                print_header()
            elif key == 'c':
                print("\nPlace known weight and press Enter.")
                input()
                known_weight = float(input("Enter known weight in grams: "))
                show_progress("Calibrating")
                raw = average_weight()
                ref_unit = (raw - hx.get_offset()) / known_weight
                hx.set_reference_unit(ref_unit)
                print_header()
                print(f"Calibrated. New reference unit: {ref_unit:.2f}")
            elif key == 'q':
                print("\nExiting.")
                break

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print("\nGoodbye!")
