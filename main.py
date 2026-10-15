#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量图片尺寸调整工具
支持按比例缩放、指定宽度/高度、填充等
"""

import argparse
from pathlib import Path
from PIL import Image


def resize_image(input_path, output_path, width=None, height=None, scale=None, mode="contain"):
    """调整图片尺寸"""
    with Image.open(input_path) as img:
        orig_w, orig_h = img.size

        if scale:
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
        elif width and height:
            if mode == "contain":
                # 等比例缩放，不裁剪
                ratio = min(width / orig_w, height / orig_h)
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
            elif mode == "cover":
                # 等比例缩放，裁剪填满
                ratio = max(width / orig_w, height / orig_h)
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                left = (new_w - width) // 2
                top = (new_h - height) // 2
                img = img.crop((left, top, left + width, top + height))
                img.save(output_path)
                return
            else:  # stretch
                new_w, new_h = width, height
        elif width:
            ratio = width / orig_w
            new_w = width
            new_h = int(orig_h * ratio)
        elif height:
            ratio = height / orig_h
            new_w = int(orig_w * ratio)
            new_h = height
        else:
            img.save(output_path)
            return

        img = img.resize((new_w, new_h), Image.LANCZOS)
        img.save(output_path)


def batch_resize(folder, output_folder, width=None, height=None, scale=None, mode="contain"):
    """批量调整尺寸"""
    folder = Path(folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    supported = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
    count = 0

    for f in folder.iterdir():
        if not f.is_file() or f.suffix.lower() not in supported:
            continue

        out_path = output_folder / f.name
        try:
            resize_image(f, out_path, width=width, height=height, scale=scale, mode=mode)
            with Image.open(f) as orig, Image.open(out_path) as resized:
                print(f"[完成] {f.name}: {orig.size} -> {resized.size}")
            count += 1
        except Exception as e:
            print(f"[失败] {f.name}: {e}")

    print(f"\n共处理 {count} 张图片")


def main():
    parser = argparse.ArgumentParser(description="批量图片尺寸调整工具")
    parser.add_argument("folder", help="图片所在文件夹")
    parser.add_argument("-o", "--output", default="output", help="输出文件夹")
    parser.add_argument("--width", type=int, help="目标宽度")
    parser.add_argument("--height", type=int, help="目标高度")
    parser.add_argument("--scale", type=float, help="缩放比例（如 0.5 表示缩小一半）")
    parser.add_argument("--mode", default="contain", choices=["contain", "cover", "stretch"],
                        help="contain=等比不裁剪, cover=等比裁剪填满, stretch=拉伸")
    args = parser.parse_args()

    if not any([args.width, args.height, args.scale]):
        parser.error("必须指定 --width、--height 或 --scale 之一")

    batch_resize(args.folder, args.output, args.width, args.height, args.scale, args.mode)


if __name__ == "__main__":
    main()
