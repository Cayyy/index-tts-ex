# IndexTTS 二次开发项目

基于 [IndexTTS](https://github.com/index-tts/index-tts) 的二次开发框架，提供完整的语音合成解决方案。

## 项目概述

IndexTTS 是一个工业级、可控且高效的零样本文本转语音（TTS）系统。本项目在此基础上构建了一个完整的二次开发框架，包含 Web 界面、API 服务、工具类等模块，便于快速开发和部署。

## 项目结构

```
index-tts2/
├── index-tts/                    # IndexTTS 子模块（Git 版本控制）
├── src/                          # 二次开发源码
│   ├── core/                     # 核心模块
│   │   ├── tts_wrapper.py        # TTS 包装器
│   │   └── audio_processor.py    # 音频处理工具
│   ├── api/                      # API 服务
│   │   └── api_server.py         # FastAPI 服务器
│   ├── web/                      # Web 界面
│   │   └── web_ui.py             # Gradio Web 界面
│   ├── config/                   # 配置管理
│   │   └── settings.py           # 配置设置类
│   ├── utils/                    # 工具类
│   │   ├── file_utils.py         # 文件工具
│   │   └── text_utils.py         # 文本工具
│   └── tests/                    # 测试文件
├── 更新tts2.bat                  # 更新 TTS 仓库脚本
├── 启动.bat                      # 启动二次开发项目
├── 启动TTS2.bat                  # 启动原始 TTS2 项目
├── setup_env.bat                 # 环境设置脚本
├── environment.yml               # Conda 环境配置
├── requirements.txt              # Python 依赖
├── config.yaml                   # 项目配置文件
├── web_ui.py                     # Web 界面启动脚本
├── api_server.py                 # API 服务器启动脚本
└── .gitignore                    # Git 忽略文件
```

## 快速开始

### 1. 环境准备

确保您的系统已安装：
- Python 3.10+
- Anaconda 或 Miniconda
- Git

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd index-tts2
```

### 3. 环境设置

#### 方法一：使用批处理脚本（推荐）
```bash
# Windows
setup_env.bat
```

#### 方法二：手动设置
```bash
# 创建 conda 环境
conda env create -f environment.yml

# 激活环境
conda activate index-tts-dev

# 安装依赖
pip install -r requirements.txt
```

### 4. 下载 IndexTTS 模型

```bash
# 运行更新脚本
更新tts2.bat

# 或手动下载模型
huggingface-cli download IndexTeam/IndexTTS-1.5 \
  config.yaml bigvgan_discriminator.pth bigvgan_generator.pth \
  bpe.model dvae.pth gpt.pth unigram_12000.vocab \
  --local-dir index-tts/checkpoints
```

### 5. 启动项目

#### 启动二次开发项目
```bash
# 使用批处理脚本
启动.bat

# 或直接启动
python web_ui.py        # Web 界面
python api_server.py    # API 服务
```

#### 启动原始 IndexTTS2 项目
```bash
启动TTS2.bat
```

## 功能特性

### 核心功能

- **语音合成**：支持中英文语音合成
- **情感控制**：支持多种情感表达
- **批量处理**：支持批量文本合成
- **音频处理**：音频格式转换、质量优化
- **文本处理**：文本清理、分割、情感分析

### 界面支持

- **Web 界面**：基于 Gradio 的用户友好界面
- **API 服务**：RESTful API，支持程序化调用
- **命令行工具**：支持命令行操作

### 技术特性

- **模块化设计**：清晰的代码结构，易于维护
- **配置灵活**：支持多种配置方式
- **错误处理**：完善的异常处理机制
- **日志记录**：详细的运行日志
- **测试支持**：完整的测试框架

## 配置说明

### 主要配置文件

- `config.yaml`：项目主配置文件
- `environment.yml`：Conda 环境配置
- `requirements.txt`：Python 依赖列表

### 配置项说明

```yaml
# 项目配置
project:
  name: "IndexTTS-Dev"
  version: "1.0.0"
  debug: true

# TTS 配置
tts:
  model_dir: "index-tts/checkpoints"
  config_path: "index-tts/checkpoints/config.yaml"
  use_v2: true
  use_fp16: false

# 音频配置
audio:
  sample_rate: 22050
  output_dir: "outputs"
  max_duration: 300

# API 配置
api:
  host: "127.0.0.1"
  port: 8000

# Web 配置
web:
  host: "127.0.0.1"
  port: 7860
```

## API 使用

### 启动 API 服务

```bash
python api_server.py
```

### API 端点

- `GET /`：服务状态
- `GET /health`：健康检查
- `GET /model/info`：模型信息
- `POST /synthesize`：语音合成
- `POST /batch_synthesize`：批量合成

### 使用示例

```python
import requests

# 语音合成
response = requests.post('http://localhost:8000/synthesize', 
    files={'voice_file': open('voice.wav', 'rb')},
    data={'text': '你好，这是一个测试文本。'}
)

# 保存结果
with open('output.wav', 'wb') as f:
    f.write(response.content)
```

## 开发指南

### 添加新功能

1. 在 `src/` 目录下创建新模块
2. 实现功能类和方法
3. 添加相应的测试文件
4. 更新配置文件（如需要）

### 代码规范

- 使用 Python 3.10+ 语法
- 遵循 PEP 8 代码规范
- 添加详细的文档字符串
- 编写单元测试

### 测试

```bash
# 运行所有测试
python -m pytest src/tests/

# 运行特定测试
python -m pytest src/tests/test_tts_wrapper.py
```

## 常见问题

### Q: 如何更新 IndexTTS 到最新版本？

A: 运行 `更新tts2.bat` 脚本，或手动执行：
```bash
cd index-tts
git pull origin main
cd ..
```

### Q: 模型文件下载失败怎么办？

A: 可以尝试使用镜像：
```bash
export HF_ENDPOINT="https://hf-mirror.com"
huggingface-cli download IndexTeam/IndexTTS-1.5 ...
```

### Q: 如何修改默认配置？

A: 编辑 `config.yaml` 文件，或通过环境变量覆盖：
```bash
export TTS_MODEL_DIR="your/model/path"
export API_PORT=8080
```

### Q: 支持哪些音频格式？

A: 支持常见的音频格式：WAV、MP3、FLAC、M4A 等。

## 更新日志

### v1.0.0 (2025-01-17)
- 初始版本发布
- 支持 IndexTTS1 和 IndexTTS2
- 提供 Web 界面和 API 服务
- 完整的工具类和配置系统

## 贡献指南

1. Fork 本项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目基于原始 IndexTTS 项目的许可证。请查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

- [IndexTTS](https://github.com/index-tts/index-tts) - 原始 TTS 系统
- [Gradio](https://gradio.app/) - Web 界面框架
- [FastAPI](https://fastapi.tiangolo.com/) - API 框架

## 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 [Issue](https://github.com/your-repo/issues)
- 发送邮件至：your.email@example.com

---

**注意**：本项目仅供学习和研究使用，请遵守相关法律法规和版权规定。
