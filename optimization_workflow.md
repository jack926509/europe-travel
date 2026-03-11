# 🛠 專案優化工作流程

> **定位**：個人旅遊規劃靜態網站，供出發前查閱用途。
> 優化目標以「**手機易讀、資料正確、程式碼不打架**」為核心，不需 SEO 或社群分享功能。
>
> 三角色分工：
> - 🧭 **旅遊專家** — 確保交通票價、景點資訊、時刻表正確
> - 📱 **前端工程師** — 以手機為主的 UX/UI，tab 分頁清晰易操作
> - ⚙️ **後端工程師** — 消滅程式碼重複、清理 inline style、統一命名

---

## ✅ 已完成（v2.1，2026-03-11）

### 🧭 旅遊資料修正

| 項目 | 修正前 | 修正後 |
|------|--------|--------|
| Lisboa Card 24hr 票價 | €19（錯誤） | **€21**（補全 48hr €35 / 72hr €44） |
| 里斯本↔波多列車時間 | IC「3.5 小時」（錯誤） | AP 約 2h50m €34.6 / IC 約 3h13m €27.4 |
| Navegante 大小寫 | `navigante 卡` | `Navegante 卡`（補 €0.50 卡費、€1.61/次） |
| 緊急聯絡資訊 | 無 | 新增：歐盟 112、三國警察、台灣駐外館處 |
| 求生語速查 | 無 | 新增：西葡法三語緊急短句 + Google 翻譯建議 |
| 語氣與詞彙在地化 | 使用「貼士」 | 全面替換為台灣慣用詞「叮嚀/叮囑」 |
| 版權與免責聲明 | 單行文字 | 新增版號、免責聲明、與 ETIAS/EES 官網重要預警連結 |

### 📱 前端 UX 優化

| 項目 | 修正前 | 修正後 |
|------|--------|--------|
| 主分頁按鈕觸控高度 | 未定義（約 38px） | `min-height: 44px` + `touch-action` |
| 子分頁按鈕觸控高度 | 未定義 | `min-height: 44px` + `touch-action` |
| Tab 導覽列排版 | `flex-wrap: wrap`（手機多行） | 橫向單行可滑動（`overflow-x: auto`），內容精簡（如：跨國移動→跨國） |
| 手機 table 字體 | 與桌機相同 | `@media` 內縮小字體與內距 |
| 景點卡排版 | 多欄（手機擠壓） | `@media` 內改單欄 |
| 迪士尼雙欄 | 純 inline style | 改用 `.park-grid`（手機自動變單欄） |
| **全站導航架構** | 4000+行單頁滾動到底 | **5大隱藏分頁系統（行前/交通/攻略/購物/叮囑），支援左右滑動手勢** |
| **手機選單** | 隱藏在頂部需回捲 | **懸浮毛玻璃底部導航列（Bottom Nav）支援單手操作** |
| **視覺色彩設計** | 傳統配色與內建行高 | **更換高質感陶土紅/琥珀金色系，加大行高至 `1.8`** |

### ⚙️ 程式碼品質

| 項目 | 修正前 | 修正後 |
|------|--------|--------|
| Tab 切換函式 | 4 個邏輯重複函式（`showLtab / showCtab / showTtab / showStab`） | 合併為 2 個（`showTabPanel` / `showSubTab`），script 36 行 → 14 行 |
| onclick handler | 27 個使用舊函式名 | 全部更新，無殘留 |
| Utility classes | 無 | 新增 `.mt-0/sm/md/lg/xl`、`.park-grid`、`.park-card-*`、`.section-h3` |
| 迪士尼 inline style | `style="display:grid; background:linear-gradient(...)"` | 改用 CSS class |
| 分頁與動態佈局邏輯 | 全網頁依賴 CSS media query | 導入 JavaScript 分頁控制 `switchPage()`、Resize 監測與手勢滑動事件監聽 |
| 水平滑動體驗 (Tabs) | 容易滑過頭或卡在中間，易誤觸換頁 | 1. 新增 `scroll-snap-type` 磁吸對齊<br>2. 導入 **Safe Zone** 防誤觸邏輯（滑動 tab 時忽略換頁）<br>3. 提高滑動門檻 (Threshold) 至 120px |

---

## 🔄 待辦：下一輪迭代

### 🧭 旅遊專家

- [ ] **景點 Google Maps 連結**
  為各國主要景點（聖家堂、阿爾罕布拉宮、貝倫塔等）加上 `<a href="..." target="_blank" rel="noopener">` 導航連結，方便手機一鍵開啟
- [ ] **素食 / 特殊飲食補充**
  各城市補充 1–2 間素食友善或有英文菜單的餐廳選項
- [ ] **定期票價校對**（每年出發前更新）
  - Lisboa Card 官網最新成人票價（官網：visitlisboa.com）
  - Hola BCN、Madrid Tarjeta Turística 票價
  - Pass SUD AZUR、Paris Visite 票價
  - 廉航參考票價（Ryanair / Vueling / TAP）

- [ ] **新增「打包清單與急用藥物」模組**
  在「行前」分頁中加入一區快速 Check-list（如常備藥、防竊暗袋、轉接頭等），這對於手機隨身查看非常有幫助。

### 📱 前端工程師

- [ ] **剩餘 inline style 替換為 utility class**
  全文現有 180+ 處 `style="margin-top:...px"` → 改用 `.mt-sm/md/lg/xl`
  優先清理交通分頁（`ttab-*`）與精品購物分頁（`ltab-*`）

- [ ] **區段 `<h3>` 標題替換為 `.section-h3` class**
  現況：`<h3 style="font-family:'Playfair Display',serif; color:var(--terra); margin:28px 0 16px">` 等散落各處
  目標：統一用 `<h3 class="section-h3">` / `<h3 class="section-h3 pt">` / `<h3 class="section-h3 fr">`

- [ ] **`.attraction-card` 色彩改用 CSS 變數**
  現況：`.attraction-card.pt { border-left-color: #006600; }` 重複宣告
  目標：改用 `data-country` attribute 搭配 CSS 變數減少重複

  ```css
  /* 目標結構 */
  .attraction-card { border-left-color: var(--accent, var(--terra)); }
  [data-country="pt"] { --accent: #006600; }
  [data-country="fr"] { --accent: #002395; }
  ```

- [ ] **支援深色模式 (Dark Mode)**
  導入 `@media (prefers-color-scheme: dark)`，把 `--cream`, `--ink`, `--parchment` 等變數自動轉換為深灰與黑的組合，以降低用戶在歐洲夜間巴士查資料時的螢幕刺眼度。

- [ ] **iOS 下拉回彈體驗優化 (Overscroll)**
  設定 `overscroll-behavior-y: none` 在 body 上，避免在手機版（尤其是 iOS）滑到頂部或底部時觸發整頁拉動的 Safari 原生回彈效果，讓整體更像 Native App。

### ⚙️ 後端工程師

- [ ] **抽取 CSS → `assets/css/style.css`**
  將 `index.html` 內 `<style>` 區塊（目前約 800 行）移至獨立檔案
  ```
  europe-travel/
  ├── assets/
  │   └── css/
  │       └── style.css
  └── index.html  ← 僅留 <link rel="stylesheet" href="assets/css/style.css">
  ```

- [ ] **抽取 JS → `assets/js/main.js`**
  將 `<script>` 區塊移至獨立檔案。由於現在加入了 Swipe 手勢辨識、Resize 偵測、以及動態分頁切換，JS 邏輯變重，獨立出來比較符合關注點分離 (SoC)。
  ```
  europe-travel/
  ├── assets/
  │   └── js/
  │       └── main.js
  └── index.html  ← 僅留 <script src="assets/js/main.js" defer></script>
  ```
  > 加上 `defer` 屬性，確保 DOM 載入後才執行，避免 `getElementById` 返回 null

- [ ] **事件委託取代 inline onclick**
  現況：27 個按鈕仍使用 `onclick="..."` inline handler
  目標：`main.js` 改用事件委託，HTML 改用 `data-tab` / `data-container` 屬性
  ```js
  // 目標寫法
  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-tab]');
    if (!btn) return;
    showTabPanel(btn.dataset.tab, btn);
  });
  ```

---

## 📌 長期評估（視需求決定是否執行）

### 資料與展示分離
將頻繁變動的票價數據抽離至 `data/prices.json`，避免每次更新都需翻找 HTML：
```
data/
├── prices.json      ← 各城市票卡價格、退稅門檻
└── attractions.json ← 景點名稱、開放時間、門票價格
```

### 靜態網站產生器（SSG）評估
當 `index.html` 超過 5,000 行或需要新增第四個國家時，考慮導入 Astro 或 Eleventy，
將重複結構（`attraction-card`、`food-card`）改為可複用元件。
目前規模尚在手工維護的合理範圍內，**暫不優先執行**。

---

## 📋 校對清單（每次出發前執行）

出發前 **1–2 個月**，逐一查閱官方網站確認下列數據仍為最新：

- [ ] Lisboa Card 票價（visitlisboa.com）
- [ ] Hola Barcelona 票價（holabarcelona.com）
- [ ] 馬德里旅遊票 Tarjeta Turística 票價（metromadrid.es）
- [ ] Paris Visite / Navigo 票價（ratp.fr）
- [ ] Pass SUD AZUR 票價（zou.maregionsud.fr）
- [ ] 法國 ETIAS 申請是否已正式上線（travel-europe.europa.eu）
- [ ] 聖家堂、阿爾罕布拉宮門票是否需提前購買及目前票價
- [ ] 台灣駐西班牙 / 葡萄牙辦事處聯絡方式是否有變更

---

*最後更新：2026-03-11 ｜ v2.1 三角色優化後*
