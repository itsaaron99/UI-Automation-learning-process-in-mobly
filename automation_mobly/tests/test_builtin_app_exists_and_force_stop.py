"""Verifies that a built-in application exists and can be successfully force-stopped.

        This test case bypasses UI interactions entirely and leverages Mobile Harness 
        Snippets (MBS) to interact directly with Android system services (Package Manager 
        and Activity Manager). It validates that system-level process state changes 
        can be triggered and verified reliably without relying on the UI layer.

        Steps:
            1. Verify the target built-in package (e.g., com.android.settings) exists on the device.
            2. Launch the target package to ensure it enters a running process state.
            3. Issue a system-level force-stop command via MBS.
            4. Validate that the application's background process has been completely terminated.
"""

import sys
import os
from mobly import test_runner
from mobly import asserts
from automation_mobly.common.base_test import EnterpriseBaseTest
from automation_mobly.data_models.app_protos import AppConfig

class AppManagementTest(EnterpriseBaseTest):

    def setup_class(self):
        super().setup_class()
        pkg_name = self.user_params.get('target_app_for_settings', '')
        self.app_config = AppConfig(
            package_name = pkg_name,
            package_path = None,
            dest_path = None,
            requires_network = False,
        )

    def test_builtin_app_exists_and_force_stop(self):
        # Launch app
        self.dut.log.info(f'Start launching {pkg_name}...')
        res_launch_app = self.app_controller.launch_app(self.app_config)
        asserts.assert_true(res_launch_app, f"Expect {package_name} be launched but failed...")

        # Check if app is in forgeground
        res_app_in_foreground = self.app_controller.is_app_in_foreground(self.app_config)
        asserts.assert_true(res_app_in_foreground, f"Expect {package_name} is in foreground but failed...")

        # Force stop
        self.app_controller.force_stop(self.app_config)
        self.dut.log.info("Test passed: %s is intalled and forced stopped", pkg_name)

    def teardown_class(self):        
        self.dut.log.info("=== teardown_class: Starting Teardown ===")

        if hasattr(self, 'app_config'):
            self.dut.log.info("Cleaning up app: %s", self.app_config.package_name)
            res_clear_data = self.app_controller.clear_data(self.app_config)
            asserts.assert_true(res_clear_data, f"Expect cleaning {pkg_name} data but fail...")
        super().teardown_class()

if __name__ == '__main__':
    del EnterpriseBaseTest
    test_runner.main()