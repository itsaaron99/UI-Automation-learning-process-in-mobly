"""
Constants for test scripts.

This module holds shared constant values used across different test cases,
such as UI element IDs, coordinates, and default timeouts.
"""
# Expect calculation result
EXP_RESULT = '50'
RESET_RESULT = ''

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
CALC_BTN_DEL = "com.darkempire78.opencalculator:id/backspaceButton"

# === Google Chrome Constants ===
CHROME_PKG_NAME = "com.android.chrome"
#home page
CHROME_ID_SEARCH_BOX = "com.android.chrome:id/search_box_text"
#url bar
CHROME_ID_URL_BAR = "com.android.chrome:id/url_bar"
CHROME_OFFLINE_TEXT = "You are offline"
CHROME_ERROR_CODE = "ERR_INTERNET_DISCONNECTED"
# Additional test data
# List with tuples
ADDITION_TEST_DATA = [
    (CALC_BTN_1, CALC_BTN_2, "3"),
    (CALC_BTN_3, CALC_BTN_8, "11"),
    (CALC_BTN_8, CALC_BTN_2, "10"),
]
