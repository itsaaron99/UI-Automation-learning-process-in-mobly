"""
Data model of Application
A standard contract between scipts and controller
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    package_name: str
    package_path: Optional[str] = None
    dest_path: Optional[str] = None