# 法國・西班牙・葡萄牙旅遊攻略

整合 `europe-travel`、`CDG-BCN` 與 `disneyland-paris`，作為不綁定出發日期的旅遊資料庫。維護主專案為本 repository。

## 頁面

| 頁面 | 內容 |
| --- | --- |
| `index.html` | 國家入口、全文搜尋、主題入口 |
| `france.html` | 巴黎、凡爾賽、里昂、南法、波爾多及原南法筆記 |
| `spain.html` | 巴塞隆納、馬德里、安達魯西亞、瓦倫西亞 |
| `portugal.html` | 里斯本、辛特拉、波多、杜羅河谷、阿爾加維 |
| `disney.html` | 合併雙來源的迪士尼交通、票務、設施、餐廳與購物 |
| `routes.html` | 無指定日期的路線建議與 16 個原行程城市模組 |
| `transport.html` | 三國交通查詢順序、官方入口及原筆記 |
| `prep.html` | 行前清單、官方入境入口及航班／旅遊筆記 |
| `shopping.html` | 購物規劃、官方稅務入口及品牌／伴手禮筆記 |
| `collection.html` | 開啟 GitHub Issue 草稿，確認送出後永久保存 |
| `updates.html` | 整合、查核範圍、原始來源與照片授權 |

## 維護與建置

不需 Node 套件或前端框架。以 Python 3 標準函式庫產生完整靜態頁面：

```sh
python3 scripts/build.py
node --check assets/app.js
```

- `scripts/build.py`：共用版型、主要內容與頁面建置。
- `content/*-legacy.html`：原專案整理出的延伸閱讀，預設標示待複查。
- `content/route-modules.json`：原 16 天景點模組，無出發日期。
- `assets/site.css`、`assets/app.js`：共用樣式、全文搜尋與收集表單。
- `assets/search-index.json`：建置時產生的全文索引，不要手動修改。
- 產出的根目錄 HTML 與索引一併提交，既有靜態部署方式可沿用。

本機以 HTTP 預覽，例如 `python3 -m http.server 8000`。直接以 `file://` 開啟時，瀏覽器可能禁止搜尋索引的 fetch；頁面與導覽不依賴 JavaScript。

## 收集 → 查核 → 更新

1. 網頁的「收集資料」表單開啟 GitHub 確認頁；使用者登入並送出後，資料才儲存為 Issue。
2. Issue 為公開資料。不要提交護照、訂位代號、信用卡、住宿訂單或私人聯絡方式。
3. 查核來源與重複內容，在相應頁面／模組整理，保留查核日期及來源。
4. 更新 `updates` 頁面及 `CHANGELOG.md`，重新建置並提交 PR。
5. 經確認合併後才進入既有部署流程。網站不會把未查核 Issue 自動當成攻略。

收集表單不使用 localStorage，不放 GitHub token，不直接呼叫 GitHub 寫入 API。資料收件匣在 GitHub，可跨裝置檢視；本站不是即時 Issue 編輯器。

## 查核與日期政策

- 取消固定旅遊日期、星期、倒數及「已訂」暗示；季節資訊、事件日期與查核日期仍可保留。
- 新頁面的建議天數與路線是編輯規劃建議，並非即時班次或完整費用試算。
- 迪士尼園區名稱及 2026-03-29 開放事件已依官方公告查核。
- 原專案的完整票價、營業時間、節慶、店家推薦與價差尚未全面複查，集中於有明確提示的延伸閱讀。
- 原 ETIAS/EES 預測與退稅數值改為官方入口，不沿用舊法規或推出日期。
- 定期查核由 ChatGPT 排程執行，非網站背景服務；結果先整理為更新建議或草稿 PR，不自動合併與發布。

## 整合與相容性

沒有刪除或封存另外兩個 repository；舊版首頁可從 Git 歷史取得。原主站 `#visa`、`#flight`、`#transport`、`#destinations`、`#disney`、`#souvenir`、`#luxury`、`#taxrefund`、`#tips` 入口會導向對應新頁。其他兩個舊站的轉址留待確認正式網址後處理。

詳細來源映射與後續工作見 `docs/MIGRATION.md`。照片為 Joe deSousa 的巴黎塞納河全景，CC0，來源列於更新頁。
