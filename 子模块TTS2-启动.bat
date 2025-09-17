@echo off
chcp 65001 >nul
echo ========================================
echo    启动原始 IndexTTS2 项目
echo ========================================
echo.

REM 检查 conda 是否安装
where conda >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 conda，请先安装 Anaconda 或 Miniconda
    pause
    exit /b 1
)

REM 激活环境
echo 正在激活 conda 环境...
call conda activate index-tts-dev

REM 检查 IndexTTS 子模块
if not exist "index-tts\indextts" (
    echo 错误: IndexTTS 子模块未找到，请运行 更新tts2.bat
    pause
    exit /b 1
)

REM 进入 IndexTTS 目录
cd index-tts

REM 设置环境变量
set PYTHONPATH=.
set CUDA_VISIBLE_DEVICES=0

echo 正在启动原始 IndexTTS2 项目...
echo.

REM 检查是否有模型文件
if not exist "checkpoints\config.yaml" (
    echo 警告: 未找到模型文件，请先下载模型
    echo 运行以下命令下载模型:
    echo huggingface-cli download IndexTeam/IndexTTS-1.5 config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab --local-dir checkpoints
    echo.
    pause
)

REM 启动 WebUI
echo 启动 IndexTTS2 Web 界面...
python webui.py

cd ..
pause
