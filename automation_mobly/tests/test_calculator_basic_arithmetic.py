import sys
import os
import time
from mobly import test_runner
from mobly import asserts
from automation_mobly.common.base_test import EnterpriseBaseTest
from automation_mobly.data_models.app_protos import AppConfig
from automation_mobly.tests.constants import (EXP_RESULT, 
                                            RESET_RESULT, 
                                            CALC_RES_ID_RESULT, 
                                            UI_DEFAULT_WAIT_SEC_3, 
                                            UI_DEFAULT_WAIT_SEC_1, 
                                            CALC_BTN_1, CALC_BTN_2, 
                                            CALC_BTN_3, CALC_BTN_8, 
                                            CALC_BTN_ADD, 
                                            CALC_BTN_EQUAL, 
                                            CALC_BTN_DEL, 
                                            ADDITION_TEST_DATA)
class CalculatorTest(EnterpriseBaseTest):

    def setup_class(self):
        super().setup_class()
        pkg_name = self.user_params.get('target_app_pkg_for_calculator') or self.user_params.get('target_app_pkg', '')
        pkg_path = self.user_params.get('test_app_path_for_calculator') or self.user_params.get('test_app_path', '')
        dest_path = self.user_params.get('test_app_screenshot_path', '/tmp/mobly_screenshots')
        self.app_config = AppConfig(package_name=pkg_name, package_path=pkg_path, dest_path=dest_path)

        #check if app is installed aready, else install first and launch it.
        if not self.app_controller.is_installed(self.app_config):
            install_result = self.app_controller.install(self.app_config)
            asserts.assert_true(install_result, f"Expected app {pkg_name} to be installed, but failed")

        #launch app
        if not self.app_controller.is_app_in_foreground(self.app_config):
            launch_result = self.app_controller.launch_app(self.app_config)
            asserts.assert_true(launch_result, f"Expected app {pkg_name} to be launched, but failed")
        self.dut.log.info(f'App: {pkg_name} has been launched successfully.')
        time.sleep(UI_DEFAULT_WAIT_SEC_1)

    def setup_generated_tests(self):
        self.generate_tests(
            test_logic=self.logic_calculator_addition,
            name_func=lambda no_use_var1, no_use_var2, expected_res: f"test_dynamic_addition_{expected_res}",
            arg_sets=ADDITION_TEST_DATA
        )

    def setup_test(self):
        """Runs on every TC, which will reset the calculator """
        self.dut.log.info("Setup Test: Reseting the calculator...")
        asserts.assert_true(self.ui_controller.long_click_by_id(CALC_BTN_DEL), "Failed to reset...")
        self.ui_controller.wait_for_element_by_ui(UI_DEFAULT_WAIT_SEC_1)
        #check if text is empty
        current_text = self.ui_controller.get_text_by_id(CALC_RES_ID_RESULT)
        asserts.assert_equal(
                    current_text,
                    RESET_RESULT,
                    f'Setup Test: Fail to reset text...'
        )

    def test_calculator_basic_addition(self):
        """ *** Test logic will be replaced by TC3 ***
        
        Verifies basic arithmetic addition functionality via UI interactions.

        This test case simulates a user performing '12 + 38' on the OpenCalculator 
        app by clicking coordinate-based buttons and verifies the result output 
        via Mobly snippets to ensure UI-logic synchronization.

        Steps:
        1. Launch the OpenCalculator application.
        2. Enter '12' by clicking the corresponding numeric coordinates.
        3. Click the '+' operator button.
        4. Enter '38' by clicking the corresponding numeric coordinates.
        5. Click the '=' button to execute the calculation.
        6. Take screenshot

        Verification:
        - The calculation result display should show the string '50'.
        """
        self.dut.log.info("=== Start test calculator basic addition ===")
        self.dut.log.info("Typing: 12 + 38 =")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_1), "Failed to click button '1'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_2), "Failed to click button '2'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_ADD), "Failed to click button '+'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_3), "Failed to click button '3'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_8), "Failed to click button '8'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_EQUAL), "Failed to click button '='")
        self.ui_controller.wait_for_element_by_ui(UI_DEFAULT_WAIT_SEC_3)

        # verification of calculation matches the expectation
        self.dut.log.info("Verifying if the result... ")
        act_result = self.ui_controller.get_text_by_id(CALC_RES_ID_RESULT)
        asserts.assert_equal(
                    act_result, 
                    EXP_RESULT, 
                    f"Expected the result to be '{EXP_RESULT}' but got '{act_result}'"
                )

        self.dut.log.info('Result matches expectation: %s', EXP_RESULT)

        # take screen shot
        take_screenshot_result = self.app_controller.take_screenshot(self.app_config.dest_path)
        asserts.assert_true(take_screenshot_result, f"Expected to take screenshot but failed")
        self.dut.log.info('Screenshot has been saved to %s', self.app_config.dest_path)

    def test_calculator_long_click_clear(self):
        """ TC2: test calculator long click clear """
        self.dut.log.info("=== Start test calculator long click clear all ===")
        self.dut.log.info("Typing '123' to prepare for deletion...")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_1), "Failed to click '1'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_2), "Failed to click '2'")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_3), "Failed to click '3'")
        current_text = self.ui_controller.get_text_by_id(CALC_RES_ID_RESULT)
        asserts.assert_equal(current_text, "123", f"Setup failed! Expected '123' but got '{current_text}'")

        #long click delete button
        self.dut.log.info("Long clicking the DEL button...")
        asserts.assert_true(self.ui_controller.long_click_by_id(CALC_BTN_DEL), "Failed to long click...")

        #check if text is deleted
        self.dut.log.info("Checking if text is deleted...")
        final_text = self.ui_controller.get_text_by_id(CALC_RES_ID_RESULT)
        asserts.assert_equal(
                            final_text, 
                            RESET_RESULT, 
                            f"Clear Error! Expected empty string but got '{final_text}'")

        self.dut.log.info('Long click delete successful. Screen is completely empty.')

    def logic_calculator_addition(self, btn_a, btn_b, expected_res):
        """ TC3: additional test by using generate_tests. """
        self.dut.log.info("=== Running Addition Logic: %s ===", expected_res)
        asserts.assert_true(self.ui_controller.click_by_id(btn_a), "Failed to click button A")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_ADD), "Failed to click button '+")
        asserts.assert_true(self.ui_controller.click_by_id(btn_b), "Failed to click button B")
        asserts.assert_true(self.ui_controller.click_by_id(CALC_BTN_EQUAL), "Failed to click button '='")
        # wait for result
        self.ui_controller.wait_for_element_by_ui(UI_DEFAULT_WAIT_SEC_1, CALC_RES_ID_RESULT)
        # check result
        act_res = self.ui_controller.get_text_by_id(CALC_RES_ID_RESULT)
        asserts.assert_equal(
            expected_res,
            act_res,
            f'Expect {expected_res} but got {act_res}'
        )

    def teardown_class(self):        
        self.dut.log.info("=== teardown_class: Starting Teardown ===")

        if hasattr(self, 'app_config'):
            self.dut.log.info("Cleaning up app: %s", self.app_config.package_name)
            self.app_controller.clear_data(self.app_config)
            uninstall_result = self.app_controller.uninstall(self.app_config)

            if not uninstall_result:
                self.dut.log.warning("Failed to uninstall %s during teardown.", self.app_config.package_name)

        super().teardown_class()

if __name__ == '__main__':
    del EnterpriseBaseTest
    test_runner.main()