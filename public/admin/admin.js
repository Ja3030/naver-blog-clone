// admin.js — GitHub API 기반 블로그 어드민
const REPO = 'Ja3030/naver-blog-clone';
const POST_PATH = 'public/posts/tonsil-stone';
const BRANCH = 'main';

let PAT = '';
let blocks = [];
let config = {};
let fileShas = {}; // { 'index.html': sha, 'config.json': sha }
let currentImageBlockId = null;

// ===== Auth =====
function doLogin() {
  const pat = document.getElementById('pat-input').value.trim();
  if (!pat) return;
  PAT = pat;
  ghAPI('/repos/' + REPO).then(r => {
    if (r.ok) {
      sessionStorage.setItem('gh_pat', pat);
      document.getElementById('login-screen').style.display = 'none';
      document.getElementById('editor-screen').style.display = 'block';
      loadPost();
    } else {
      document.getElementById('login-error').textContent = 'PAT이 유효하지 않습니다';
    }
  });
}

function doLogout() {
  sessionStorage.removeItem('gh_pat');
  PAT = '';
  location.reload();
}

// 세션 복원
(function () {
  const saved = sessionStorage.getItem('gh_pat');
  if (saved) {
    PAT = saved;
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('editor-screen').style.display = 'block';
    loadPost();
  }
})();

// ===== GitHub API =====
function ghAPI(path, opts = {}) {
  return fetch('https://api.github.com' + path, {
    ...opts,
    headers: {
      Authorization: 'Bearer ' + PAT,
      Accept: 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      ...(opts.headers || {})
    }
  });
}

async function getFile(filePath) {
  const r = await ghAPI('/repos/' + REPO + '/contents/' + POST_PATH + '/' + filePath + '?ref=' + BRANCH);
  const data = await r.json();
  fileShas[filePath] = data.sha;
  const binary = atob(data.content.replace(/\n/g, ''));
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return new TextDecoder('utf-8').decode(bytes);
}

async function putFile(filePath, content, message) {
  const encoded = btoa(unescape(encodeURIComponent(content)));
  const r = await ghAPI('/repos/' + REPO + '/contents/' + POST_PATH + '/' + filePath, {
    method: 'PUT',
    body: JSON.stringify({
      message: message,
      content: encoded,
      sha: fileShas[filePath],
      branch: BRANCH
    })
  });
  const data = await r.json();
  if (data.content) fileShas[filePath] = data.content.sha;
  return r.ok;
}

async function uploadImage(file) {
  const name = Date.now() + '_' + file.name.replace(/[^a-zA-Z0-9._-]/g, '');
  const reader = new FileReader();
  return new Promise((resolve, reject) => {
    reader.onload = async () => {
      const base64 = reader.result.split(',')[1];
      const r = await ghAPI('/repos/' + REPO + '/contents/' + POST_PATH + '/images/' + name, {
        method: 'PUT',
        body: JSON.stringify({
          message: 'Upload image: ' + name,
          content: base64,
          branch: BRANCH
        })
      });
      if (r.ok) resolve('./images/' + name);
      else {
        const err = await r.json().catch(() => ({}));
        console.error('Image upload error:', r.status, err);
        reject(new Error('Image upload failed: ' + (err.message || r.status)));
      }
    };
    reader.readAsDataURL(file);
  });
}

// ===== Load Post =====
async function loadPost() {
  showLoading('불러오는 중...');
  try {
    const [html, configStr] = await Promise.all([
      getFile('index.html'),
      getFile('config.json')
    ]);
    config = JSON.parse(configStr);
    loadConfig();
    parseBlocks(html);
    renderBlocks();
    toast('불러오기 완료', 'success');
  } catch (e) {
    toast('불러오기 실패: ' + e.message, 'error');
  }
  hideLoading();
}

// ===== Config UI =====
function loadConfig() {
  document.getElementById('cfg-post-title').value = config.post?.title || '';
  document.getElementById('cfg-category').value = config.post?.category || '';
  document.getElementById('cfg-date').value = config.post?.date || '';
  document.getElementById('cfg-blog-name').value = config.blog?.name || '';
  document.getElementById('cfg-blog-title').value = config.blog?.title || '';
  document.getElementById('cfg-likes').value = config.social?.likes || 0;
  document.getElementById('cfg-shares').value = config.social?.shares || 0;
  document.getElementById('cfg-views').value = config.social?.views || 0;
  document.getElementById('cfg-cta-url').value = config.cta?.url || '';
  document.getElementById('cfg-cta-text').value = config.cta?.text || '';
  renderComments();
}

function collectConfig() {
  config.post = {
    title: document.getElementById('cfg-post-title').value,
    category: document.getElementById('cfg-category').value,
    date: document.getElementById('cfg-date').value
  };
  config.blog = {
    ...config.blog,
    name: document.getElementById('cfg-blog-name').value,
    title: document.getElementById('cfg-blog-title').value
  };
  config.social = {
    likes: parseInt(document.getElementById('cfg-likes').value) || 0,
    shares: parseInt(document.getElementById('cfg-shares').value) || 0,
    views: parseInt(document.getElementById('cfg-views').value) || 0
  };
  config.cta = {
    url: document.getElementById('cfg-cta-url').value,
    text: document.getElementById('cfg-cta-text').value
  };
  collectComments();
}

// ===== Comments =====
function renderComments() {
  const list = document.getElementById('comments-list');
  list.innerHTML = (config.comments || []).map((c, i) => `
    <div class="comment-item" data-idx="${i}">
      <div class="comment-row">
        <input type="text" value="${esc(c.author)}" placeholder="작성자" data-field="author">
        <input type="text" value="${esc(c.time)}" placeholder="시간" data-field="time">
      </div>
      <textarea data-field="text" placeholder="댓글 내용">${esc(c.text)}</textarea>
      <div class="comment-row">
        <input type="number" value="${c.likes || 0}" placeholder="좋아요" data-field="likes">
        <button class="btn-danger" onclick="removeComment(${i})">삭제</button>
      </div>
    </div>
  `).join('');
}

function collectComments() {
  const items = document.querySelectorAll('.comment-item');
  config.comments = Array.from(items).map(el => ({
    author: el.querySelector('[data-field="author"]').value,
    profile_color: config.comments?.[el.dataset.idx]?.profile_color || '#ccc',
    time: el.querySelector('[data-field="time"]').value,
    text: el.querySelector('[data-field="text"]').value,
    likes: parseInt(el.querySelector('[data-field="likes"]').value) || 0
  }));
}

function addComment() {
  if (!config.comments) config.comments = [];
  collectComments();
  config.comments.push({ author: '', profile_color: '#ccc', time: '방금 전', text: '', likes: 0 });
  renderComments();
}

function removeComment(idx) {
  collectComments();
  config.comments.splice(idx, 1);
  renderComments();
}

// ===== Block Parser =====
function parseBlocks(html) {
  blocks = [];
  const startMarker = '<!-- POST CONTENT START -->';
  const endMarker = '<!-- POST CONTENT END -->';
  const startIdx = html.indexOf(startMarker);
  const endIdx = html.indexOf(endMarker);
  if (startIdx < 0 || endIdx < 0) { toast('POST CONTENT 마커를 찾을 수 없습니다', 'error'); return; }

  const content = html.substring(startIdx + startMarker.length, endIdx).trim();

  // se-component 단위로 분리
  const regex = /<div class="se-component ([^"]*)"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>/g;
  // 더 안전한 방식: 임시 DOM 파싱
  const parser = new DOMParser();
  const doc = parser.parseFromString('<div id="root">' + content + '</div>', 'text/html');
  const components = doc.querySelectorAll('#root > .se-component');

  components.forEach((comp, idx) => {
    if (comp.classList.contains('se-text')) {
      // 텍스트 블록
      const paragraphs = [];
      // CTA 링크 감지: <a> 태그가 있는 문단이 있으면 CTA 블록으로 분리
      let hasCta = false;
      let ctaText = '';
      let ctaUrl = '';
      comp.querySelectorAll('.se-text-paragraph').forEach(p => {
        const link = p.querySelector('a');
        const span = p.querySelector('span');
        const bold = !!p.querySelector('b');
        let fontSize = 'fs15';
        if (span) {
          const cls = Array.from(span.classList).find(c => c.startsWith('se-fs-'));
          if (cls) fontSize = cls.replace('se-fs-', '');
        }
        // 색상 감지
        let color = '';
        if (span && span.style.color) {
          color = span.style.color;
        }
        if (link) {
          hasCta = true;
          ctaText = link.textContent.trim();
          ctaUrl = link.getAttribute('href') || '';
        } else {
          // 빈 줄 감지: <br>만 있거나, span 안에 <br>만 있거나, 텍스트가 빈 경우
          const hasBr = !!p.querySelector('br');
          const rawText = p.textContent.replace(/\u200B/g, '').trim();
          const text = (hasBr && !rawText) ? '' : rawText;
          paragraphs.push({ text, bold, fontSize, color });
        }
      });
      if (paragraphs.length > 0) {
        blocks.push({ id: genId(), type: 'text', paragraphs });
      }
      if (hasCta) {
        blocks.push({ id: genId(), type: 'cta', text: ctaText, url: ctaUrl });
      }
    } else if (comp.classList.contains('se-image')) {
      // 이미지 블록
      const img = comp.querySelector('img');
      blocks.push({
        id: genId(),
        type: 'image',
        src: img ? img.getAttribute('src') : '',
        alt: img ? img.getAttribute('alt') || '' : ''
      });
    } else if (comp.classList.contains('se-horizontalLine')) {
      blocks.push({ id: genId(), type: 'hr' });
    }
  });
}

// Enter 키 일관성: 모든 contenteditable에서 <div>로 줄바꿈
try { document.execCommand('defaultParagraphSeparator', false, 'div'); } catch(e) {}

// ===== Block Renderer =====
function renderBlocks() {
  const container = document.getElementById('blocks-container');
  container.innerHTML = blocks.map((b, idx) => {
    const controls = `
      <div class="block-controls">
        ${idx > 0 ? '<button onclick="moveBlock(' + idx + ',-1)" title="위로">↑</button>' : ''}
        ${idx < blocks.length - 1 ? '<button onclick="moveBlock(' + idx + ',1)" title="아래로">↓</button>' : ''}
        <button onclick="removeBlock(' + idx + ')" title="삭제" style="color:#e53e3e">×</button>
      </div>`;

    if (b.type === 'text') {
      const fsOptions = ['fs11','fs13','fs15','fs17','fs19','fs24','fs28','fs34'].map(f =>
        '<option value="' + f + '"' + (b.paragraphs[0]?.fontSize === f ? ' selected' : '') + '>' + f.replace('fs','') + 'px</option>'
      ).join('');
      const html = b.paragraphs.map(p => {
        const content = p.text ? ((p.bold ? '<b>' : '') + esc(p.text) + (p.bold ? '</b>' : '')) : '<br>';
        const cStyle = p.color ? ' style="color:' + p.color + '"' : '';
        return '<div' + cStyle + '>' + content + '</div>';
      }).join('');
      return `<div class="block block-text" data-idx="${idx}">
        ${controls}
        <div class="text-toolbar">
          <button onclick="toggleBold(${idx})" class="${b.paragraphs[0]?.bold ? 'active' : ''}" title="굵게"><b>B</b></button>
          <select onchange="changeFontSize(${idx}, this.value)">${fsOptions}</select>
          <input type="color" value="${b.paragraphs[0]?.color ? colorToHex(b.paragraphs[0].color) : '#000000'}" onchange="changeColor(${idx}, this.value)" title="글씨 색">
          <button onclick="changeColor(${idx}, '')" title="색상 초기화" class="btn-reset-color">↺</button>
        </div>
        <div class="block-content" contenteditable="true" data-idx="${idx}"
             oninput="updateTextBlock(${idx}, this)">${html}</div>
      </div>`;
    }

    if (b.type === 'image') {
      const inner = b.src
        ? '<img src="' + resolveImageUrl(b.src) + '" alt="' + esc(b.alt) + '">'
        : '<div class="image-placeholder">클릭하여 이미지 추가</div>';
      return `<div class="block block-image" data-idx="${idx}" onclick="pickImage(${idx})">
        ${controls}
        ${inner}
      </div>`;
    }

    if (b.type === 'cta') {
      return `<div class="block block-cta" data-idx="${idx}">
        ${controls}
        <div class="cta-label">🔗 CTA 버튼</div>
        <input type="text" class="cta-text-input" value="${esc(b.text)}" placeholder="버튼 텍스트 (예: 여기서 확인해보세요 →)" oninput="updateCtaBlock(${idx}, 'text', this.value)">
        <input type="url" class="cta-url-input" value="${esc(b.url)}" placeholder="링크 URL" oninput="updateCtaBlock(${idx}, 'url', this.value)">
      </div>`;
    }

    if (b.type === 'hr') {
      return `<div class="block block-hr" data-idx="${idx}">
        ${controls}
        <hr>
      </div>`;
    }
  }).join('');
}

function resolveImageUrl(src) {
  if (src.startsWith('http')) return src;
  if (src.startsWith('./')) {
    return 'https://raw.githubusercontent.com/' + REPO + '/' + BRANCH + '/' + POST_PATH + '/' + src.substring(2);
  }
  return src;
}

// ===== Block Actions =====
function addBlock(type) {
  if (type === 'text') {
    blocks.push({ id: genId(), type: 'text', paragraphs: [{ text: '', bold: false, fontSize: 'fs15' }] });
  } else if (type === 'image') {
    blocks.push({ id: genId(), type: 'image', src: '', alt: '' });
  } else if (type === 'hr') {
    blocks.push({ id: genId(), type: 'hr' });
  } else if (type === 'cta') {
    blocks.push({ id: genId(), type: 'cta', text: '여기서 확인해보세요 →', url: '' });
  }
  renderBlocks();
}

function removeBlock(idx) {
  blocks.splice(idx, 1);
  renderBlocks();
}

function moveBlock(idx, dir) {
  const newIdx = idx + dir;
  if (newIdx < 0 || newIdx >= blocks.length) return;
  [blocks[idx], blocks[newIdx]] = [blocks[newIdx], blocks[idx]];
  renderBlocks();
}

function updateTextBlock(idx, el) {
  const b = blocks[idx];
  const baseBold = b.paragraphs[0]?.bold || false;
  const baseFontSize = b.paragraphs[0]?.fontSize || 'fs15';
  const baseColor = b.paragraphs[0]?.color || '';

  // contenteditable에서 각 줄은 <div> 안에 들어감 (Chrome 기본 동작)
  const children = el.childNodes;
  const lines = [];

  if (children.length === 0) {
    // 빈 블록
    lines.push('');
  } else {
    for (const node of children) {
      if (node.nodeType === Node.TEXT_NODE) {
        // 첫 줄이 div로 안 감싸진 경우
        const text = node.textContent.replace(/\u200B/g, '');
        lines.push(text);
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        const tag = node.tagName.toLowerCase();
        if (tag === 'br') {
          // 단독 <br>은 빈 줄
          lines.push('');
        } else {
          // <div>, <p> 등
          const text = node.textContent.replace(/\u200B/g, '');
          // <div><br></div>는 빈 줄
          if (!text && node.querySelector('br')) {
            lines.push('');
          } else {
            lines.push(text);
          }
        }
      }
    }
  }

  b.paragraphs = lines.map(line => ({
    text: line,
    bold: baseBold,
    fontSize: baseFontSize,
    color: baseColor
  }));
}

function updateCtaBlock(idx, field, value) {
  blocks[idx][field] = value;
}

function toggleBold(idx) {
  const b = blocks[idx];
  const newBold = !b.paragraphs[0]?.bold;
  b.paragraphs.forEach(p => p.bold = newBold);
  renderBlocks();
}

function changeFontSize(idx, fs) {
  blocks[idx].paragraphs.forEach(p => p.fontSize = fs);
}

function changeColor(idx, color) {
  blocks[idx].paragraphs.forEach(p => p.color = color);
  renderBlocks();
}

function colorToHex(c) {
  if (!c) return '#000000';
  if (c.startsWith('#')) return c;
  // rgb(r, g, b) → #rrggbb
  const m = c.match(/(\d+)/g);
  if (m && m.length >= 3) {
    return '#' + m.slice(0,3).map(n => parseInt(n).toString(16).padStart(2,'0')).join('');
  }
  return '#000000';
}

// ===== Image Upload =====
function pickImage(idx) {
  currentImageBlockId = idx;
  document.getElementById('image-upload').click();
}

document.getElementById('image-upload')?.addEventListener('change', async function (e) {
  const file = e.target.files[0];
  if (!file || currentImageBlockId === null) return;
  showLoading('이미지 업로드 중...');
  try {
    const src = await uploadImage(file);
    blocks[currentImageBlockId].src = src;
    blocks[currentImageBlockId].alt = file.name;
    renderBlocks();
    toast('이미지 업로드 완료', 'success');
  } catch (err) {
    toast('이미지 업로드 실패: ' + err.message, 'error');
  }
  hideLoading();
  this.value = '';
  currentImageBlockId = null;
});

// ===== Serializer: Blocks → SE HTML =====
function blocksToHTML() {
  return blocks.map(b => {
    if (b.type === 'text') {
      const paras = b.paragraphs.map(p => {
        const text = p.text || '';
        const colorStyle = p.color ? ' style="color:' + p.color + '"' : '';
        if (!text.trim()) {
          return `      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-${p.fontSize} se-ff-system"${colorStyle}><br></span>
      </p>`;
        }
        const inner = p.bold ? '<b>' + esc(text) + '</b>' : esc(text);
        return `      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-${p.fontSize} se-ff-system"${colorStyle}>${inner}</span>
      </p>`;
      }).join('\n');
      return `<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
${paras}
    </div>
  </div>
</div>`;
    }

    if (b.type === 'image') {
      return `<div class="se-component se-image se-l-default">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a class="se-module-image-link">
        <img src="${esc(b.src)}" alt="${esc(b.alt)}" class="se-image-resource">
      </a>
    </div>
  </div>
</div>`;
    }

    if (b.type === 'cta') {
      const href = b.url || '#';
      const text = b.text || 'CTA';
      return `<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><a href="${esc(href)}" target="_blank" rel="noopener" onclick="if(typeof fbq==='function'){fbq('track','Lead');}">${esc(text)}</a></span>
      </p>
    </div>
  </div>
</div>`;
    }

    if (b.type === 'hr') {
      return `<div class="se-component se-horizontalLine se-l-default">
  <div class="se-section se-section-horizontalLine se-l-default">
    <div class="se-module se-module-horizontalLine">
      <hr class="se-hr">
    </div>
  </div>
</div>`;
    }
    return '';
  }).join('\n\n');
}

// ===== Save All =====
async function saveAll() {
  collectConfig();
  const saveBtn = document.querySelector('.btn-primary');
  saveBtn.disabled = true;
  saveBtn.textContent = '저장 중...';
  showLoading('저장 & 배포 중...');

  try {
    // 1. config.json 저장
    const configOk = await putFile('config.json', JSON.stringify(config, null, 2) + '\n', 'Update config.json via admin');
    if (!configOk) throw new Error('config.json 저장 실패');

    // 2. index.html 본문 교체 후 저장
    const currentHtml = await getFile('index.html');
    const startMarker = '<!-- POST CONTENT START -->';
    const endMarker = '<!-- POST CONTENT END -->';
    const startIdx = currentHtml.indexOf(startMarker);
    const endIdx = currentHtml.indexOf(endMarker);
    if (startIdx < 0 || endIdx < 0) throw new Error('POST CONTENT 마커 없음');

    const before = currentHtml.substring(0, startIdx + startMarker.length);
    const after = currentHtml.substring(endIdx);
    const newContent = blocksToHTML();
    const newHtml = before + '\n\n' + newContent + '\n\n' + after;

    const htmlOk = await putFile('index.html', newHtml, 'Update post content via admin');
    if (!htmlOk) throw new Error('index.html 저장 실패');

    toast('저장 완료! Vercel 배포 진행 중...', 'success');
    document.getElementById('deploy-status').textContent = '✅ 저장됨 ' + new Date().toLocaleTimeString();
  } catch (e) {
    toast('저장 실패: ' + e.message, 'error');
  }

  saveBtn.disabled = false;
  saveBtn.textContent = '저장 & 배포';
  hideLoading();
}

// ===== Utils =====
function genId() { return 'b' + Math.random().toString(36).substring(2, 8); }
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

function toast(msg, type = 'info') {
  const el = document.createElement('div');
  el.className = 'toast toast-' + type;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function showLoading(msg) {
  if (document.getElementById('loading-overlay')) return;
  const el = document.createElement('div');
  el.id = 'loading-overlay';
  el.className = 'loading-overlay';
  el.textContent = msg || '로딩 중...';
  document.body.appendChild(el);
}

function hideLoading() {
  document.getElementById('loading-overlay')?.remove();
}
