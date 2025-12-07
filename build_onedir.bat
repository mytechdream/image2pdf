@echo off
chcp 65001 >nul
echo ==========================================
echo   Image to PDF Converter - 打包脚本
echo   (文件夹模式 - 体积更小，启动更快)
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
echo [✓] 清理完成

echo.
echo [4/5] 开始打包应用程序（文件夹模式）...
echo 这可能需要几分钟时间，请耐心等待...
echo.

pyinstaller --name=Image2PDF ^
    --windowed ^
    --onedir ^
    --clean ^
    --noconfirm ^
    --add-data "*.py;." ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=reportlab.pdfbase._fontdata ^
    --hidden-import=reportlab.pdfbase._cidfontdata ^
    main.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [5/5] 验证打包结果...
if exist "dist\Image2PDF\Image2PDF.exe" (
    echo.
    echo ==========================================
    echo   打包成功！
    echo ==========================================
    echo.
    echo 应用程序文件夹: dist\Image2PDF\
    echo 可执行文件: dist\Image2PDF\Image2PDF.exe
    echo.
    echo 提示：
    echo - 需要将整个 Image2PDF 文件夹复制到目标位置
    echo - 不要单独复制 exe 文件，需要配套的 DLL 文件
    echo - 文件夹模式启动速度更快，占用空间更小
    echo - 可以为 Image2PDF.exe 创建快捷方式放到桌面
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
