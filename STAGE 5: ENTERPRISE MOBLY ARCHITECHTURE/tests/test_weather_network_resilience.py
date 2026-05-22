import sys
import os

sys.path.insert(0, os.getcwd())
from mobly import test_runner
from mobly import asserts
from common.base_test import EnterpriseBaseTest
from data_models.app_protos import AppConfig
from tests.constants import (
    UI_DEFAULT_WAIT_SEC_3, 
    UI_DEFAULT_WAIT_SEC_1, 
    CHROME_PKG_NAME, 
    CHROME_ID_SEARCH_BOX, 
    CHROME_OFFLINE_TEXT,
    UI_DEFAULT_WAIT_SEC_5
)
import time

class ChromeNetworkTest(EnterpriseBaseTest):
    
    def setup_class(self):
        super().setup_class()
        pkg_name = self.user_params.get('target_app_pkg_for_chrome', '')
        dest_path = self.user_params.get('test_app_screenshot_path')
        network_status = self.user_params.get('requires_network')
        self.app_config = AppConfig(package_name=pkg_name,
                                    package_path=None,
                                    dest_path=dest_path,
                                    requires_network=True)
                                    
    def test_offline_dinosaur_appears(self) -> bool:
        """ 
        launch app -> 
        disconnect network -> 
        refresh current web page (or search for anything under internet is disconneted) -> 
        check if "No internet" string pops out
        """
        self.dut.log.info('=== Start testing offline donosaur appears ===')
        # launch app
        asserts.assert_true(self.app_controller.launch_app(self.app_config), 
                            f'Expect launching {self.app_config} but fail...')
        # disconnect Wifi
        self.dut.mbs.wifiDisable()
        time.sleep(UI_DEFAULT_WAIT_SEC_5)
        # refresh current web page by searching under network is offline
        asserts.assert_true(self.ui_controller.click_by_id(CHROME_ID_SEARCH_BOX), 'Expect clicking on search box but fail...')
        self.dut.adb.shell("input text 'mobly'")
        self.dut.adb.shell("input keyevent 66")

        found = self.ui_controller.wait_for_element_by_text(UI_DEFAULT_WAIT_SEC_3, CHROME_OFFLINE_TEXT)
        asserts.assert_true(found, 'Failed to verify Chrome offline page (Dinosaur page) appeared.')

    def teardown_test(self):
        """ Restoring network to default status """
        self.dut.log.info("=== Teardown_test: Restoring network ===")
        self.dut.mbs.wifiEnable()

    def teardown_class(self):
        self.dut.log.info("=== Teardown_class: Starting Teardown ===")
        self.app_controller.clear_data(self.app_config)
        super().teardown_class()

if __name__ == '__main__':
    del EnterpriseBaseTest
    test_runner.main()






    

    

