# rhb-gauge-panel

Raspberry Pi Zero 2 W gauge panel controller.

A fixed-rate control loop that reads **8 analog inputs** (2× ADS1115), computes
outputs, and drives **8 analog outputs** (2× MCP4728) plus a **WS2811 LED strip**.

## Hardware

| Part      | Role            | Count | I2C address      | Notes                          |
|-----------|-----------------|-------|------------------|--------------------------------|
| ADS1115   | 4-ch 16-bit ADC | 2     | `0x48`, `0x49`   | Address set by ADDR pin strap  |
| MCP4728   | 4-ch 12-bit DAC | 2     | `0x60`, `0x61`   | 2nd must be re-addressed (LDAC) |
| WS2811    | LED strip       | 1     | — (GPIO18 data)  | Run as root (DMA/PWM)          |

All ADCs and DACs share one I2C bus (SDA=GPIO2, SCL=GPIO3). The LED data line is
on **GPIO18** (`board.D18`).

### Wiring notes

- **ADS1115 addressing:** strap the `ADDR` pin — GND→`0x48`, VDD→`0x49`,
  SDA→`0x4A`, SCL→`0x4B`. Use two distinct addresses.
- **MCP4728 addressing:** both boards ship at `0x60`. To put the second at `0x61`
  you must run the I2C address-change command **while pulsing the `LDAC` pin** —
  it can't be set in software alone. Do this once (a small one-off script, with
  only that board on the bus), then it persists in EEPROM.
- **Input range:** with `ADS1115_GAIN = 1` the full-scale range is ±4.096 V.
  Never exceed VDD + 0.3 V on any analog pin — scale/divide higher-voltage
  sources down first.
- **WS2811 power:** drive the strip from its own 5 V supply with common ground;
  GPIO18 only carries the data signal. A level shifter (3.3 V→5 V) on the data
  line is recommended for reliable signaling.

## Setup

On the Pi:

```bash
# Enable I2C: sudo raspi-config -> Interface Options -> I2C
sudo apt install -y python3-venv i2c-tools
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# Confirm all four I2C devices are present:
i2cdetect -y 1
```

## Run

```bash
sudo .venv/bin/python main.py     # sudo: WS2811 needs DMA/PWM access
```

Ctrl-C stops the loop and zeros all outputs.

## Where the logic goes

The hardware plumbing is complete. Application behavior lives in one function,
`process(inputs)` in `main.py`:

```python
def process(inputs):
    # inputs: list of 8 ADC voltages
    # return (dac_levels, led_colors)
    #   dac_levels: 8 floats 0.0..1.0
    #   led_colors: list of (r, g, b) tuples
    ...
```

The default placeholder echoes each input to its matching DAC channel and shows
a green bar on the LEDs — replace it with your mapping.

Wiring constants (addresses, gain, LED count/order, loop rate) are all in
`config.py`.