@echo off
chcp 65001 >nul
echo ========================================
echo    IndexTTS 二次开发环境设置脚本
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

echo 正在创建 conda 环境...
conda env create -f environment.yml

if errorlevel 1 (
    echo 环境创建失败！
    pause
    exit /b 1
)

echo.
echo 环境创建成功！
echo.
echo 请运行以下命令激活环境:
echo conda activate index-tts-dev
echo.
echo 然后运行 更新tts2.bat 下载 IndexTTS 模型
echo.
pause
