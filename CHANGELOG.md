# 修改記錄 CHANGELOG

> 依照 `optimization_workflow.md` 三角色（旅遊專家 / 前端工程師 / 後端工程師）分工完成
> 修改日期：2026-03-11
> 作業分支：`claude/code-optimization-review-XPuIa`

---

## 旅遊專家角色修改

### 1. Lisboa Card 24 小時票價修正
- **位置**：`index.html` 葡萄牙貼士區 `pt-tips` 面板
- **問題**：「里斯本卡 Lisboa Card 24hr €19」與交通票卡詳細表格（€21）數字不一致
- **修正**：改為 €21，並補充 48hr €35 / 72hr €44 完整定價，使全頁資訊統一

### 2. 里斯本 ↔ 波多 IC 列車時間修正
- **位置**：`index.html` 葡萄牙貼士區 `pt-tips` 面板
- **問題**：「IC 火車約 3.5 小時」錯誤，實際 IC 約 3h13m（Alfa Pendular 約 2h50m）
- **修正**：改為「Alfa Pendular 約 2h50m（€34.6）、IC 約 3h13m（€27.4）」，附上票價與早鳥訂位建議

### 3. Navegante 卡大小寫修正
- **位置**：`index.html` 葡萄牙貼士區 `pt-tips` 面板
- **問題**：「navigante 卡」全小寫，與全文其他處「Navegante」不一致
- **修正**：改為「Navegante 卡」，並補充卡費 €0.50 及每次 €1.61 費用

### 4. 新增緊急聯絡與求生語速查
- **位置**：`index.html` 旅遊貼士區 `#tips` 末尾
- **新增內容**：
  - 🆘 **緊急聯絡速查**：歐盟統一 112、三國警察電話、台灣駐外館處聯絡方式
  - 🗣 **當地求生語**：西葡法三語緊急求助短句 + Google 翻譯離線包建議

---

## 前端工程師角色修改

### 5. ctab-btn 手機觸控面積優化
- **位置**：`<style>` `.ctab-btn` 規則
- **修改**：加入 `min-height: 44px`（Apple HIG 建議觸控目標尺寸）、`touch-action: manipulation`（消除 300ms 延遲）
- **效果**：手機端按鈕更好點擊，避免誤觸

### 6. stab-btn 手機觸控面積優化
- **位置**：`<style>` `.stab-btn` 規則
- **修改**：`padding` 從 `7px 16px` 調整為 `8px 18px`，加入 `min-height: 44px`、`touch-action: manipulation`

### 7. ctab-nav 改為橫向滑動（單行不換行）
- **位置**：`<style>` `.ctab-nav` 規則
- **問題**：原本 `flex-wrap: wrap` 導致手機上按鈕多行排列，需要捲動大量空間
- **修改**：改為 `flex-wrap: nowrap` + `overflow-x: auto` + `scrollbar-width: none`（隱藏捲軸），加入 `-webkit-overflow-scrolling: touch`
- **效果**：與原生 App tab bar 一致的滑動體驗

### 8. stab-nav 同樣改為橫向滑動
- **位置**：`<style>` `.stab-nav` 規則
- **修改**：同上，並加 `padding-bottom: 4px` 避免 active 底線截切

### 9. 手機版 media query 補強（max-width: 600px）
- **位置**：`<style>` `@media (max-width: 600px)` 區塊
- **新增**：
  - `.ctab-panel`：內距縮小至 `16px 14px`，節省手機螢幕空間
  - `.ctab-btn`：縮小字體至 12.5px
  - `table, thead th, tbody td`：縮小字體、內距，改善橫向閱讀
  - `.attraction-grid`：改為單欄
  - `.food-grid`：改為 2 欄
  - `.section-header`：縮短上方留白
  - `.park-grid`：手機改為單欄

---

## 後端工程師角色修改

### 10. 合併 4 個 tab 函式為 2 個
- **位置**：`<script>` 區塊（原 `index.html:4112–4145`）
- **問題**：`showLtab / showCtab / showTtab` 三個函式邏輯完全相同，僅 ID prefix 不同；`showStab` 邏輯亦可統一
- **修改**：
  - 刪除 `showLtab`, `showCtab`, `showTtab`, `showStab`（共 4 個函式）
  - 新增 **`showTabPanel(id, btn)`**：統一處理上層分頁切換（交通 / 各國 / 精品購物），呼叫時直接傳完整 element ID
  - 新增 **`showSubTab(containerId, tabId, btn)`**：統一處理子分頁切換（各國景點 / 迪士尼）
- **效果**：script 從 36 行縮減至 14 行，邏輯清晰，無重複

### 11. 更新全部 27 個 onclick handler
- **位置**：全文 `.ctab-btn` 和 `.stab-btn` 元素
- **修改對照**：
  | 原函式呼叫 | 新函式呼叫 |
  |---|---|
  | `showTtab('cross',this)` | `showTabPanel('ttab-cross',this)` |
  | `showTtab('es-t',this)` | `showTabPanel('ttab-es-t',this)` |
  | `showCtab('es',this)` | `showTabPanel('ctab-es',this)` |
  | `showCtab('pt',this)` | `showTabPanel('ctab-pt',this)` |
  | `showCtab('fr',this)` | `showTabPanel('ctab-fr',this)` |
  | `showLtab('brands',this)` | `showTabPanel('ltab-brands',this)` |
  | `showStab('es','sights',this)` | `showSubTab('ctab-es','es-sights',this)` |
  | `showStab('pt','food',this)` | `showSubTab('ctab-pt','pt-food',this)` |
  | `showStab('disney','intro',this)` | `showSubTab('ctab-disney','disney-intro',this)` |
  | （其餘同規則依此類推，共 27 處）| |

### 12. 新增 utility classes（取代高頻 inline style）
- **位置**：`<style>` 新增 `/* UTILITY CLASSES */` 區塊
- **新增**：
  - `.mt-0 / .mt-sm / .mt-md / .mt-lg / .mt-xl`：取代散落的 `style="margin-top:...px"`
  - `.section-h3` / `.section-h3.pt` / `.section-h3.fr`：取代區段標題的 inline font/color style
  - `.park-grid`：取代迪士尼雙欄 `style="display:grid; grid-template-columns:1fr 1fr;..."`
  - `.park-card-pink` / `.park-card-purple`：取代迪士尼兩個園區卡片的 `style="background:linear-gradient(...)"` inline style

### 13. 迪士尼園區介紹 inline style 替換
- **位置**：迪士尼 `#disney-intro` 面板內的雙欄 grid div
- **修改**：移除 `style="display:grid..."` inline style，改用 `.park-grid` 類別；移除兩個 `style="background:linear-gradient(...)"` inline style，改用 `.park-card-pink` / `.park-card-purple`

---

## 待辦（下一輪迭代）

- [ ] 將剩餘 180+ 處 `style="margin-top:..."` inline style 替換為 utility class
- [ ] 區段 `<h3>` 標題內的 `style="font-family:...; color:..."` 替換為 `.section-h3` class
- [ ] 抽取 `<style>` 至 `assets/css/style.css` 獨立檔案
- [ ] 抽取 `<script>` 至 `assets/js/main.js` 獨立檔案
- [ ] 為景點卡加入 Google Maps 超連結（一鍵導航）
- [ ] 補充各城市素食友善餐廳建議

---

## 優化前後程式碼對比

| 項目 | 優化前 | 優化後 |
|------|--------|--------|
| JS tab 函式數量 | 4 個（含邏輯重複） | 2 個（統一清晰） |
| script 區塊行數 | ~36 行 | ~14 行 |
| ctab-btn 觸控高度 | 未定義（約 38px） | `min-height: 44px` |
| tab 導覽列行為 | `flex-wrap: wrap`（多行） | 橫向可滑動單行 |
| Lisboa Card 24hr 資訊 | €19（錯誤） | €21（正確） |
| IC 列車時間 | 3.5 小時（錯誤） | 3h13m（正確） |
| Navegante 大小寫 | navigante（錯誤） | Navegante（正確） |
| 緊急聯絡資訊 | 無 | 含 112、各國警察、駐外館處 |
| 求生語速查 | 無 | 三語緊急短句 + Google 翻譯建議 |
| 迪士尼雙欄 inline style | 完全 inline | `.park-grid` class |
