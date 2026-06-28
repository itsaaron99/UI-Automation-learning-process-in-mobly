from mobly import base_test
from mobly.controllers import android_device
from automation_mobly.libs.wifi_controller import WifiController
from automation_mobly.libs.app_controller import AppController
from automation_mobly.libs.ui_controller import UIController


class EnterpriseBaseTest(base_test.BaseTestClass):
    """
    Base class for enterprise tests, handling device setup and controller injection.
    """

    def setup_class(self):
        """ Register the Android device controller """
        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]

        """ Load the snippet package (required for WifiController to function) """
        self.dut.load_snippet('mbs', 'com.google.android.mobly.snippet.bundled')

        """ Dependency Injection: Create WifiController instance with the device """
        self.wifi_controller = WifiController(self.dut)
        self.app_controller = AppController(self.dut)
        self.ui_controller = UIController(self.dut)

    def teardown_class(self):
        """ Global Teardown: Return to home screen after all tests are done """
        if hasattr(self, 'dut'):
            self.dut.log.info("Executing EnterpriseBaseTest global teardown...")
            self.dut.adb.shell(['input', 'keyevent', 'KEYCODE_HOME'])

    def on_fail(self, record):
        """Lifecycle callback automatically triggered by Mobly when a test case fails.

        This method acts as a global safety net to capture the exact state of the 
        Device Under Test (DUT) at the moment of failure. It extracts failure details 
        from the test record and can be extended to perform automated triage actions 
        such as capturing screenshots, dumping logcat, or uploading artifacts to 
        the test dashboard.

        Args:
            record: A mobly.records.TestResultRecord object containing telemetry 
                    and execution details about the failed test case.
        """
        self.dut.log.error(f"--- [Global Failure Hook] Test case failed in: {record.test_name} ---")
        self.dut.log.error(f"Reason: {record.details}")

        if hasattr(self, 'app_controller'):
            try:
                if hasattr(self, 'app_config') and getattr(self.app_config, 'test_app_screenshot_path', None):
                    screenshot_dir = self.test_app_screenshot_path.dest_path
                else:
                    screenshot_dir = "/tmp/mobly_failure_screenshots"
                
                self.dut.log.info(f"BaseTest: Disastrous scene detected. Capturing screenshot to: {screenshot_dir}")
                self.app_controller.take_screenshot(screenshot_dir)
                
            except Exception as e:
                self.dut.log.error(f"BaseTest: Failed to take failure screenshot due to: {e}")
        else:
            self.dut.log.warn("BaseTest: app_controller is not initialized. Skipping automated screenshot.")