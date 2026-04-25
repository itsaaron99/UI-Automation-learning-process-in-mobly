"""
UI Controller

This controller handles device-level UI interactions using Android Debug Bridge (ADB)
commands. It provides programmatic access to simulate user inputs such as clicks,
swipes, and text entry.

Args:
    ad_device (AndroidDevice): The Mobly AndroidDevice object to interact with.
"""
import xml.etree.ElementTree as ET
import re

class UIController:

    def __init__(self, ad_device):
        """Initializes the UIController with a Mobly AndroidDevice."""
        self.ad = ad_device

    def click(self, x: int, y: int) -> bool:
        """Simulates a single tap at the specified (x, y) coordinates on the screen.

        Args:
            x: The x-coordinate on the screen.
            y: The y-coordinate on the screen.

        Returns:
            True if the tap command was executed successfully, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('UIController: Clicking at coordinates (%d, %d)', x, y)
        
        try:
            self.ad.adb.shell(['input', 'tap', str(x), str(y)])
            return True
        except Exception as e:
            self.ad.log.error('UIController: Failed to click at (%d, %d). Error: %s', x, y, e)
            return False

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int) -> bool:
        """Simulates a single swipe with the specified delta x to delta y coordinates on the screen.

        Args:
        start_x: The start x-coordinate on the screen.
        start_y: The start y-coordinate on the screen.
        end_x: The end x-coordinate on the screen.
        end_y: The end y-coordinate on the screen.
        duration_ms: The swip duration in ms.
        Returns:
            True if the swipe command was executed successfully, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('UIController: Swiping coordinates (%d, %d, %d, %d), duration: %d',
         start_x, start_y, end_x, end_y, duration_ms)

        try:
            self.ad.adb.shell(['input', 'swipe', str(start_x), str(start_y), str(end_x), str(end_y), str(duration_ms)])
            return True
        except Exception as e:
            self.ad.log.error('UIController: Fail to swipe from (x1: %d, y1: %d) to (x2: %d, y2: %d), duration: %d, error: %s',
             start_x, start_y, end_x, end_y, duration_ms, e)
            return False

    def long_click(self, x: int, y: int, duration_ms: int) -> bool:
        """Simulates a single long click with the specified (x, y) coordinates on the screen.

        Args:
        x: The x-coordinate on the screen.
        y: The y-coordinate on the screen.
        duration_ms: The swip duration in ms.

        Returns:
            True if the long click was executed successfully, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('UIController: Long click coordinates (%d, %d), duration: %d', x, y, duration_ms)

        #calls swipe() function which sets start_x == end_x, start_y == end_y.
        return self.swipe(x, y, x, y, duration_ms)

    def input_text(self, text: str) -> bool:
        """Simulates the text input box on the screen has been clicked and gained focus, 
        this function can be used to automatically input text.

        Args:
        text: Input text content

        Returns:
            True if the input text was executed successfully, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('UIController: Input text content as %s', text)
        formatted_text = text.replace(' ', '%s')

        try:
            self.ad.adb.shell(['input', 'text', formatted_text])
            return True
        except Exception as e:
            self.ad.log.error('UIController: Fail to enter content %s, error: %s', text, e)
            return False

    def press_enter(self) -> bool:
        """Simulates pressing enter of text input on the screen.

        Returns:
            True if pressing enter was executed successfully, False otherwise.

        Raises:
            RuntimeError: If the device gets disconnected or goes offline.
        """
        self.ad.log.info('UIController: Switch to new row by pressing enter.')

        try:
            self.ad.adb.shell(['input', 'keyevent', '66'])
            return True
        except Exception as e:
            self.ad.log.error('UIController: Fail to press enter. error: %s', e)
            return False

    def click_by_id(self, resource_id: str) -> bool:
            """Finds an element by resource-id on the screen and clicks its center point.

            Args:
                resource_id: The ID of the UI element to click.

            Returns:
                True if the click was successful, False otherwise.
            """
            self.ad.log.info('UIController: Trying to click element with ID [%s]...', resource_id)

            try:
                # 1. Dump UI hierarchy
                self.ad.adb.shell(['uiautomator', 'dump', '/data/local/tmp/window_dump.xml'])
                xml_content = self.ad.adb.shell(['cat', '/data/local/tmp/window_dump.xml']).decode('utf-8')
                
                # 2. Parse XML tree
                root = ET.fromstring(xml_content)
                
                # 3. Find the node
                for node in root.iter('node'):
                    if node.attrib.get('resource-id') == resource_id:
                        bounds_str = node.attrib.get('bounds', '')
                        self.ad.log.info('UIController: Found element! Bounds: %s', bounds_str)
                        
                        # 4. Extract coordinates from bounds="[x1,y1][x2,y2]"
                        # re.findall('\d+') will extract all numbers into a list: ['x1', 'y1', 'x2', 'y2']
                        coords = re.findall(r'\d+', bounds_str)
                        if len(coords) == 4:
                            x1, y1, x2, y2 = map(int, coords)
                            
                            # 5. Calculate the center point
                            center_x = (x1 + x2) // 2
                            center_y = (y1 + y2) // 2
                            
                            self.ad.log.info('UIController: Calculated center point at (%d, %d). Clicking now...', center_x, center_y)
                            # 6. Reuse your existing absolute click method
                            return self.click(center_x, center_y)
                        
                self.ad.log.warning('UIController: Could not find element [%s] to click.', resource_id)
                return False
                
            except Exception as e:
                self.ad.log.error('UIController: Failed to click by ID. Error: %s', e)
                return False