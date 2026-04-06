"""
Data model of Wi-Fi connection,
A standard contract between scripts and controller
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class WifiConfig:
    ssid: str
    password: Optional[str] = None