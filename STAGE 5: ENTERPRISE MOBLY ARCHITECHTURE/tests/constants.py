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
CALC_BTN_1 = "com.darkempire78.opencalculator:id/oneButton"
CALC_BTN_2 = "com.darkempire78.opencalculator:id/twoButton"
CALC_BTN_3 = "com.darkempire78.opencalculator:id/threeButton"
CALC_BTN_8 = "com.darkempire78.opencalculator:id/eightButton"
CALC_BTN_ADD = "com.darkempire78.opencalculator:id/addButton"
CALC_BTN_EQUAL = "com.darkempire78.opencalculator:id/equalsButton"