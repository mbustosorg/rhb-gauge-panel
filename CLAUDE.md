# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A control program for a Raspberry Pi Zero 2 W gauge panel. It runs a fixed-rate
loop that reads 8 analog inputs, computes outputs, and drives 8 analog outputs
plus a WS2811 LED strip.

Hardware:
- **2x ADS1115** (4-ch 16-bit I2C ADC) -> 8 analog inputs, at I2C `0x48` / `0x49`
- **2x MCP4728** (4-ch 12-bit I2C DAC) -> 8 analog outputs, at I2C `0x60` / `0x61`
- **WS2811** addressable LED strip on the data pin `board.D18` (GPIO18)

Built on the **Adafruit CircuitPython + Blinka** stack.

## Architecture

- `main.py` — entry point and the control loop. The loop is pure plumbing:
  `read inputs -> process() -> write outputs + LEDs`, paced to `config.LOOP_HZ`.
  **`process(inputs)` is the single stub for application logic** — it takes the 8
  input voltages and returns `(dac_levels, led_colors)`. Everything else is done.
- `config.py` — all wiring-dependent constants (I2C addresses, gain/vref, LED
  pin/count/order, loop rate). Nothing else hard-codes an address or pin.
- `hardware/` — one wrapper class per device class, each exposing a small
  list-oriented API so the loop deals in plain numbers, never registers:
  - `adc.ADCBank.read_voltages()` -> 8 floats (volts). Index 0-3 = first ADS1115.
  - `dac.DACBank.write(levels)` — 8 floats in `0.0..1.0`. Index 0-3 = first MCP4728.
  - `leds.LEDStrip.set_colors(colors)` — list of `(r,g,b)` tuples, buffered + shown.

To change behavior, edit `process()`. To change wiring, edit `config.py`. The
`hardware/` wrappers only change if you add/replace a device.

## Running

Requires `sudo` — the WS2811 driver (`rpi_ws281x`) needs DMA/PWM access:

```bash
sudo .venv/bin/python main.py
```

## Gotchas

- **This code only runs on the Pi.** `board`/`busio` (Blinka) are not installable
  on macOS, so imports show as unresolved when editing off-device. That's expected.
- **The second MCP4728 must be re-addressed to `0x61`** before use. Out of the box
  both DACs answer at `0x60`; the address change requires the LDAC-pin sequence
  (see README). The ADS1115 address, by contrast, is just strapped via the ADDR pin.
- **WS2811 vs WS2812 color order** differs (RGB vs GRB). If red/green look swapped,
  flip `config.LED_ORDER`.
- I2C must be enabled (`raspi-config`); verify all four devices with `i2cdetect -y 1`.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```