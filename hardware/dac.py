"""DAC output bank: two MCP4728 boards exposed as 8 analog outputs."""

import adafruit_mcp4728

import config

_VREF = {
    "VDD": adafruit_mcp4728.Vref.VDD,
    "INTERNAL": adafruit_mcp4728.Vref.INTERNAL,
}


class DACBank:
    """Writes the 8 analog outputs across two MCP4728 boards.

    Channel index 0-3 -> first board (A,B,C,D), 4-7 -> second board (A,B,C,D).
    Output levels are normalized floats in 0.0 .. 1.0.
    """

    def __init__(self, i2c):
        self._channels = []
        vref = _VREF[config.MCP4728_VREF]
        for address in config.MCP4728_ADDRESSES:
            mcp = adafruit_mcp4728.MCP4728(i2c, address=address)
            for channel in (mcp.channel_a, mcp.channel_b,
                            mcp.channel_c, mcp.channel_d):
                channel.vref = vref
                self._channels.append(channel)

    @property
    def channel_count(self):
        return len(self._channels)

    def write(self, levels):
        """Set all outputs. `levels` is an iterable of floats in 0.0 .. 1.0."""
        for channel, level in zip(self._channels, levels):
            # MCP4728 .value is a 16-bit register (scaled to the 12-bit DAC).
            channel.value = _clamp16(level)

    def all_off(self):
        for channel in self._channels:
            channel.value = 0


def _clamp16(level):
    return max(0, min(65535, int(level * 65535)))