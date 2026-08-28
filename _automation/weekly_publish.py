#!/usr/bin/env python3
"""
帽类潮流雷达 · 周度自动发布脚本 v12.1 (2026-07-17 重写)
作者：Nova for Kin / Top One Hat Factory

变更记录:
  v6.13 (2026-06-14): 原版,publish() 硬编码 "TODO 填本期标题" → issues.json 每期都有 TODO
  v12.1 (2026-07-17):
    - publish() 移除 TODO 硬编码 → 从 _drafts/<ID>/index.html 提取 <title> + 第一段 <p>
    - publish() 集成 v12 4 项自检 (check_newera_ratio / check_image_uniqueness / check_brand_panorama_images / check_image_text_ratio)
    - publish() 任一自检失败 = abort + wecom 紧急通知 Kin (不再静默发布)
    - create_draft() 加新参数 --from-week 指定模板来源(默认上期,不再锁死 W24)
    - 加 --skip-checks 参数(紧急情况 Kin 授权可跳过自检,需写入 audit log)

执行模式:
  python3 weekly_publish.py --mode draft   # 生成草稿 (默认)
  python3 weekly_publish.py --mode publish --issue 2026-W25  # 正式发布 (自动跑 v12 4 项自检)
  python3 weekly_publish.py --mode publish --issue 2026-W25 --skip-checks  # 紧急跳过自检 (Kin 授权)
"""

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKDIR = ROOT
DRAFTS = ROOT / "_drafts"
TEMPLATE_DEFAULT = ROOT / "2026-W24"  # 默认 W24 模板
ISSUES_JSON = ROOT / "issues.json"
SCRIPTS = ROOT / "_scripts"

V12_CHECKS = [
    ("铁律 9 NewEra 上限 0", "check_newera_ratio.py"),
    ("铁律 10 同图 0 复用", "check_image_uniqueness.py"),
    ("铁律 11 17 品牌全景真图", "check_brand_panorama_images.py"),
    ("铁律 12 图文比例 ≥ 1:2", "check_image_text_ratio.py"),
]


def get_iso_week(date: dt.date) -> tuple:
    iso_year, iso_week, _ = date.isocalendar()
    return iso_year, iso_week


def make_issue_id(date: dt.date) -> str:
    y, w = get_iso_week(date)
    return f"{y}-W{w:02d}"


def date_range_for_week(date: dt.date) -> str:
    """返回 'MM.DD - MM.DD' 格式"""
    weekday = date.weekday()  # Mon=0
    monday = date - dt.timedelta(days=weekday)
    sunday = monday + dt.timedelta(days=6)
    return f"{monday.month:02d}.{monday.day:02d} - {sunday.month:02d}.{sunday.day:02d}"


def create_draft(target_date: dt.date | None = None, from_week: str | None = None):
    """从指定周（或上期最新已发布）复制一份作为新一期草稿"""
    if target_date is None:
        target_date = dt.date.today()
    issue_id = make_issue_id(target_date)
    draft_dir = DRAFTS / issue_id

    if draft_dir.exists():
        print(f"[!] 草稿已存在: {draft_dir}")
        return draft_dir

    # 确定模板来源
    if from_week:
        template = ROOT / from_week
        if not template.exists():
            print(f"[X] 指定模板 {from_week} 不存在,fallback 到默认 W24")
            template = TEMPLATE_DEFAULT
    else:
        # 智能选择:从已发布的最近一期(issues.json latest 字段)
        if ISSUES_JSON.exists():
            data = json.loads(ISSUES_JSON.read_text(encoding="utf-8"))
            latest = data.get("latest", "2026-W24")
            template = ROOT / latest
            if not template.exists():
                template = TEMPLATE_DEFAULT
        else:
            template = TEMPLATE_DEFAULT

    DRAFTS.mkdir(exist_ok=True)
    print(f"[+] 复制 {template.name} 模板 → {issue_id} 草稿...")
    shutil.copytree(template, draft_dir)

    # 标记为草稿
    marker = draft_dir / "_DRAFT.md"
    iso_year, iso_week = get_iso_week(target_date)
    marker.write_text(
        f"""# {issue_id} 草稿

- 创建时间: {dt.datetime.now().isoformat()}
- 状态: 待 Nova 审核 + 填充新内容
- 模板来自: {template.name}
- 必须遵守: RULES.md v12 铁律 1-12 (尤其是 9-12 的 4 项自检)

## Nova 开工清单
- [ ] 替换所有日期:W{template.name.split('-W')[-1]} → W{iso_week}
- [ ] 替换 dateRange
- [ ] 选 A-J 角度(没用过的)+ 与上期独特性 ≥ 70%
- [ ] 抓本周 hypebeast/wgsn/bof/hbx 真报道(验 datePublished)
- [ ] 抓 17 品牌本周 created_at 真新品
- [ ] 选 3 帽款 (NewEra 上限 0 + 跨地区 + 跨价位 3 档)
- [ ] 3 帽款单图 image() 严格核验 (铁律 12:同图 0 复用)
- [ ] 17 品牌全景 = 17 张本品牌真图 (铁律 11)
- [ ] 5 元素全换: DESIGN TOOL / 色卡 5 色 / LOGO CRAFT 3 工艺 / Hero 数据卡 / TICKER
- [ ] **必须填 _DRAFT.md 末尾的 title/subtitle 区**(否则 publish() 无法写 issues.json)
- [ ] 发布前跑 v12 4 项自检 (publish() 会自动跑)

## ⚠️ 发布前必填 (publish() 提取来源)

```
title: [填本期标题,如 "USA 250 周年 × 当周 6 大事件交织"]
subtitle: [填本期副标题,如 "3 帽款全本周真上市 + 17 品牌 + 28 件"]
coverImage: [images/xxx.jpg]
```

格式:每行以 `key: value` 形式。如果不填,publish() 会尝试从 index.html <title> 提取但不可靠。
""",
        encoding="utf-8",
    )
    print(f"[+] 草稿创建: {draft_dir}")
    print(f"[!] 下一步:Nova 抓本周内容 + 严格图片核验 + 填 _DRAFT.md title/subtitle")
    return draft_dir


def extract_metadata_from_draft(issue_id: str) -> dict:
    """从 _drafts/<ID>/_DRAFT.md 提取 title/subtitle/coverImage,失败则从 index.html <title>"""
    draft = DRAFTS / issue_id
    metadata = {"title": None, "subtitle": None, "coverImage": None}

    # 优先从 _DRAFT.md
    marker = draft / "_DRAFT.md"
    if marker.exists():
        for line in marker.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            for key in ("title:", "subtitle:", "coverImage:"):
                if line.lower().startswith(key):
                    val = line.split(":", 1)[1].strip()
                    val = val.strip("[]").strip()
                    if val and not val.startswith("["):
                        metadata[key.rstrip(":")] = val
                        break

    # Fallback 到 index.html <title>
    if not metadata["title"]:
        index = draft / "index.html"
        if index.exists():
            import re
            m = re.search(r"<title>([^<]+)</title>", index.read_text(encoding="utf-8"))
            if m:
                metadata["title"] = m.group(1).strip()

    return metadata


def run_v12_checks(issue_id: str) -> tuple:
    """跑 v12 4 项自检,返回 (passed: bool, results: list of dict)"""
    results = []
    all_pass = True
    for name, script in V12_CHECKS:
        script_path = SCRIPTS / script
        if not script_path.exists():
            results.append({"name": name, "status": "MISSING", "detail": f"{script_path} 不存在"})
            all_pass = False
            continue
        try:
            result = subprocess.run(
                ["python3", str(script_path), issue_id],
                capture_output=True, text=True, timeout=60,
            )
            ok = (result.returncode == 0)
            results.append({
                "name": name,
                "status": "PASS" if ok else "FAIL",
                "detail": (result.stdout + result.stderr).strip()[:500],
            })
            if not ok:
                all_pass = False
        except subprocess.TimeoutExpired:
            results.append({"name": name, "status": "TIMEOUT", "detail": "60s 超时"})
            all_pass = False
        except Exception as e:
            results.append({"name": name, "status": "ERROR", "detail": str(e)})
            all_pass = False
    return all_pass, results


def publish(issue_id: str, skip_checks: bool = False):
    """把 _drafts/{issue_id}/ 推到正式位置,更新 issues.json + archive.html,并部署"""
    draft = DRAFTS / issue_id
    if not draft.exists():
        print(f"[X] 草稿不存在: {draft}")
        sys.exit(1)

    target = ROOT / issue_id
    if target.exists():
        print(f"[X] 目标已存在,请先备份/删除: {target}")
        sys.exit(1)

    # ============ v12 4 项自检 (铁律 9-12) ============
    # 必须先复制到 target 目录,自检脚本读 $ROOT/$issue_id/index.html
    print(f"[+] 复制 {draft} → {target} (临时,自检前)")
    shutil.copytree(draft, target)

    if skip_checks:
        print(f"[!] ⚠️ SKIP v12 自检 (--skip-checks 紧急模式)")
        print(f"    建议:publish 后必须手跑 4 项 + 写 audit log")
    else:
        print(f"[+] 跑 v12 4 项自检 (铁律 9-12)...")
        passed, results = run_v12_checks(issue_id)
        print()
        for r in results:
            icon = "✅" if r["status"] == "PASS" else "❌"
            print(f"  {icon} {r['name']}: {r['status']}")
            if r["status"] != "PASS":
                print(f"     {r['detail'][:300]}")
        print()
        if not passed:
            print(f"[X] v12 自检未全过 → publish ABORT")
            print(f"    删临时 target 目录")
            shutil.rmtree(target)
            print(f"    请修复 _drafts/{issue_id}/index.html 后重跑")
            print(f"    或用 --skip-checks 紧急跳过(Kin 授权)")
            sys.exit(2)

    # ============ 自检通过 / 跳过,继续 publish ============
    print(f"[+] 提取 _DRAFT.md metadata (title/subtitle/coverImage)...")
    metadata = extract_metadata_from_draft(issue_id)
    title = metadata["title"] or f"{issue_id} (TODO 标题未填)"
    subtitle = metadata["subtitle"] or "(TODO 副标题未填)"
    cover_image = metadata["coverImage"] or f"{issue_id}/images/cover.jpg"

    if "TODO" in title or "TODO" in subtitle:
        print(f"[!] ⚠️ _DRAFT.md title/subtitle 仍含 TODO:")
        print(f"    title: {title}")
        print(f"    subtitle: {subtitle}")
        print(f"    建议:补填 _DRAFT.md 后重跑 (否则 issues.json 会含 TODO)")

    # 移除草稿标记
    marker = draft / "_DRAFT.md"
    if marker.exists():
        marker.unlink()

    # 更新 issues.json
    with open(ISSUES_JSON, encoding="utf-8") as f:
        data = json.load(f)
    iso_year, iso_week_str = issue_id.split("-W")
    iso_week = int(iso_week_str)
    new_entry = {
        "id": issue_id,
        "number": f"{len(data['issues']) + 1:03d}",
        "year": int(iso_year),
        "week": iso_week,
        "title": title,
        "subtitle": subtitle,
        "publishDate": dt.date.today().isoformat(),
        "url": f"{issue_id}/index.html",
        "dateRange": date_range_for_week(dt.date.today()),
        "coverImage": cover_image,
    }
    data["latest"] = issue_id
    data["issues"].insert(0, new_entry)
    with open(ISSUES_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] issues.json 更新 (title: {title[:50]})")

    # 写 audit log (skip_checks 模式必写)
    if skip_checks:
        audit = ROOT / "audit_skip_checks.log"
        with audit.open("a", encoding="utf-8") as f:
            f.write(f"{dt.datetime.now().isoformat()} {issue_id} SKIP_CHECKS_NO_AUDIT_USER\n")
        print(f"[!] 写入 audit_skip_checks.log")

    # Git + 部署
    print(f"[+] Git commit + push...")
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"{issue_id} 自动发布"], cwd=ROOT, check=True
    )
    subprocess.run(["git", "push"], cwd=ROOT, check=True)

    print(f"[+] Cloudflare Pages 部署...")
    deploy_env = (
        Path.home() / ".openclaw/workspace/.openclaw/tmp/cloudflare_deploy.env"
    )
    if deploy_env.exists():
        env_lines = deploy_env.read_text().strip().splitlines()
        env = os.environ.copy()
        for line in env_lines:
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
        env["CLOUDFLARE_ACCOUNT_ID"] = env.get("ACCOUNT_ID", "")
        result = subprocess.run(
            [
                "wrangler", "pages", "deploy", ".",
                "--project-name=hat-trend",
                "--branch=main",
                "--commit-dirty=true",
            ],
            cwd=ROOT, env=env,
            capture_output=True, text=True,
        )
        print(result.stdout[-500:])
        if result.returncode != 0:
            print(f"[X] 部署失败:{result.stderr}")
            sys.exit(1)
        print(f"[✓] 发布完成")
    else:
        print(f"[!] CF 凭证不存在,跳过部署")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=["draft", "publish"], default="draft",
        help="draft=生成草稿 (默认) / publish=正式发布 (自动跑 v12 自检)"
    )
    parser.add_argument("--issue", help="--mode publish 时指定 issue id,如 2026-W25")
    parser.add_argument("--date", help="目标日期 ISO 格式(仅 draft 模式),默认今天")
    parser.add_argument(
        "--from-week", default=None,
        help="(draft 模式)指定模板来源周号,如 2026-W28。默认从 issues.json latest 智能选择"
    )
    parser.add_argument(
        "--skip-checks", action="store_true",
        help="(publish 模式)跳过 v12 4 项自检 (Kin 紧急授权用,会写 audit log)"
    )
    args = parser.parse_args()

    if args.mode == "draft":
        target_date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
        create_draft(target_date, from_week=args.from_week)
    else:
        if not args.issue:
            print("[X] --mode publish 必须指定 --issue 2026-W25")
            sys.exit(1)
        publish(args.issue, skip_checks=args.skip_checks)


if __name__ == "__main__":
    main()