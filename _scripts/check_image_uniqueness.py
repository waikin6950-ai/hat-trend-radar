#!/usr/bin/env python3
"""
v12 铁律 10 自检 — 同图 0 复用
检查 HTML 中 src= 是否每张图片只出现 1 次,返回 0 = 通过,1 = 失败
W27 失败案例: dodgers-usa250.png 被复用 5 次
"""
import sys
import re
from collections import Counter
from pathlib import Path

if len(sys.argv) < 2:
    print("usage: check_image_uniqueness.py <issue_id>")
    sys.exit(1)

issue_id = sys.argv[1]
root = Path(__file__).resolve().parent.parent
index = root / issue_id / "index.html"

if not index.exists():
    print(f"[X] {index} 不存在")
    sys.exit(1)

html = index.read_text(encoding="utf-8")

# 提取所有 img src + background-image url
srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
bgs = re.findall(r'background-image\s*:\s*url\(["\']?([^"\')\s]+)', html)
all_imgs = srcs + bgs

counter = Counter(all_imgs)
repeated = {k: v for k, v in counter.items() if v > 1}

print(f"图地址总数: {len(all_imgs)}")
print(f"唯一图数: {len(counter)}")

if repeated:
    print(f"\n[X] 铁律 10 失败 — {len(repeated)} 张图被重复使用:")
    for img, count in sorted(repeated.items(), key=lambda x: -x[1]):
        print(f"    {count} 次: {img}")
    print(f"\n    老板原话(2026-07-07):「图片也是重复」")
    sys.exit(1)

print(f"\n[OK] 铁律 10 通过 — 同图 0 复用")
sys.exit(0)
