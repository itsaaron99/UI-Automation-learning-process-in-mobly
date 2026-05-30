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

    def test_builtin_app_exists_and_force_stop(self):
        """ Update the proto """
        pkg_name = self.user_params.get('target_app_pkg', 'com.android.settings')
        app_config = AppConfig(package_name = pkg_name)

        """ Check if app is installed through controller """
        is_installed = self.app_controller.is_installed(app_config)
        asserts.assert_true(is_installed, f"Expected app {pkg_name} to be installed, but it is not.")

        """ Force stop """
        self.app_controller.force_stop(app_config)
        self.dut.log.info("Test passed: %s is intalled and forced stopped", pkg_name)
