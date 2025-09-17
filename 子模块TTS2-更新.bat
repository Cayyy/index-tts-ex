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

REM 显示子模块更新日志
echo ========================================
echo    子模块更新日志
echo ========================================
echo.

REM 获取当前子模块的提交哈希
cd index-tts
for /f "tokens=1" %%i in ('git rev-parse HEAD') do set "current_commit=%%i"
cd ..

REM 获取主项目中记录的子模块提交哈希
for /f "tokens=1" %%i in ('git ls-tree HEAD index-tts') do set "recorded_commit=%%i"

echo 当前子模块提交: %current_commit%
echo 主项目记录提交: %recorded_commit%
echo.

REM 检查是否有更新
if not "%current_commit%"=="%recorded_commit%" (
    echo ✅ 发现子模块更新！
    echo.
    echo 更新内容摘要:
    cd index-tts
    git log --oneline %recorded_commit%..%current_commit%
    cd ..
    echo.
    
    echo 详细更新日志:
    cd index-tts
    git log --pretty=format:"%%h - %%an, %%ar : %%s" %recorded_commit%..%current_commit%
    cd ..
    echo.
    
    echo 更新统计:
    cd index-tts
    git diff --stat %recorded_commit%..%current_commit%
    cd ..
    echo.
) else (
    echo ℹ️  子模块已是最新版本，无需更新
)

echo ========================================
echo.
echo 注意：如果需要下载模型文件，请运行以下命令：
echo huggingface-cli download IndexTeam/IndexTTS-1.5 ^
echo   config.yaml bigvgan_discriminator.pth bigvgan_generator.pth ^
echo   bpe.model dvae.pth gpt.pth unigram_12000.vocab ^
echo   --local-dir index-tts/checkpoints
echo.

