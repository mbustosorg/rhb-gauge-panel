"""Hardware abstraction layer for the gauge panel.

Each module wraps one class of device behind a small, list-oriented API so the
main loop deals in plain Python numbers (8 input voltages in, 8 output levels
out) and never touches device registers directly.
"""