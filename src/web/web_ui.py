"""
Web 用户界面
"""

import gradio as gr
import os
import logging
from pathlib import Path
from typing import Optional, List
import sys

# 添加项目根目录到路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.tts_wrapper import TTSWrapper
from src.config.settings import Settings


class WebUI:
    """Web 用户界面类"""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        初始化 Web UI
        
        Args:
            settings: 配置设置
        """
        self.settings = settings or Settings()
        self.tts_wrapper = None
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        log_config = self.settings.get_logging_config()
        logging.basicConfig(
            level=getattr(logging, log_config.get("level", "INFO")),
            format=log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_tts(self):
        """初始化 TTS 模型"""
        try:
            tts_config = self.settings.get_tts_config()
            self.tts_wrapper = TTSWrapper(**tts_config)
            self.logger.info("TTS 模型初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"TTS 模型初始化失败: {e}")
            return False
    
    def synthesize_audio(self, 
                        text: str,
                        voice_file,
                        emotion_vector: Optional[List[float]] = None,
                        use_emo_text: bool = False,
                        emo_text: Optional[str] = None,
                        emo_alpha: float = 0.6,
                        use_random: bool = False) -> Optional[str]:
        """
        语音合成
        
        Args:
            text: 要合成的文本
            voice_file: 参考语音文件
            emotion_vector: 情感向量
            use_emo_text: 是否使用文本情感
            emo_text: 情感文本
            emo_alpha: 情感强度
            use_random: 是否使用随机采样
            
        Returns:
            Optional[str]: 输出文件路径
        """
        if not self.tts_wrapper:
            self.logger.error("TTS 模型未初始化")
            return None
        
        if not text.strip():
            self.logger.error("文本不能为空")
            return None
        
        if voice_file is None:
            self.logger.error("请上传参考语音文件")
            return None
        
        try:
            # 创建输出目录
            output_dir = Path(self.settings.get("audio.output_dir", "outputs"))
            output_dir.mkdir(exist_ok=True)
            
            # 生成输出文件名
            import time
            timestamp = int(time.time())
            output_path = output_dir / f"output_{timestamp}.wav"
            
            # 执行语音合成
            success = self.tts_wrapper.synthesize(
                text=text,
                voice_path=voice_file.name,
                output_path=str(output_path),
                emotion_vector=emotion_vector,
                use_emo_text=use_emo_text,
                emo_text=emo_text,
                emo_alpha=emo_alpha,
                use_random=use_random
            )
            
            if success:
                self.logger.info(f"语音合成成功: {output_path}")
                return str(output_path)
            else:
                self.logger.error("语音合成失败")
                return None
                
        except Exception as e:
            self.logger.error(f"语音合成异常: {e}")
            return None
    
    def create_interface(self):
        """创建 Gradio 界面"""
        with gr.Blocks(title="IndexTTS 二次开发界面") as interface:
            gr.Markdown("# IndexTTS 二次开发界面")
            gr.Markdown("基于 IndexTTS 的语音合成系统")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # 输入区域
                    gr.Markdown("## 输入设置")
                    
                    text_input = gr.Textbox(
                        label="要合成的文本",
                        placeholder="请输入要合成的文本...",
                        lines=5,
                        max_lines=10
                    )
                    
                    voice_file = gr.File(
                        label="参考语音文件",
                        file_types=["audio"]
                    )
                    
                    # 情感控制
                    gr.Markdown("### 情感控制")
                    
                    use_emo_text = gr.Checkbox(
                        label="使用文本情感",
                        value=False
                    )
                    
                    emo_text = gr.Textbox(
                        label="情感文本",
                        placeholder="描述情感状态的文本...",
                        visible=False
                    )
                    
                    emo_alpha = gr.Slider(
                        label="情感强度",
                        minimum=0.0,
                        maximum=1.0,
                        value=0.6,
                        step=0.1
                    )
                    
                    use_random = gr.Checkbox(
                        label="使用随机采样",
                        value=False
                    )
                    
                    # 控制按钮
                    synthesize_btn = gr.Button("开始合成", variant="primary")
                    
                with gr.Column(scale=1):
                    # 输出区域
                    gr.Markdown("## 输出结果")
                    
                    output_audio = gr.Audio(
                        label="合成结果",
                        type="filepath"
                    )
                    
                    status_text = gr.Textbox(
                        label="状态信息",
                        interactive=False
                    )
            
            # 事件处理
            def on_emo_text_change(use_emo):
                return gr.update(visible=use_emo)
            
            use_emo_text.change(
                on_emo_text_change,
                inputs=[use_emo_text],
                outputs=[emo_text]
            )
            
            def on_synthesize(text, voice, use_emo, emo_text_val, emo_alpha_val, use_random_val):
                if not text.strip():
                    return None, "错误: 文本不能为空"
                
                if voice is None:
                    return None, "错误: 请上传参考语音文件"
                
                output_path = self.synthesize_audio(
                    text=text,
                    voice_file=voice,
                    use_emo_text=use_emo,
                    emo_text=emo_text_val if use_emo else None,
                    emo_alpha=emo_alpha_val,
                    use_random=use_random_val
                )
                
                if output_path:
                    return output_path, "合成成功！"
                else:
                    return None, "合成失败，请检查输入和模型状态"
            
            synthesize_btn.click(
                on_synthesize,
                inputs=[text_input, voice_file, use_emo_text, emo_text, emo_alpha, use_random],
                outputs=[output_audio, status_text]
            )
            
            # 示例
            gr.Markdown("## 使用示例")
            gr.Examples(
                examples=[
                    ["大家好，我现在正在体验 AI 科技，这真是太神奇了！", None],
                    ["今天天气真好，心情也很愉快。", None],
                    ["这是一个测试文本，用于验证语音合成效果。", None]
                ],
                inputs=[text_input, voice_file]
            )
        
        return interface
    
    def launch(self):
        """启动 Web 界面"""
        # 初始化 TTS 模型
        if not self.initialize_tts():
            self.logger.error("无法启动 Web 界面：TTS 模型初始化失败")
            return
        
        # 创建界面
        interface = self.create_interface()
        
        # 获取配置
        web_config = self.settings.get_web_config()
        
        # 启动服务
        self.logger.info(f"启动 Web 界面: http://{web_config['host']}:{web_config['port']}")
        interface.launch(
            server_name=web_config["host"],
            server_port=web_config["port"],
            share=web_config.get("share", False),
            show_error=True
        )


def main():
    """主函数"""
    settings = Settings()
    web_ui = WebUI(settings)
    web_ui.launch()


if __name__ == "__main__":
    main()
