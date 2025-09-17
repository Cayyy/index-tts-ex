"""
TTS 包装器测试
"""

import pytest
import os
import tempfile
from pathlib import Path
import sys

# 添加项目根目录到路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.tts_wrapper import TTSWrapper
from src.config.settings import Settings


class TestTTSWrapper:
    """TTS 包装器测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.settings = Settings()
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization_without_model(self):
        """测试在没有模型文件时的初始化"""
        with pytest.raises(FileNotFoundError):
            TTSWrapper(
                model_dir="nonexistent",
                config_path="nonexistent.yaml"
            )
    
    def test_get_model_info(self):
        """测试获取模型信息"""
        # 这里需要实际的模型文件才能测试
        # 暂时跳过
        pytest.skip("需要实际的模型文件")
    
    def test_synthesize_without_model(self):
        """测试在没有模型时的合成"""
        # 创建临时文件
        temp_voice = os.path.join(self.temp_dir, "voice.wav")
        temp_output = os.path.join(self.temp_dir, "output.wav")
        
        # 创建一个空的音频文件用于测试
        with open(temp_voice, 'w') as f:
            f.write("dummy")
        
        # 这里需要实际的模型文件才能测试
        pytest.skip("需要实际的模型文件")
    
    def test_batch_synthesize(self):
        """测试批量合成"""
        # 这里需要实际的模型文件才能测试
        pytest.skip("需要实际的模型文件")


if __name__ == "__main__":
    pytest.main([__file__])
