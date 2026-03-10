# 🚀 專案重構與優化流程指南

為確保 `Europe-travel-guide` 專案在未來能夠穩定擴充與維護，基於導遊、前端工程師與後端工程師視角的全面盤點，我們將接下來的優化項目劃分為明確的四個階段流程。

## 📍 階段一：架構重構與基礎建設

**目標：降低維護成本，實現關注點分離（Separation of Concerns），並確保檔案庫的乾淨。**

1. **入口整併與冗餘檔案清除**：
   - 確認唯一對外的頁面為 `index.html`。
   - 移除高度重疊的備份與開發中的單獨版 HTML（如 `europe-travel-guide.html`）以防止後續維護產生「改 A 忘記改 B」的同步災難。
   - 將剩下的開發前草稿（Markdown 檔）移至 `docs/` 或封存庫中。
2. **抽取與整合樣式（CSS）**：
   - 建立 `assets/css/style.css`。
   - 將 `index.html` 內建近 400 行的 `<style>` 全部移入獨立 CSS 檔案。
   - 清洗散落於 HTML 標籤內的大量 Inline Styles（例如 `style="margin-top:32px"` 或迪士尼園區卡片的特設漸層樣式），將其轉化為通用的 Utility Classes（如 `.mt-lg`、`.park-card-pink`）。
   - 優化重複出現的卡片 CSS 結構（如 `.attraction-card.pt`, `.attraction-card.fr`），利用 CSS 變數或資料屬性（`data-country`）重構以大幅簡化樣式表。
3. **抽取行為邏輯（JavaScript）**：
   - 建立 `assets/js/main.js`。
   - 移除多達 30 處以上的 Inline Handler（`onclick="showCtab('es',this)"` 等），改為在 JS 檔案中利用 `document.addEventListener` 進行事件委託綁定。

## 📍 階段二：使用者體驗（UX）、無障礙（A11y）與 SEO 升級

**目標：確保網站在不同裝置上表現優異、對輔助工具友善，同時提升外部搜尋能見度。**

1. **加強無障礙屬性（WAI-ARIA）**：
   - 針對所有自製的 Tab 元件（國家、交通、購物等），追加完整的 ARIA 屬性（`role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-controls`）。
   - 確保導航列（`<nav>`）及 Tab 可完全經由鍵盤按鍵來切換與瀏覽。
2. **SEO 標記完善**：
   - 補齊缺失的 `<meta name="description">`。
   - 加入 Open Graph 標籤（`og:title`, `og:description`, `og:image`），確保網址在 Line、Facebook 等社群平台分享時有漂亮的預覽卡片。
3. **導入向量圖示（SVG Icons）**：
   - 逐步汰換依賴作業系統字型的 Emoji 圖示，改採輕量級且具一致性的向量圖示庫（如 Lucide 或 Phosphor Icons）。

## 📍 階段三：旅遊內容擴充與痛點解決

**目標：導入導遊實務經驗，解決自由行旅客常見的出遊盲點。**

1. **擴充在地實用指南區塊**：
   - **氣候與穿搭行李清單**：針對夏季 40°C 或者南法強風（Mistral）給予「洋蔥式穿搭」建議與打包表。
   - **特殊飲食限制建議**：針對素食者（Vegetarian / Vegan）與無麩質（Gluten-Free）需求，新增如何在餐廳溝通與點餐的指南。
   - **當地求生與緊急聯絡**：補上各國緊急聯絡電話（如 112）、駐外館處聯繫方式，以及附上簡單的幾個當地母語問候/求生實用句。
2. **在地導航與內容精確性修正**：
   - 為所有主要的景點與特色餐廳加上直接連動至 **Google Maps 的超連結**（支援 `target="_blank"`），讓手機讀者能一鍵打開導航。
   - 修正文中少數的資訊不對稱（如交通卡一小節提及 Lisboa Card 為 €21，但貼士區為 €19，需統整至最新動態定價）。

## 📍 階段四：進階工程化與自動化擴展

**目標：將「純手工維護」升級為「可擴展架構」，解決數千行代碼帶來的 Git 難以比對問題。**

1. **資料與展示分離**：
   - 將票價、交通花費等頻繁變更的數據，抽離至獨立的 `data/prices.json` 中管理，避免未來更新時必須翻找茫茫的 HTML 結構。
2. **靜態網站產生器（SSG）導入評估**：
   - 考慮導入如 Astro 或是 Eleventy 框架，將龐大的 `index.html` 拆解成獨立元件（如 `Header.astro`, `CountryCard.astro`），由建構系統負責組裝，大幅提升專案維護效益。
3. **持續整合（CI）流程建立**：
   - 於 GitHub Actions 中加入 `htmlhint`（保證 HTML 語法正確）、自動化失效連結檢查（確保所附的官方來源未斷鏈），甚至引入 `pa11y` 自動測試無障礙評分。
