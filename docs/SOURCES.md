# 旅遊資料查核來源

最後查核：2026-09-08

本文件記錄網站中會影響票價、退改、交通使用與退稅的資料。官方頁若在查核後更新，應以官方最新內容為準，並同步修改 `scripts/build.py`、相應的 `content/*-legacy.html`、`updates.html` 與 `CHANGELOG.md`。

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
| 索格島市集 | 普羅旺斯市集為週四、週日上午；週日另有跳蚤市場 | [L'Isle-sur-la-Sorgue Tourism](https://uk.islesurlasorguetourisme.com/marche-provencal-de-l-isle-sur-la-sorgue---en-218623) | 確定旅行日期後 |
| ETIAS | 查核日仍未啟用、不受理申請 | [European Union — What is ETIAS](https://travel-europe.europa.eu/etias/about-etias/what-is-etias) | 每月或出發前 |
| 波爾多無車酒鄉 | Saint-Émilion 可搭火車，車站距村中心約 1 公里；部分酒莊可搭電車 | [Bordeaux Tourism](https://www.bordeaux-tourism.co.uk/how-go-vineyard/discover-vineyard-without-car) | 排入行程後 |
| 瓦倫西亞 | 舊城、藝術科學城、海灘為兩日主軸；Albufera 建議另留時間 | [Spain.info — Valencia in two days](https://www.spain.info/en/route/valencia-two-days/) | 排入行程後 |

## 尚未逐項查核

- 航班與列車實際班次、浮動票價、開賣窗口及行李費。
- 餐廳與商店的營業時間、菜單、庫存、價格及分店狀態。
- 品牌相對台灣售價、匯率、促銷與退稅後價差。
- 每年節慶日期、薰衣草花況、海況、步道或道路封閉。
- 景點當日休館、施工、罷工與最後入場時間。

這些項目保留為規劃線索，不應轉寫成無期限的保證。確定旅行日期後，再把可訂的班次、住宿、門票與備案加入行程。
