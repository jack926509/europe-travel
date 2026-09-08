# 三專案整合紀錄

主專案：jack926509/europe-travel。來源讀取與本次整合：2026-09-08。

| 原始來源 | 整合位置 | 處理方式 |
| --- | --- | --- |
| europe-travel 各國分頁 | content/france-legacy.html、spain-legacy.html、portugal-legacy.html | 保留景點、美食與節慶資料；清除原切頁程式與行內樣式，使用共用介面 |
| europe-travel 交通 | content/transport-legacy.html | 保留詳細表格，標示待複查 |
| europe-travel 航班與提醒 | content/prep-legacy.html | 保留延伸資料，標示待複查 |
| europe-travel 伴手禮與精品 | content/shopping-legacy.html | 保留原品牌與購物筆記，價差不可當最新報價 |
| europe-travel 迪士尼 | content/disney-legacy.html | 只補充餐飲與行程提醒，避免重複堆放兩份完整專題 |
| disneyland-paris 五個 section | content/disney-legacy.html | 合入同一迪士尼專題，沿用新園區名稱與共用樣式 |
| CDG-BCN 16 個 day row | content/route-modules.json | 保留每個模組與景點地圖；移除固定日期、已訂暗示與具體班次 |
| CDG-BCN 16 日全套順序 | routes.html | 拆成模組；新增一國、二國、三國天數選擇，不將緊湊的舊路線當固定建議 |
| 舊 ETIAS/EES 預測、退稅數值 | prep.html、shopping.html | 改用官方查詢入口 |

## 合併時取捨

不是把三個首頁放在 iframe，也沒有把舊站直接設為正式頁面。可重用內容按主題歸併，重新整理主頁摘要，仍未查核的細節集中在延伸閱讀。原始 CDG 行程中關於固定日落時間、實際票價、最難搶排名與日期限定預訂提醒不再作為可重複使用的行程建議。原檔保留在來源 repository，無不可逆刪除。

## 驗證範圍

- 11 頁靜態入口、站內連結及 fragment 目標。
- 無重複 ID、遺留 onclick／onchange 等原切頁事件。
- 共用 JavaScript 語法、搜尋索引可解析、16 個路線模組保留。
- 搜尋非同步請求以 revision 避免舊結果覆蓋新查詢。
- 搜尋與收集輸入以 textContent／URLSearchParams 處理；來源僅接受 HTTP(S)。
- 未執行瀏覽器視覺或端對端測試；外部連結不保證永久有效。

## 尚待後續

- 逐項核對延伸閱讀的票價、開放時間、特殊規定與店家推薦。
- 城市擴充目前以規劃摘要及官方入口為主，後續可按實際興趣加入更完整景點卡。
- 正式站網址確認後，再決定其他兩個舊站是否轉址；不自動刪除或封存。
- 若希望在網頁內直接編輯並即時同步資料，需另建登入與資料庫；目前以 GitHub Issue 收集、PR 整理維護。
