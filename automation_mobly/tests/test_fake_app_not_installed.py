"""
TODO: Finish the test lifecycle
"""

import sys
import os

sys.path.insert(0, os.getcwd())
from mobly import test_runner
from mobly import asserts
from common.base_test import EnterpriseBaseTest
from data_models.app_protos import AppConfig

class AppManagementTest(EnterpriseBaseTest):

    def test_fake_app_not_installed(self):
        fake_config = AppConfig(package_name='com.ghost.app.not.exist')

        is_installed = self.app_controller.is_installed(fake_config)
        asserts.assert_false(is_installed, "Ghost app shouldn't be installed")
        self.dut.log.info("Test passed: Ghost app is correctly identified as not installed")
