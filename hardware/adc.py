"""ADC input bank: two ADS1115 boards exposed as 8 single-ended channels."""

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import config

# The four single-ended inputs on each ADS1115, in channel order.
_PINS = (ADS.P0, ADS.P1, ADS.P2, ADS.P3)


class ADCBank:
    """Reads the 8 analog inputs across two ADS1115 boards.

    Channel index 0-3 -> first board, 4-7 -> second board.
    """

    def __init__(self, i2c):
        self._inputs = []
        for address in config.ADS1115_ADDRESSES:
            ads = ADS.ADS1115(i2c, address=address)
            ads.gain = config.ADS1115_GAIN
            for pin in _PINS:
                self._inputs.append(AnalogIn(ads, pin))

    @property
    def channel_count(self):
        return len(self._inputs)

    def read_voltages(self):
        """Return all channels as a list of floats in volts."""
        return [chan.voltage for chan in self._inputs]

    def read_raw(self):
        """Return all channels as signed 16-bit ADC counts."""
        return [chan.value for chan in self._inputs]