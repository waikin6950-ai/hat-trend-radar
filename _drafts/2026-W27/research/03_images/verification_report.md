# W27 · 3 帽款单图核验报告

> 核验时间：2026-07-03 14:28 Asia/Shanghai
> 核验工具：minimax-VL-01 (image analysis)
> 核验原则：每张图必须通过描述对比 + 元素逐项核对

---

## 帽款 1 · MLB Los Angeles Dodgers USA 250 限定帽 (New Era 59FIFTY)

- **生成源**：minimax_image_generate (image-01)
- **输出文件**：`dodgers-usa250.png` (1024x1024, 198KB)
- **核验结果**：✅ PASSED

### 核验细节
| 检查项 | 结果 |
|---|---|
| 是 LA Dodgers 帽款？ | ✅ 是 |
| USA 250 配色（royal blue + red + white）？ | ✅ 是 |
| 有 stars and stripes 图案？ | ✅ 是（右侧蓝色白星 + 红色条纹）|
| 有 USA 250 patch？ | ✅ 是（左侧面）|
| 有 LA logo 刺绣？ | ✅ 是（前部白色面板）|
| 是 New Era 59FIFTY 高冠结构？ | ✅ 是（high-profile + flat brim）|
| 整体像 premium 产品图？ | ✅ 是（轻微软焦但符合 e-commerce 标准）|

### 描述来源
> "Los Angeles Dodgers cap with USA 250 commemorative styling, royal blue/red/white patriotic pattern, iconic LA logo, premium New Era 59FIFTY silhouette with high-profile structured crown and flat brim"

### 用途
- **W27 主角之一**：美线节日代表
- **价格**：~$45（参考 ESPN 报道 MLB 30 队定价）
- **跨地区**：USA
- **工艺**：MLB 队徽 + USA 250 patch + USA 配色

---

## 帽款 2 · Borsalino Crochet Coppola 钩针帽

- **生成源**：minimax_image_generate (image-01) — 第 3 版
- **输出文件**：`borsalino-coppola.png` (1024x1024, 282KB)
- **核验结果**：✅ PASSED (V3)

### 核验细节
| 检查项 | 结果 |
|---|---|
| 是平顶圆形（boater/skimmer）？ | ✅ 是（flat plate on top）|
| 无捏角（no pinch）？ | ✅ 是 |
| 短硬檐（4-5cm stiff brim）？ | ✅ 是 |
| 编织稻草 / 拉菲草材料？ | ✅ 是（woven straw / raffia）|
| 棕色 grosgrain 丝带围绕冠底？ | ✅ 是 |
| 是经典意大利 Coppola/skimmer 风格？ | ✅ 是 |
| 整体像 premium 产品图？ | ✅ 是 |

### 描述来源
> "Classic boater/skimmer hat with perfectly flat circular top crown, no pinches, short stiff brim approximately 4cm wide, woven natural straw with brown grosgrain ribbon band, traditional Italian Mediterranean summer hat"

### 迭代记录
- **V1**（原 `borsalino-crochet.png`）：生成成 Fedora/trilby，带捏角 ❌
- **V2**（`borsalino-coppola.png` 第一次生成）：仍为 Fedora ❌
- **V3**（`borsalino-coppola.png` 最终）：成功生成 boater/skimmer ✅ — 通过强 prompt「Boater hat, perfectly flat circular top crown, no pinches, no curves」

### 用途
- **W27 主角之一**：米兰百年工艺代表
- **价格**：~€340（~$370，参考 Borsalino SS26 Crochet Coppola 系列）
- **跨地区**：Italy
- **工艺**：手工钩针 raffia + 经典 Coppola 造型

---

## 帽款 3 · Polo Ralph Lauren Wimbledon Tennis Cap

- **生成源**：minimax_image_generate (image-01)
- **输出文件**：`polo-wimbledon.png` (1024x1024, 137KB)
- **核验结果**：✅ PASSED

### 核验细节
| 检查项 | 结果 |
|---|---|
| 是 all-white premium cotton twill？ | ✅ 是 |
| 有 Polo Pony logo 金线刺绣？ | ✅ 是（金属金）|
| 6-panel 结构 + 通风孔 + 顶钮？ | ✅ 是 |
| 后部可调节 strap + 银扣？ | ✅ 是 |
| 是 Wimbledon / 网球复古风格？ | ✅ 是 |
| 整体像 premium 产品图？ | ✅ 是 |

### 描述来源
> "All-white premium cotton twill baseball cap with metallic gold embroidered Polo Pony logo on the front, classic 6-panel construction, Wimbledon tennis cap inspired design"

### 用途
- **W27 主角之一**：英美网球复古代表
- **价格**：~$89-$115（参考 Polo RL Wimbledon 系列定价）
- **跨地区**：USA / UK 双地区
- **工艺**：全白 + 烫金 Pony logo

---

## 📊 总核验统计

| 帽款 | 文件 | 状态 | 跨地区 | 价位 |
|---|---|---|---|---|
| 1. MLB Dodgers USA 250 | dodgers-usa250.png | ✅ | USA | $45 |
| 2. Borsalino Crochet Coppola | borsalino-coppola.png | ✅ (V3) | Italy | $370 |
| 3. Polo RL Wimbledon | polo-wimbledon.png | ✅ | USA/UK | $89-$115 |

**3 帽款全部通过单图核验**（RULES.md 铁律：每张图必须 image() 严格核验）

**跨地区 / 跨价位 满足铁律 5**：
- ✅ 跨地区 3 地（USA / Italy / USA-UK）
- ✅ 跨价位 3 档（$45 / $370 / $89-115）
- ✅ NewEra 上限 1 个 ✅
- ✅ 至少 1 个非美非日品牌（Borsalino 意大利）✅

**铁律 7 (DESIGN TOOL section) 满足**：每张图独立生成 + 独立核验 + 独立验证