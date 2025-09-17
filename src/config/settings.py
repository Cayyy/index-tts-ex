"""
项目配置设置
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class Settings:
    """项目配置类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = config_file or self.project_root / "config.yaml"
        
        # 默认配置
        self.default_config = {
            "project": {
                "name": "IndexTTS-Dev",
                "version": "1.0.0",
                "debug": True
            },
            "tts": {
                "model_dir": "index-tts/checkpoints",
                "config_path": "index-tts/checkpoints/config.yaml",
                "use_v2": True,
                "use_fp16": False,
                "use_cuda_kernel": False,
                "use_deepspeed": False
            },
            "audio": {
                "sample_rate": 22050,
                "output_dir": "outputs",
                "max_duration": 300,  # 最大时长（秒）
                "normalize": True
            },
            "api": {
                "host": "127.0.0.1",
                "port": 8000,
                "workers": 1
            },
            "web": {
                "host": "127.0.0.1",
                "port": 7860,
                "share": False
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/app.log"
            }
        }
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config = self.default_config.copy()
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        config.update(user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return config
    
    def save_config(self, config_file: Optional[str] = None):
        """保存配置到文件"""
        file_path = config_file or self.config_file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_tts_config(self) -> Dict[str, Any]:
        """获取 TTS 配置"""
        return self.get("tts", {})
    
    def get_audio_config(self) -> Dict[str, Any]:
        """获取音频配置"""
        return self.get("audio", {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """获取 API 配置"""
        return self.get("api", {})
    
    def get_web_config(self) -> Dict[str, Any]:
        """获取 Web 配置"""
        return self.get("web", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.get("logging", {})
    
    def update_from_env(self):
        """从环境变量更新配置"""
        env_mappings = {
            "TTS_MODEL_DIR": "tts.model_dir",
            "TTS_CONFIG_PATH": "tts.config_path",
            "AUDIO_SAMPLE_RATE": "audio.sample_rate",
            "API_HOST": "api.host",
            "API_PORT": "api.port",
            "WEB_HOST": "web.host",
            "WEB_PORT": "web.port",
            "DEBUG": "project.debug"
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # 类型转换
                if config_key in ["api.port", "web.port", "audio.sample_rate"]:
                    value = int(value)
                elif config_key == "project.debug":
                    value = value.lower() in ("true", "1", "yes")
                
                self.set(config_key, value)
