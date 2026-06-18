#!/usr/bin/env python3
"""
帽类潮流雷达 · 周度自动发布脚本
作者：Nova for Kin / Top One Hat Factory
最后更新：2026-06-14

执行模式：
  python3 weekly_publish.py --mode draft   # 生成草稿到 _drafts/，给 Nova 审核（默认）
  python3 weekly_publish.py --mode publish --issue 2026-W25  # 正式发布

每周日 20:00 cron 触发 mode=draft，Nova 看到通知后审核 → 让 Kin 拍板 → 才走 publish
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
TEMPLATE_ISSUE = ROOT / "2026-W24"
ISSUES_JSON = ROOT / "issues.json"


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


def create_draft(target_date: dt.date | None = None):
    """从最新一期 (W24) 复制一份作为 W25 草稿，等 Nova 填新内容"""
    if target_date is None:
        target_date = dt.date.today()
    issue_id = make_issue_id(target_date)
    draft_dir = DRAFTS / issue_id

    if draft_dir.exists():
        print(f"[!] 草稿已存在: {draft_dir}")
        return draft_dir

    DRAFTS.mkdir(exist_ok=True)
    print(f"[+] 复制 W24 模板 → {issue_id} 草稿...")
    shutil.copytree(TEMPLATE_ISSUE, draft_dir)

    # 标记为草稿
    marker = draft_dir / "_DRAFT.md"
    iso_year, iso_week = get_iso_week(target_date)
    marker.write_text(
        f"""# {issue_id} 草稿

- 创建时间：{dt.datetime.now().isoformat()}
- 状态：待 Nova 审核 + 填充新内容
- 模板来自：2026-W24

## Nova 审核清单
- [ ] 替换所有日期：W24 → W{iso_week}
- [ ] 替换 dateRange："06.09 - 06.15" → "{date_range_for_week(target_date)}"
- [ ] 抓本周 hypebeast / wgsn / business of fashion 帽类联名
- [ ] 每张帽款图 **单图 image() 严格核验** （铁律）
- [ ] 更新 trends.html 累计期数
- [ ] 替换设计工具（W25 介绍 LOOK AI 或 Refabric）
- [ ] 替换 logo 工艺（W25 介绍 3D Embossed 压胶）
""",
        encoding="utf-8",
    )
    print(f"[+] 草稿创建: {draft_dir}")
    print(f"[!] 下一步：Nova 抓本周内容 + 严格图片核验后填入 → 跑 --mode publish")
    return draft_dir


def publish(issue_id: str):
    """把 _drafts/{issue_id}/ 推到正式位置，更新 issues.json + archive.html，并部署"""
    draft = DRAFTS / issue_id
    if not draft.exists():
        print(f"[X] 草稿不存在: {draft}")
        sys.exit(1)

    target = ROOT / issue_id
    if target.exists():
        print(f"[X] 目标已存在，请先备份/删除: {target}")
        sys.exit(1)

    print(f"[+] 发布 {issue_id} ...")
    # 移除草稿标记
    marker = draft / "_DRAFT.md"
    if marker.exists():
        marker.unlink()
    shutil.copytree(draft, target)

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
        "title": "TODO 填本期标题",
        "subtitle": "TODO 填本期副标题",
        "publishDate": dt.date.today().isoformat(),
        "url": f"{issue_id}/index.html",
    }
    data["latest"] = issue_id
    data["issues"].insert(0, new_entry)
    with open(ISSUES_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] issues.json 更新")

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
                "wrangler",
                "pages",
                "deploy",
                ".",
                "--project-name=hat-trend",
                "--branch=main",
                "--commit-dirty=true",
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        print(result.stdout[-500:])
        if result.returncode != 0:
            print(f"[X] 部署失败：{result.stderr}")
            sys.exit(1)
        print(f"[✓] 发布完成")
    else:
        print(f"[!] CF 凭证不存在，跳过部署")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=["draft", "publish"], default="draft", help="draft=生成草稿 (默认) / publish=正式发布"
    )
    parser.add_argument(
        "--issue", help="--mode publish 时指定要发布的 issue id，如 2026-W25"
    )
    parser.add_argument("--date", help="目标日期 ISO 格式（仅 draft 模式），默认今天")
    args = parser.parse_args()

    if args.mode == "draft":
        target_date = (
            dt.date.fromisoformat(args.date) if args.date else dt.date.today()
        )
        create_draft(target_date)
    else:
        if not args.issue:
            print("[X] --mode publish 必须指定 --issue 2026-W25")
            sys.exit(1)
        publish(args.issue)


if __name__ == "__main__":
    main()
