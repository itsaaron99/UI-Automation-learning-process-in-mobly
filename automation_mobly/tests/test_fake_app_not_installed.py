import sys
import os
from mobly import test_runner
from mobly import asserts
from automation_mobly.common.base_test import EnterpriseBaseTest
from automation_mobly.data_models.app_protos import AppConfig

class AppManagementTest(EnterpriseBaseTest):

    def setup_class(self):
        super().setup_class
        pkg_name = self.user_params.get('test_not_exist_app', '')
        self.app_config = AppConfig(package_name='pkg_name')

    def test_fake_app_not_installed(self):
        is_installed = self.app_controller.is_installed(self.app_config)
        asserts.assert_false(is_installed, "App shouldn't be installed...")
        self.dut.log.info("Test passed: Ghost app is correctly identified as not installed")

    def teardown_class(self):
        self.dut.log.info('=== teardown_class: Starting Teardown ===')
        self.dut.log.info('Ghost app, not exist... dut executing home screen.')
        super().teardown_class()

if __name__ == '__main__':
    del EnterpriseBaseTest
    test_runner.main()