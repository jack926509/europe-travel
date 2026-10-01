# 旅遊資料查核來源

最後查核：2026-10-01（本次採增量查核；未列為異動的項目保留原快照）

本文件記錄網站中會影響票價、退改、交通使用與退稅的資料。官方頁若在查核後更新，應以官方最新內容為準，並同步修改 `scripts/build.py`、相應的 `content/*-legacy.html`、`updates.html` 與 `CHANGELOG.md`。

## 2026-10-01 增量查核

| 項目 | 查核結果 | 官方來源 | 適用範圍／後續 |
| --- | --- | --- | --- |
| EES | **有異動**：已自 2026-04-10 起全面運作，申根外部邊境對短期停留的非歐盟旅客改以電子方式記錄入出境，並登錄旅行文件、臉部影像與指紋等資料 | [European Commission — EES fully operational](https://home-affairs.ec.europa.eu/news/entryexit-system-ees-fully-operational-2026-04-10_en) | 申根外部邊境；官方流程異動或出發前重查 |
| ETIAS | **時程更新**：仍未啟用、不受理申請；目前官方只確認預計於 2026 年第 4 季推出，確切日期仍待公告 | [EU — Revised timeline for EES and ETIAS](https://travel-europe.europa.eu/en/etias/about-etias/news-corner/revised-timeline-ees-and-etias)、[ETIAS official entry](https://travel-europe.europa.eu/en/etias) | 免簽旅客；每月及出發前重查，正式入口開放前不向第三方付費 |
| 阿爾罕布拉宮 | **營運快照更新**：Alcazaba 已於 2026-09-23 恢復開放但採調整動線；Casa Horno de Oro 與 Palace of Dar al-Horra 在查核日仍因安全理由關閉 | [Patronato de la Alhambra — Official tickets and notices](https://tickets.alhambra-patronato.es/en/) | 僅為 2026-10-01 快照；路線與關閉區域到訪前重查 |
| 巴黎、里斯本、波多交通 | **無異動**：官方頁仍支持本站既有 2026 票價與票種限制 | 本文件下表各城市官方連結 | 2026 年票價；年度調價後重查 |
| Lisboa Card | **無異動**：價格效期、實體卡兌換、熱門景點預約與暫停開放清單未見新規則 | [Visit Lisboa Shop — Lisboa Card](https://shop.visitlisboa.com/products/lisboa-card) | 僅代表 2026-10-01 官網狀態；購買前重查 |
| 巴黎迪士尼 | **無異動**：指定日期票、Basic 票、未指定日期票的退改與登錄規則未見新變更 | [Disneyland Paris — ticket rules](https://www.disneylandparis.com/en-int/visit-paris-and-disneyland-paris) | 官方直售票；第三方及套裝另看各自條款 |

| 主題 | 本站採用資訊 | 官方來源 | 後續重查時機 |
| --- | --- | --- | --- |
| 法國退稅 | 同日、同店含稅購物總額須超過 €100；在離開歐盟的出口點驗證 | [French Customs — PABLO](https://www.douane.gouv.fr/en/fiche/tax-exemption-france-tourists-pablo) | 法規異動或出發前 |
| 西班牙退稅 | 旅客 VAT 退稅無最低消費額；店家開 DER、離境以 DIVA／海關驗證 | [Spain.info — Tax Free](https://www.spain.info/en/tax-free/)、[Agencia Tributaria — DIVA](https://sede.agenciatributaria.gob.es/Sede/en_gb/viajeros-trabajadores-desplazados-fronterizos/devoluciones-iva-compras-viajeros/informacion-general-sobre-devolucion-iva-viajeros.html) | 法規異動或出發前 |
| 葡萄牙退稅 | 每張發票未稅金額超過 €50；23% VAT 商品相當於含稅超過 €61.50 | [Lisbon Airport — VAT refund](https://www.lisbonairport.pt/en/lis/services-shopping/essential-services/vat-refund)、[Visit Portugal — Tax free shopping](https://www.visitportugal.com/en/node/56) | 法規異動或出發前 |
| 巴黎交通 | 2026 Metro–Train–RER €2.55、Bus–Tram €2.05、機場票 €14、Navigo Day €12.30、Week €32.40 | [Île-de-France Mobilités — 2026 fares](https://www.iledefrance-mobilites.fr/en/tarifs-titre-de-transport-en-commun-2026) | 每年調價後 |
| 巴塞隆納交通 | 2026 T-casual 一區 €13、單人使用、不含 L9 Sud 機場站；機場票 €5.90 | [TMB — T-casual](https://www.tmb.cat/en/barcelona-fares-metro-bus/t-casual)、[TMB — fares](https://www.tmb.cat/en/barcelona-fares-metro-bus) | 每年調價後 |
| 里斯本交通 | 2026 Carris／Metro €1.90、Metro Zapping €1.72、日票 €7.25、含 CP 日票 €11.40 | [Metro Lisboa — 2026 fares](https://www.metrolisboa.pt/en/2025/12/19/new-fares-2026-2/) | 每年調價後 |
| 波多交通 | Andante Tour 1 €7.75、Tour 3 €16.55；不含 Guindais 纜車與 STCP 歷史電車 | [Andante — Andante Tour](https://andante.pt/en/purchase/andante-tour/) | 每年調價後 |
| Lisboa Card | 原價 24h €31／€21、48h €51／€28、72h €62／€35；價格有效至 2027-03-31；實體卡及熱門景點預約限制 | [Visit Lisboa Shop — Lisboa Card](https://shop.visitlisboa.com/products/lisboa-card) | 購買前及 2027-04 |
| 巴黎迪士尼票務 | 一般指定日期票可在到訪日前 3 日取消；Basic 票除外；未指定日期票不可取消退款且須登錄日期 | [Disneyland Paris — ticket rules](https://www.disneylandparis.com/en-int/visit-paris-and-disneyland-paris) | 購票前 |
| 巴黎迪士尼園區 | Disney Adventure World、World of Frozen 於 2026-03-29 開放 | [Disneyland Paris News](https://news.disneylandparis.com/en/disneyland-paris-enters-a-new-era-with-the-inauguration-of-world-of-frozen-and-the-many-new-experiences-at-disney-adventure-world-its-reimagined-second-park/) | 新園區公告時 |
| 聖家堂工程 | 2026 完成的是耶穌基督塔里程碑，不表示整座教堂所有工程完工 | [Sagrada Família — History](https://sagradafamilia.org/en/history-of-the-temple) | 新工程公告時 |
| 阿爾罕布拉宮 | Alcazaba 已恢復開放但採調整動線；個別安達魯西亞古蹟仍可能因安全或維護關閉 | [Patronato de la Alhambra — Official tickets and notices](https://tickets.alhambra-patronato.es/en/) | 到訪前及官方公告異動時 |
| 索格島市集 | 普羅旺斯市集為週四、週日上午；週日另有跳蚤市場 | [L'Isle-sur-la-Sorgue Tourism](https://uk.islesurlasorguetourisme.com/marche-provencal-de-l-isle-sur-la-sorgue---en-218623) | 確定旅行日期後 |
| EES | 2026-04-10 起全面運作，以電子紀錄取代申根外部邊境的護照蓋章，並登錄短期停留非歐盟旅客的旅行文件與生物辨識資料 | [European Commission — EES fully operational](https://home-affairs.ec.europa.eu/news/entryexit-system-ees-fully-operational-2026-04-10_en) | 官方流程異動或出發前 |
| ETIAS | 查核日仍未啟用、不受理申請；官方預計 2026 年第 4 季推出，確切日期待公告 | [EU — Revised timeline for EES and ETIAS](https://travel-europe.europa.eu/en/etias/about-etias/news-corner/revised-timeline-ees-and-etias)、[ETIAS official entry](https://travel-europe.europa.eu/en/etias) | 每月或出發前 |
| 波爾多無車酒鄉 | Saint-Émilion 可搭火車，車站距村中心約 1 公里；部分酒莊可搭電車 | [Bordeaux Tourism](https://www.bordeaux-tourism.co.uk/how-go-vineyard/discover-vineyard-without-car) | 排入行程後 |
| 瓦倫西亞 | 舊城、藝術科學城、海灘為兩日主軸；Albufera 建議另留時間 | [Spain.info — Valencia in two days](https://www.spain.info/en/route/valencia-two-days/) | 排入行程後 |

## 尚未逐項查核

- 航班與列車實際班次、浮動票價、開賣窗口及行李費。
- 餐廳與商店的營業時間、菜單、庫存、價格及分店狀態。
- 品牌相對台灣售價、匯率、促銷與退稅後價差。
- 每年節慶日期、薰衣草花況、海況、步道或道路封閉。
- 景點當日休館、施工、罷工與最後入場時間。

這些項目保留為規劃線索，不應轉寫成無期限的保證。確定旅行日期後，再把可訂的班次、住宿、門票與備案加入行程。
