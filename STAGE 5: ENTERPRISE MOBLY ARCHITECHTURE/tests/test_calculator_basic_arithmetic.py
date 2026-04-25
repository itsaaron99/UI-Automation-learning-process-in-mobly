import sys
import os

sys.path.insert(0, os.getcwd())
from mobly import test_runner
from mobly import asserts
from common.base_test import EnterpriseBaseTest
from data_models.app_protos import AppConfig
from tests.constants import EXP_RESULT, CALC_RES_ID_RESULT, UI_DEFAULT_WAIT_SEC_3, UI_DEFAULT_WAIT_SEC_1, CALC_BTN_1, CALC_BTN_2, CALC_BTN_3, CALC_BTN_8, CALC_BTN_ADD, CALC_BTN_EQUAL
import time

class CalculatorTest(EnterpriseBaseTest):

    def setup_test(self):
        self.apps_to_cleanup = []


    def test_calculator_basic_addition(self):
        """Verifies basic arithmetic addition functionality via UI interactions.

        This test case simulates a user performing '12 + 38' on the OpenCalculator 
        app by clicking coordinate-based buttons and verifies the result output 
        via Mobly snippets to ensure UI-logic synchronization.

        Steps:
        1. Launch the OpenCalculator application.
        2. Enter '12' by clicking the corresponding numeric coordinates.
        3. Click the '+' operator button.
        4. Enter '38' by clicking the corresponding numeric coordinates.
        5. Click the '=' button to execute the calculation.

        Verification:
        - The calculation result display should show the string '50'.
        """
        pkg_name = self.user_params.get('target_app_pkg', '')
        pkg_path = self.user_params.get('test_app_path', '')
        dest_path = self.user_params.get('test_app_screenshot_path')
        app_config = AppConfig(package_name=pkg_name, package_path=pkg_path, dest_path=dest_path)

        #check if app is installed aready, else install first and launch it.
        if not self.app_controller.is_installed(app_config):
            install_result = self.app_controller.install(app_config)
            asserts.assert_true(install_result, f"Expected app {pkg_name} to be installed, but failed")

        # Add app_config into the cleanup list for tear down test
        self.apps_to_cleanup.append(app_config)
        self.dut.log.info("App exists and is installed successfully!")

        #launch app
        if not self.app_controller.is_app_in_foreground(app_config):
            launch_result = self.app_controller.launch_app(app_config)
            asserts.assert_true(launch_result, f"Expected app {pkg_name} to be launched, but failed")
        self.dut.log.info(f'App: {pkg_name} has been launched successfully.')
        time.sleep(UI_DEFAULT_WAIT_SEC_1)


        #click on '1' '2' -> '+' -> '3' '8' -> '=' on calculator
        # 12 + 38 = 50
        self.dut.log.info("Typing: 12 + 38 =")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_1), "Failed to click button '1'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_2), "Failed to click button '2'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_ADD), "Failed to click button '+'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_3), "Failed to click button '3'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_8), "Failed to click button '8'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_EQUAL), "Failed to click button '='")
        time.sleep(UI_DEFAULT_WAIT_SEC_3)

        #verificaiton of calculation matches the expection
        self.dut.log.info("Verifying if the result... ")
        act_result = self.ui_controller.get_text_by_id(CALC_RES_ID_RESULT)
        asserts.assert_equal(
                    act_result, 
                    EXP_RESULT, 
                    f"Expected the result to be '{EXP_RESULT}' but got '{act_result}'"
                )

        self.dut.log.info('Result matches expection: %s', EXP_RESULT)

        # take screen shot
        take_screenshot_result = self.app_controller.take_screenshot(dest_path)
        asserts.assert_true(take_screenshot_result, f"Expected to take screenshot to {dest_path}, but failed")
        self.dut.log.info('Screenshot has been saved to %s', dest_path)

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
