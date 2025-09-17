"""
音频处理工具类
"""

import os
import librosa
import soundfile as sf
import numpy as np
from typing import Tuple, Optional, Union
import logging


class AudioProcessor:
    """音频处理工具类"""
    
    def __init__(self, sample_rate: int = 22050):
        """
        初始化音频处理器
        
        Args:
            sample_rate: 采样率
        """
        self.sample_rate = sample_rate
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        加载音频文件
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            Tuple[np.ndarray, int]: 音频数据和采样率
        """
        try:
            audio, sr = librosa.load(file_path, sr=self.sample_rate)
            return audio, sr
        except Exception as e:
            logging.error(f"加载音频文件失败: {e}")
            raise
    
    def save_audio(self, audio: np.ndarray, file_path: str, sample_rate: Optional[int] = None):
        """
        保存音频文件
        
        Args:
            audio: 音频数据
            file_path: 输出文件路径
            sample_rate: 采样率
        """
        try:
            if sample_rate is None:
                sample_rate = self.sample_rate
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            sf.write(file_path, audio, sample_rate)
            logging.info(f"音频文件已保存: {file_path}")
        except Exception as e:
            logging.error(f"保存音频文件失败: {e}")
            raise
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        音频归一化
        
        Args:
            audio: 音频数据
            
        Returns:
            np.ndarray: 归一化后的音频数据
        """
        # 避免除零
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio
    
    def trim_silence(self, audio: np.ndarray, top_db: int = 20) -> np.ndarray:
        """
        去除静音
        
        Args:
            audio: 音频数据
            top_db: 静音阈值
            
        Returns:
            np.ndarray: 处理后的音频数据
        """
        try:
            trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
            return trimmed
        except Exception as e:
            logging.warning(f"去除静音失败: {e}")
            return audio
    
    def get_audio_info(self, file_path: str) -> dict:
        """
        获取音频文件信息
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            dict: 音频信息
        """
        try:
            audio, sr = self.load_audio(file_path)
            duration = len(audio) / sr
            
            return {
                "file_path": file_path,
                "sample_rate": sr,
                "duration": duration,
                "channels": 1 if audio.ndim == 1 else audio.shape[0],
                "samples": len(audio),
                "max_amplitude": np.max(np.abs(audio)),
                "rms": np.sqrt(np.mean(audio**2))
            }
        except Exception as e:
            logging.error(f"获取音频信息失败: {e}")
            return {}
    
    def resample_audio(self, audio: np.ndarray, target_sr: int) -> np.ndarray:
        """
        重采样音频
        
        Args:
            audio: 音频数据
            target_sr: 目标采样率
            
        Returns:
            np.ndarray: 重采样后的音频数据
        """
        try:
            resampled = librosa.resample(audio, orig_sr=self.sample_rate, target_sr=target_sr)
            return resampled
        except Exception as e:
            logging.error(f"重采样失败: {e}")
            return audio
