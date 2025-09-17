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
echo 是否要推送子模块更新到远程仓库？
set /p push_choice="输入 y 推送，其他键跳过: "

if /i "%push_choice%"=="y" (
    echo.
    echo 正在推送子模块更新...
    call "推送子模块TTS2.bat"
) else (
    echo 跳过推送，您可以稍后运行 推送子模块TTS2.bat 来推送更新
)

echo.
pause
