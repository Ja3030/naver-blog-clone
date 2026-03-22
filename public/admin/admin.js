// admin.js — 멀티 포스트 contenteditable 에디터
const REPO = 'Ja3030/naver-blog-clone';
const BRANCH = 'main';
const BASE_URL = 'https://naver-blog-clone-ten.vercel.app/posts/';

let PAT = '';
let currentPostSlug = '';
let config = {};
let fileShas = {};
let rawHtml = ''; // 원본 index.html 전체

function getPostPath() {
  return 'public/posts/' + currentPostSlug;
}

// ===== Auth =====
function doLogin() {
  const pat = document.getElementById('pat-input').value.trim();
  if (!pat) return;
  PAT = pat;
  ghAPI('/repos/' + REPO).then(r => {
    if (r.ok) {
      sessionStorage.setItem('gh_pat', pat);
      showScreen('postlist');
      loadPostList();
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

function showScreen(name) {
  document.getElementById('login-screen').style.display = name === 'login' ? '' : 'none';
  document.getElementById('postlist-screen').style.display = name === 'postlist' ? 'block' : 'none';
  document.getElementById('editor-screen').style.display = name === 'editor' ? 'block' : 'none';
}

(function () {
  const saved = sessionStorage.getItem('gh_pat');
  if (saved) {
    PAT = saved;
    showScreen('postlist');
    loadPostList();
  }
})();

// ===== Post List =====
async function loadPostList() {
  const grid = document.getElementById('postlist-grid');
  grid.innerHTML = '<p class="postlist-loading">게시글 목록을 불러오는 중...</p>';
  try {
    const r = await ghAPI('/repos/' + REPO + '/contents/public/posts?ref=' + BRANCH);
    const items = await r.json();
    const dirs = items.filter(i => i.type === 'dir');

    // Fetch config.json for each post in parallel
    const cards = await Promise.all(dirs.map(async (dir) => {
      try {
        const cr = await ghAPI('/repos/' + REPO + '/contents/public/posts/' + dir.name + '/config.json?ref=' + BRANCH);
        const cdata = await cr.json();
        const binary = atob(cdata.content.replace(/\n/g, ''));
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
        const cfg = JSON.parse(new TextDecoder('utf-8').decode(bytes));
        return { slug: dir.name, config: cfg };
      } catch (e) {
        return { slug: dir.name, config: null };
      }
    }));

    grid.innerHTML = '';
    cards.forEach(({ slug, config: cfg }) => {
      const title = cfg?.post?.title || slug;
      const blogName = cfg?.blog?.name || '-';
      const date = cfg?.post?.date || '-';
      const card = document.createElement('div');
      card.className = 'post-card';
      card.innerHTML = `
        <div class="post-card-body">
          <h3 class="post-card-title">${esc(title)}</h3>
          <p class="post-card-meta">${esc(blogName)} · ${esc(date)}</p>
          <p class="post-card-slug">${esc(slug)}</p>
        </div>
        <div class="post-card-actions">
          <button class="btn-primary btn-sm" onclick="selectPost('${esc(slug)}')">편집</button>
          <a href="${BASE_URL}${encodeURIComponent(slug)}/" target="_blank" class="btn-secondary btn-sm" style="text-decoration:none">보기 ↗</a>
        </div>
      `;
      grid.appendChild(card);
    });

    if (cards.length === 0) {
      grid.innerHTML = '<p class="postlist-loading">게시글이 없습니다.</p>';
    }
  } catch (e) {
    grid.innerHTML = '<p class="postlist-loading" style="color:#e53e3e">목록 불러오기 실패: ' + esc(e.message) + '</p>';
  }
}

function selectPost(slug) {
  currentPostSlug = slug;
  document.getElementById('view-post-link').href = BASE_URL + encodeURIComponent(slug) + '/';
  showScreen('editor');
  loadPost();
}

function backToList() {
  currentPostSlug = '';
  fileShas = {};
  config = {};
  rawHtml = '';
  document.getElementById('editor').innerHTML = '';
  document.getElementById('deploy-status').textContent = '';
  showScreen('postlist');
  loadPostList();
}

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
  const r = await ghAPI('/repos/' + REPO + '/contents/' + getPostPath() + '/' + filePath + '?ref=' + BRANCH);
  const data = await r.json();
  fileShas[filePath] = data.sha;
  const binary = atob(data.content.replace(/\n/g, ''));
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return new TextDecoder('utf-8').decode(bytes);
}

async function putFile(filePath, content, message) {
  const encoded = btoa(unescape(encodeURIComponent(content)));
  const r = await ghAPI('/repos/' + REPO + '/contents/' + getPostPath() + '/' + filePath, {
    method: 'PUT',
    body: JSON.stringify({ message, content: encoded, sha: fileShas[filePath], branch: BRANCH })
  });
  const data = await r.json();
  if (data.content) fileShas[filePath] = data.content.sha;
  return r.ok;
}

async function uploadImageFile(file) {
  const name = Date.now() + '_' + file.name.replace(/[^a-zA-Z0-9._-]/g, '');
  const reader = new FileReader();
  return new Promise((resolve, reject) => {
    reader.onload = async () => {
      const base64 = reader.result.split(',')[1];
      const r = await ghAPI('/repos/' + REPO + '/contents/' + getPostPath() + '/images/' + name, {
        method: 'PUT',
        body: JSON.stringify({ message: 'Upload image: ' + name, content: base64, branch: BRANCH })
      });
      if (r.ok) resolve('./images/' + name);
      else reject(new Error('Upload failed'));
    };
    reader.readAsDataURL(file);
  });
}

// ===== Font Size Map =====
const FS_MAP = { 11:'fs11', 13:'fs13', 15:'fs15', 17:'fs17', 19:'fs19', 24:'fs24', 28:'fs28', 34:'fs34' };
const FS_REV = {}; Object.keys(FS_MAP).forEach(k => FS_REV[FS_MAP[k]] = k);

function resolveImageUrl(src) {
  if (!src) return '';
  if (src.startsWith('http')) return src;
  if (src.startsWith('./')) return 'https://raw.githubusercontent.com/' + REPO + '/' + BRANCH + '/' + getPostPath() + '/' + src.substring(2);
  return src;
}

// ===== Load Post =====
async function loadPost() {
  showLoading('불러오는 중...');
  try {
    const [html, configStr] = await Promise.all([getFile('index.html'), getFile('config.json')]);
    rawHtml = html;
    config = JSON.parse(configStr);
    loadConfig();
    loadEditor(html);
    toast('불러오기 완료', 'success');
  } catch (e) {
    toast('불러오기 실패: ' + e.message, 'error');
  }
  hideLoading();
}

// ===== SE HTML → Editor HTML =====
function loadEditor(html) {
  const startMarker = '<!-- POST CONTENT START -->';
  const endMarker = '<!-- POST CONTENT END -->';
  const s = html.indexOf(startMarker);
  const e = html.indexOf(endMarker);
  if (s < 0 || e < 0) { toast('POST CONTENT 마커 없음', 'error'); return; }

  const content = html.substring(s + startMarker.length, e).trim();
  const parser = new DOMParser();
  const doc = parser.parseFromString('<div id="root">' + content + '</div>', 'text/html');
  const components = doc.querySelectorAll('#root > .se-component');

  const editor = document.getElementById('editor');
  editor.innerHTML = '';

  components.forEach(comp => {
    if (comp.classList.contains('se-text')) {
      comp.querySelectorAll('.se-text-paragraph').forEach(p => {
        const div = document.createElement('div');
        const span = p.querySelector('span');
        const link = p.querySelector('a');
        const bold = !!p.querySelector('b');
        const hasBr = !!p.querySelector('br');

        // fontSize
        let fs = '15';
        if (span) {
          const cls = Array.from(span.classList).find(c => c.startsWith('se-fs-'));
          if (cls) fs = cls.replace('se-fs-fs', '');
        }

        // color
        let color = '';
        if (span && span.style.color) color = span.style.color;

        if (link) {
          // CTA link
          const a = document.createElement('a');
          a.href = link.getAttribute('href') || '#';
          a.textContent = link.textContent;
          a.className = 'editor-cta';
          a.contentEditable = 'false';
          a.setAttribute('data-cta', 'true');
          div.appendChild(a);
        } else {
          const rawText = p.textContent.replace(/\u200B/g, '').trim();
          if (hasBr && !rawText) {
            div.innerHTML = '<br>';
          } else {
            const textSpan = document.createElement('span');
            if (fs !== '15') textSpan.style.fontSize = fs + 'px';
            if (color) textSpan.style.color = color;
            if (bold) {
              const b = document.createElement('b');
              b.textContent = rawText;
              textSpan.appendChild(b);
            } else {
              textSpan.textContent = rawText;
            }
            div.appendChild(textSpan);
          }
        }
        editor.appendChild(div);
      });
    } else if (comp.classList.contains('se-image')) {
      const img = comp.querySelector('img');
      if (img) {
        const wrapper = document.createElement('div');
        wrapper.className = 'editor-image-wrapper';
        wrapper.contentEditable = 'false';
        const imgEl = document.createElement('img');
        imgEl.src = resolveImageUrl(img.getAttribute('src') || '');
        imgEl.setAttribute('data-src', img.getAttribute('src') || '');
        imgEl.alt = img.getAttribute('alt') || '';
        wrapper.appendChild(imgEl);
        // 교체 버튼
        const replace = document.createElement('button');
        replace.className = 'img-replace';
        replace.textContent = '🔄';
        replace.title = '이미지 교체';
        replace.onclick = () => { triggerImageReplace(wrapper); };
        wrapper.appendChild(replace);
        // 삭제 버튼
        const del = document.createElement('button');
        del.className = 'img-delete';
        del.textContent = '×';
        del.onclick = () => { wrapper.remove(); };
        wrapper.appendChild(del);
        // 이미지 클릭으로도 교체
        imgEl.style.cursor = 'pointer';
        imgEl.onclick = () => { triggerImageReplace(wrapper); };
        editor.appendChild(wrapper);
      }
    } else if (comp.classList.contains('se-horizontalLine')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'editor-hr-wrapper';
      wrapper.contentEditable = 'false';
      wrapper.innerHTML = '<hr><button class="hr-delete" onclick="this.parentElement.remove()">×</button>';
      editor.appendChild(wrapper);
    }
  });

  // 에디터가 비어있으면 빈 div 추가
  if (!editor.innerHTML.trim()) {
    editor.innerHTML = '<div><br></div>';
  }
}

// ===== Editor HTML → SE HTML =====
function editorToSE() {
  const editor = document.getElementById('editor');
  const children = editor.childNodes;
  const seBlocks = [];
  let textParas = [];

  function flushText() {
    if (textParas.length === 0) return;
    const parasHtml = textParas.join('\n');
    seBlocks.push(`<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
${parasHtml}
    </div>
  </div>
</div>`);
    textParas = [];
  }

  for (const node of children) {
    if (node.nodeType !== Node.ELEMENT_NODE) continue;

    // 이미지 블록
    if (node.classList && node.classList.contains('editor-image-wrapper')) {
      flushText();
      const img = node.querySelector('img');
      const src = img?.getAttribute('data-src') || img?.getAttribute('src') || '';
      const alt = img?.alt || '';
      seBlocks.push(`<div class="se-component se-image se-l-default">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a class="se-module-image-link">
        <img src="${esc(src)}" alt="${esc(alt)}" class="se-image-resource">
      </a>
    </div>
  </div>
</div>`);
      continue;
    }

    // HR 블록
    if (node.classList && node.classList.contains('editor-hr-wrapper')) {
      flushText();
      seBlocks.push(`<div class="se-component se-horizontalLine se-l-default">
  <div class="se-section se-section-horizontalLine se-l-default">
    <div class="se-module se-module-horizontalLine">
      <hr class="se-hr">
    </div>
  </div>
</div>`);
      continue;
    }

    // CTA 링크
    const ctaLink = node.querySelector('[data-cta]');
    if (ctaLink) {
      const href = ctaLink.getAttribute('href') || '#';
      const text = ctaLink.textContent || 'CTA';
      textParas.push(`      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><a href="${esc(href)}" target="_blank" rel="noopener" onclick="if(typeof fbq==='function'){fbq('track','Lead');}">${esc(text)}</a></span>
      </p>`);
      continue;
    }

    // 텍스트 줄
    const text = node.textContent.replace(/\u200B/g, '').trim();
    const hasBr = node.querySelector('br') && !text;

    if (hasBr || (!text && node.innerHTML === '<br>') || node.innerHTML === '' || node.innerHTML === '<br>') {
      // 빈 줄
      textParas.push(`      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>`);
      continue;
    }

    // 줄 내 모든 인라인 요소를 개별 span으로 변환
    const spans = node.querySelectorAll('span');
    if (spans.length > 1) {
      // 여러 span이 있으면 각각의 서식을 보존
      let paraSpans = '';
      spans.forEach(s => {
        let fs = 'fs15';
        let color = '';
        let bold = false;
        const segText = s.textContent.replace(/\u200B/g, '').trim();
        if (!segText) return;

        if (s.style.fontSize) {
          const px = parseInt(s.style.fontSize);
          if (FS_MAP[px]) fs = FS_MAP[px];
        }
        if (s.style.color) color = s.style.color;
        if (s.querySelector('b') || s.querySelector('strong') || s.closest('b') || s.closest('strong')) bold = true;

        // font 태그 처리
        const font = s.querySelector('font');
        if (font) {
          if (font.color) color = font.color;
          if (font.size) {
            const sizeMap = {1:11, 2:13, 3:15, 4:17, 5:19, 6:24, 7:34};
            const px = sizeMap[parseInt(font.size)] || 15;
            if (FS_MAP[px]) fs = FS_MAP[px];
          }
        }

        const colorStyle = color ? ' style="color:' + color + '"' : '';
        const inner = bold ? '<b>' + esc(segText) + '</b>' : esc(segText);
        paraSpans += `<span class="se-fs-${fs} se-ff-system"${colorStyle}>${inner}</span>`;
      });
      if (paraSpans) {
        textParas.push(`      <p class="se-text-paragraph se-text-paragraph-align- ">
        ${paraSpans}
      </p>`);
      }
    } else {
      // 단일 span 또는 span 없음 — 기존 로직
      let fs = 'fs15';
      let color = '';
      let bold = false;

      const span = node.querySelector('span');
      if (span) {
        if (span.style.fontSize) {
          const px = parseInt(span.style.fontSize);
          if (FS_MAP[px]) fs = FS_MAP[px];
        }
        if (span.style.color) color = span.style.color;
      }
      if (node.querySelector('b') || node.querySelector('strong')) bold = true;

      // font 태그 (execCommand 산출물) 처리
      const font = node.querySelector('font');
      if (font) {
        if (font.color) color = font.color;
        if (font.size) {
          const sizeMap = {1:11, 2:13, 3:15, 4:17, 5:19, 6:24, 7:34};
          const px = sizeMap[parseInt(font.size)] || 15;
          if (FS_MAP[px]) fs = FS_MAP[px];
        }
      }

      const colorStyle = color ? ' style="color:' + color + '"' : '';
      const inner = bold ? '<b>' + esc(text) + '</b>' : esc(text);
      textParas.push(`      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-${fs} se-ff-system"${colorStyle}>${inner}</span>
      </p>`);
    }
  }

  flushText();
  return seBlocks.join('\n\n');
}

// ===== Toolbar Actions =====
function execFmt(cmd, value) {
  document.execCommand(cmd, false, value || null);
  document.getElementById('editor').focus();
}

function applyFontSizeAll(size) {
  if (!size) return;
  const editor = document.getElementById('editor');
  const lines = editor.querySelectorAll(':scope > div');
  lines.forEach(line => {
    // 이미지, HR, CTA 등 비편집 요소 건너뛰기
    if (line.querySelector('img') || line.querySelector('hr') || line.querySelector('[data-cta]')) return;
    if (line.getAttribute('contenteditable') === 'false') return;
    const spans = line.querySelectorAll('span');
    if (spans.length === 0) {
      const content = line.innerHTML;
      if (!content || content === '<br>') return;
      const span = document.createElement('span');
      span.innerHTML = content;
      line.innerHTML = '';
      line.appendChild(span);
      span.style.fontSize = size + 'px';
    } else {
      spans.forEach(s => s.style.fontSize = size + 'px');
    }
  });
  editor.focus();
}

function applyFontSize(size) {
  if (!size) return;
  const sel = window.getSelection();
  if (!sel.rangeCount) return;
  const range = sel.getRangeAt(0);

  if (range.collapsed) {
    // 선택 없으면 → 현재 줄 전체에 적용
    const node = sel.anchorNode;
    const div = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
    const line = div.closest('#editor > div') || div;
    if (line && line.parentElement?.id === 'editor') {
      const spans = line.querySelectorAll('span');
      if (spans.length === 0) {
        const content = line.innerHTML;
        const span = document.createElement('span');
        span.innerHTML = content;
        line.innerHTML = '';
        line.appendChild(span);
        span.style.fontSize = size + 'px';
      } else {
        spans.forEach(s => s.style.fontSize = size + 'px');
      }
    }
  } else {
    // 선택 영역에 span 래핑
    const contents = range.extractContents();
    const span = document.createElement('span');
    span.style.fontSize = size + 'px';
    span.appendChild(contents);
    range.insertNode(span);
    sel.removeAllRanges();
    const newRange = document.createRange();
    newRange.selectNodeContents(span);
    sel.addRange(newRange);
  }
  document.getElementById('editor').focus();
}

function applyColor(color) {
  if (color) {
    document.execCommand('foreColor', false, color);
  } else {
    document.execCommand('removeFormat', false, null);
  }
  document.getElementById('editor').focus();
}

function insertHR() {
  const editor = document.getElementById('editor');
  const sel = window.getSelection();
  const wrapper = document.createElement('div');
  wrapper.className = 'editor-hr-wrapper';
  wrapper.contentEditable = 'false';
  wrapper.innerHTML = '<hr><button class="hr-delete" onclick="this.parentElement.remove()">×</button>';

  if (sel.rangeCount) {
    const range = sel.getRangeAt(0);
    const node = range.startContainer;
    const line = node.nodeType === Node.TEXT_NODE ? node.parentElement.closest('#editor > *') || node.parentElement : node.closest('#editor > *') || node;
    if (line && line.parentElement === editor) {
      editor.insertBefore(wrapper, line.nextSibling);
    } else {
      editor.appendChild(wrapper);
    }
  } else {
    editor.appendChild(wrapper);
  }
  // 다음 줄 추가
  const next = document.createElement('div');
  next.innerHTML = '<br>';
  editor.insertBefore(next, wrapper.nextSibling);
}

let _replaceTarget = null;

function triggerImageReplace(wrapper) {
  _replaceTarget = wrapper;
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file || !_replaceTarget) return;
    showLoading('이미지 교체 중...');
    try {
      const src = await uploadImageFile(file);
      const img = _replaceTarget.querySelector('img');
      if (img) {
        img.src = resolveImageUrl(src);
        img.setAttribute('data-src', src);
        img.alt = file.name;
      }
    } catch (err) {
      alert('이미지 교체 실패: ' + err.message);
    } finally {
      _replaceTarget = null;
      hideLoading();
    }
  };
  input.click();
}

function insertImage() {
  document.getElementById('image-upload').click();
}

document.getElementById('image-upload')?.addEventListener('change', async function(e) {
  const file = e.target.files[0];
  if (!file) return;
  showLoading('이미지 업로드 중...');
  try {
    const src = await uploadImageFile(file);
    const editor = document.getElementById('editor');
    const wrapper = document.createElement('div');
    wrapper.className = 'editor-image-wrapper';
    wrapper.contentEditable = 'false';
    const img = document.createElement('img');
    img.src = resolveImageUrl(src);
    img.setAttribute('data-src', src);
    img.alt = file.name;
    wrapper.appendChild(img);
    const replace = document.createElement('button');
    replace.className = 'img-replace';
    replace.textContent = '🔄';
    replace.title = '이미지 교체';
    replace.onclick = () => { triggerImageReplace(wrapper); };
    wrapper.appendChild(replace);
    const del = document.createElement('button');
    del.className = 'img-delete';
    del.textContent = '×';
    del.onclick = () => { wrapper.remove(); };
    wrapper.appendChild(del);
    img.style.cursor = 'pointer';
    img.onclick = () => { triggerImageReplace(wrapper); };

    // 커서 위치에 삽입
    const sel = window.getSelection();
    if (sel.rangeCount) {
      const range = sel.getRangeAt(0);
      const node = range.startContainer;
      const line = node.nodeType === Node.TEXT_NODE ? node.parentElement.closest('#editor > *') : node.closest('#editor > *');
      if (line && line.parentElement === editor) {
        editor.insertBefore(wrapper, line.nextSibling);
      } else {
        editor.appendChild(wrapper);
      }
    } else {
      editor.appendChild(wrapper);
    }
    const next = document.createElement('div');
    next.innerHTML = '<br>';
    editor.insertBefore(next, wrapper.nextSibling);
    toast('이미지 업로드 완료', 'success');
  } catch (err) {
    toast('이미지 업로드 실패: ' + err.message, 'error');
  }
  hideLoading();
  this.value = '';
});

function insertCTA() {
  const ctaUrl = config.cta?.url || prompt('CTA URL:') || '#';
  const ctaText = config.cta?.text || '여기서 확인해보세요 →';
  const editor = document.getElementById('editor');

  const div = document.createElement('div');
  const a = document.createElement('a');
  a.href = ctaUrl;
  a.textContent = ctaText;
  a.className = 'editor-cta';
  a.contentEditable = 'false';
  a.setAttribute('data-cta', 'true');
  div.appendChild(a);
  editor.appendChild(div);

  const next = document.createElement('div');
  next.innerHTML = '<br>';
  editor.appendChild(next);
}

// ===== Config =====
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

// ===== Save =====
async function saveAll() {
  collectConfig();
  const saveBtn = document.querySelector('.btn-primary');
  saveBtn.disabled = true;
  saveBtn.textContent = '저장 중...';
  showLoading('저장 & 배포 중...');

  try {
    const configOk = await putFile('config.json', JSON.stringify(config, null, 2) + '\n', 'Update config via admin');
    if (!configOk) throw new Error('config.json 저장 실패');

    const currentHtml = await getFile('index.html');
    const startMarker = '<!-- POST CONTENT START -->';
    const endMarker = '<!-- POST CONTENT END -->';
    const si = currentHtml.indexOf(startMarker);
    const ei = currentHtml.indexOf(endMarker);
    if (si < 0 || ei < 0) throw new Error('POST CONTENT 마커 없음');

    const before = currentHtml.substring(0, si + startMarker.length);
    const after = currentHtml.substring(ei);
    const newContent = editorToSE();
    const newHtml = before + '\n\n' + newContent + '\n\n' + after;

    const htmlOk = await putFile('index.html', newHtml, 'Update post via admin');
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
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

function toast(msg, type) {
  const el = document.createElement('div');
  el.className = 'toast toast-' + (type || 'info');
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

// Enter 키 → div로 줄바꿈
try { document.execCommand('defaultParagraphSeparator', false, 'div'); } catch(e) {}
