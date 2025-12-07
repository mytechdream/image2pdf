# Image to PDF Converter - 打包说明

## 打包脚本说明

本项目提供了两种打包方式，您可以根据需求选择：

### 方式一：单文件模式（推荐用于分发）
**脚本：`build.bat`**

**优点：**
- ✅ 生成单个 exe 文件，方便分发
- ✅ 用户只需复制一个文件即可运行

**缺点：**
- ⚠️ 文件体积较大（约 100-200 MB）
- ⚠️ 首次启动较慢（需要解压临时文件）

**使用方法：**
```cmd
build.bat
```

**输出：**
- `dist\Image2PDF.exe` - 可独立运行的单个可执行文件

---

### 方式二：文件夹模式（推荐用于开发测试）
**脚本：`build_onedir.bat`**

**优点：**
- ✅ 启动速度快
- ✅ 总体积较小
- ✅ 便于调试

**缺点：**
- ⚠️ 需要复制整个文件夹
- ⚠️ 包含多个文件和 DLL

**使用方法：**
```cmd
build_onedir.bat
```

**输出：**
- `dist\Image2PDF\` - 包含可执行文件和依赖的文件夹
- `dist\Image2PDF\Image2PDF.exe` - 主程序

---

## 打包前准备

### 1. 确保已安装所有依赖
```cmd
pip install -r requirements.txt
```

### 2. 测试应用程序
```cmd
python main.py
```
确保程序能够正常运行，没有错误。

---

## 打包步骤

### 快速打包
1. 双击运行 `build.bat` 或 `build_onedir.bat`
2. 等待打包完成（可能需要 2-5 分钟）
3. 在 `dist` 文件夹中找到生成的可执行文件

### 手动打包（高级用户）
如果需要自定义打包参数，可以使用 spec 文件：

```cmd
pyinstaller build.spec
```

---

## 自定义配置

### 添加应用图标
1. 准备一个 `.ico` 格式的图标文件（建议 256x256 像素）
2. 将图标文件放在项目根目录，命名为 `icon.ico`
3. 编辑 `build.spec` 文件，修改这一行：
   ```python
   icon='icon.ico'
   ```

### 修改应用程序名称
在 `build.spec` 或批处理脚本中修改 `name` 参数：
```python
name='你的应用名称'
```

---

## 常见问题

### Q1: 打包后程序无法运行
**解决方案：**
- 检查是否有杀毒软件拦截
- 尝试以管理员身份运行
- 查看是否缺少 Visual C++ 运行库

### Q2: 打包失败，提示缺少模块
**解决方案：**
- 确保虚拟环境中安装了所有依赖
- 在 `build.spec` 的 `hiddenimports` 中添加缺少的模块

### Q3: 生成的文件太大
**解决方案：**
- 使用 `build_onedir.bat` 而不是 `build.bat`
- 移除不必要的依赖包
- 使用 UPX 压缩（已在 spec 文件中启用）

### Q4: 打包速度很慢
**解决方案：**
- 这是正常现象，PyInstaller 需要分析所有依赖
- 后续打包会使用缓存，速度会快一些
- 可以删除 `build` 文件夹以清理缓存

---

## 分发建议

### 单文件模式 (build.bat)
1. 将 `dist\Image2PDF.exe` 复制给用户
2. 用户可以直接双击运行
3. 建议压缩为 ZIP 文件分发

### 文件夹模式 (build_onedir.bat)
1. 将整个 `dist\Image2PDF\` 文件夹打包为 ZIP
2. 用户解压后运行 `Image2PDF.exe`
3. 可以创建快捷方式到桌面

---

## 测试清单

打包完成后，建议进行以下测试：

- [ ] 程序能否正常启动
- [ ] 能否添加图片
- [ ] 能否调整参数（页面大小、旋转等）
- [ ] 预览功能是否正常
- [ ] 能否导出 PDF
- [ ] 在没有安装 Python 的电脑上能否运行

---

## 技术说明

### 打包工具
- **PyInstaller 6.0+** - Python 应用打包工具

### 包含的依赖
- PyQt5 - GUI 框架
- Pillow - 图像处理
- ReportLab - PDF 生成
- PyMuPDF - PDF 预览

### 打包原理
PyInstaller 将 Python 解释器、项目代码和所有依赖打包成可执行文件，使得应用可以在没有安装 Python 的环境中运行。

---

## 高级选项

### 减小文件体积
编辑 `build.spec`，添加排除模块：
```python
excludes=['tkinter', 'matplotlib', 'numpy'],
```

### 添加数据文件
如果需要包含额外的资源文件：
```python
datas=[('resources', 'resources')],
```

### 启用控制台（用于调试）
在 spec 文件中设置：
```python
console=True
```

---

## 需要帮助？

如果遇到问题，请检查：
1. PyInstaller 输出的错误信息
2. 是否所有依赖都已正确安装
3. Python 版本是否兼容（建议 Python 3.8+）

---

**祝您打包顺利！** 🎉
