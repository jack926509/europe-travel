"""Build portable HTML pages and a full-text search index using only Python stdlib."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
import re
ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'content'
DATE='2026-09-08'
REPO='https://github.com/jack926509/europe-travel'
SITE='https://europetrip.xiehnet.com'
NAV=[('index','攻略首頁'),('france','法國'),('spain','西班牙'),('portugal','葡萄牙'),('disney','巴黎迪士尼'),('routes','路線靈感'),('transport','交通'),('prep','行前準備'),('shopping','購物'),('collection','收集資料'),('updates','更新紀錄')]
PAGES={}
def link(url,title):return f'<a href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(title)} ↗</a>'
def card(title,body,url=None,kicker=''):
 return f'<article class="card"><p class="eyebrow">{kicker}</p><h3>{escape(title)}</h3><p>{body}</p>'+ (f'<a class="text-link" href="{url}">閱讀攻略 →</a>' if url else '')+'</article>'
def section(title,body,id=''):
 return f'<section class="section"'+(f' id="{id}"' if id else '')+f'><h2>{title}</h2>{body}</section>'
def grid(cards):return '<div class="grid">'+''.join(cards)+'</div>'
def legacy(name,title='延伸閱讀・原專案資料'):
 return f'<details class="legacy"><summary>{title}</summary><div class="notice"><strong>整合筆記・部分內容仍會變動</strong><p>交通票價、退稅門檻、迪士尼票務及已發現的矛盾已於 {DATE} 更新；店家價格、營業時間、節慶日期與主觀推薦仍須在使用前查看官方頁。每個已查核項目的來源列在<a href="updates.html">更新紀錄</a>。</p></div><div class="legacy-body">'+(CONTENT/(name+'-legacy.html')).read_text()+'</div></details>'
def add(slug,title,sub,body):PAGES[slug]=(title,sub,body)
def sources(items):return '<p class="source-line">官方查詢：'+' · '.join(link(u,t) for t,u in items)+'</p>'
add('index','法西葡，慢慢收集。','法國・西班牙・葡萄牙｜一份隨旅程長大的攻略', '''<div class="search-area"><label for="guide-search">想找哪個城市或主題？</label><div class="search-row"><input id="guide-search" type="search" placeholder="例如：巴黎、辛特拉、迪士尼、交通卡" autocomplete="off"><kbd class="search-hint" aria-hidden="true">／</kbd><button id="search-clear" type="button">清除</button></div><p id="search-status" role="status">搜尋三國攻略、路線與專題內容</p><div id="search-results"></div></div>
<figure class="panorama"><picture><source srcset="assets/paris-seine.webp" type="image/webp"><img src="assets/paris-seine.jpg" alt="巴黎塞納河、橋梁與西堤島的城市全景" width="3840" height="869" fetchpriority="high" decoding="async"></picture><figcaption>PARIS · 沿著塞納河，開始下一段旅程</figcaption></figure>'''+
section('從一個國家開始',grid([card('法國','巴黎與凡爾賽、里昂、普羅旺斯和蔚藍海岸。','france.html','01 / FRANCE'),card('西班牙','高第建築、馬德里藝術與安達魯西亞古城。','spain.html','02 / ESPAÑA'),card('葡萄牙','里斯本、辛特拉、波多與杜羅河沿岸。','portugal.html','03 / PORTUGAL')]))+
section('把靈感，接成旅行',grid([card('巴黎迪士尼','交通、雙園選擇、設施、美食與購物集中閱讀。','disney.html','主題樂園'),card('可以拆開的路線','原本 16 天行程改為城市模組，依假期長短自由組合。','routes.html','不指定出發日'),card('收集下一個想去的地方','保存來源連結、城市與筆記，整理成之後會用到的攻略。','collection.html','旅遊資料收件匣')]))+
'<div class="notice">已整合三個專案。旅遊日期不預設；資料查核日期仍保留。新整理內容與舊資料分開標示，可到<a href="updates.html">更新紀錄</a>查看查核範圍。</div>')
country_data={
'france':('法國','FRANCE','從巴黎的街區，走到南法的海岸。',[
('巴黎 Paris','3–5 天','以塞納河兩岸分區安排：羅浮宮與杜樂麗花園、奧塞與左岸、蒙馬特各留半天到一天。大型博物館一天選一座，保留散步與用餐時間。','https://www.france.fr/en/destination/paris/'),
('凡爾賽 Versailles','一日延伸','從巴黎出發另留一天；先選宮殿、花園與特里亞農宮的參觀範圍，再選票種。不要與迪士尼排在同一天。','https://en.chateauversailles.fr/'),
('里昂 Lyon','2–3 天','作為巴黎與南法之間的停留選項，收集老城、河岸散步與在地餐館；是否加住取決於整體移動次數。','https://en.visiterlyon.com/'),
('普羅旺斯 Provence','3–5 天','以亞維農或艾克斯為據點，挑選小鎮延伸。沒有自駕時，先查大眾運輸與回程，避免一天塞入太多鄉間景點。','https://www.france.fr/en/'),
('尼斯與蔚藍海岸','3–4 天','尼斯留作城市據點，再分別安排芒通、摩納哥或周邊海岸；單日只選一個主要方向。','https://www.explorenicecotedazur.com/en/'),
('波爾多 Bordeaux','2–3 天','適合將酒鄉、城市建築與餐飲列為另一段法國主題行程；先確認是否值得從原路線繞行。','https://www.bordeaux-tourism.co.uk/')]),
'spain':('西班牙','ESPAÑA','建築、美術館與古城，選擇自己的步調。',[
('巴塞隆納 Barcelona','3–4 天','將聖家堂、奎爾公園與格拉西亞大道分區規劃；高第建築選最有興趣的入內，哥德區留半天慢走。','https://www.spain.info/en/destination/barcelona/'),
('馬德里 Madrid','3–4 天','美術館、王宮與公園分日安排；托雷多或塞哥維亞擇一作近郊延伸，不和多座博物館擠在同一天。','https://www.esmadrid.com/en'),
('塞維亞 Sevilla','2–3 天','王宮、大教堂與聖十字區可作一組；西班牙廣場、Triana 與佛朗明哥作另一組。表演與景點場次留出用餐時間。','https://visitasevilla.es/en/'),
('格拉納達 Granada','2 天','阿爾罕布拉宮保留半天以上，再安排阿爾拜辛與觀景點。參觀日若需要移動，先確認指定入場時段與行李安排。','https://tickets.alhambra-patronato.es/en/'),
('瓦倫西亞 Valencia','2–3 天','城市建築、海邊與米食文化可成為獨立停留點；只有短假期時不必為湊城市數特別繞行。','https://www.visitvalencia.com/en')]),
'portugal':('葡萄牙','PORTUGAL','從山城電車，到杜羅河畔的慢日子。',[
('里斯本 Lisboa','3–4 天','阿爾法馬與市中心一天、貝倫另一天；把上下坡、電車排隊與用餐納入步行安排。','https://www.visitlisboa.com/en'),
('辛特拉 Sintra','一日延伸','從里斯本搭火車前往，再銜接當地交通。山區宮殿先選一至兩處，依入場時段規劃；避免每座都想去。','https://www.visitportugal.com/en/destinos/lisboa-regiao/73779'),
('波多 Porto','2–3 天','聖本篤車站、老城與河岸以步行串聯；跨河至 Gaia 的酒窖安排半天，留意回程坡度。','https://www.visitportugal.com/en/destinos/porto-e-norte'),
('杜羅河谷 Douro','1–2 天延伸','以風景、酒莊或遊船為主題先選一種玩法，再決定住波多往返或留宿河谷。','https://www.visitportugal.com/en/destinos/porto-e-norte'),
('阿爾加維 Algarve','3–4 天','適合另留一段海岸假期；先選住宿據點與交通，再收集海灘和步道，勿把整段海岸當單一景點。','https://www.visitportugal.com/en/destinos/algarve')])}
country_guides={
'france':section('把住宿區域和玩法配在一起','''<table><thead><tr><th>地區</th><th>適合的旅行方式</th><th>安排時先確認</th></tr></thead><tbody>
<tr><td>巴黎</td><td>第一次可選 1–6 區鄰近地鐵站；每天依塞納河左右岸分區。</td><td>博物館指定時段、住宿到機場／主要車站的轉乘。</td></tr>
<tr><td>里昂</td><td>Presqu’île 適合步行與短住；Vieux Lyon 適合老城氛圍。</td><td>若只是巴黎到南法中繼，先衡量多搬一次行李是否值得。</td></tr>
<tr><td>普羅旺斯</td><td>無車可住亞維農或艾克斯，選鐵路、公車或一日團可達的小鎮。</td><td>鄉間末班交通；薰衣草花況與採收會隨年份、地點變動。</td></tr>
<tr><td>尼斯</td><td>以 Nice-Ville 或電車沿線為據點，分日去摩納哥、芒通或坎城。</td><td>海岸鐵路施工、活動日與回程末班。</td></tr></tbody></table>''')+
section('波爾多 2–3 天規劃建議','<p>第一天用舊城、河岸與 Cité du Vin 建立城市方向；第二天選 Saint‑Émilion 或市郊酒莊。無車可搭火車到 Saint‑Émilion，但車站距村中心約 1 公里，酒莊仍要依預約與接駁安排；部分酒莊可從波爾多搭電車前往。若只為一間酒莊繞行，先衡量從原路線增加的住宿與移動。</p>'+sources([('波爾多無車酒鄉玩法','https://www.bordeaux-tourism.co.uk/how-go-vineyard/discover-vineyard-without-car')]))+
section('優先預訂','<p>巴黎大型博物館、凡爾賽與熱門展覽先用官方售票頁確認指定時段。南法節慶與市集只保留季節靈感；確定旅行年份後再查當屆日期。</p>'+sources([('羅浮宮官方票務','https://ticket.louvre.fr/en'),('凡爾賽宮官方票務','https://en.chateauversailles.fr/plan-your-visit/tickets-and-prices'),("索格島普羅旺斯市集",'https://uk.islesurlasorguetourisme.com/marche-provencal-de-l-isle-sur-la-sorgue---en-218623')])),
'spain':section('用區域拆開城市','''<table><thead><tr><th>城市</th><th>一天的合理組合</th><th>需先鎖定</th></tr></thead><tbody>
<tr><td>巴塞隆納</td><td>聖家堂＋聖保羅醫院；奎爾公園＋Gràcia；格拉西亞大道＋哥德區分開安排。</td><td>聖家堂、奎爾公園與高第建築的指定時段。</td></tr>
<tr><td>馬德里</td><td>王宮＋舊城；普拉多＋麗池公園；近郊另留整天。</td><td>美術館休館日；Tourist Travel Pass 不含 AVE、Avant 與區域列車。</td></tr>
<tr><td>塞維亞</td><td>王宮＋大教堂＋聖十字區；西班牙廣場＋Triana。</td><td>王宮與佛朗明哥場次，避免表演和晚餐時間相撞。</td></tr>
<tr><td>格拉納達</td><td>阿爾罕布拉宮半天；阿爾拜辛與觀景台另半天。</td><td>納斯里德宮指定入場時間與票面證件資料。</td></tr></tbody></table>''')+
section('瓦倫西亞 2–3 天規劃建議','<p>第一天走舊城、市場與 Turia 花園；第二天安排藝術科學城，想去海灘可接在同一方向。Albufera 自然公園與日落若是重點，另留一天會比把市中心、科學城、海灘和濕地塞進兩天更合理。</p>'+sources([('西班牙旅遊局瓦倫西亞兩日路線','https://www.spain.info/en/route/valencia-two-days/')]))+
section('2026 建築進度說明','<p>聖家堂在 2026 年完成並啟用的是耶穌基督塔的重要里程碑，不代表整座教堂所有工程都已完工。參觀票、塔樓開放與施工影響仍以官方票務頁為準。</p>'+sources([('聖家堂歷史與工程進度','https://sagradafamilia.org/en/history-of-the-temple'),('阿爾罕布拉宮官方票務','https://tickets.alhambra-patronato.es/en/')])),
'portugal':section('葡萄牙各段怎麼選據點','''<table><thead><tr><th>地區</th><th>建議據點</th><th>實用取捨</th></tr></thead><tbody>
<tr><td>里斯本</td><td>Baixa／Chiado 轉乘方便；Avenida 周邊較平坦；Alfama 氣氛好但坡與石板路多。</td><td>有大行李先看住宿到地鐵站的坡度與電梯，不只看直線距離。</td></tr>
<tr><td>辛特拉</td><td>多數旅客由里斯本當日往返。</td><td>宮殿選一至兩座；先鎖定指定時段，再排當地公車。</td></tr>
<tr><td>波多</td><td>São Bento／Bolhão 適合步行；Trindade 方便接機場；Ribeira 景觀好但坡多。</td><td>酒窖在 Gaia；把過橋、坡度和晚間回程算進路線。</td></tr>
<tr><td>杜羅河谷</td><td>想輕鬆可由波多參團；想慢遊再住 Peso da Régua 或 Pinhão。</td><td>火車、遊船和酒莊不一定能無縫銜接，酒莊多需預約。</td></tr>
<tr><td>阿爾加維</td><td>Lagos 適合西岸與步道；Faro 方便鐵路與機場；其餘海岸依租車與活動選擇。</td><td>海蝕洞船班、步道封閉與海況需在出發前確認。</td></tr></tbody></table>''')+
section('Lisboa Card 使用前先看','''<p>官方原價（成人／4–15 歲兒童）為 24 小時 €31／€21、48 小時 €51／€28、72 小時 €62／€35，標示有效至 2027-03-31；截至 '''+DATE+''' 官網另有 5% 網路優惠。Lisboa Card 是實體個人卡，網購憑證須在 6 個月內到 Askme Lisboa 兌換。</p><p>貝倫塔與熱羅尼莫斯修道院要先拿到實體卡號，才能預約指定日期與時段，名額不保證。截至 '''+DATE+'''，官方列出國家磁磚博物館、國家古代藝術博物館、國家服飾博物館、國家戲劇與舞蹈博物館、國家考古博物館及聖胡斯塔升降梯暫停開放。這是當日狀態，買卡前要按實際想去的景點重查並試算。</p>'''+sources([('Lisboa Card 官方銷售與最新限制','https://shop.visitlisboa.com/products/lisboa-card'),('佩納宮官方票務','https://www.parquesdesintra.pt/en/plan-your-visit/ticket-office/')])),
}
for slug,(cn,en,intro,cities) in country_data.items():
 body='<p class="notice">停留天數是規劃建議，可依步調調整，不代表已訂行程。城市摘要供選路線；最新票務與開放資訊請查各城市入口。</p>'
 body+=grid([card(t, f'<span class="pill">建議 {days}</span><br>{desc}<br>'+link(url,'旅遊／景點官方入口'),kicker=en) for t,days,desc,url in cities])
 if slug=='france':body+='<p class="related">巴黎近郊：<a href="disney.html">巴黎迪士尼專題</a> · <a href="routes.html#paris">巴黎散步模組</a></p>'
 body+=country_guides[slug]
 body+=section('住宿與交通怎麼選','<p>先把預計參觀地點與抵達、離開車站放在同一張地圖上，再挑住宿。比房價時一起看行李移動、轉乘次數與回程方式；訂房資料留在私人訂單中。</p><a class="text-link" href="transport.html">查看三國交通工具 →</a>')
 body+=legacy(slug,'原專案整合：景點、美食、節慶與在地筆記')
 add(slug,cn+'旅遊攻略',intro,body)
add('transport','交通與移動','2026 票價快查、票卡限制與跨城規劃。',
'<div class="notice verified"><strong>票價快照已查核</strong><p>以下金額適用於 2026 年官方公告；票價年度變動後要重新確認。城際列車與航班採浮動價格，因此不保留「最低價」、每日班數或固定開賣天數。</p><p>查核：'+DATE+'</p></div>'+section('2026 市區交通重點','''<table><thead><tr><th>城市</th><th>適合短期旅客的選項</th><th>機場與限制</th></tr></thead><tbody>
<tr><td>巴黎</td><td>Metro–Train–RER 單程 €2.55；Bus–Tram 單程 €2.05；Navigo Day 全區 €12.30。</td><td>CDG RER B／Orly 地鐵 14 使用 Paris Region ↔ Airports 票 €14；Navigo Day 不含機場。</td></tr>
<tr><td>巴塞隆納</td><td>T-casual 一區 €13，共 10 次，限單人使用；多人共用要看 T-familiar 等票種。</td><td>T-casual 不適用 L9 Sud 的 Aeroport T1／T2；機場地鐵單程 €5.90，T-usual 可含機場站。</td></tr>
<tr><td>里斯本</td><td>Carris／Metro €1.90；Zapping 搭 Metro 每次 €1.72；24 小時 Carris／Metro €7.25。</td><td>24 小時 Carris／Metro／CP €11.40，才含 Sintra、Cascais 等 CP 市郊線；每人需各自持卡。</td></tr>
<tr><td>波多</td><td>Andante Tour 1：€7.75／24 小時；Tour 3：€16.55／72 小時，全 Andante 聯運網路。</td><td>機場可用；不含 Guindais 纜車與 STCP 歷史電車，每次轉線或轉車仍要重新驗票。</td></tr>
</tbody></table>''')+
sources([('巴黎 2026 票價','https://www.iledefrance-mobilites.fr/en/tarifs-titre-de-transport-en-commun-2026'),('巴塞隆納 T-casual','https://www.tmb.cat/en/barcelona-fares-metro-bus/t-casual'),('巴塞隆納全部票價','https://www.tmb.cat/en/barcelona-fares-metro-bus'),('里斯本 2026 票價','https://www.metrolisboa.pt/en/2025/12/19/new-fares-2026-2/'),('波多 Andante Tour','https://andante.pt/en/purchase/andante-tour/')])+
section('跨城與跨國先這樣比','''<table><thead><tr><th>路線</th><th>先查的方式</th><th>判斷重點</th></tr></thead><tbody>
<tr><td>巴黎 ↔ 亞維農／里昂／波爾多</td><td>SNCF Connect 查 TGV 與轉乘。</td><td>巴黎與目的地的實際車站；住宿到站時間；票種退改。</td></tr>
<tr><td>馬德里 ↔ 巴塞隆納</td><td>Renfe、iryo、OUIGO 分別查。</td><td>含行李、選位與退改後總價，不只看首頁最低價。</td></tr>
<tr><td>里斯本 ↔ 波多</td><td>CP 查 Alfa Pendular 與 Intercidades。</td><td>里斯本 Santa Apolónia／Oriente 與波多 Campanhã／São Bento 的轉乘。</td></tr>
<tr><td>巴塞隆納 ↔ 馬賽</td><td>先查 Renfe 與 SNCF 的當日直達／轉乘。</td><td>與尼斯是不同路線，不共用「約 5 小時」；核對跨境段營運日。</td></tr>
<tr><td>巴塞隆納 ↔ 尼斯</td><td>SNCF／Renfe 查經法國南部轉乘，另與航班比較。</td><td>轉車次數、延誤緩衝與門到門時間；不可套用馬賽行車時間。</td></tr>
<tr><td>馬德里 ↔ 里斯本</td><td>比較航班與長途巴士；鐵路須依當期銜接查詢。</td><td>兩地市區到機場時間、行李費及夜車抵達時間。</td></tr>
</tbody></table>''')+
section('一段移動的查詢順序','<ol class="steps"><li>輸入確定的城市與日期，先找直達，再看只需一次轉乘的方案。</li><li>比較門到門時間：住宿到站、報到／候車、轉乘及抵達後交通。</li><li>比較含行李、選位與付款費的總價，閱讀退改條件。</li><li>班次尚未開賣時只保存官方入口，不拿舊行程的時刻或低價當承諾。</li><li>付款前核對車站、航廈、旅客姓名及行李規格。</li></ol>')+
section('三國城際官方入口',grid([card('法國｜SNCF Connect','查 TGV、Intercités 與 TER 的實際班次、車站及票種。<br>'+link('https://www.sncf-connect.com/en-en','SNCF Connect')),card('西班牙｜Renfe','查 AVE 與其他 Renfe 車種；若比較 iryo／OUIGO，要各自核對行李和退改。<br>'+link('https://www.renfe.com/es/en','Renfe')),card('葡萄牙｜CP','查 Alfa Pendular、Intercidades 與市郊鐵路。<br>'+link('https://www.cp.pt/passageiros/en','CP'))]))+legacy('transport'))
add('disney','巴黎迪士尼','樂園獨立一頁，行前與當天都好查。',
'<div class="notice verified"><strong>園區名稱已核對</strong><p>第二座園區使用 Disney Adventure World 名稱；World of Frozen 與新體驗於 2026 年 3 月 29 日開放。這是歷史資訊，不是你的旅遊日期。</p>'+link('https://news.disneylandparis.com/en/disneyland-paris-enters-a-new-era-with-the-inauguration-of-world-of-frozen-and-the-many-new-experiences-at-disney-adventure-world-its-reimagined-second-park/','迪士尼官方公告')+f'<p>查核：{DATE}；僅限上述園區資訊。</p></div>'+
grid([card('先決定單園或雙園','城堡、經典童話以 Disneyland Park 為主；World of Frozen 位於 Disney Adventure World。依最想玩的設施選園區，再比較票種。'),card('交通與入場','將目的地設為 Marne-la-Vallée–Chessy。由巴黎市區、CDG 機場出發是不同交通選擇；查當天路線與回程末班。'),card('安排順序','先列最想玩的三至五項，再配合當天營運、表演場次和排隊情況調整。Premier Access 是否划算，依實際人潮與預算決定。')])+
section('先分清楚門票退改規則','''<table><thead><tr><th>票種</th><th>官方規則</th><th>行前動作</th></tr></thead><tbody>
<tr><td>指定日期票 1–4 日</td><td>一般指定日期票最晚可在到訪日前 3 日取消退款；Basic 指定日期票除外。</td><td>付款前查看票名與確認信，第三方平台依該平台條款。</td></tr>
<tr><td>未指定日期票</td><td>購買日起有效 1 年，但不可取消、不可退款；入園前需登錄日期且受容量限制。</td><td>先查園區名額，再完成日期登錄。</td></tr>
<tr><td>飯店＋門票套裝</td><td>使用另一套取消條款，不套用單買門票的 3 日規則。</td><td>以套裝確認信及官方 Booking Conditions 為準。</td></tr>
</tbody></table>''')+
section('一日雙園不要鎖死時間表','<p>兩園夜間表演、遊行與閉園時間可能重疊或更動，無法預先保證同晚完整看完。到訪當日用官方 App 選一場最想看的壓軸，再由該場次倒排換園時間。Single Rider 與 Premier Access 的開放設施也以 App 和入口標示為準；Crush’s Coaster 曾提供 Single Rider，但不可把它當成固定省時方案。</p>')+
sources([('指定／未指定日期票規則','https://www.disneylandparis.com/en-int/visit-paris-and-disneyland-paris'),('官方園區介紹','https://www.disneylandparis.com/en-int/destinations/disney-adventure-world'),('官網票務、App 與營運查詢','https://www.disneylandparis.com/en-int/')])+legacy('disney','完整整合筆記：交通、門票、設施、餐廳與購物'))
mods=json.loads((CONTENT/'route-modules.json').read_text())
citynames={'paris':'巴黎','lisbon':'里斯本','sintra':'辛特拉','porto':'波多','sevilla':'塞維亞','granada':'格拉納達','madrid':'馬德里','bcn':'巴塞隆納'}
body=section('依假期長短挑選','<p>以下是行程組合建議，天數包含城市间移動，不含洲際飛行；請依航班再調整首尾。沒有固定出發日，也沒有預設已訂班次。</p>'.replace('城市间','城市間')+grid([
card('7–10 天｜一國深度','巴黎＋近郊＋里昂／南法擇一；或巴塞隆納＋馬德里；或里斯本＋辛特拉＋波多。'),
card('12–16 天｜二國銜接','巴黎＋南法＋巴塞隆納，或馬德里＋安達魯西亞＋里斯本。優先選較少住宿搬遷的組合。'),
card('18–24 天｜三國慢遊','巴黎 → 里斯本／辛特拉 → 波多 → 馬德里 → 巴塞隆納。跨國段依當期交通調整；想加塞維亞與格拉納達，另增天數或刪掉一個城市。')]))
body+=section('原 16 天行程，改成 16 個可拆用模組','<p>保留原有城市、景點與地圖入口。一天可選一個模組，也可以拆成兩天；移動日減少付費景點，日落與入場時段依實際日期查詢。</p>')
order=[]
for m in mods:
 if m['city'] not in order:order.append(m['city'])
body+='<nav class="page-toc" aria-label="城市模組"><span class="page-toc-label">跳到城市</span><ul>'+''.join(f'<li><a href="#{escape(c)}">{escape(citynames.get(c,c))}</a></li>' for c in order)+'</ul></nav>'
last=None
for m in mods:
 city=m['city'];title=m['title'].replace('抵達巴黎 CDG・','巴黎・').replace('抵達里斯本・','里斯本・').replace('抵達塞維亞・','塞維亞・').replace(' + 離境 BCN','').replace('・全西班牙最難搶門票','').replace('羅浮宮 + 奧塞美術館 + 蒙馬特','巴黎藝術散步：羅浮宮／奧塞擇一＋蒙馬特')
 if city!=last:body+=f'<h2 id="{escape(city)}" tabindex="-1">{citynames.get(city,city)}</h2>';last=city
 body+=f'<article class="route-module" id="{m["id"]}"><h3>{escape(title)}</h3><p><span class="pill">建議 {escape(m["duration"])}</span></p><p><strong>順路排法：</strong>{escape(m["plan"])}</p><p><strong>先確認：</strong>{escape(m["booking"])}</p><p><strong>時間不足：</strong>{escape(m["cut"])}</p><ul>'+''.join('<li>'+link(p['url'],p['name'])+'</li>' for p in m['places'])+'</ul></article>'
add('routes','路線靈感','不用綁日期，也能把想去的地方排順。',body)
add('prep','行前準備','把預訂順序與重要官方入口放在一起。',section('確認日期後再完成', '<ol class="steps"><li>確認護照、入境資格與官方最新申請要求。</li><li>安排進出城市，再訂機票與可接受退改條件的住宿。</li><li>把有指定入場時段的景點列出：阿爾罕布拉宮、聖家堂、迪士尼與熱門博物館。</li><li>確認城際交通與機場接駁，保留轉乘緩衝。</li><li>出發前再檢查景點休館、罷工或交通異動，保存必要離線資料。</li></ol>')+
section('入境資訊｜直接查官方','<p>截至 '+DATE+'，ETIAS 官方仍標示尚未啟用，也不受理申請。不要向非官方網站預先付費；接近出發日再核對啟用狀態、資格與申請入口。EES 狀態也以歐盟官方頁為準。</p>'+sources([('歐盟 ETIAS','https://travel-europe.europa.eu/etias/about-etias/what-is-etias'),('歐盟 EES','https://travel-europe.europa.eu/en/ees'),('外交部領事事務局','https://www.boca.gov.tw/')]))+
section('航班資料怎麼保存','<p>航線、航空公司、轉機點與價格都會變動。攻略只保存「開口票是否減少折返、行李是否直掛、轉機時間與退改條件」等決策欄位；實際班次、票價與是否直飛等到旅行日期確定後再查。舊筆記的參考價格與「一定要提前幾個月」不作為購票規則。</p>')+
section('訂單與旅行資料分開','<p>攻略收集城市、景點、來源與一般筆記。護照、訂位代號、信用卡與住宿訂單，另外放在自己的私人儲存空間。</p>')+legacy('prep','原專案整合：航班選項與旅遊提醒'))
add('shopping','美食、購物與伴手禮','按地區收集，等行程確定再排順路。',
grid([card('法國','把巴黎購物與南法伴手禮分開整理；同一家店不同分店的位置與營業資訊要個別記錄。'),card('西班牙','收藏想買的品牌、食品與店家；實際比價時看品項、容量、尺寸與幣別，不沿用固定價差百分比。'),card('葡萄牙','蛋塔、軟木、瓷磚與在地品牌可依里斯本、波多分類；食品與易碎品另記攜帶方式。')])+
section('退稅門檻與驗證地點','''<table><thead><tr><th>國家</th><th>目前規則</th><th>實際辦理</th></tr></thead><tbody>
<tr><td>法國</td><td>同一天、同一店家含稅消費總額須超過 €100；旅客須符合非歐盟居住等資格。</td><td>結帳時由參與退稅的店家開 PABLO 退稅單。</td></tr>
<tr><td>西班牙</td><td>旅客購買商品申請 VAT 退稅沒有最低消費金額；店家須開電子退稅文件 DER。</td><td>離開歐盟時使用 DIVA／海關完成出口驗證。</td></tr>
<tr><td>葡萄牙</td><td>每張發票未稅金額須超過 €50；若商品適用本土 23% VAT，相當於含稅金額超過 €61.50。</td><td>結帳時確認店家參與 e‑Taxfree 並取得文件。</td></tr>
</tbody></table><p>驗證地點是實際離開歐盟的出口點，不等於「最後一個申根國」。若在歐盟內轉機後才飛往非歐盟地區，依商品是否托運及出口機場指示預留時間。退稅服務商會收取費用，退款不等於退回完整 VAT 稅率。</p>''')+
sources([('法國海關 PABLO','https://www.douane.gouv.fr/en/fiche/tax-exemption-france-tourists-pablo'),('西班牙官方 Tax Free','https://www.spain.info/en/tax-free/'),('西班牙稅務機關 DIVA','https://sede.agenciatributaria.gob.es/Sede/en_gb/viajeros-trabajadores-desplazados-fronterizos/devoluciones-iva-compras-viajeros/informacion-general-sobre-devolucion-iva-viajeros.html'),('里斯本機場 VAT Refund','https://www.lisbonairport.pt/en/lis/services-shopping/essential-services/vat-refund'),('葡萄牙旅遊局 Tax Free','https://www.visitportugal.com/en/node/56'),('臺灣關務署','https://web.customs.gov.tw/')])+legacy('shopping','原專案整合：伴手禮、精品品牌與美食購物筆記'))
add('collection','旅遊資料收件匣','先記下來源，再慢慢整理成自己的攻略。', '''<div class="collection-layout"><form id="collect-form" class="card">
<h2>收集一筆資料</h2><p>填寫後會開啟 GitHub 確認頁，按下送出才會儲存。需登入 GitHub；資料會保存在這個公開專案，可跨裝置查看。</p>
<label for="note-title">名稱</label><input id="note-title" name="title" required maxlength="100" placeholder="例如：巴黎想去的咖啡店">
<label for="note-country">國家</label><select id="note-country" name="country"><option>法國</option><option>西班牙</option><option>葡萄牙</option><option>跨國／通用</option></select>
<label for="note-city">城市</label><input id="note-city" name="city" required maxlength="80" placeholder="例如：巴黎 Paris">
<label for="note-category">分類</label><select id="note-category" name="category"><option>景點</option><option>餐飲</option><option>交通</option><option>住宿區域</option><option>購物</option><option>行程靈感</option><option>資料更正</option></select>
<label for="note-url">來源網址</label><input id="note-url" name="url" type="url" required maxlength="700" placeholder="https://…">
<label for="note-body">想保留的重點</label><textarea id="note-body" name="notes" required rows="5" maxlength="600" placeholder="值得去的原因、位置、需要再確認的資訊…"></textarea>
<button class="primary" type="submit">前往 GitHub 確認並儲存 ↗</button><p id="collect-status" role="status">請勿填入護照、訂位代號或其他私人資料。</p></form>
<aside><article class="card"><p class="eyebrow">INBOX → GUIDE</p><h2>收集到攻略的流程</h2><ol class="steps"><li>加入來源、城市與筆記。</li><li>資料先保存在 GitHub 收件匣。</li><li>查核官方資訊、整理重複內容。</li><li>編輯對應攻略，確認後合併更新。</li></ol><a class="text-link" href="https://github.com/jack926509/europe-travel/issues?q=is%3Aissue+is%3Aopen" target="_blank" rel="noopener noreferrer">開啟資料收件匣 ↗</a></article>
<article class="card"><h3>修正既有內容</h3><p>在每一頁底部選「回報更新」，附上新來源與需修正的段落，就能追蹤到整理完成。</p><p>收件匣不會自動出現在攻略頁；經過查核與合併後才發布。</p></article></aside></div>''')
add('updates','更新與查核紀錄','記錄改了什麼，也標明哪些仍要確認。',
'<article class="update-entry"><p class="eyebrow">'+DATE+' / 資料校正</p><h2>修正會直接影響行程與花費的資料</h2><ul><li>更新巴黎、巴塞隆納、里斯本與波多的 2026 市區票價及票卡限制。</li><li>修正法國、西班牙、葡萄牙旅客 VAT 退稅門檻與歐盟出口驗證說明。</li><li>分清巴黎迪士尼指定日期票、Basic 票、未指定日期票及套裝的不同退改規則。</li><li>修正 Single Rider、遊行地點及雙園夜間表演無法保證全部銜接等矛盾。</li><li>補上 Lisboa Card 實體兌換、熱門景點指定時段與 '+DATE+' 暫停開放名單。</li><li>釐清 2026 是聖家堂耶穌基督塔里程碑，不代表整座教堂所有工程完成。</li><li>補充三國住宿區域、無車玩法、波爾多、瓦倫西亞及 16 個路線模組的取捨。</li></ul></article>'+
section('本輪查核狀態','''<table><thead><tr><th>內容</th><th>狀態</th><th>適用範圍</th></tr></thead><tbody>
<tr><td>巴黎、巴塞隆納、里斯本、波多市區票價</td><td>已查核</td><td>2026 官方票價；年度調價後重查。</td></tr>
<tr><td>法國、西班牙、葡萄牙退稅</td><td>已查核</td><td>旅客購買商品的一般資格與門檻；店家、商品和離境路線仍影響實際辦理。</td></tr>
<tr><td>巴黎迪士尼票務與園區名稱</td><td>已查核</td><td>官方直售票規則；第三方平台及飯店套裝看各自條款。</td></tr>
<tr><td>Lisboa Card 景點限制</td><td>已查核快照</td><td>暫停開放名單截至 '''+DATE+'''；使用前必須重查。</td></tr>
<tr><td>聖家堂 2026 工程說明</td><td>已查核</td><td>耶穌基督塔里程碑；不延伸為全工程完工。</td></tr>
<tr><td>住宿區域與路線取捨</td><td>規劃建議</td><td>協助排順路；不是即時營運或個人訂單。</td></tr>
<tr><td>店家、菜單、品牌價差、航班與節慶</td><td>持續收集</td><td>變動頻繁，確定旅行年份或日期後再查。</td></tr>
</tbody></table>''')+
section('需要持續收集的資料','''<table><thead><tr><th>頻率</th><th>優先收集</th><th>完成標準</th></tr></thead><tbody>
<tr><td>每月</td><td>交通票價、熱門景點預約、迪士尼營運、入境與退稅公告</td><td>官方來源、最後查核日、適用期間、異動摘要。</td></tr>
<tr><td>每季</td><td>住宿區域、無車交通、餐廳、商店、城市新內容</td><td>正確分店／車站、休息日、訂位方式與替代方案。</td></tr>
<tr><td>年度公告後</td><td>節慶、市集特殊日期、季節活動</td><td>當屆官方日程；不沿用前一年日期。</td></tr>
<tr><td>確定旅行日期後</td><td>航班、列車、房價、休館、施工、罷工、末班車與天氣</td><td>綁定實際日期的可訂方案與備案。</td></tr>
</tbody></table><p>每筆更新都應留下官方來源、查核日期、適用期間與「已查核／待查核」狀態。完整來源清單保存在 GitHub 的 <a href="'''+REPO+'''/blob/main/docs/SOURCES.md" target="_blank" rel="noopener noreferrer">查核來源文件 ↗</a>。</p>''')+
section('本輪官方來源','<ul>'+''.join('<li>'+link(u,t)+'</li>' for t,u in [
('法國海關 PABLO','https://www.douane.gouv.fr/en/fiche/tax-exemption-france-tourists-pablo'),
('西班牙官方 Tax Free','https://www.spain.info/en/tax-free/'),
('里斯本機場 VAT Refund','https://www.lisbonairport.pt/en/lis/services-shopping/essential-services/vat-refund'),
('葡萄牙官方 Tax Free','https://www.visitportugal.com/en/node/56'),
('巴黎 2026 交通票價','https://www.iledefrance-mobilites.fr/en/tarifs-titre-de-transport-en-commun-2026'),
('巴塞隆納 T-casual','https://www.tmb.cat/en/barcelona-fares-metro-bus/t-casual'),
('里斯本 2026 票價','https://www.metrolisboa.pt/en/2025/12/19/new-fares-2026-2/'),
('波多 Andante Tour','https://andante.pt/en/purchase/andante-tour/'),
('巴黎迪士尼門票規則','https://www.disneylandparis.com/en-int/visit-paris-and-disneyland-paris'),
('Lisboa Card 最新限制','https://shop.visitlisboa.com/products/lisboa-card'),
('聖家堂工程歷史','https://sagradafamilia.org/en/history-of-the-temple')])+'</ul><p>查核日：'+DATE+'。來源若更新，以官方頁最新版本為準。</p>')+
'<article class="update-entry"><p class="eyebrow">'+DATE+' / 架構整合</p><h2>三個專案，一個法西葡攻略</h2><ul><li>新增三國入口、路線、交通、行前、購物、資料收集與更新頁。</li><li>將原本 16 天固定日期行程改為可拆用城市模組。</li><li>合併迪士尼專題及原攻略的餐廳、行程提醒。</li><li>建立跨頁全文搜尋與 GitHub 資料收件匣。</li></ul></article>'+
section('內容來源','<ul>'+''.join('<li>'+link('https://github.com/jack926509/'+r,r)+'：'+t+'</li>' for r,t in [('europe-travel','西葡南法、交通、購物與行前資料'),('CDG-BCN','巴黎至巴塞隆納的城市與景點模組'),('disneyland-paris','迪士尼交通、門票、設施與商店專題')])+'</ul><p>原始專案及 Git 歷史仍保留，整合內容以這個專案繼續維護。</p>')+
section('照片來源',link('https://commons.wikimedia.org/wiki/File:A_panorama_of_the_Pont_Neuf_bridge_across_the_Seine_in_Paris,_8_July_2015.jpg','Joe deSousa / Wikimedia Commons，CC0')+'<p>巴黎塞納河全景，拍攝於 2015 年。僅供城市意象參考。</p>'))
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
def plain(s):
 p=Text();p.feed(s);return ' '.join(' '.join(p.parts).split())
SEC=re.compile(r'<section class="section"(?P<attrs>[^>]*)><h2>(?P<title>.*?)</h2>')
def anchor(body):
 """Give every top-level section a stable id and return the on-page table of contents."""
 items=[]
 def mark(m):
  attrs,heading=m.group('attrs'),m.group('title')
  sid=re.search(r'id="([^"]+)"',attrs)
  sid=sid.group(1) if sid else 'sec-%d'%(len(items)+1)
  items.append((sid,plain(heading)))
  attrs=attrs if 'id="' in attrs else f' id="{sid}"'+attrs
  return f'<section class="section"{attrs}><h2 tabindex="-1">{heading}</h2>'
 body=SEC.sub(mark,body)
 if len(items)<3:return body,''
 links=''.join(f'<li><a href="#{sid}">{escape(t)}</a></li>' for sid,t in items)
 return body,f'<nav class="page-toc" aria-label="頁內章節"><span class="page-toc-label">這一頁</span><ul>{links}</ul></nav>'
index=[]
for slug,(title,sub,body) in PAGES.items():
 nav=''.join(f'<a href="{s}.html"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in NAV)
 body,toc=anchor(body)
 url=f'{SITE}/{slug}.html'
 html=f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#183c4a"><title>{escape(title)}｜法西葡旅遊攻略</title><meta name="description" content="{escape(sub)}"><link rel="canonical" href="{escape(url,quote=True)}"><meta property="og:type" content="website"><meta property="og:site_name" content="法西葡旅遊攻略"><meta property="og:locale" content="zh_TW"><meta property="og:title" content="{escape(title,quote=True)}｜法西葡旅遊攻略"><meta property="og:description" content="{escape(sub,quote=True)}"><meta property="og:url" content="{escape(url,quote=True)}"><meta property="og:image" content="{SITE}/assets/paris-seine.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="assets/site.css"><script src="assets/app.js" defer></script></head><body><a class="skip" href="#main">跳到主要內容</a><header class="site-header"><a class="brand" href="index.html"><span class="brand-mark">F / E / P</span><span>法西葡旅遊攻略<small>TRAVEL FIELD NOTES</small></span></a><a class="collect-link" href="collection.html">＋ 收集資料</a></header><div class="main-nav-wrap"><nav class="main-nav" aria-label="主要導覽">{nav}</nav></div><main id="main"><div class="page-heading"><p class="eyebrow">FRANCE / ESPAÑA / PORTUGAL</p><h1>{escape(title)}</h1><p>{escape(sub)}</p></div>{toc}{body}</main><footer><div><strong>法西葡旅遊攻略</strong><p>不預設出發日 · 保存靈感與來源 · 持續整理</p></div><div><a href="updates.html">更新與來源</a> · <a href="{REPO}/issues/new?title={escape('資料更新：'+title,quote=True)}" target="_blank" rel="noopener noreferrer">回報更新 ↗</a><p>內容整合 {DATE}；查核範圍見更新紀錄</p></div></footer><button id="to-top" class="to-top" type="button" hidden><span aria-hidden="true">↑</span><span class="sr-only">回到頁面頂端</span></button></body></html>'''
 (ROOT/(slug+'.html')).write_text(html)
 index.append({'title':title,'url':slug+'.html','text':plain(body)})
(ROOT/'assets/search-index.json').write_text(json.dumps(index,ensure_ascii=False))
print(f'Built {len(PAGES)} pages and full-text index.')
