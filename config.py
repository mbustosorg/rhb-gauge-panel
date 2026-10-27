"""Hardware configuration for the gauge panel.

All wiring-dependent constants live here so the rest of the code never hard-codes
an address or a pin. Adjust these to match your board.
"""

import board

# --- I2C bus ---------------------------------------------------------------
# Enable with `sudo raspi-config` -> Interface Options -> I2C, then verify the
# devices show up with `i2cdetect -y 1`.
I2C_FREQUENCY = 400_000  # 400 kHz fast-mode; drop to 100_000 if the bus is flaky

# --- ADS1115 ADCs (inputs) -------------------------------------------------
# Two boards => 8 single-ended channels. The address is set by the ADDR pin:
#   ADDR -> GND = 0x48, ADDR -> VDD = 0x49, ADDR -> SDA = 0x4A, ADDR -> SCL = 0x4B
ADS1115_ADDRESSES = (0x48, 0x49)

# Gain selects the full-scale input range. 1 => +/-4.096 V.
# Use 2/3 for 0-6.144 V inputs. Must not exceed VDD + 0.3 V on any pin.
ADS1115_GAIN = 1

# --- MCP4728 DACs (outputs) ------------------------------------------------
# Default address is 0x60. The SECOND board must be re-addressed to 0x61 using
# the LDAC-pin address-change sequence (see README) before this will work.
MCP4728_ADDRESSES = (0x60, 0x61)

# Reference / gain for every DAC channel:
#   "VDD"      -> 0 .. VDD (e.g. 3.3 V), unbuffered
#   "INTERNAL" -> internal 2.048 V reference (x1 gain) or 4.096 V (x2 gain)
MCP4728_VREF = "VDD"

# --- WS2811 LED strip (output) ---------------------------------------------
# Data line must be on a PWM/PCM/SPI-capable pin. D18 (GPIO18, PWM0) is the
# usual choice and requires running the program with sudo.
LED_PIN = board.D18
LED_COUNT = 50
LED_BRIGHTNESS = 0.3  # 0.0 .. 1.0, scales every pixel

# WS2811 chips are commonly wired RGB; WS2812 are GRB. Wrong order = swapped
# colors, so flip this if red/green look reversed.
LED_ORDER = "RGB"

# --- Main loop -------------------------------------------------------------
LOOP_HZ = 50  # target control-loop rate