# 🚀 專案重構與優化流程指南

為確保 `Europe-travel-guide` 專案在未來能夠穩定擴充與維護，以下將接下來的優化項目劃分為明確的四個階段流程，方便開發者逐步執行。

## 📍 階段一：架構重構與基礎建設

**目標：降低維護成本，實現關注點分離（Separation of Concerns）。**

1. **入口整併**：確認唯一的進入點為 `index.html`，並將開發過程中的草稿與重複 HTML（如 `europe-travel-guide.html`）移除或歸檔。
2. **抽取樣式（CSS）**：
   - 建立 `assets/css/style.css` 檔案。
   - 將 `index.html` 內 `<style>` 標籤中的所有 CSS 規則搬移至該檔案。
   - 在 HTML `<head>` 引入 `<link rel="stylesheet" href="assets/css/style.css">`。
3. **抽取邏輯（JavaScript）**：
   - 建立 `assets/js/main.js` 檔案。
   - 將原本寫在 HTML 中的 `onclick` 事件觸發方式移除，改由 JS 檔案內的 `document.addEventListener` 進行綁定。
   - 在 HTML 底部引入 `<script src="assets/js/main.js"></script>`。

## 📍 階段二：使用者體驗（UX）與無障礙（A11y）升級

**目標：確保網站在不同裝置上表現一致，並對輔助工具友善。**

1. **導入向量圖示（SVG Icons）**：
   - 評估並引入輕量級圖示庫（如 Phosphor Icons 或是 Lucide）。
   - 汰換現有大篇幅使用的 Emoji，統一視覺風格與品牌調性。
2. **加強無障礙屬性（WAI-ARIA）**：
   - 針對「國家切換」與「交通指南」等所有 Tab 元件，追加以下屬性：
     - 按鈕：`role="tab"`, `aria-selected="..."`, `aria-controls="..."`
     - 面板：`role="tabpanel"`, `aria-labelledby="..."`
   - 確保鍵盤使用者（使用 Tab 鍵）能順暢瀏覽與切換所有頁籤。

## 📍 階段三：旅遊內容擴充

**目標：導入導遊視角的實用資訊，解決旅客出遊痛點。**

1. **導航體驗升級**：為所有景點（如聖家堂）及餐廳（如 Pastéis de Belém）加上帶有座標的 Google Maps 外部超連結（使用 `target="_blank" rel="noopener noreferrer"`）。
2. **擴充實用指南區塊**：
   - 新增「氣候與穿搭建議」（如：洋蔥式穿搭原則說明）。
   - 新增「小費潛規則與文化說明」。
   - 新增「飲食限制（素食/無麩質）點餐教學」與「當地基本求生實用句」。

## 📍 階段四：進階模組化與未來規劃

**目標：若專案規模持續擴大，準備升級整體技術架構。**

1. **靜態網站產生器（SSG）評估**：
   - 由於現行單頁 HTML 已接近 3,000 行，若內容持續增長，可評估導入 Astro 等現代輕量級框架。
   - 將 Header、Footer、景點卡片（Card）等重複出現的區塊，抽離成獨立組件（Components），大幅簡化開發流程。
2. **即時資料動態整合（選配）**：
   - 若未來需再次提供動態資料（例如「當地即時天氣」或「鐵路罷工通報」等），可建立輕量級的 Serverless API（如 Cloudflare Workers），讓前端透過 Fetch API 動態獲取 JSON 資料點綴畫面。
