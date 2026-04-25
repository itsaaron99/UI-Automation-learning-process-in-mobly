"""
AppController

This controller handles Android application management and lifecycle operations
using Android Debug Bridge (ADB) commands. It acts as a wrapper to perform 
common app-related tasks securely with built-in error handling and logging.

Args:
    ad_device (AndroidDevice): The Mobly AndroidDevice object to interact with.

Dependencies:
    AppConfig: A dataclass model containing application details (e.g., package_name, package_path).

Core Functions:
    - App lifecycle: install, uninstall, launch_app, force_stop, clear_data
    - App inspection: is_installed, is_app_in_foreground, get_app_version
    - Device UI: take_screenshot
"""
from data_models.app_protos import AppConfig
import time

class AppController:

    def __init__(self, ad_device):
        """Initializes the AppController with a Mobly AndroidDevice.

        Args:
            ad_device (AndroidDevice): The Mobly AndroidDevice object to interact with.
        """
        self.ad = ad_device

    def is_installed(self, config: AppConfig) -> bool:
        """Checks if the specified package is installed via ADB.

        Args:
            config: An AppConfig object containing the target package_name.

        Returns:
            True if the package is installed, False otherwise.
        """
        self.ad.log.info('AppController: Checking if %s is installed...', config.package_name)

        try:
            output = self.ad.adb.shell(f'pm list packages {config.package_name}')

            if isinstance(output, bytes):
                output = output.decode('utf-8')

            return f"package:{config.package_name}" in output
        
        except Exception as e:
            self.ad.log.error("AppController: Failed to check package %s", e)
            return False

    def force_stop(self, config: AppConfig):
        """Force stops the specified package.

        Args:
            config: An AppConfig object containing the target package_name.
        """
        self.ad.log.info('AppController: Force stopping %s ...', config.package_name)
        self.ad.adb.shell(f'am force-stop {config.package_name}')

    def install(self, config: AppConfig) -> bool:
        """Installs an APK through ADB and verifies the installation.

        Args:
            config: An AppConfig object containing the package_name and package_path.

        Returns:
            True if the installation was successful and verified, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Start installing APK %s', config.package_name)

        try:
            self.ad.adb.install(['-r', config.package_path])

        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error(f"AppController: device disconnection, fail to install {config.package_name}")
                raise RuntimeError(f"ADB connection error: {e}")

            self.ad.log.error('AppController: Failed to install %s. Error: %s', config.package_name, e)
            return False

        return self.is_installed(config)

    def uninstall(self, config: AppConfig) -> bool:
        """Uninstalls the specified package via ADB.

        Args:
            config: An AppConfig object containing the target package_name.

        Returns:
            True if the uninstallation was successful or already uninstalled, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Start uninstalling APK %s', config.package_name)
        if not self.is_installed(config):
            self.ad.log.info('AppController: %s is already been uninstalled', config.package_name)
            return True

        try:
            self.ad.adb.uninstall(config.package_name)

        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error(f'AppController: device disconnection, fail to uninstall {config.package_name}')
                raise RuntimeError(f"ADB connection error: {e}")

            self.ad.log.error('AppController: adb uninstall command failed. Error: %s', e)
            return False

        """ Recheck if the app is uninstalled """
        is_still_present = self.is_installed(config)

        if is_still_present:
            self.ad.log.error('AppController: Failed to uninstall %s. It still exists.', config.package_name)
            return False

        self.ad.log.info('AppController: %s uninstalled successfully', config.package_name)
        return True
    
    def clear_data(self, config: AppConfig) -> bool:
        """Clears all app data for the specified package.

        Args:
            config: An AppConfig object containing the target package_name.

        Returns:
            True if data was successfully cleared, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Executing %s data cleaning proccess...', config.package_name)
        if not self.is_installed(config):
            self.ad.log.info('AppController: %s is not installed, no need to clear data.', config.package_name)
            return True
        
        try:
            raw_output = self.ad.adb.shell(['pm', 'clear', config.package_name])

        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error(f'AppController: device disconnection, fail to clear {config.package_name}')
                raise RuntimeError(f"ADB connection error: {e}")

            self.ad.log.error('AppController: adb clear command failed. Error: %s', e)
            return False

        """ Check log msg if the data of apk has been cleanned """
        msg = raw_output.decode('utf-8').lower() if isinstance(raw_output, bytes) else str(raw_output).lower()
        if 'success' in msg:
            self.ad.log.info('AppController: Data of %s has been cleared successfully.', config.package_name)
            return True

        self.ad.log.error('AppController: Fail to clear %s.', config.package_name)
        return False

    def launch_app(self, config: AppConfig) -> bool:
        """Launches the specified app using the monkey command and waits for it to open.

        Args:
            config: An AppConfig object containing the target package_name.

        Returns:
            True if the app was successfully launched and brought to foreground, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Launching %s...', config.package_name)
        if not self.is_installed(config):
            self.ad.log.error('AppController: %s is not installed, please try again.', config.package_name)
            return False
        
        try:
            self.ad.adb.shell(['monkey', '-p', config.package_name, '-c', 'android.intent.category.LAUNCHER', '1'])

        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error(f'AppController: device disconnection, fail to launch {config.package_name}')
                raise RuntimeError(f"ADB connection error: {e}")

            self.ad.log.error('AppController: adb launch command failed. Error: %s', e)
            return False

        # Using polling to avoid the test fail 
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_app_in_foreground(config):
                return True
            self.ad.log.info('AppController: Waiting for %s to be in foreground...', config.package_name)
            time.sleep(1)
            
        self.ad.log.error('AppController: Fail to launch app %s, is not in foreground', config.package_name)
        return False

    def is_app_in_foreground(self, config: AppConfig) -> bool:
        """Checks if the specified app is currently running in the foreground.

        Args:
            config: An AppConfig object containing the target package_name.

        Returns:
            True if the target app is in the foreground, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Checking if %s in foreground...', config.package_name)

        try:
            log_output = self.ad.adb.shell(['dumpsys', 'activity', 'activities'])
        
        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error('AppController: device disconnection, fail to check if %s launching...', config.package_name)
                raise RuntimeError(f"ADB connection error: {e}")
            
            self.ad.log.error('AppController: adb dumpsys command failed. Error: %s', e)
            return False

        msg = log_output.decode('utf-8') if isinstance(log_output, bytes) else str(log_output)
        """ 
        Using .splitlines to capture both 'mResumedActivity' and config.target_app_pkg is in log or not 
        """
        foreground_keywords = ['mResumedActivity', 'topResumedActivity', 'mCurrentFocus', 'mFocusedApp']
        for line in msg.splitlines():
            if any(keyword in line for keyword in foreground_keywords) and config.package_name in line:
                self.ad.log.info('AppController: %s is currently in foreground.', config.package_name)
                return True

        self.ad.log.error('AppController: %s is NOT in foreground.', config.package_name)
        return False

    def get_app_version(self, config: AppConfig) -> str | None:
        """Retrieves the version name of the specified installed app.

        Args:
            config: An AppConfig object containing the target package_name.

        Returns:
            The version string (e.g., '1.2.0') if found, or None if the app is not installed or version not found.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Executing %s version checking process ...', config.package_name)
        if not self.is_installed(config):
            self.ad.log.error('AppController: %s is not installed, please check again.', config.package_name)
            return None

        try:
            log_output = self.ad.adb.shell(['dumpsys', 'package', config.package_name])
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error('AppController: device disconnection, fail to get %s version...', config.package_name)
                raise RuntimeError(f"ADB connection error: {e}")
            
            self.ad.log.error('AppController: adb dumpsys command failed. Error: %s', e)
            return None

        msg = log_output.decode('utf-8') if isinstance(log_output, bytes) else str(log_output)
        for line in msg.splitlines():
            if 'versionName=' in line:
                version = line.split('=')[1].strip()
                return version

        self.ad.log.error('AppController: Cannot get %s version, please try again', config.package_name)
        return None

    def take_screenshot(self, dest_path: str) -> bool:
        """Takes a screenshot of the current device screen and pulls it to the local machine.

        Args:
            dest_path: The local file path where the screenshot will be saved.

        Returns:
            True if the screenshot was successfully taken and pulled, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('AppController: Taking screenshot and saving to %s... ', dest_path)

        try:
            self.ad.adb.shell(['screencap', '-p', '/sdcard/temp_screen.png'])
            self.ad.adb.pull(['/sdcard/temp_screen.png', dest_path])

        except Exception as e:
            error_msg = str(e).lower()
            if 'offline' in error_msg or 'not found' in error_msg or 'disconnected' in error_msg:
                self.ad.log.error('AppController: device disconnection, fail to pull screenshot into %s... ', dest_path)
                raise RuntimeError(f"ADB connection error: {e}")

            self.ad.log.error('AppController: adb shell command failed. Error: %s', e)
            return False
                        
        finally:

            try:
                self.ad.adb.shell(['rm', '/sdcard/temp_screen.png'])

            except Exception as eclean_e:
                """ 
                Use warning to avoid the message replaced the error msg in step1 and step2,
                will not return True or False.
                """
                self.ad.log.warning('AppController: adb shell command failed. Error: %s', eclean_e)

        self.ad.log.info('AppController: Screenshot successfully saved to %s', dest_path)
        return True
