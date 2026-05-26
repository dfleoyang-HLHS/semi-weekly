// ============================================================
// 半導體週報 - 前端主程式
// 載入 data/db.json 與 data/companies.json,渲染首頁
// ============================================================

const DB_URL = 'data/db.json';
const COMPANIES_URL = 'data/companies.json';

let allArticles = [];
let allCompanies = [];

async function loadData() {
  try {
    const [dbRes, compRes] = await Promise.all([
      fetch(DB_URL),
      fetch(COMPANIES_URL),
    ]);
    const db = await dbRes.json();
    allArticles = db.articles || [];
    allCompanies = await compRes.json();

    renderLatest();
    renderCompanyCloud();
    renderArticleList(allArticles);
  } catch (err) {
    document.getElementById('latest-content').innerHTML =
      '<p style="color:var(--danger)">無法載入資料。請先執行 <code>python scripts/build_index.py</code></p>';
    console.error(err);
  }
}

function renderLatest() {
  const el = document.getElementById('latest-content');
  if (!allArticles.length) {
    el.innerHTML = '<p>尚無報告</p>';
    return;
  }
  const latest = allArticles[0];
  el.innerHTML = `
    <div class="article-title">${latest.title}</div>
    <div class="meta">📅 ${latest.date} · ${latest.week || ''} · ${(latest.regions || []).join(' / ')}</div>
    <div class="summary">${latest.summary}</div>
    <a href="article.html?slug=${encodeURIComponent(latest.slug)}" class="read-more">閱讀完整報告 →</a>
  `;
}

function renderCompanyCloud() {
  const el = document.getElementById('company-cloud');
  if (!allCompanies.length) {
    el.innerHTML = '<p style="color:var(--text-dim)">尚無資料</p>';
    return;
  }
  // 取前 20 名
  const top = allCompanies.slice(0, 20);
  el.innerHTML = top.map(c => `
    <a href="company.html?name=${encodeURIComponent(c.name)}" class="company-tag">
      ${c.name} <span class="count">${c.count}</span>
    </a>
  `).join('');
}

function renderArticleList(articles) {
  const el = document.getElementById('article-list');
  if (!articles.length) {
    el.innerHTML = '<p style="color:var(--text-dim)">沒有符合的文章</p>';
    return;
  }
  el.innerHTML = articles.map(a => `
    <article class="article-card">
      ${a.week ? `<span class="week-badge">${a.week}</span>` : ''}
      <h3><a href="article.html?slug=${encodeURIComponent(a.slug)}">${a.title}</a></h3>
      <div class="meta">📅 ${a.date} · ${(a.regions || []).join(' / ')}</div>
      <div class="summary">${a.summary}</div>
      ${(a.tags || []).length ? `
        <div class="tags">
          ${a.tags.map(t => `<span class="tag">#${t}</span>`).join('')}
        </div>
      ` : ''}
    </article>
  `).join('');
}

// 搜尋與篩選
function applyFilters() {
  const q = document.getElementById('search-input').value.toLowerCase();
  const region = document.getElementById('region-filter').value;

  const filtered = allArticles.filter(a => {
    const haystack = [
      a.title, a.summary,
      ...(a.tags || []), ...(a.companies || []),
    ].join(' ').toLowerCase();
    const matchText = !q || haystack.includes(q);
    const matchRegion = !region || (a.regions || []).includes(region);
    return matchText && matchRegion;
  });
  renderArticleList(filtered);
}

document.addEventListener('DOMContentLoaded', () => {
  loadData();
  const search = document.getElementById('search-input');
  const region = document.getElementById('region-filter');
  if (search) search.addEventListener('input', applyFilters);
  if (region) region.addEventListener('change', applyFilters);
});
