@echo off
chcp 65001 >nul
echo ========================================
echo    查看 IndexTTS 子模块更新日志
echo ========================================
echo.

REM 检查子模块是否存在
if not exist "index-tts" (
    echo 错误: 子模块不存在
    echo 请先运行 子模块TTS2-更新.bat
    pause
    exit /b 1
)

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
    
    echo ========================================
    echo    更新内容摘要
    echo ========================================
    cd index-tts
    git log --oneline %recorded_commit%..%current_commit%
    cd ..
    echo.
    
    echo ========================================
    echo    详细更新日志
    echo ========================================
    cd index-tts
    git log --pretty=format:"%%h - %%an, %%ar : %%s" %recorded_commit%..%current_commit%
    cd ..
    echo.
    
    echo ========================================
    echo    更新统计
    echo ========================================
    cd index-tts
    git diff --stat %recorded_commit%..%current_commit%
    cd ..
    echo.
    
    echo ========================================
    echo    最近 10 次提交
    echo ========================================
    cd index-tts
    git log --oneline -10
    cd ..
    echo.
    
) else (
    echo ℹ️  子模块已是最新版本，无需更新
    echo.
    
    echo ========================================
    echo    最近 10 次提交
    echo ========================================
    cd index-tts
    git log --oneline -10
    cd ..
    echo.
)

echo ========================================
echo    子模块状态
echo ========================================
git submodule status
echo.

echo ========================================
echo    主项目子模块更新历史
echo ========================================
git log --oneline --grep="Update IndexTTS submodule" -10
echo.

echo 提示: 使用以下命令查看更多信息:
echo   - git submodule status
echo   - cd index-tts ^&^& git log --oneline -20
echo   - git log --grep="Update IndexTTS submodule"
echo.
pause
