# 🌍 西班牙・葡萄牙・南法 自由行全攻略

> 個人旅遊規劃參考用的單頁靜態網站，涵蓋景點行程、美食、交通票卡、精品購物與退稅攻略。
> 適合從台灣出發、前往西班牙、葡萄牙、法國南法的自由行旅客。

---

## 📌 網站概覽

| 項目 | 說明 |
|------|------|
| 目標對象 | 台灣旅客，規劃西葡法三國自由行 |
| 旅行時間 | 2025–2026 年版本 |
| 技術架構 | 純靜態 HTML / CSS / Vanilla JavaScript（無框架依賴） |
| 開啟方式 | 直接用瀏覽器開啟 `index.html`，無需安裝任何套件 |

---

## 🗂 網頁分區說明

| 區塊 | 錨點 | 內容摘要 |
|------|------|---------|
| 簽證 & 入境 | `#visa` | 台灣護照申根免簽條件、ETIAS 2026 新制、EES 系統 |
| 航班選擇 | `#flight` | 卡達/土耳其/長榮等航班比較、開口票策略、旺季訂票建議 |
| 三國交通 | `#transport` | 跨國廉航/高鐵、各城市票卡（含機場線）、實用 App |
| 各國旅遊指南 | `#destinations` | 西班牙 / 葡萄牙 / 南法：景點、美食、節慶、貼士（分頁切換） |
| 巴黎迪士尼 | `#disney` | 2026 冰雪奇緣王國開幕攻略、票價、設施、行程規劃 |
| 伴手禮 | `#souvenir` | 三國必買推薦、台灣海關注意事項 |
| 精品購物 | `#luxury` | LOEWE / Cutipol / L'Occitane 等在地品牌 CP 值分析 |
| 退稅攻略 | `#taxrefund` | 三國退稅門檻、步驟、Global Blue / Wevat App 說明 |
| 實用貼士 | `#tips` | 治安、景點預訂、天氣、緊急聯絡、三語求生短句 |

---

## 📁 檔案說明

```
europe-travel/
├── index.html                 # 主網頁（唯一對外入口）
├── CHANGELOG.md               # 各版本修改記錄
├── optimization_workflow.md   # 專案優化流程與未來規劃
└── README.md                  # 本說明文件
```

---

## 🖥 本機開啟方式

不需要安裝任何工具，直接在瀏覽器開啟即可：

```bash
# 方法 A：直接雙擊
open index.html      # macOS
start index.html     # Windows

# 方法 B：VS Code Live Server（推薦，支援即時預覽）
# 安裝 Live Server 擴充 → 右鍵 index.html → Open with Live Server
```

> **注意**：Google Fonts 需連線才能載入；離線時會 fallback 至系統字型，版面不受影響。

---

## 🛠 技術規格

| 項目 | 說明 |
|------|------|
| 前端技術 | HTML5 / CSS3 / Vanilla JavaScript |
| 字型 | Google Fonts（Noto Serif TC / Playfair Display / Noto Sans TC） |
| 分頁切換 | `showTabPanel()` 上層分頁 + `showSubTab()` 子分頁，共 2 個函式處理全站 27 個按鈕 |
| CSS 架構 | CSS 變數（`:root`）定義色票 + Utility Classes（`.mt-*`、`.park-grid` 等） |
| 響應式設計 | `@media (max-width: 600px)` 手機版：橫滑 tab、縮小表格字體、單欄 grid |
| 外部依賴 | 僅 Google Fonts（CSS CDN），無 jQuery / 無 npm 套件 |

---

## 🗓 版本記錄

| 版本 | 日期 | 更新內容 |
|------|------|----------|
| v1.0 | 2026-03 | 初始版本，基礎景點交通資訊 |
| v1.4 | 2026-03 | 升級交通區塊為六分頁完整攻略 |
| v2.0 | 2026-03 | 移除冗餘自動化腳本，精簡為純靜態部署包 |
| v2.1 | 2026-03-11 | 三角色優化：修正 Lisboa Card 票價（€19→€21）、IC 列車時間、Navegante 大小寫；手機 tab 改橫滑、按鈕觸控面積至 44px；JS 四函式合併為二，移除所有殘留舊 handler |

---

*資料更新至 2026 年 3 月 ｜ 僅供個人旅遊規劃參考，實際資訊以官方最新公告為準*
