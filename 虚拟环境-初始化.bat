@echo off
chcp 65001 >nul
echo ========================================
echo    虚拟环境初始化脚本
echo ========================================
echo.

REM 检查 conda 是否安装
where conda >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 conda，请先安装 Anaconda 或 Miniconda
    echo.
    echo 下载连接: https://www.anaconda.com/download
    echo.
    echo 配置环境变量
    echo.
    echo ANACONDA_PATH：安装路径
    echo.
    echo PATH：
    echo    %%ANACONDA_PATH%%\Scripts
    echo    %%ANACONDA_PATH%%\condabin
    echo    %%ANACONDA_PATH%%\Library\bin
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到 conda 已安装
echo.

REM 检查环境是否已存在
conda info --envs | findstr "index-tts-dev" >nul
if errorlevel 1 (
    echo 环境不存在，正在创建...
    echo.
    
    REM 创建 conda 环境
    echo 正在创建 conda 环境: index-tts-dev
    conda env create -f environment.yml
    
    if errorlevel 1 (
        echo.
        echo ❌ 环境创建失败！
        echo.
        echo 可能的原因:
        echo 1. 网络连接问题
        echo 2. 依赖包冲突
        echo 3. 磁盘空间不足
        echo.
        echo 请检查错误信息并重试
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ 环境创建成功！
    
) else (
    echo 环境已存在，正在更新...
    echo.
    
    REM 更新现有环境
    echo 正在更新 conda 环境: index-tts-dev
    conda env update -f environment.yml
    
    if errorlevel 1 (
        echo.
        echo ❌ 环境更新失败！
        echo.
        echo 可能的原因:
        echo 1. 网络连接问题
        echo 2. 依赖包冲突
        echo.
        echo 请检查错误信息并重试
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ 环境更新成功！
)

echo.
echo ========================================
echo    环境信息
echo ========================================
echo.

REM 显示环境信息
conda info --envs | findstr "index-tts-dev"

echo.
echo ========================================
echo    下一步操作
echo ========================================
echo.

echo 1. 激活环境:
echo    conda activate index-tts-dev
echo.
echo 2. 验证安装:
echo    python --version
echo    pip list
echo.
echo 3. 更新子模块:
echo    子模块TTS2-更新.bat
echo.
echo 4. 下载模型文件:
echo    huggingface-cli download IndexTeam/IndexTTS-1.5 ^
echo      config.yaml bigvgan_discriminator.pth bigvgan_generator.pth ^
echo      bpe.model dvae.pth gpt.pth unigram_12000.vocab ^
echo      --local-dir index-tts/checkpoints
echo.
echo 5. 启动项目:
echo    子模块TTS2-启动.bat
echo.

echo ========================================
echo    环境初始化完成！
echo ========================================
echo.

set /p activate_now="是否现在激活环境？(y/n): "
if /i "%activate_now%"=="y" (
    echo.
    echo 正在激活环境...
    call conda activate index-tts-dev
    
    echo.
    echo 当前环境信息:
    echo Python 版本: 
    python --version
    echo.
    echo 已安装的包数量:
    pip list | find /c /v ""
    
    echo.
    echo 环境已激活！您现在可以运行项目了。
    echo.
    echo 提示: 要退出环境，请运行: conda deactivate
) else (
    echo.
    echo 环境已准备就绪！
    echo 请手动运行: conda activate index-tts-dev
)

echo.
pause
