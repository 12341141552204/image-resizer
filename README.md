# 批量图片尺寸调整工具 (image-resizer)

批量调整图片尺寸，支持等比缩放、指定宽高、裁剪填充等模式。

## 功能

- 按比例缩放（--scale）
- 指定宽度或高度（等比）
- 指定宽高 + 模式选择（contain/cover/stretch）
- 高质量 LANCZOS 重采样

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
# 缩小到 50%
python main.py ./images --scale 0.5

# 指定宽度为 800px（高度等比）
python main.py ./images --width 800

# 指定宽高，等比缩放不裁剪
python main.py ./images --width 1920 --height 1080 --mode contain

# 指定宽高，裁剪填满
python main.py ./images --width 1920 --height 1080 --mode cover
```

## 模式说明

| 模式 | 说明 |
|------|------|
| `contain` | 等比缩放，完整显示，不裁剪（默认） |
| `cover` | 等比缩放，裁剪填满目标尺寸 |
| `stretch` | 拉伸到目标尺寸（可能变形） |

## 依赖

- Pillow
