# Hat Trend Radar — 永久铁律

> 老板 2026-06-19 00:25 定调："**每期都要耳目一新,要令所有人眼前一亮**"
> 这是项目存在的唯一意义。每期不达到这个标准 = 项目失败。

---

## 🔴 核心铁律（违反就是失职）

> **2026-07-07 21:14 老板 v12 升级**:W25/W26/W27 架构有问题(图片重复/参考位置没图/文字比图多/全是 NewEra)。以下铁律 9-12 为 v12 新增,违反 = 项目失败。



### 铁律 1 — 每期必须主题不同
- 不能两期连续做同样路线（比如 W25 已经做过 "跨品牌联名"，W26 必须换角度）
- **每期换一个观察维度**：
  - 角度 A：跨品牌联名（W25 做过）
  - 角度 B：单一品牌深度（比如 NewEra 一年的 colorway 演变）
  - 角度 C：地理性（比如东京 / 巴黎 / 米兰本周新店开业 / 限定）
  - 角度 D：工艺集中（比如本周 5 顶帽都用什么新刺绣工艺）
  - 角度 E：人物 / 设计师（比如 Verdy / Jerry Lorenzo / Daniel Arnold 本周动作）
  - 角度 F：奢侈品 vs 街头（比如 LV / Dior / Hermès 本周帽款分析）
  - 角度 G：体育即时纪念（NBA / NFL / MLB / EPL / F1 / Olympics 等夺冠 / 关键事件）
  - 角度 H：节日 / 季节性（开学季 / 父亲节 / 黑五 / 圣诞 / 情人节等）
  - 角度 I：颜色 / 材质潮流（比如本周哪种颜色突然火 / 哪种材质回归）
  - 角度 J：复古回潮（比如本周哪个 90s/Y2K/2010s 元素被重新挖出来）

### 铁律 2 — 模板复用率上限 30%
- 与上一期 HTML 文件 diff 后,新增内容必须 ≥ 70%（独特性 ≥ 70%）
- 上版 W24 → W25 第一版 = 12.6% 独特性 → 被批
- 上版 W25 → W25 v3 = 45.2% 独特性 → 老板说 "一般般"（仍不够）
- **W26 起目标 ≥ 70% 独特性**

### 铁律 3 — 每期换 3 个核心元素
| 必须每期换的元素 | W24 内容 | W25 v3 内容 | W26 必须换成 |
|---|---|---|---|
| **DESIGN TOOL** | Vizcom AI 渲染 | 水钻外协 3 家询价指南 | 必须再换（比如 3D 打印 / Khroma 配色）|
| **本周色卡 5 色** | 暖色调（Cloud Dancer 等）| 羊毛棕 / 学院蓝 / 总冠军白 / 皇家蓝 / 水晶透明 | 必须再换 |
| **LOGO CRAFT 3 工艺** | Chenille / Quidditch | 复古平绣 / Side Patch / Swarovski 水钻 | 必须再换 |
| **3 帽款主角** | 不同 | Pluto / Knicks / Swar47 | 必须再换 |
| **Hero 数据卡 4 项** | 略有不同 | 跨品牌联名导向 | 必须再换 |
| **TICKER 3 条** | 当周 | 当周 | 必须当周新事件 |

### 铁律 4 — 数据真实性（SOUL.md 第一条铁律的具体应用）
- ✅ 用 Shopify `created_at` 字段筛真本周新品（不是 `updated_at`）
- ✅ 媒体引用必须验证 `datePublished` 字段
- ✅ 任何 "本周一波 X 款" 故事，先 grep `created` 看分布
- ❌ 不能凭印象凑数 / 不能找一两个二手汇总源
- ❌ 不能用上期模板填新数字

### 铁律 5 — 强制跨品牌
- 3 帽款里 NewEra 上限 1 个（上限值,不是必须）
- 至少要有 1 个非美国非日本品牌（欧洲 / 亚洲新兴 / 澳洲等）
- 价位至少要跨 3 档（比如 $30-50 / $50-100 / $100+ 各 1）

### 铁律 6 — 每一期都永久保留
- **每一期** archive 永远不能删（不只是 W24）
- W24 / W25 / W26 / W27 / ... 全部要永远在线可访问
- issues.json 必须列全所有期号
- archive.html 必须能翻看每期
- 部署前必须 verify 所有历史期号 HTTP 200

### 铁律 7 — DESIGN TOOL section 必须包含 AI 软件介绍
- 每期至少 2-3 个新 AI 软件 / 设计工具（带价格、用法、链接）
- 软件 ≠ 外协供应商（外协可以单独一块，但软件不能省）
- 老板原话：「W25 没了软件介绍」→ 永久铁律

### 铁律 8 — Cloudflare Pages 免费档,长期运行 OK
- Cloudflare Pages 免费档：**无限带宽 / 500 builds 月 / 100 项目 / 1 并发 build**
- 我们用量：每周 1 build（远低于 500/月）
- 文件：每期 ~20MB，10 年 = 1GB（无问题）
- **不会产生费用**，老板不用担心
- 唯一付费触发：用 Workers Functions 超 100K 请求/天 → 我们目前是纯静态站,不用 Functions

---

### 铁律 9 — NewEra 上限 0（v12 升级,2026-07-07 老板拍板）
- ❌ 旧版："上限 1 个" — W24 实际 2/3 是 NewEra,W27 也含 NewEra
- ✅ 新版：**NewEra 上限 0** = 3/3 强制全非 NewEra
- 老板原话：「每期都是 new era 的帽, 完全没新意」
- NewEra 高频出现在跨品牌联名时**可作为第 4 备选**，但 3 主角位绝不占位
- 自动检查:每期 publish 前跑 `_scripts/check_newera_ratio.py`,3 帽款 NewEra 命中数必须 = 0

### 铁律 10 — 同图 0 复用（v12 升级,2026-07-07 老板拍板）
- ❌ 旧版：W27 dodgers-usa250.png 被复用 5 次（5 个不同 alt）
- ✅ 新版：**每张图在 HTML 中只能出现 1 次**
- 3 帽款 = 至少 3 × 3 = 9 张不同角度真图
- 不允许"假多角度"(同一 src 换 alt)
- 自动检查:每期 publish 前跑 `_scripts/check_image_uniqueness.py`,src 去重后必须 ≥ 9 张

### 铁律 11 — 17 品牌全景墙 = 17 张真图（v12 升级,2026-07-07 老板拍板）
- ❌ 旧版：W24-W27 全是文字卡片墙(纯文字列名)
- ✅ 新版：**17 品牌全景 = 17 张本品牌真图网格**(每品牌 1 张本周新品)
- 品牌池扩到 **50+**,横跨 7 类:街头 / 奢侈 / 运动 / 独立设计 / 快时尚 / 复古 / 童装
- 不允许占位图(灰色块 / 模板 SVG 替代) = 必须真本品牌当周新品图
- 自动检查:每期 publish 前跑 `_scripts/check_brand_panorama_images.py`,17 品牌每行必须有 1 个真 img

### 铁律 12 — 图为主角,文为注释（v12 升级,2026-07-07 老板拍板）
- ❌ 旧版：W27 = 85 段文字 : 17 处图 = 5:1（披图皮）
- ✅ 新版：**图 vs 文字段比例 ≥ 1:2**（即每段文字必须配 ≥1 张图）
- DESIGN PACK 预览必须**预渲染 1 张图**(色彩矩阵 / 工艺样品 / 走针参考 / 配色矩阵) — 不许文字占位
- 17 品牌全景 = 17 张真图(见铁律 11)
- 自动检查:每期 publish 前跑 `_scripts/check_image_text_ratio.py`,img_count ≥ p_count/2 失败即不让 publish

---

## v12 自动检查脚本（每期 publish 前必跑,任一失败 = 不发）

```bash
# 必须全部返回 0 = 通过才能继续 publish
python3 _scripts/check_newera_ratio.py 2026-W28
python3 _scripts/check_image_uniqueness.py 2026-W28
python3 _scripts/check_brand_panorama_images.py 2026-W28
python3 _scripts/check_image_text_ratio.py 2026-W28
```

铁律 9-12 任一不达标 = publish 流程 abort + wecom 紧急通知 Kin

---

## 📋 每期开工 checklist（自动化用）

每期开工前必须做：

```
[ ] 1. 看 RULES.md 铁律 1-6 确认理解
[ ] 2. 看上一期的「3 帽款主角」「DESIGN TOOL」「色卡」「LOGO CRAFT」 — 都不能重
[ ] 3. 选择本期主题角度（A-J 选一个新的 / 或没做过的）
[ ] 4. 扩品牌池 25+，扫真本周 created 新品
[ ] 5. 看 hypebeast/highsnobiety/PR Newswire/InTheKnow 当周报道 verify datePublished
[ ] 6. 选 3 帽款（强制 1 NewEra 上限 + 跨地区 + 跨价位）
[ ] 7. 写每个 section 时检查与上一期 diff
[ ] 8. 部署前用 agent-browser 截 11 张图过审
[ ] 9. 生成独特性报告（与上一期 diff %）
[ ] 10. 部署 + Git push + 更新 issues.json
[ ] 11. **跑 v12 4 项自检**: check_newera_ratio / check_image_uniqueness / check_brand_panorama_images / check_image_text_ratio — 任一失败 = 不发
[ ] 12. **禁止同图复用**:HTML 完成前 grep src 确保每张图片地址唯一命中 1 次
[ ] 13. **17 品牌真图**:每品牌 1 张本品牌当周新品图(模板图禁用)
```

---

## 🤖 Cron 自动化时间表

每周固定节点：

- **周三 09:00** — 启动新一期采集（W+1）
- **周三 14:00** — 选定 3 帽款 + 主题角度
- **周四 09:00** — 写第一稿
- **周四 18:00** — 主稿完成
- **周五 09:00** — 部署 + 截图过审

---

## 📊 历史期号档案

| 期号 | 主题 | 3 帽款 | 独特性 | 老板反馈 |
|---|---|---|---|---|
| 2026-W24 | 跨品牌联名 + Khroma + Vizcom + 世界杯 | 多个跨品牌 | 基线 | 通过 |
| 2026-W25 v1-3 | 跨品牌联名 | Pluto / Knicks / Swar47 | 12.6/42.2/45.2% | "一般般" — 架构问题没暴露 |
| 2026-W26 | USA 250 周年 | Padres / Dunkin / Polo Bear | 未测 | 待 v12 自检补测 |
| 2026-W27 | 三城记 SS27 | MLB USA250 / Borsalino / Polo Wimbledon | 79.5% 内容 / **架构 0/4 自检 FAIL** | 21:14 批架构 / 21:00 紧急发布 |
| **2026-W28** | v12 重做基线 | 必须 0/0/17/≥1:2 全通过 | 目标 ≥ 70% | 24h 内必出 |
| 2026-W25 v1 | 偷懒 39 款 NewEra | NewEra×HP / NewEra×MLB / Patta×Tom Trago | 12.6% | "90% 跟 W24 一样" |
| 2026-W25 v2 | 重写 39 款 NewEra | NewEra×HP / NewEra×MLB / Patta×Tom Trago | 42.2% | "为什么资料总是 NewEra" |
| 2026-W25 v3 | 跨品牌联名 (1 NewEra + 2 非) | Pluto×DSM / NewEra×Knicks / Swar×47 | 45.2% | "一般般，先用着跑" |
| 2026-W26 | （待定 — 必须换主题角度） | （必须不重） | **目标 ≥ 70%** | 必须 "耳目一新" |

---

*本文件每期开工前必读。违反铁律 = 项目失败。*
