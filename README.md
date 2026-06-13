# 🎩 帽类潮流雷达 (Hat Trend Radar)

> 帽类工厂设计部每周潮流资讯仪表板
> Powered by Rex · Designer Agent

## 📡 在线访问

部署后可通过 Cloudflare Pages 访问。

## 🎯 用途

每周自动收集全球帽类潮流资讯：
- 大牌新品 / Lookbook（Supreme、'47、Carhartt WIP、New Era、Stussy、Kangol）
- 街头潮流（HYPEBEAST、Highsnobiety、小红书）
- 电商爆款（Amazon Best Sellers、Hatclub、Lids）
- 流行色趋势（Pantone）

整理成可视化周报，分享给设计部全体成员。

## 📅 更新频率

- **每日 9:00**：数据采集
- **每周日 20:00**：生成本周报告
- **每周一 8:30**：推送 WeCom + 邮件

## 🔗 数据真实性

所有信息均附原始来源链接，可点击跳转溯源。

## 📐 技术栈

- HTML + Tailwind CSS + Chart.js
- 数据采集：Tavily Search + web_fetch + Agent Browser
- AI 分析：云端模型（doubao / minimax）
- 自动部署：GitHub + Cloudflare Pages

---

*Built for hat factory design team · 2026*
