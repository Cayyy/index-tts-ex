"""
核心模块 - 封装 IndexTTS 功能
"""

from .tts_wrapper import TTSWrapper
from .audio_processor import AudioProcessor

__all__ = ["TTSWrapper", "AudioProcessor"]
