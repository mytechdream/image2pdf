@echo off
chcp 65001 >nul
echo ==========================================
echo   Image to PDF Converter - 打包脚本
echo ==========================================
echo.

REM 检查是否在虚拟环境中
if not defined VIRTUAL_ENV (
    echo [警告] 未检测到虚拟环境
    echo 建议在虚拟环境中运行此脚本
    echo 是否继续？
    pause
)

echo [1/5] 检查依赖...
python -c "import PyQt5, PIL, reportlab, fitz" 2>nul
if errorlevel 1 (
    echo [错误] 缺少必要的依赖包
    echo 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请手动运行：pip install -r requirements.txt
        pause
        exit /b 1
    )
)
echo [✓] 依赖检查完成

echo.
echo [2/5] 检查 PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [提示] PyInstaller 未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)
echo [✓] PyInstaller 已就绪

echo.
echo [3/5] 清理旧的构建文件...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist "Image2PDF.spec" del /q "Image2PDF.spec"
echo [✓] 清理完成

echo.
echo [4/5] 开始打包应用程序...
echo 这可能需要几分钟时间，请耐心等待...
echo.
pyinstaller build.spec

if errorlevel 1 (
    echo.
    echo [错误] 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [5/5] 验证打包结果...
if exist "dist\Image2PDF.exe" (
    echo.
    echo ==========================================
    echo   打包成功！
    echo ==========================================
    echo.
    echo 可执行文件位置: dist\Image2PDF.exe
    echo.
    echo 提示：
    echo - 可以将 dist\Image2PDF.exe 复制到任何位置运行
    echo - 首次运行可能需要较长时间加载
    echo - 如需创建快捷方式，右键点击 exe 文件选择"创建快捷方式"
    echo.
    
    REM 获取文件大小
    for %%A in ("dist\Image2PDF.exe") do set size=%%~zA
    set /a size_mb=%size% / 1048576
    echo 文件大小: 约 %size_mb% MB
    echo.
    
    echo 是否打开 dist 文件夹？
    choice /c YN /m "按 Y 打开，按 N 退出"
    if errorlevel 2 goto end
    if errorlevel 1 explorer dist
) else (
    echo.
    echo [错误] 未找到生成的可执行文件
    echo 请检查 PyInstaller 输出的错误信息
)

:end
echo.
pause
