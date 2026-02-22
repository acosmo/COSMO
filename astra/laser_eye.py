#!/usr/bin/env python3
"""
IR module for operating the Magcubic HY320 Mini Projector and any IR-controlled projector or TV
Most TVs can be controlled via Tuya smart sockets, but projectors require IR switch
(I've tried using IR Tuya switch, but it haven't worked as I expected, so I opted for my own custom IR switch module)

You will need for 1 USD Infrared Receiver / Transmitter https://www.aliexpress.com/item/1005006385368806.html
see astra folder -> ir_pinout.jpg

pip3 install PiIR
pip3 install isodate
or
python3 -m pip install PiIR isodate --break-system-packages

apt install pigpio python3-pigpio

sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# Record your remote’s IR key combinations (Note current 'light.json' is for Magcubic HY320)
piir record --gpio 17 --file light.json

# Test commands via console
piir play --gpio 18 --file light.json on
piir play --gpio 18 --file light.json left
piir play --gpio 18 --file light.json enter
"""

import subprocess
import time

PIIR_PATH = "/usr/local/bin/piir"  # full path to PiIR binary

# Swith ON Magcubic HY320
subprocess.run([PIIR_PATH, "play", "--gpio", "18", "--file", "light.json", "on"])

# Wait 40 seconds (it takes time to warm-up)
time.sleep(40)

# Select HDMI output
subprocess.run([PIIR_PATH, "play", "--gpio", "18", "--file", "light.json", "left"])
time.sleep(1)
subprocess.run([PIIR_PATH, "play", "--gpio", "18", "--file", "light.json", "ok"])
