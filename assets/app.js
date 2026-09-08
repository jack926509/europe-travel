'use strict';
(() => {
  // ---- 深色模式：跟隨系統，使用者可自行覆寫並記住選擇 ----
  const root = document.documentElement;
  const toggle = document.querySelector('#theme-toggle');
  if (toggle) {
    const system = window.matchMedia('(prefers-color-scheme: dark)');
    const label = toggle.querySelector('.theme-toggle-text');
    const isDark = () => (root.dataset.theme ? root.dataset.theme === 'dark' : system.matches);
    const render = () => {
      const dark = isDark();
      toggle.setAttribute('aria-pressed', String(dark));
      const text = dark ? '淺色模式' : '深色模式';
      if (label) label.textContent = text;
      toggle.title = `切換為${text}`;
      toggle.setAttribute('aria-label', `切換為${text}`);
    };
    toggle.hidden = false;
    render();
    toggle.addEventListener('click', () => {
      const next = isDark() ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('fep-theme', next); } catch { /* 無痕模式下略過保存 */ }
      render();
    });
    // 尚未手動覆寫時，系統設定改變要跟著更新按鈕文字。
    system.addEventListener('change', () => { if (!root.dataset.theme) render(); });
  }

  // ---- 主導覽：把目前頁面捲進視野，並提示左右還有項目 ----
  const nav = document.querySelector('.main-nav');
  if (nav) {
    const wrap = nav.parentElement;
    const marks = () => {
      const max = nav.scrollWidth - nav.clientWidth;
      const state = [];
      if (nav.scrollLeft > 4) state.push('start');
      if (nav.scrollLeft < max - 4) state.push('end');
      wrap.dataset.overflow = state.join(' ');
    };
    const current = nav.querySelector('[aria-current]');
    if (current) current.scrollIntoView({ inline: 'center', block: 'nearest' });
    marks();
    nav.addEventListener('scroll', marks, { passive: true });
    window.addEventListener('resize', marks);
  }

  // ---- 寬表格：可用鍵盤捲動，並在真的溢出時才顯示提示 ----
  for (const table of document.querySelectorAll('table')) {
    const check = () => {
      const wide = table.scrollWidth > table.clientWidth + 1;
      if (wide) table.tabIndex = 0; else table.removeAttribute('tabindex');
      const hint = table.previousElementSibling?.classList.contains('table-hint') ? table.previousElementSibling : null;
      if (wide && !hint) {
        const note = document.createElement('p');
        note.className = 'table-hint';
        note.textContent = '表格較寬，可左右捲動查看其餘欄位。';
        table.before(note);
      } else if (!wide && hint) hint.remove();
    };
    check();
    window.addEventListener('resize', check);
  }

  // ---- 回到頁面頂端 ----
  const toTop = document.querySelector('#to-top');
  if (toTop) {
    const watch = () => { toTop.hidden = window.scrollY < 700; };
    watch();
    window.addEventListener('scroll', watch, { passive: true });
    toTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      document.querySelector('.brand')?.focus();
    });
  }

  // ---- 頁內章節：跳轉後把焦點放到標題，鍵盤與螢幕閱讀器才跟得上 ----
  for (const jump of document.querySelectorAll('.page-toc a')) {
    jump.addEventListener('click', () => {
      const target = document.getElementById(decodeURIComponent(jump.hash.slice(1)));
      if (target) requestAnimationFrame(() => (target.querySelector('h2') || target).focus({ preventScroll: true }));
    });
  }

  // ---- 全文搜尋 ----
  const input = document.querySelector('#guide-search');
  if (input) {
    const results = document.querySelector('#search-results');
    const status = document.querySelector('#search-status');
    let records;
    let pending;
    let revision = 0;
    let timer;
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase();
    // 逐段輸出，命中的字詞用 <mark> 標出，避免以 innerHTML 插入未轉義內容。
    function highlight(target, text, words) {
      const lower = normalize(text);
      const spans = [];
      for (const word of words) {
        for (let at = lower.indexOf(word); at !== -1; at = lower.indexOf(word, at + word.length)) spans.push([at, at + word.length]);
      }
      spans.sort((a, b) => a[0] - b[0]);
      let cursor = 0;
      for (const [start, end] of spans) {
        if (start < cursor) continue;
        target.append(text.slice(cursor, start));
        const mark = document.createElement('mark');
        mark.textContent = text.slice(start, end);
        target.append(mark);
        cursor = end;
      }
      target.append(text.slice(cursor));
    }
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
        status.textContent = hits.length ? `找到 ${hits.length} 個相關頁面；按 Enter 開啟第一筆。舊資料的查核狀態請見各頁標示。` : '找不到資料，試試城市名稱、中文或當地名稱。';
        for (const hit of hits) {
          const article = document.createElement('article'); article.className = 'search-result';
          const a = document.createElement('a'); a.href = hit.url; a.textContent = hit.title;
          const p = document.createElement('p');
          const at = Math.max(0, normalize(hit.text).indexOf(words[0]) - 24);
          highlight(p, (at ? '…' : '') + hit.text.slice(at, at + 160) + '…', words);
          article.append(a, p); results.append(article);
        }
      } catch {
        if (current === revision) status.textContent = '搜尋暫時無法載入，請使用上方國家與主題導覽，或稍後再試。';
      }
    }
    // 中文輸入法組字期間不送出查詢，打字停下來再搜尋。
    let composing = false;
    const schedule = () => { clearTimeout(timer); timer = setTimeout(search, 140); };
    input.addEventListener('compositionstart', () => { composing = true; });
    input.addEventListener('compositionend', () => { composing = false; schedule(); });
    input.addEventListener('input', () => { if (!composing) schedule(); });
    input.addEventListener('keydown', event => {
      if (event.key === 'Enter') { event.preventDefault(); results.querySelector('a')?.click(); }
      if (event.key === 'Escape' && input.value) { input.value = ''; search(); }
    });
    document.querySelector('#search-clear').addEventListener('click', () => { input.value = ''; search(); input.focus(); });
    // 「／」快速跳到搜尋框，跟多數文件站的習慣一致。
    document.addEventListener('keydown', event => {
      if (event.key !== '/' || event.metaKey || event.ctrlKey || event.altKey) return;
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || document.activeElement?.isContentEditable) return;
      event.preventDefault();
      input.focus();
      input.select();
    });
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
