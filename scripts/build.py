"""Build portable HTML pages and a full-text search index using only Python stdlib."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'content'
DATE='2026-09-08'
REPO='https://github.com/jack926509/europe-travel'
NAV=[('index','攻略首頁'),('france','法國'),('spain','西班牙'),('portugal','葡萄牙'),('disney','巴黎迪士尼'),('routes','路線靈感'),('transport','交通'),('prep','行前準備'),('shopping','購物'),('collection','收集資料'),('updates','更新紀錄')]
PAGES={}
def link(url,title):return f'<a href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(title)} ↗</a>'
def card(title,body,url=None,kicker=''):
 return f'<article class="card"><p class="eyebrow">{kicker}</p><h3>{escape(title)}</h3><p>{body}</p>'+ (f'<a class="text-link" href="{url}">閱讀攻略 →</a>' if url else '')+'</article>'
def section(title,body,id=''):
 return f'<section class="section"'+(f' id="{id}"' if id else '')+f'><h2>{title}</h2>{body}</section>'
def grid(cards):return '<div class="grid">'+''.join(cards)+'</div>'
def legacy(name,title='延伸閱讀・原專案資料'):
 return f'<details class="legacy"><summary>{title}</summary><div class="notice"><strong>待複查的整理資料</strong><p>以下保留原專案的景點、美食、交通與購物筆記；其中票價、營業時間、節慶日期、排名與推薦尚未逐項重新查證。請先用本頁官方入口確認，再安排與預訂。</p></div><div class="legacy-body">'+(CONTENT/(name+'-legacy.html')).read_text()+'</div></details>'
def add(slug,title,sub,body):PAGES[slug]=(title,sub,body)
def sources(items):return '<p class="source-line">官方查詢：'+' · '.join(link(u,t) for t,u in items)+'</p>'
add('index','法西葡，慢慢收集。','法國・西班牙・葡萄牙｜一份隨旅程長大的攻略', '''<div class="search-area"><label for="guide-search">想找哪個城市或主題？</label><div class="search-row"><input id="guide-search" type="search" placeholder="例如：巴黎、辛特拉、迪士尼、交通卡" autocomplete="off"><button id="search-clear" type="button">清除</button></div><p id="search-status" role="status">搜尋三國攻略、路線與專題內容</p><div id="search-results"></div></div>
<figure class="panorama"><img src="assets/paris-seine.jpg" alt="巴黎塞納河、橋梁與西堤島的城市全景" width="3840" height="869"><figcaption>PARIS · 沿著塞納河，開始下一段旅程</figcaption></figure>'''+
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
for slug,(cn,en,intro,cities) in country_data.items():
 body='<p class="notice">停留天數是規劃建議，可依步調調整，不代表已訂行程。城市摘要供選路線；最新票務與開放資訊請查各城市入口。</p>'
 body+=grid([card(t, f'<span class="pill">建議 {days}</span><br>{desc}<br>'+link(url,'旅遊／景點官方入口'),kicker=en) for t,days,desc,url in cities])
 if slug=='france':body+='<p class="related">巴黎近郊：<a href="disney.html">巴黎迪士尼專題</a> · <a href="routes.html#paris">巴黎散步模組</a></p>'
 body+=section('住宿與交通怎麼選','<p>先把預計參觀地點與抵達、離開車站放在同一張地圖上，再挑住宿。比房價時一起看行李移動、轉乘次數與回程方式；訂房資料留在私人訂單中。</p><a class="text-link" href="transport.html">查看三國交通工具 →</a>')
 body+=legacy(slug,'原專案整合：景點、美食、節慶與在地筆記')
 add(slug,cn+'旅遊攻略',intro,body)
add('transport','交通與移動','先選城市順序，再查班次與票種。',
section('三國交通查詢入口',grid([card('法國｜SNCF Connect','查詢城際與區域列車，確認實際出發站、到達站、是否轉車與行李規則。<br>'+link('https://www.sncf-connect.com/en-en','SNCF Connect')),card('西班牙｜Renfe','查詢列車及車站；比較票價時，同時確認退改條件與行李。<br>'+link('https://www.renfe.com/es/en','Renfe')),card('葡萄牙｜CP','查詢城際與市郊鐵路。出發、到達車站要與住宿位置一起比較。<br>'+link('https://www.cp.pt/passageiros/en','CP'))]))+
section('一段跨國移動的查詢順序','<ol class="steps"><li>輸入確定的城市與日期，先找直達選項。</li><li>比較門到門時間：去車站／機場、等候、轉乘和抵達後交通。</li><li>比較含行李與選位的總價，閱讀退改條件。</li><li>若班次尚未開賣，保留官方查詢入口；不要拿舊行程時間當保證。</li><li>訂票前再核對車站名稱、航廈與住宿位置。</li></ol>')+
section('機場與市區票卡','<p>巴黎、巴塞隆納、里斯本與波多的機場交通及市區票卡，會因搭乘範圍與票種而異。先算預計搭乘次數，再比較單程、回數或通票。</p>'+sources([('巴黎交通','https://www.iledefrance-mobilites.fr/en'),('巴塞隆納 TMB','https://www.tmb.cat/en/home'),('里斯本 Metro','https://www.metrolisboa.pt/en/'),('波多 Andante','https://andante.pt/en/')]))+legacy('transport'))
add('disney','巴黎迪士尼','樂園獨立一頁，行前與當天都好查。',
'<div class="notice verified"><strong>園區名稱已核對</strong><p>第二座園區使用 Disney Adventure World 名稱；World of Frozen 與新體驗於 2026 年 3 月 29 日開放。這是歷史資訊，不是你的旅遊日期。</p>'+link('https://news.disneylandparis.com/en/disneyland-paris-enters-a-new-era-with-the-inauguration-of-world-of-frozen-and-the-many-new-experiences-at-disney-adventure-world-its-reimagined-second-park/','迪士尼官方公告')+f'<p>查核：{DATE}；僅限上述園區資訊。</p></div>'+
grid([card('先決定單園或雙園','城堡、經典童話以 Disneyland Park 為主；World of Frozen 位於 Disney Adventure World。依最想玩的設施選園區，再比較票種。'),card('交通與入場','將目的地設為 Marne-la-Vallée–Chessy。由巴黎市區、CDG 機場出發是不同交通選擇；查當天路線與回程末班。'),card('安排順序','先列最想玩的三至五項，再配合當天營運、表演場次和排隊情況調整。Premier Access 是否划算，依實際人潮與預算決定。')])+
sources([('官方園區介紹','https://www.disneylandparis.com/en-int/destinations/disney-adventure-world'),('官網票務與營運查詢','https://www.disneylandparis.com/en-int/')])+legacy('disney','完整整合筆記：交通、門票、設施、餐廳與購物'))
mods=json.loads((CONTENT/'route-modules.json').read_text())
citynames={'paris':'巴黎','lisbon':'里斯本','sintra':'辛特拉','porto':'波多','sevilla':'塞維亞','granada':'格拉納達','madrid':'馬德里','bcn':'巴塞隆納'}
body=section('依假期長短挑選','<p>以下是行程組合建議，天數包含城市间移動，不含洲際飛行；請依航班再調整首尾。沒有固定出發日，也沒有預設已訂班次。</p>'.replace('城市间','城市間')+grid([
card('7–10 天｜一國深度','巴黎＋近郊＋里昂／南法擇一；或巴塞隆納＋馬德里；或里斯本＋辛特拉＋波多。'),
card('12–16 天｜二國銜接','巴黎＋南法＋巴塞隆納，或馬德里＋安達魯西亞＋里斯本。優先選較少住宿搬遷的組合。'),
card('18–24 天｜三國慢遊','巴黎 → 里斯本／辛特拉 → 波多 → 馬德里 → 巴塞隆納。跨國段依當期交通調整；想加塞維亞與格拉納達，另增天數或刪掉一個城市。')]))
body+=section('原 16 天行程，改成 16 個可拆用模組','<p>保留原有城市、景點與地圖入口。一天可選一個模組，也可以拆成兩天；移動日減少付費景點，日落與入場時段依實際日期查詢。</p>')
last=None
for m in mods:
 city=m['city'];title=m['title'].replace('抵達巴黎 CDG・','巴黎・').replace('抵達里斯本・','里斯本・').replace('抵達塞維亞・','塞維亞・').replace(' + 離境 BCN','').replace('・全西班牙最難搶門票','').replace('羅浮宮 + 奧塞美術館 + 蒙馬特','巴黎藝術散步：羅浮宮／奧塞擇一＋蒙馬特')
 if city!=last:body+=f'<h2 id="{escape(city)}">{citynames.get(city,city)}</h2>';last=city
 body+=f'<article class="route-module" id="{m["id"]}"><h3>{escape(title)}</h3><ul>'+''.join('<li>'+link(p['url'],p['name'])+'</li>' for p in m['places'])+'</ul></article>'
add('routes','路線靈感','不用綁日期，也能把想去的地方排順。',body)
add('prep','行前準備','把預訂順序與重要官方入口放在一起。',section('確認日期後再完成', '<ol class="steps"><li>確認護照、入境資格與官方最新申請要求。</li><li>安排進出城市，再訂機票與可接受退改條件的住宿。</li><li>把有指定入場時段的景點列出：阿爾罕布拉宮、聖家堂、迪士尼與熱門博物館。</li><li>確認城際交通與機場接駁，保留轉乘緩衝。</li><li>出發前再檢查景點休館、罷工或交通異動，保存必要離線資料。</li></ol>')+
section('入境資訊｜直接查官方','<p>不保留舊版對 ETIAS／EES 上線時程的預測。申請資格、啟用狀態與費用，請依旅行當時的官方公告確認。</p>'+sources([('歐盟 ETIAS','https://travel-europe.europa.eu/en/etias'),('歐盟 EES','https://travel-europe.europa.eu/en/ees'),('外交部領事事務局','https://www.boca.gov.tw/')]))+
section('訂單與旅行資料分開','<p>攻略收集城市、景點、來源與一般筆記。護照、訂位代號、信用卡與住宿訂單，另外放在自己的私人儲存空間。</p>')+legacy('prep','原專案整合：航班選項與旅遊提醒'))
add('shopping','美食、購物與伴手禮','按地區收集，等行程確定再排順路。',
grid([card('法國','把巴黎購物與南法伴手禮分開整理；同一家店不同分店的位置與營業資訊要個別記錄。'),card('西班牙','收藏想買的品牌、食品與店家；實際比價時看品項、容量、尺寸與幣別，不沿用固定價差百分比。'),card('葡萄牙','蛋塔、軟木、瓷磚與在地品牌可依里斯本、波多分類；食品與易碎品另記攜帶方式。')])+
section('退稅與攜帶規定','<p>購物前確認商品與旅客是否適用退稅；付款時向店家確認文件、手續費與退款方式。依實際離境行程查驗證流程，回臺攜帶與申報規定另外確認。</p>'+sources([('法國海關','https://www.douane.gouv.fr/'),('西班牙稅務機關','https://sede.agenciatributaria.gob.es/'),('葡萄牙稅務機關','https://www.portaldasfinancas.gov.pt/'),('臺灣關務署','https://web.customs.gov.tw/')]))+legacy('shopping','原專案整合：伴手禮、精品品牌與美食購物筆記'))
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
'<article class="update-entry"><p class="eyebrow">'+DATE+' / 架構整合</p><h2>三個專案，一個法西葡攻略</h2><ul><li>新增三國入口、路線、交通、行前、購物、資料收集與更新頁。</li><li>將原本 16 天固定日期行程改為 16 個城市模組。</li><li>合併迪士尼專題及原攻略的餐廳、行程提醒。</li><li>擴充巴黎、凡爾賽、里昂、波爾多、瓦倫西亞與阿爾加維等規劃入口。</li><li>建立跨頁全文搜尋與 GitHub 資料收件匣。</li></ul></article>'+
section('查核範圍','<table><thead><tr><th>內容</th><th>狀態</th><th>處理方式</th></tr></thead><tbody><tr><td>迪士尼新園區名稱與開放事件</td><td>已查核</td><td>引用官方公告，保留事件日期。</td></tr><tr><td>巴黎、巴塞隆納、葡萄牙旅遊與鐵路入口</td><td>已查閱入口</td><td>供後續查詢，不表示所有票價與服務已查核。</td></tr><tr><td>原專案的票價、時刻、店家推薦與節慶</td><td>待複查</td><td>置於各頁延伸閱讀，明示來源狀態。</td></tr><tr><td>ETIAS／EES、退稅與攜帶規定</td><td>改為官方查詢</td><td>移除舊版數值與預測，不推定最新規定。</td></tr></tbody></table>')+
section('持續更新的順序','<ol class="steps"><li>優先查核票務、交通、景點營運與官方規則。</li><li>檢查收件匣，合併相同景點與重複連結。</li><li>記錄來源、查核日期、適用範圍與差異。</li><li>確認修改後，再更新攻略與本頁紀錄。</li></ol><p>已設定每月 1 日上午（臺灣時間，從 2026 年 10 月起）查核，結果先整理成更新建議或草稿修改；未查證的價格與時刻不自動覆寫。此排程由 ChatGPT 執行，網站本身沒有背景更新服務。</p>')+
section('內容來源', '<ul>'+''.join('<li>'+link('https://github.com/jack926509/'+r,r)+'：'+t+'</li>' for r,t in [('europe-travel','西葡南法、交通、購物與行前資料'),('CDG-BCN','巴黎至巴塞隆納的城市與景點模組'),('disneyland-paris','迪士尼交通、門票、設施與商店專題')])+'</ul><p>原始專案及 Git 歷史仍保留，整合內容以這個專案繼續維護。</p>')+
section('照片來源',link('https://commons.wikimedia.org/wiki/File:A_panorama_of_the_Pont_Neuf_bridge_across_the_Seine_in_Paris,_8_July_2015.jpg','Joe deSousa / Wikimedia Commons，CC0')+'<p>巴黎塞納河全景，拍攝於 2015 年。僅供城市意象參考。</p>'))
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
def plain(s):
 p=Text();p.feed(s);return ' '.join(' '.join(p.parts).split())
index=[]
for slug,(title,sub,body) in PAGES.items():
 nav=''.join(f'<a href="{s}.html"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in NAV)
 html=f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#183c4a"><title>{escape(title)}｜法西葡旅遊攻略</title><meta name="description" content="{escape(sub)}"><link rel="stylesheet" href="assets/site.css"><script src="assets/app.js" defer></script></head><body><a class="skip" href="#main">跳到主要內容</a><header class="site-header"><a class="brand" href="index.html"><span class="brand-mark">F / E / P</span><span>法西葡旅遊攻略<small>TRAVEL FIELD NOTES</small></span></a><a class="collect-link" href="collection.html">＋ 收集資料</a></header><nav class="main-nav" aria-label="主要導覽">{nav}</nav><main id="main"><div class="page-heading"><p class="eyebrow">FRANCE / ESPAÑA / PORTUGAL</p><h1>{escape(title)}</h1><p>{escape(sub)}</p></div>{body}</main><footer><div><strong>法西葡旅遊攻略</strong><p>不預設出發日 · 保存靈感與來源 · 持續整理</p></div><div><a href="updates.html">更新與來源</a> · <a href="{REPO}/issues/new?title={escape('資料更新：'+title,quote=True)}" target="_blank" rel="noopener noreferrer">回報更新 ↗</a><p>內容整合 {DATE}；查核範圍見更新紀錄</p></div></footer></body></html>'''
 (ROOT/(slug+'.html')).write_text(html)
 index.append({'title':title,'url':slug+'.html','text':plain(body)})
(ROOT/'assets/search-index.json').write_text(json.dumps(index,ensure_ascii=False))
print(f'Built {len(PAGES)} pages and full-text index.')
