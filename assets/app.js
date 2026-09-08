'use strict';
(() => {
  const input = document.querySelector('#guide-search');
  if (input) {
    const results = document.querySelector('#search-results');
    const status = document.querySelector('#search-status');
    let records;
    let pending;
    let revision = 0;
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase();
    async function search() {
      const current = ++revision;
      const query = input.value.trim();
      results.replaceChildren();
      if (!query) { status.textContent = '搜尋三國攻略、路線與專題內容'; return; }
      status.textContent = '搜尋中…';
      try {
        if (!records) {
          pending ||= fetch('assets/search-index.json').then(r => {
            if (!r.ok) throw new Error('Search unavailable');
            return r.json();
          }).catch(error => { pending = null; throw error; });
          records = await pending;
        }
        if (current !== revision) return;
        const words = normalize(query).split(/\s+/u);
        const hits = records.filter(r => words.every(w => normalize(r.title + ' ' + r.text).includes(w)));
        status.textContent = hits.length ? `找到 ${hits.length} 個相關頁面；舊資料的查核狀態請見各頁標示。` : '找不到資料，試試城市名稱、中文或當地名稱。';
        for (const hit of hits) {
          const article = document.createElement('article'); article.className = 'search-result';
          const a = document.createElement('a'); a.href = hit.url; a.textContent = hit.title;
          const p = document.createElement('p');
          const at = Math.max(0, normalize(hit.text).indexOf(words[0]) - 24);
          p.textContent = (at ? '…' : '') + hit.text.slice(at, at + 160) + '…';
          article.append(a, p); results.append(article);
        }
      } catch {
        if (current === revision) status.textContent = '搜尋暫時無法載入，請使用上方國家與主題導覽，或稍後再試。';
      }
    }
    input.addEventListener('input', search);
    document.querySelector('#search-clear').addEventListener('click', () => { input.value = ''; search(); input.focus(); });
  }
  const form = document.querySelector('#collect-form');
  if (form) form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    let source;
    try {
      source = new URL(data.url);
      if (!['https:', 'http:'].includes(source.protocol)) throw new Error('Invalid URL');
    } catch {
      document.querySelector('#collect-status').textContent = '請輸入 http 或 https 開頭的來源網址。';
      return;
    }
    const issue = new URL('https://github.com/jack926509/europe-travel/issues/new');
    issue.searchParams.set('title', `[旅遊收集][${data.country}] ${data.title.trim()}`);
    issue.searchParams.set('body', `## 基本資料\n- 國家：${data.country}\n- 城市：${data.city.trim()}\n- 分類：${data.category}\n- 來源：${source.href}\n- 收集日期：${new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date())}\n- 狀態：待查核\n\n## 想保留的重點\n${data.notes.trim()}\n\n## 整理流程\n- [ ] 核對官方資訊與查核日期\n- [ ] 合併重複資料\n- [ ] 整理到攻略頁並記錄變更\n`);
    // Open only a draft. GitHub authentication and final submission remain with the user.
    const opened = window.open(issue.href, '_blank', 'noopener,noreferrer');
    const status = document.querySelector('#collect-status');
    status.replaceChildren(document.createTextNode('請在 GitHub 確認並送出後完成儲存。若新分頁未開啟：'));
    const fallback = document.createElement('a'); fallback.href = issue.href; fallback.target = '_blank'; fallback.rel = 'noopener noreferrer'; fallback.textContent = '開啟確認頁'; status.append(fallback);
  });
  // Keep old deep links useful after migration; no dependency on rewrite rules.
  if (location.pathname.endsWith('/') || location.pathname.endsWith('/index.html')) {
    const old = {visa:'prep.html',flight:'prep.html',transport:'transport.html',destinations:'france.html',disney:'disney.html',souvenir:'shopping.html',luxury:'shopping.html',taxrefund:'shopping.html',tips:'prep.html'};
    const target = old[location.hash.slice(1)];
    if (target) location.replace(target);
  }
})();
