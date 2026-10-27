"""Gauge panel controller for Raspberry Pi Zero 2 W.

Reads 8 analog inputs (2x ADS1115), computes outputs, and drives 8 analog
outputs (2x MCP4728) plus a WS2811 LED strip — at a fixed loop rate.

The hardware plumbing is complete; put your application logic in process().

Run with sudo (the WS2811 driver needs DMA/PWM access):

    sudo .venv/bin/python main.py
"""

import time

import board
import busio

import config
from hardware.adc import ADCBank
from hardware.dac import DACBank
from hardware.leds import LEDStrip


def process(inputs):
    """Map the 8 input voltages to outputs. <-- YOUR LOGIC GOES HERE.

    Args:
        inputs: list of 8 floats, the ADC channel voltages (volts).

    Returns:
        (dac_levels, led_colors)
        dac_levels: list of 8 floats in 0.0 .. 1.0, one per DAC channel.
        led_colors: list of (r, g, b) tuples (0-255) for the LED strip.

    The placeholder below just echoes each input onto its matching DAC channel
    (scaled by the ADC full-scale range) and lights the first 8 LEDs with a
    green bar proportional to each input. Replace it.
    """
    full_scale = 4.096  # volts, for ADS1115_GAIN == 1
    dac_levels = [max(0.0, min(1.0, v / full_scale)) for v in inputs]
    led_colors = [(0, int(level * 255), 0) for level in dac_levels]
    return dac_levels, led_colors


def main():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=config.I2C_FREQUENCY)

    adc = ADCBank(i2c)
    dac = DACBank(i2c)
    leds = LEDStrip()

    period = 1.0 / config.LOOP_HZ
    print(f"Running: {adc.channel_count} inputs -> {dac.channel_count} outputs "
          f"+ {leds.count} LEDs at {config.LOOP_HZ} Hz. Ctrl-C to stop.")

    try:
        while True:
            start = time.monotonic()

            inputs = adc.read_voltages()
            dac_levels, led_colors = process(inputs)
            dac.write(dac_levels)
            leds.set_colors(led_colors)

            elapsed = time.monotonic() - start
            if elapsed < period:
                time.sleep(period - elapsed)
    except KeyboardInterrupt:
        print("\nStopping; zeroing outputs.")
    finally:
        dac.all_off()
        leds.off()


if __name__ == "__main__":
    main()