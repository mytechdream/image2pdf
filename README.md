# Image to PDF Converter

一个功能强大的桌面应用程序，用于将图片转换为 PDF 文件，类似于 Adobe Acrobat 的图片拼接工具。

## 功能特性

- **多种页面格式支持**：A4、A3、A5、Letter、Legal、Tabloid
- **图片处理功能**：
  - 调整大小和缩放
  - 旋转（0°、90°、180°、270°）
  - 自定义位置
  - 裁剪功能
- **实时预览**：左侧显示 PDF 预览，右侧显示参数调整面板
- **白色背景**：图片可放置在可配置的白色背景上
- **批量处理**：支持添加多张图片，生成多页 PDF
- **图片顺序管理**：可上下移动图片调整页面顺序
- **PDF 拼接**：合并多个 PDF 文件为单个文档

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

## 使用说明

### 图片转 PDF

1. **添加图片**：
   - 点击"Add Images"按钮或使用 Ctrl+O
   - 选择一张或多张图片文件

2. **调整参数**：
   - 在右侧面板选择页面格式（A4等）
   - 选择背景颜色
   - 设置边距
   - 对于每张图片，可以调整：
     - 缩放比例
     - 位置（X和Y坐标）
     - 旋转角度
     - 是否适应页面大小

3. **预览**：
   - 左侧会实时显示当前选中图片的 PDF 预览
   - 参数更改会立即反映在预览中

4. **导出 PDF**：
   - 点击"Export PDF"按钮或使用 Ctrl+S
   - 选择保存位置
   - PDF 文件将包含所有添加的图片

### PDF 拼接

1. **打开合并对话框**：
   - 点击菜单 "File" → "Merge PDFs..." 或使用 Ctrl+M
   - 或点击工具栏的 "Merge PDFs" 按钮

2. **添加 PDF 文件**：
   - 点击 "Add PDFs..." 按钮
   - 选择要合并的 PDF 文件（可多选）
   - 文件将显示在列表中，附带页数信息

3. **调整顺序**：
   - 使用 "↑ Move Up" 和 "↓ Move Down" 按钮调整文件顺序
   - 合并后的 PDF 将按列表顺序排列

4. **合并文件**：
   - 点击 "Merge PDFs..." 按钮
   - 选择输出文件位置
   - 等待合并完成

## 技术栈

- **PyQt5**：GUI 框架
- **Pillow (PIL)**：图片处理
- **reportlab**：PDF 生成
- **PyMuPDF (fitz)**：PDF 渲染和合并

## 项目结构

```
image2pdf/
├── main.py              # 应用程序入口
├── main_window.py       # 主窗口
├── preview_widget.py    # 预览组件
├── control_panel.py     # 控制面板
├── pdf_generator.py     # PDF 生成器
├── pdf_merger.py        # PDF 合并模块
├── pdf_merge_dialog.py  # PDF 合并对话框
├── image_processor.py   # 图片处理模块
├── models.py            # 数据模型
├── page_formats.py      # 页面格式定义
└── requirements.txt     # 依赖列表
```

## 快捷键

- `Ctrl+O`：添加图片
- `Ctrl+S`：导出 PDF
- `Ctrl+M`：合并 PDF 文件
- `Ctrl+Q`：退出程序

## 打包发布

查看 [BUILD_GUIDE.md](BUILD_GUIDE.md) 了解如何将应用打包为可执行文件。

## 许可证

MIT License
