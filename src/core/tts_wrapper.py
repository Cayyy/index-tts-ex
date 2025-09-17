"""
IndexTTS 包装器 - 提供简化的 API 接口
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Union, List

# 添加 IndexTTS 路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
index_tts_path = project_root / "index-tts"
sys.path.insert(0, str(index_tts_path))

try:
    from indextts.infer_v2 import IndexTTS2
    from indextts.infer import IndexTTS
except ImportError as e:
    logging.warning(f"无法导入 IndexTTS: {e}")
    IndexTTS2 = None
    IndexTTS = None


class TTSWrapper:
    """IndexTTS 包装器类"""
    
    def __init__(self, 
                 model_dir: str = "index-tts/checkpoints",
                 config_path: str = "index-tts/checkpoints/config.yaml",
                 use_v2: bool = True,
                 use_fp16: bool = False,
                 use_cuda_kernel: bool = False,
                 use_deepspeed: bool = False):
        """
        初始化 TTS 包装器
        
        Args:
            model_dir: 模型目录路径
            config_path: 配置文件路径
            use_v2: 是否使用 IndexTTS2
            use_fp16: 是否使用半精度
            use_cuda_kernel: 是否使用 CUDA 内核
            use_deepspeed: 是否使用 DeepSpeed
        """
        self.model_dir = model_dir
        self.config_path = config_path
        self.use_v2 = use_v2
        self.tts = None
        
        # 检查模型文件是否存在
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"模型目录不存在: {model_dir}")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        self._initialize_tts()
    
    def _initialize_tts(self):
        """初始化 TTS 模型"""
        try:
            if self.use_v2 and IndexTTS2 is not None:
                self.tts = IndexTTS2(
                    cfg_path=self.config_path,
                    model_dir=self.model_dir,
                    use_fp16=self.use_fp16,
                    use_cuda_kernel=self.use_cuda_kernel,
                    use_deepspeed=self.use_deepspeed
                )
                logging.info("已加载 IndexTTS2 模型")
            elif IndexTTS is not None:
                self.tts = IndexTTS(
                    model_dir=self.model_dir,
                    cfg_path=self.config_path
                )
                logging.info("已加载 IndexTTS1 模型")
            else:
                raise ImportError("无法导入 IndexTTS 模块")
        except Exception as e:
            logging.error(f"初始化 TTS 模型失败: {e}")
            raise
    
    def synthesize(self, 
                   text: str,
                   voice_path: str,
                   output_path: str,
                   emotion_vector: Optional[List[float]] = None,
                   use_emo_text: bool = False,
                   emo_text: Optional[str] = None,
                   emo_alpha: float = 0.6,
                   use_random: bool = False,
                   verbose: bool = True) -> bool:
        """
        语音合成
        
        Args:
            text: 要合成的文本
            voice_path: 参考语音文件路径
            output_path: 输出文件路径
            emotion_vector: 情感向量
            use_emo_text: 是否使用文本情感
            emo_text: 情感文本
            emo_alpha: 情感强度
            use_random: 是否使用随机采样
            verbose: 是否显示详细信息
            
        Returns:
            bool: 合成是否成功
        """
        try:
            if not os.path.exists(voice_path):
                raise FileNotFoundError(f"参考语音文件不存在: {voice_path}")
            
            if self.use_v2 and hasattr(self.tts, 'infer'):
                # IndexTTS2 接口
                self.tts.infer(
                    spk_audio_prompt=voice_path,
                    text=text,
                    output_path=output_path,
                    emo_vector=emotion_vector,
                    use_emo_text=use_emo_text,
                    emo_text=emo_text,
                    emo_alpha=emo_alpha,
                    use_random=use_random,
                    verbose=verbose
                )
            else:
                # IndexTTS1 接口
                self.tts.infer(voice_path, text, output_path)
            
            logging.info(f"语音合成完成: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"语音合成失败: {e}")
            return False
    
    def batch_synthesize(self, 
                        texts: List[str],
                        voice_path: str,
                        output_dir: str,
                        **kwargs) -> List[str]:
        """
        批量语音合成
        
        Args:
            texts: 文本列表
            voice_path: 参考语音文件路径
            output_dir: 输出目录
            **kwargs: 其他参数
            
        Returns:
            List[str]: 输出文件路径列表
        """
        os.makedirs(output_dir, exist_ok=True)
        output_paths = []
        
        for i, text in enumerate(texts):
            output_path = os.path.join(output_dir, f"output_{i:03d}.wav")
            success = self.synthesize(text, voice_path, output_path, **kwargs)
            if success:
                output_paths.append(output_path)
            else:
                logging.warning(f"第 {i+1} 个文本合成失败: {text}")
        
        return output_paths
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            "model_dir": self.model_dir,
            "config_path": self.config_path,
            "use_v2": self.use_v2,
            "model_loaded": self.tts is not None
        }
