@echo off
chcp 65001 >nul
echo ========================================
echo    虚拟环境激活脚本
echo ========================================
echo.

REM 检查 conda 是否安装
where conda >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 conda，请先安装 Anaconda 或 Miniconda
    echo.
    echo 下载地址:
    echo   Anaconda: https://www.anaconda.com/download
    echo   Miniconda: https://docs.conda.io/en/latest/miniconda.html
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到 conda 已安装
echo.

REM 检查环境是否存在
conda info --envs | findstr "index-tts-dev" >nul
if errorlevel 1 (
    echo 错误: 环境 'index-tts-dev' 不存在
    echo.
    echo 请先运行 虚拟环境-初始化.bat 创建环境
    echo.
    set /p create_now="是否现在创建环境？(y/n): "
    if /i "%create_now%"=="y" (
        echo.
        echo 正在运行环境初始化脚本...
        call "虚拟环境-初始化.bat"
        if errorlevel 1 (
            echo 环境创建失败！
            pause
            exit /b 1
        )
    ) else (
        echo 请手动运行 虚拟环境-初始化.bat 创建环境
        pause
        exit /b 1
    )
)

echo ✅ 检测到环境 'index-tts-dev' 已存在
echo.

REM 检查当前是否已经在目标环境中
if "%CONDA_DEFAULT_ENV%"=="index-tts-dev" (
    echo ℹ️  您已经在 'index-tts-dev' 环境中
    echo.
    echo 当前环境信息:
    echo 环境名称: %CONDA_DEFAULT_ENV%
    echo Python 版本: 
    python --version
    echo.
    echo 已安装的包数量:
    pip list | find /c /v ""
    echo.
    echo 环境已激活，无需重复激活
    echo.
    pause
    exit /b 0
)

echo 正在激活环境 'index-tts-dev'...
echo.

REM 激活环境
call conda activate index-tts-dev

if errorlevel 1 (
    echo ❌ 环境激活失败！
    echo.
    echo 可能的原因:
    echo 1. 环境损坏
    echo 2. conda 配置问题
    echo 3. 权限问题
    echo.
    echo 解决方案:
    echo 1. 重新创建环境: 虚拟环境-初始化.bat
    echo 2. 重新初始化 conda: conda init
    echo 3. 重启命令行窗口
    echo.
    pause
    exit /b 1
)

echo ✅ 环境激活成功！
echo.

echo ========================================
echo    环境信息
echo ========================================
echo.

echo 环境名称: %CONDA_DEFAULT_ENV%
echo 环境路径: %CONDA_PREFIX%
echo Python 版本: 
python --version
echo.

echo 已安装的包数量:
pip list | find /c /v ""

echo.
echo ========================================
echo    可用命令
echo ========================================
echo.

echo 项目相关:
echo   - 更新子模块: 子模块TTS2-更新.bat
echo   - 推送更新: 子模块TTS2-推送.bat
echo   - 启动项目: 子模块TTS2-启动.bat
echo.

echo Python 相关:
echo   - 查看包列表: pip list
echo   - 安装包: pip install <package>
echo   - 更新包: pip install --upgrade <package>
echo   - 查看 Python 路径: where python
echo.

echo 环境管理:
echo   - 退出环境: conda deactivate
echo   - 查看环境: conda info --envs
echo   - 更新环境: conda env update -f environment.yml
echo.

echo ========================================
echo    环境已激活！
echo ========================================
echo.

echo 提示: 要退出环境，请运行: conda deactivate
echo.

REM 检查是否有项目文件
if exist "src" (
    echo 检测到项目文件，您可以开始开发了！
    echo.
    set /p start_project="是否要启动项目？(y/n): "
    if /i "%start_project%"=="y" (
        echo.
        echo 正在启动项目...
        call "子模块TTS2-启动.bat"
    )
) else (
    echo 未检测到项目文件，请确保在正确的目录中运行此脚本
)

echo.
pause
