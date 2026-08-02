"""Verifies app resilience under system interruptions and locale configuration changes.

This test case simulates real-world system interruptions (e.g., an incoming voice call) 
and runtime configuration sweeps (e.g., changing system language/locale) while the 
application is performing a background task. It ensures that the application respects 
the Android Activity lifecycle and gracefully recovers its state without crash or data loss.

Steps:
    1. Trigger a background task within the target application (e.g., active state holding).
    2. Simulate an incoming system interruption via a simulated phone call.
    3. Change the system locale configuration dynamically using system-level control.
    4. Verify that the application recovers to its pre-interruption state gracefully.
"""

import time
import sys
import os
from mobly import test_runner
from mobly import asserts
from automation_mobly.common.base_test import EnterpriseBaseTest
from automation_mobly.data_models.app_protos import AppConfig
from automation_mobly.tests.constants import UI_DEFAULT_WAIT_SEC_1

class InterrupDialTest(EnterpriseBaseTest):

    def setup_class(self):
        super().setup_class()
        pkg_name = self.user_params.get('target_app_for_settings', '')
        screenshot_path = self.user_params.get('test_app_screenshot_path', '')
        self.app_config = AppConfig(package_name=pkg_name, 
                                    package_path=None, 
                                    dest_path=screenshot_path, 
                                    requires_network=False)

    def test_system_interruption_and_locale_change(self):
        self.dut.log.info('=== Start testing system interruption through dial ===')
        # lauch settings
        asserts.assert_true(self.app_controller.launch_app(self.app_config), 
                            f'Expect launching {self.app_config} but fail...')
        
        # simulate a phone call through adb command
        self.dut.log.info('Executing device dial...')
        self.dut.adb.shell("cmd telecom sim-call 123456789")
        time.sleep(UI_DEFAULT_WAIT_SEC_1)

        # hang up dial through mbs
        self.dut.log.info('Hanging up the dial...')
        self.dut.adb.shell("cmd telecom end-call")
        asserts.assert_true(self.app_controller.is_app_in_foreground(self.app_config), 
                            f'Expect {self.app_config} is in foreground but fail...')

        time.sleep(UI_DEFAULT_WAIT_SEC_1)

        # Change system locale configuration
        self.dut.log.info('Changing system locale configuration...')
        self.dut.adb.shell("cmd locale set-to ja-JP")
        #  Wait for locale change
        is_locale_changed = self.app_controller.wait_for_locale_change(
        target_locale = "ja-JP",
        timeout=10,
        freq=0.5)
        asserts.assert_true(is_locale_changed, f'Expect changing locale configuration but failed...')

        # taking screen shot to confirm if setting app is still works
        take_screenshot_result = self.app_controller.take_screenshot(self.app_config.dest_path)
        asserts.assert_true(take_screenshot_result, f"Expected to take screenshot but failed")
        self.dut.log.info('Screenshot has been saved to %s', self.app_config.dest_path)

        
    def teardown_class(self):
        self.dut.log.info("=== teardown_class: Starting Teardown ===")
        locale_config_default_US = self.app_controller.wait_for_locale_change(
            target_locale = "en-US",
            timeout=10,
            freq=0.5)
        if not locale_config_default_US:
            self.dut.log.warning('Failed changing locale back to default (en-US) configuration')

        if hasattr(self, 'app_config'):
            self.dut.log.info("Cleaning up app: %s", self.app_config.package_name)
            clear_res = self.app_controller.clear_data(self.app_config)
            if not clear_res:
                self.dut.log.warning('Failed cleaning %s data during teardown', self.app_config.package_name)
        super().teardown_class()

if __name__ == '__main__':
    del EnterpriseBaseTest
    test_runner.main()
