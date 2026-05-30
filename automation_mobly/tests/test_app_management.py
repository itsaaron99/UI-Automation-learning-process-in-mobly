"""
Execution:
install -> launch app -> get app version -> take screen shot
-> clear_data
"""

import sys
import os

sys.path.insert(0, os.getcwd())
from mobly import test_runner
from mobly import asserts
from common.base_test import EnterpriseBaseTest
from data_models.app_protos import AppConfig

class AppManagementTest(EnterpriseBaseTest):

    def setup_test(self):
        """
        An object collects apps which needed to be cleanned up,
        will call by teardown_test()
        """
        self.apps_to_cleanup = []

    def test_launch_app_from_install_to_uninstall(self):
        pkg_name = self.user_params.get('target_app_pkg', '')
        pkg_path = self.user_params.get('test_app_path', '')
        dest_path = self.user_params.get('test_app_screenshot_path')
        app_config = AppConfig(package_name=pkg_name, package_path=pkg_path, dest_path=dest_path)
        
        # Install process: Check if installed first. If not, then execute install
        if not self.app_controller.is_installed(app_config):
            install_result = self.app_controller.install(app_config)
            asserts.assert_true(install_result, f"Expected app {pkg_name} to be installed, but failed")

        # Add app_config into the cleanup list for tear down test
        self.apps_to_cleanup.append(app_config)
        
        self.dut.log.info("App exists and is installed successfully!")

        # launch app
        if not self.app_controller.is_app_in_foreground(app_config):
            launch_result = self.app_controller.launch_app(app_config)
            asserts.assert_true(launch_result, f"Expected app {pkg_name} to be launched, but failed")

        self.dut.log.info("App launched successfully!")

        # get app version
        get_app_version_result = self.app_controller.get_app_version(app_config)
        asserts.assert_is_not_none(get_app_version_result, f"Expected to get {pkg_name} version, but failed")
        self.dut.log.info("App version: %s", get_app_version_result)
            
        # take screen shot
        take_screenshot_result = self.app_controller.take_screenshot(dest_path)
        asserts.assert_true(take_screenshot_result, f"Expected to take screenshot to {dest_path}, but failed")
        self.dut.log.info("Screenshot has been saved to %s", dest_path)

    def teardown_test(self):
        if not self.apps_to_cleanup:
            return None
        
        self.dut.log.info("Starting teardown process...")
        for cleanup in self.apps_to_cleanup:
            self.dut.log.info("Cleaning up app: %s", cleanup.package_name)
            self.app_controller.clear_data(cleanup)
            uninstall_result = self.app_controller.uninstall(cleanup)
            
            if not uninstall_result:
                self.dut.log.warning("Failed to uninstall %s during teardown.", cleanup.package_name)

if __name__ == '__main__':
    del EnterpriseBaseTest
    test_runner.main()