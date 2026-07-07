#!/usr/bin/env python3
"""
v12 铁律 12 自检 — 图为主角,文为注释 (img_count ≥ p_count/2)
检查 img 数 vs 文字段(p/li/h1-6)数比例,返回 0 = 通过,1 = 失败
W27 失败案例: 85 段文字 : 17 处图 = 5:1 (披图皮)
"""
import sys
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("usage: check_image_text_ratio.py <issue_id>")
    sys.exit(1)

issue_id = sys.argv[1]
root = Path(__file__).resolve().parent.parent
index = root / issue_id / "index.html"

if not index.exists():
    print(f"[X] {index} 不存在")
    sys.exit(1)

html = index.read_text(encoding="utf-8")

# 图:img + background-image
imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
bgs = re.findall(r'background-image\s*:\s*url\(["\']?([^"\')\s]+)', html)
img_count = len(set(imgs + bgs))

# 文字段:p + li + h1-6
text_segments = re.findall(r'<p[> ]|<li[> ]|<h[1-6][> ]', html)
text_count = len(text_segments)

ratio = img_count / max(text_count, 1)

print(f"图(img+bg): {img_count} 张唯一")
print(f"文字段(p+li+h): {text_count} 段")
print(f"比例: 1 : {text_count/max(img_count,1):.1f} (图:文)")
print(f"目标: img_count ≥ text_count / 2 = {text_count // 2}")

if img_count < text_count / 2:
    print(f"\n[X] 铁律 12 失败 — 图 {img_count} < 文字段一半 ({text_count // 2})")
    print(f"    老板原话(2026-07-07):「仍是文字比图片多」")
    sys.exit(1)

print(f"\n[OK] 铁律 12 通过 — 图文比例达标")
sys.exit(0)
