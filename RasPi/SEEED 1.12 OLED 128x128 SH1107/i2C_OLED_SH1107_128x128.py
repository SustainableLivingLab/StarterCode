from grove.factory import Factory
import time

oled = Factory.getDisplay("SH1107G")

oled.clear()
oled.setCursor(0, 0)
oled.write("Hello, OLED!")

oled.setCursor(5, 0)
oled.write("128x128 SH1107")

time.sleep(50)
oled.clear()