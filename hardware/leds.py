"""WS2811 LED strip wrapper."""

import neopixel

import config

_ORDER = {"RGB": neopixel.RGB, "GRB": neopixel.GRB,
          "RGBW": neopixel.RGBW, "GRBW": neopixel.GRBW}


class LEDStrip:
    """Thin wrapper over a NeoPixel strip with buffered writes.

    Colors are (r, g, b) tuples, each component 0-255.
    """

    def __init__(self):
        self._pixels = neopixel.NeoPixel(
            config.LED_PIN,
            config.LED_COUNT,
            brightness=config.LED_BRIGHTNESS,
            auto_write=False,  # batch updates; call show() once per frame
            pixel_order=_ORDER[config.LED_ORDER],
        )

    @property
    def count(self):
        return config.LED_COUNT

    def set_colors(self, colors):
        """Set the whole strip from a list of (r, g, b) tuples, then show."""
        for i, color in enumerate(colors):
            if i >= config.LED_COUNT:
                break
            self._pixels[i] = color
        self._pixels.show()

    def off(self):
        self._pixels.fill((0, 0, 0))
        self._pixels.show()