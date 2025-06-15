# 🐍 Python Development Setup on Raspberry Pi (Ubuntu, Latest)

This guide covers how to set up a Python development environment on a Raspberry Pi running **Ubuntu 22.04+** for working with:

* I2C Sensors
* OLED Displays (SH1107/SSD1306)
* Cameras
* NeoPixels (WS2812/WS2812B)

---

## ✅ 1. System Preparation

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential i2c-tools git
```

---

## 🧱 2. Enable I2C and Camera Interfaces

### Enable I2C:

```bash
echo "dtparam=i2c_arm=on" | sudo tee -a /boot/firmware/config.txt
sudo reboot
```

After reboot:

```bash
ls /dev/i2c*
i2cdetect -y 1
```

### Enable Camera (for Raspberry Pi Camera Module)

```bash
sudo apt install -y libcamera-apps v4l-utils
```

Test with:

```bash
libcamera-hello
```

---

## 🧪 3. Create and Use a Virtual Environment

```bash
mkdir ~/raspi-dev
cd ~/raspi-dev
python3 -m venv venv
source venv/bin/activate
```

Install core GPIO and helper libraries:

```bash
pip install RPi.GPIO adafruit-blinka
```

---

## 💡 4. I2C Sensors and OLED Displays

### SH1107 OLED (Seeed 1.12"):

```bash
pip install git+https://github.com/Seeed-Studio/grove.py.git
```

#### Example usage:

```python
from grove.factory import Factory
oled = Factory.getDisplay("SH1107G")
oled.setCursor(0, 0)
oled.write("Hello Seeed!")
```

### SSD1306 OLED:

```bash
pip install adafruit-circuitpython-ssd1306 pillow
```

### I2C Sensor Examples:

```bash
pip install adafruit-circuitpython-dht adafruit-circuitpython-busdevice
```

---

## 🌈 5. NeoPixels (WS2812)

```bash
pip install adafruit-circuitpython-neopixel rpi-ws281x
```

To run NeoPixel scripts:

```bash
sudo ./venv/bin/python neopixel_test.py
```

> NeoPixel control requires `sudo` to access low-level PWM/SPI.

---

## 📷 6. Working with Raspberry Pi Camera

Ubuntu 22.04+ uses `libcamera`. To capture an image:

```bash
libcamera-jpeg -o test.jpg
```

For Python use:

```bash
pip install opencv-python
```

Then use `cv2.VideoCapture(0)` to access the camera.

---

## 📦 7. Common Debugging Tools

```bash
sudo apt install -y i2c-tools v4l-utils minicom net-tools
```

---

## 🧹 8. Clean Up and Deactivate

To exit the virtual environment:

```bash
deactivate
```

---

## 📝 Optional Libraries

* `seeed-python-grove` (for Seeed Grove ecosystem)
* `adafruit-circuitpython-display-text` (text rendering for OLEDs)
* `flask`, `socketio` (for web-based control)

---

You're now ready to build Python-based hardware projects on Ubuntu-powered Raspberry Pi!
