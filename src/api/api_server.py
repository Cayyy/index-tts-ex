"""
FastAPI 服务器
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, List
import sys

# 添加项目根目录到路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.tts_wrapper import TTSWrapper
from src.config.settings import Settings


class APIServer:
    """API 服务器类"""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        初始化 API 服务器
        
        Args:
            settings: 配置设置
        """
        self.settings = settings or Settings()
        self.app = FastAPI(
            title="IndexTTS API",
            description="IndexTTS 二次开发 API 服务",
            version="1.0.0"
        )
        self.tts_wrapper = None
        self.setup_logging()
        self.setup_middleware()
        self.setup_routes()
        
    def setup_logging(self):
        """设置日志"""
        log_config = self.settings.get_logging_config()
        logging.basicConfig(
            level=getattr(logging, log_config.get("level", "INFO")),
            format=log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_middleware(self):
        """设置中间件"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """设置路由"""
        
        @self.app.on_event("startup")
        async def startup_event():
            """启动事件"""
            self.initialize_tts()
        
        @self.app.get("/")
        async def root():
            """根路径"""
            return {
                "message": "IndexTTS API 服务",
                "version": "1.0.0",
                "status": "running"
            }
        
        @self.app.get("/health")
        async def health_check():
            """健康检查"""
            return {
                "status": "healthy",
                "tts_loaded": self.tts_wrapper is not None
            }
        
        @self.app.get("/model/info")
        async def get_model_info():
            """获取模型信息"""
            if not self.tts_wrapper:
                raise HTTPException(status_code=503, detail="TTS 模型未加载")
            
            return self.tts_wrapper.get_model_info()
        
        @self.app.post("/synthesize")
        async def synthesize(
            text: str = Form(..., description="要合成的文本"),
            voice_file: UploadFile = File(..., description="参考语音文件"),
            emotion_vector: Optional[str] = Form(None, description="情感向量，JSON 格式"),
            use_emo_text: bool = Form(False, description="是否使用文本情感"),
            emo_text: Optional[str] = Form(None, description="情感文本"),
            emo_alpha: float = Form(0.6, description="情感强度"),
            use_random: bool = Form(False, description="是否使用随机采样")
        ):
            """语音合成接口"""
            if not self.tts_wrapper:
                raise HTTPException(status_code=503, detail="TTS 模型未加载")
            
            if not text.strip():
                raise HTTPException(status_code=400, detail="文本不能为空")
            
            try:
                # 保存上传的语音文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    content = await voice_file.read()
                    temp_file.write(content)
                    temp_voice_path = temp_file.name
                
                # 解析情感向量
                emo_vec = None
                if emotion_vector:
                    import json
                    try:
                        emo_vec = json.loads(emotion_vector)
                    except json.JSONDecodeError:
                        raise HTTPException(status_code=400, detail="情感向量格式错误")
                
                # 创建输出文件
                output_dir = Path(self.settings.get("audio.output_dir", "outputs"))
                output_dir.mkdir(exist_ok=True)
                
                import time
                timestamp = int(time.time())
                output_path = output_dir / f"api_output_{timestamp}.wav"
                
                # 执行语音合成
                success = self.tts_wrapper.synthesize(
                    text=text,
                    voice_path=temp_voice_path,
                    output_path=str(output_path),
                    emotion_vector=emo_vec,
                    use_emo_text=use_emo_text,
                    emo_text=emo_text,
                    emo_alpha=emo_alpha,
                    use_random=use_random
                )
                
                # 清理临时文件
                os.unlink(temp_voice_path)
                
                if success:
                    return FileResponse(
                        path=str(output_path),
                        media_type="audio/wav",
                        filename=f"output_{timestamp}.wav"
                    )
                else:
                    raise HTTPException(status_code=500, detail="语音合成失败")
                    
            except Exception as e:
                self.logger.error(f"语音合成异常: {e}")
                raise HTTPException(status_code=500, detail=f"语音合成异常: {str(e)}")
        
        @self.app.post("/batch_synthesize")
        async def batch_synthesize(
            texts: str = Form(..., description="文本列表，每行一个文本"),
            voice_file: UploadFile = File(..., description="参考语音文件"),
            **kwargs
        ):
            """批量语音合成接口"""
            if not self.tts_wrapper:
                raise HTTPException(status_code=503, detail="TTS 模型未加载")
            
            try:
                # 解析文本列表
                text_list = [text.strip() for text in texts.split('\n') if text.strip()]
                if not text_list:
                    raise HTTPException(status_code=400, detail="文本列表不能为空")
                
                # 保存上传的语音文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    content = await voice_file.read()
                    temp_file.write(content)
                    temp_voice_path = temp_file.name
                
                # 创建输出目录
                output_dir = Path(self.settings.get("audio.output_dir", "outputs"))
                batch_dir = output_dir / f"batch_{int(time.time())}"
                batch_dir.mkdir(exist_ok=True)
                
                # 执行批量合成
                output_paths = self.tts_wrapper.batch_synthesize(
                    texts=text_list,
                    voice_path=temp_voice_path,
                    output_dir=str(batch_dir)
                )
                
                # 清理临时文件
                os.unlink(temp_voice_path)
                
                return {
                    "message": f"批量合成完成，成功 {len(output_paths)} 个",
                    "output_dir": str(batch_dir),
                    "output_files": output_paths
                }
                
            except Exception as e:
                self.logger.error(f"批量合成异常: {e}")
                raise HTTPException(status_code=500, detail=f"批量合成异常: {str(e)}")
    
    def initialize_tts(self):
        """初始化 TTS 模型"""
        try:
            tts_config = self.settings.get_tts_config()
            self.tts_wrapper = TTSWrapper(**tts_config)
            self.logger.info("TTS 模型初始化成功")
        except Exception as e:
            self.logger.error(f"TTS 模型初始化失败: {e}")
    
    def run(self):
        """运行 API 服务器"""
        import uvicorn
        
        api_config = self.settings.get_api_config()
        
        self.logger.info(f"启动 API 服务器: http://{api_config['host']}:{api_config['port']}")
        
        uvicorn.run(
            self.app,
            host=api_config["host"],
            port=api_config["port"],
            workers=api_config.get("workers", 1)
        )


def main():
    """主函数"""
    settings = Settings()
    api_server = APIServer(settings)
    api_server.run()


if __name__ == "__main__":
    main()
