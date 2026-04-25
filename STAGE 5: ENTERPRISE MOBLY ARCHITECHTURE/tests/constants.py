"""
Constants for test scripts.

This module holds shared constant values used across different test cases,
such as UI element IDs, coordinates, and default timeouts.
"""

# Expect calculation result
EXP_RESULT = '50'

# Default wait time in seconds for UI to stabilize after an action.
UI_DEFAULT_WAIT_SEC_1 = 1
UI_DEFAULT_WAIT_SEC_3 = 3
UI_DEFAULT_WAIT_SEC_5 = 5

# Resource ID for the calculator's result display.
CALC_RES_ID_RESULT = "com.darkempire78.opencalculator:id/input"

# UI coordinates for calculator buttons.
# IMPORTANT: These are placeholder values and must be adjusted for your specific
# emulator screen resolution.
PIXEL_6_CALC_COORDS = {
    '1': (155, 1927), 
    '2': (410, 1930), 
    '3': (666, 1928),
    '+': (915, 1906), 
    '8': (405, 1385), 
    '=': (915, 2194),
}
