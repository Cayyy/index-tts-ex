@echo off
chcp 65001 >nul
echo ========================================
echo    IndexTTS 二次开发项目启动脚本
echo ========================================
echo.

REM 检查 conda 是否安装
where conda >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 conda，请先安装 Anaconda 或 Miniconda
    echo 下载地址: https://www.anaconda.com/download
    pause
    exit /b 1
)

REM 检查环境是否存在
conda info --envs | findstr "index-tts-dev" >nul
if errorlevel 1 (
    echo 环境不存在，正在创建 conda 环境...
    conda env create -f environment.yml
    if errorlevel 1 (
        echo 环境创建失败！
        pause
        exit /b 1
    )
)

REM 激活环境
echo 正在激活 conda 环境...
call conda activate index-tts-dev

REM 检查 IndexTTS 子模块
if not exist "index-tts\indextts" (
    echo 警告: IndexTTS 子模块未找到，请运行 更新tts2.bat
    echo.
)

REM 设置环境变量
set PYTHONPATH=.;index-tts;src
set CUDA_VISIBLE_DEVICES=0

REM 启动项目
echo 正在启动二次开发项目...
echo.
echo 可用的启动选项:
echo 1. 启动 Web 界面
echo 2. 启动 API 服务
echo 3. 启动 Jupyter Notebook
echo 4. 运行测试
echo.
set /p choice="请选择启动选项 (1-4): "

if "%choice%"=="1" (
    echo 启动 Web 界面...
    python src/web_ui.py
) else if "%choice%"=="2" (
    echo 启动 API 服务...
    python src/api_server.py
) else if "%choice%"=="3" (
    echo 启动 Jupyter Notebook...
    jupyter notebook
) else if "%choice%"=="4" (
    echo 运行测试...
    python -m pytest src/tests/
) else (
    echo 无效选择，启动默认 Web 界面...
    python src/web_ui.py
)

pause
