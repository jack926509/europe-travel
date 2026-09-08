# 法國・西班牙・葡萄牙旅遊攻略

以 **[jack926509/europe-travel](https://github.com/jack926509/europe-travel)** 為唯一主專案，整合法國、西班牙與葡萄牙的旅遊攻略，作為持續收集、整理與更新的旅遊資料庫，不綁定特定出發日期。

後續新增城市、景點、交通、購物、路線與巴黎迪士尼資料，以及 Issue、PR 和網站部署設定，統一在 `europe-travel` 維護。

**現行網站：[法西葡旅遊攻略](https://europetrip.xiehnet.com/)**

## 專案整合狀態

| 專案 | 定位 | 內容去向 |
| --- | --- | --- |
| `europe-travel` | 唯一主專案 | 法西葡攻略、資料收集、共用頁面與後續更新 |
| `CDG-BCN` | 舊內容來源，後續更新集中至主專案 | 巴黎至巴塞隆納路線拆為 `routes.html` 與 `content/route-modules.json` 的 16 個城市模組 |
| `disneyland-paris` | 舊內容來源，後續更新集中至主專案 | 交通、票務、設施、餐廳與購物合入 `disney.html` 與 `content/disney-legacy.html` |

本整合版已於 2026-09-08 透過 [PR #4](https://github.com/jack926509/europe-travel/pull/4) 合併至 `main`。兩個舊專案目前保留，後續內容統一在本專案維護。

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
- `docs/SOURCES.md`：已查核規則、官方來源、適用範圍與重查時機。
- `assets/site.css`、`assets/app.js`：共用樣式、全文搜尋與收集表單。
- `assets/search-index.json`：建置時產生的全文索引，不要手動修改。
- 產出的根目錄 HTML 與索引一併提交，既有靜態部署方式可沿用。

本機以 HTTP 預覽，例如 `python3 -m http.server 8000`。直接以 `file://` 開啟時，瀏覽器可能禁止搜尋索引的 fetch；頁面與導覽不依賴 JavaScript。

## Cloudflare Pages 部署

Cloudflare Pages 使用 GitHub Actions 部署到現有的 Direct Upload 專案：

| 設定 | 值 |
| --- | --- |
| Production branch | `main` |
| Root directory | `/` |
| Build command | `python3 scripts/build_cloudflare.py` |
| Build output directory | `dist` |
| Pages project name | `europe-travel` |
| Custom domain | `europetrip.xiehnet.com` |
| Workflow | `.github/workflows/deploy-cloudflare.yml` |

每次 push 到 `main` 後，GitHub Actions 會執行 `python3 scripts/build_cloudflare.py`，再以 Wrangler 將 `dist/` 部署到 production。也可從 GitHub Actions 頁面手動執行同一個 workflow。

Repository Actions secrets 必須設定：

- `CLOUDFLARE_API_TOKEN`：僅授予指定 Cloudflare 帳號的 Cloudflare Pages Edit 權限。
- `CLOUDFLARE_ACCOUNT_ID`：Cloudflare 帳號 ID。

`scripts/build_cloudflare.py` 會先重建網站，再把 11 個 HTML 頁面、搜尋索引、樣式、程式與圖片整理到 `dist/`。`wrangler.jsonc` 也使用相同的輸出目錄。Cloudflare Direct Upload 專案無法改成內建 Git Integration，因此由 GitHub Actions 負責持續部署，無需刪除或重建現有專案與自訂網域。

## 收集 → 查核 → 更新

1. 網頁的「收集資料」表單開啟 GitHub 確認頁；使用者登入並送出後，資料才儲存為 Issue。
2. Issue 為公開資料。不要提交護照、訂位代號、信用卡、住宿訂單或私人聯絡方式。
3. 查核來源與重複內容，在相應頁面／模組整理，保留查核日期及來源。
4. 更新 `updates` 頁面及 `CHANGELOG.md`，重新建置並提交 PR。
5. 經確認合併或 push 到 `main` 後，GitHub Actions 自動部署正式網站。網站不會把未查核 Issue 自動當成攻略。

收集表單不使用 localStorage，不放 GitHub token，不直接呼叫 GitHub 寫入 API。資料收件匣在 GitHub，可跨裝置檢視；本站不是即時 Issue 編輯器。

## 查核與日期政策

- 取消固定旅遊日期、星期、倒數及「已訂」暗示；季節資訊、事件日期與查核日期仍可保留。
- 新頁面的建議天數與路線是編輯規劃建議，並非即時班次或完整費用試算。
- 迪士尼園區名稱及 2026-03-29 開放事件已依官方公告查核。
- 2026 市區交通、三國退稅、迪士尼票務、Lisboa Card 與聖家堂工程說明已依官方來源更新；範圍見 `docs/SOURCES.md`。
- 店家營業、菜單、庫存、品牌價差、航班、城際浮動票價與節慶仍需按旅行日期重查。
- 原 ETIAS/EES 預測與退稅數值改為官方入口，不沿用舊法規或推出日期。
- 定期查核由 ChatGPT 排程執行，非網站背景服務；結果先整理為更新建議或草稿 PR，不自動合併與發布。

## 整合與相容性

主站的舊版首頁可從本專案 Git 歷史取得。原主站 `#visa`、`#flight`、`#transport`、`#destinations`、`#disney`、`#souvenir`、`#luxury`、`#taxrefund`、`#tips` 入口會導向對應新頁。

整合後的頁面、城市模組與搜尋索引存放在主專案，建置不需讀取另外兩個 repository。但本次採內容整理，**沒有將兩個舊專案的完整 Git 歷史、Issues、PR 或部署設定移入主專案**；原始版本仍在各來源專案。

### 另外兩個專案可以刪除嗎？

完成整合上線及備份後可以考慮刪除；目前尚未完成下列事項，先保留。若只希望集中維護，可在切換完成後將舊專案封存（Archive），保留原始內容與歷史供查閱。

1. 合併 PR #4，確認 `europe-travel` 正式站的攻略、路線、迪士尼、搜尋與資料收集入口正常。
2. 備份兩個舊專案的完整 Git 歷史，以及需要保留的 Issues、PR、附件與部署設定；本次整理的攻略內容不能取代完整備份。
3. 確認舊站的部署、網域及分享連結，決定保留轉址或停止使用；刪除 repository 不會自動把舊網址導向主站。
4. 若確定刪除，先更新本專案更新頁的舊來源連結與「原始專案仍保留」說明，並記錄備份位置及來源版本。

以上為退役步驟，尚未執行刪除、封存或轉址。

詳細來源映射與後續工作見 `docs/MIGRATION.md`。照片為 Joe deSousa 的巴黎塞納河全景，CC0，來源列於更新頁。
