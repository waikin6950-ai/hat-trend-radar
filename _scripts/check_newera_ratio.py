#!/usr/bin/env python3
"""
v12 铁律 9 自检 — NewEra 上限 0
检查 3 HAT 主角帽款是否为 NewEra,返回 0 = 通过,1 = 失败
"""
import sys
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("usage: check_newera_ratio.py <issue_id>")
    sys.exit(1)

issue_id = sys.argv[1]
root = Path(__file__).resolve().parent.parent
issue_dir = root / issue_id
index = issue_dir / "index.html"

if not index.exists():
    print(f"[X] {index} 不存在")
    sys.exit(1)

html = index.read_text(encoding="utf-8")

# 找 3 HAT 段（h3 含帽款名）
hat_section = re.findall(
    r"<h3[^>]*display[^>]*>(.*?)</h3>",
    html,
    re.DOTALL | re.IGNORECASE,
)

print(f"找到 {len(hat_section)} 个 H3 段")
newera_count = 0
hats = []
for h in hat_section:
    # 剥离 HTML 标签
    text = re.sub(r"<[^>]+>", " ", h)
    text = re.sub(r"\s+", " ", text).strip()
    is_newera = bool(re.search(r"new\s*era|\bNE\b", text, re.IGNORECASE))
    hats.append((text[:60], is_newera))
    if is_newera:
        newera_count += 1
    marker = "[NE]" if is_newera else "[OK]"
    print(f"  {marker} {text[:60]}")

print(f"\nNewEra 命中: {newera_count}/3")

if newera_count > 0:
    print(f"[X] 铁律 9 失败 — NewEra 上限 0,实测 {newera_count}/3")
    print(f"    老板原话(2026-07-07):「每期都是 new era 的帽, 完全没新意」")
    sys.exit(1)

print(f"[OK] 铁律 9 通过 — 3 帽款全非 NewEra")
sys.exit(0)
