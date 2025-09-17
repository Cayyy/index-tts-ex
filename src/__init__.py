"""
IndexTTS 二次开发项目
基于 IndexTTS 的扩展开发框架
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.tts_wrapper import TTSWrapper
from .config.settings import Settings

__all__ = ["TTSWrapper", "Settings"]
