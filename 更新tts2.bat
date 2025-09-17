@echo off
echo 正在更新 IndexTTS 子模块...
echo.

REM 检查子模块是否存在
if not exist "index-tts" (
    echo 子模块不存在，正在克隆...
    git submodule add https://github.com/index-tts/index-tts.git index-tts
    if errorlevel 1 (
        echo 克隆失败，尝试使用镜像...
        git submodule add https://gitee.com/mirrors/index-tts.git index-tts
    )
) else (
    echo 子模块已存在，正在更新...
    git submodule update --remote --merge
)

echo.
echo 更新完成！
pause
