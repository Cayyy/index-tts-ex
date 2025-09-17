@echo off
chcp 65001 >nul
echo ========================================
echo    更新 IndexTTS 子模块
echo ========================================
echo.

REM 检查子模块是否存在
if not exist "index-tts" (
    echo 子模块不存在，正在添加...
    git submodule add https://github.com/index-tts/index-tts.git index-tts
    if errorlevel 1 (
        echo 添加失败，尝试使用镜像...
        git submodule add https://gitee.com/mirrors/index-tts.git index-tts
    )
) else (
    echo 子模块已存在，正在更新...
    echo.
    echo 1. 更新子模块到最新版本...
    git submodule update --remote --merge
    
    echo.
    echo 2. 初始化子模块（如果未初始化）...
    git submodule update --init --recursive
    
    echo.
    echo 3. 检查子模块状态...
    git submodule status
)

echo.
echo 更新完成！
echo.
echo 注意：如果需要下载模型文件，请运行以下命令：
echo huggingface-cli download IndexTeam/IndexTTS-1.5 ^
echo   config.yaml bigvgan_discriminator.pth bigvgan_generator.pth ^
echo   bpe.model dvae.pth gpt.pth unigram_12000.vocab ^
echo   --local-dir index-tts/checkpoints
echo.
pause
