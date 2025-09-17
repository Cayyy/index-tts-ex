@echo off
chcp 65001 >nul
echo ========================================
echo    推送 IndexTTS 子模块更新
echo ========================================
echo.

REM 检查是否在 Git 仓库中
git status >nul 2>nul
if errorlevel 1 (
    echo 错误: 当前目录不是 Git 仓库
    pause
    exit /b 1
)

REM 检查是否有远程仓库
git remote -v >nul 2>nul
if errorlevel 1 (
    echo 警告: 未配置远程仓库，无法推送
    echo 请先配置远程仓库: git remote add origin <your-repo-url>
    pause
    exit /b 1
)

echo 正在检查子模块状态...
git submodule status

echo.
echo 正在检查是否有子模块更新...
git diff --quiet .gitmodules index-tts
if errorlevel 1 (
    echo 发现子模块更新，正在提交...
    
    REM 获取子模块的最新提交信息
    cd index-tts
    set "submodule_commit=%%(git log -1 --pretty=format:"%%h %%s")"
    cd ..
    
    REM 提交子模块更新
    git add .gitmodules index-tts
    git commit -m "Update IndexTTS submodule

- 更新到最新版本
- 子模块提交: %submodule_commit%
- 更新时间: %date% %time%"
    
    if errorlevel 1 (
        echo 提交失败！
        pause
        exit /b 1
    )
    
    echo 提交成功！
    echo.
    echo 正在推送到远程仓库...
    git push origin main
    
    if errorlevel 1 (
        echo 推送失败！请检查网络连接和权限
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ 子模块更新已成功推送到远程仓库！
    
) else (
    echo 没有发现子模块更新
    echo 当前子模块已是最新版本
)

echo.
echo 当前子模块状态:
git submodule status

echo.
pause
