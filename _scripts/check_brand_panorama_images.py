#!/usr/bin/env python3
"""
v12 铁律 11 自检 — 17 品牌全景 = 17 张真图
检查 BRAND PANORAMA / 17 品牌 段的每一行是否有真 img,返回 0 = 通过,1 = 失败
"""
import sys
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("usage: check_brand_panorama_images.py <issue_id>")
    sys.exit(1)

issue_id = sys.argv[1]
root = Path(__file__).resolve().parent.parent
issue_dir = root / issue_id
index = issue_dir / "index.html"

if not index.exists():
    print(f"[X] {index} 不存在")
    sys.exit(1)

html = index.read_text(encoding="utf-8")

# 找 17 品牌全景段(常见关键词)
panorama_patterns = [
    r"BRAND\s*PANORAMA",
    r"17\s*品牌",
    r"品牌全景",
    r"全景墙",
]
panorama_match = None
for pat in panorama_patterns:
    m = re.search(pat, html, re.IGNORECASE)
    if m:
        panorama_match = m
        break

if not panorama_match:
    print(f"[!] 未找到品牌全景段 — 如果本期无此段,可跳过")
    sys.exit(0)

# 取全景段后 6000 字符(因为 17 品牌墙通常很长)
start = panorama_match.start()
panorama_section = html[start:start + 6000]

imgs = re.findall(r'<img[^>]+src="([^"]+)"', panorama_section)
unique_imgs = set(imgs)

print(f"BRAND PANORAMA 段含 img: {len(imgs)} ({len(unique_imgs)} 唯一)")

# 阈值:至少 17 张图(17 品牌每品牌 1 张)
required = 17
if len(unique_imgs) < required:
    print(f"\n[X] 铁律 11 失败 — 品牌全景图 {len(unique_imgs)} 张 < {required} 张")
    print(f"    老板原话(2026-07-07):「其他位置参考也没图」")
    sys.exit(1)

print(f"\n[OK] 铁律 11 通过 — 品牌全景 {len(unique_imgs)} ≥ {required} 张真图")
sys.exit(0)
