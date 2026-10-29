// render.js — config.json 기반 소셜 증거 + 프로필 + 댓글 바텀시트 렌더링
(async function () {
  let config;
  try {
    var base = window.location.pathname.endsWith('/') ? window.location.pathname : window.location.pathname + '/';
    config = await fetch(base + 'config.json').then(r => r.json());
  } catch (e) {
    console.warn('config.json not found or invalid');
    return;
  }

  // 유틸: 숫자 포맷 (1234 → 1,234)
  const fmt = n => n != null ? n.toLocaleString('ko-KR') : '';

  // 1. 블로그 헤더 타이틀
  const headerTitle = document.querySelector('.gnb_title .ell');
  if (headerTitle && config.blog?.title) {
    headerTitle.textContent = config.blog.title;
  }

  // 2. 카테고리
  const category = document.querySelector('.blog_category');
  if (category && config.post?.category) {
    category.textContent = config.post.category;
  }

  // 3. 글 제목
  const postTitle = document.querySelector('h3.post_title');
  if (postTitle && config.post?.title) {
    postTitle.textContent = config.post.title;
  }
  // 브라우저 탭 타이틀
  if (config.post?.title) {
    document.title = config.post.title;
  }

  // 4. 프로필
  const authorArea = document.querySelector('.blog_authorArea');
  if (authorArea) {
    // 아바타
    const thumb = authorArea.querySelector('.blog_thumbnail');
    if (thumb) {
      if (config.blog?.profile_image) {
        thumb.innerHTML = '<span class="img"><img src="' + config.blog.profile_image + '" width="36" height="36" alt="프로필" style="border-radius:50%;"></span>';
      } else {
        thumb.innerHTML = '<span class="avatar_fallback"></span>';
      }
    }

    // 닉네임
    const authorName = authorArea.querySelector('.blog_author .ell');
    if (authorName && config.blog?.name) {
      authorName.textContent = config.blog.name;
    }

    // 날짜
    const date = authorArea.querySelector('.blog_date');
    if (date && config.post?.date) {
      date.textContent = config.post.date;
    }
  }

  // 5. 좋아요 수
  const likeCount = document.querySelector('[data-bind="likes"]');
  if (likeCount && config.social?.likes != null) {
    likeCount.textContent = fmt(config.social.likes);
  }

  // 6. 공유 수
  const shareCount = document.querySelector('[data-bind="shares"]');
  if (shareCount && config.social?.shares != null) {
    shareCount.textContent = fmt(config.social.shares);
  }

  // 7. 댓글 수
  const commentCounts = document.querySelectorAll('[data-bind="comments-count"]');
  const count = config.comments?.length || 0;
  commentCounts.forEach(el => { el.textContent = fmt(count); });

  // 8. 댓글 목록 렌더링 (인라인)
  const commentList = document.querySelector('[data-bind="comments"]');
  if (commentList && config.comments?.length) {
    commentList.innerHTML = config.comments.map(c => {
      const avatarHTML = c.profile_image
        ? '<img src="' + c.profile_image + '" width="28" height="28" style="border-radius:50%;">'
        : '';
      return '<div class="comment_item' + (c.reply ? ' comment_reply' : '') + '">' +
        '<div class="comment_profile">' +
          (c.reply ? '<span class="comment_reply_mark">ㄴ</span>' : '') +
          '<div class="comment_avatar comment_avatar_default">' + avatarHTML + '</div>' +
          '<span class="comment_author">' + c.author + '</span>' + (c.owner ? '<span class="comment_owner">작성자</span>' : '') +
          '<span class="comment_time">' + c.time + '</span>' +
        '</div>' +
        '<div class="comment_text">' + c.text + (c.link ? ' <a class="comment_link" href="' + c.link.href + '" target="_blank" rel="noopener">' + c.link.text + '</a>' : '') + '</div>' +
        (c.likes != null && !/비밀 댓글/.test(c.text) ? '<button type="button" class="comment_like" data-n="' + (c.likes || 0) + '">♥ <span>' + (c.likes || 0) + '</span></button>' : '') +
      '</div>';
    }).join('');
    // 10/20 Clarity: 댓글 ♥·본문을 누름 → ♥는 눌리면 +1(한 번) · 세 줄 넘는 댓글은 접고 「더보기」
    commentList.addEventListener('click', function (e) {
      var lk = e.target.closest && e.target.closest('.comment_like');
      if (lk && !lk.classList.contains('on')) { lk.classList.add('on'); var sp = lk.querySelector('span'); if (sp) sp.textContent = (+lk.getAttribute('data-n') || 0) + 1; return; }
      var mb = e.target.closest && e.target.closest('.comment_more');
      if (mb) { var tx = mb.previousElementSibling; if (tx) tx.classList.remove('comment_fold'); mb.remove(); }
    });
    commentList.querySelectorAll('.comment_text').forEach(function (tx) {
      tx.classList.add('comment_fold');
      if (tx.scrollHeight > tx.clientHeight + 2) { var b = document.createElement('button'); b.type = 'button'; b.className = 'comment_more'; b.textContent = '더보기'; tx.parentNode.insertBefore(b, tx.nextSibling); }
      else tx.classList.remove('comment_fold');
    });
  }
  // 10/20 하단 바 ♥: 누르면 채워지고 +1(한 번)
  var likeItem = document.querySelector('.social_item.like');
  if (likeItem) likeItem.addEventListener('click', function () {
    if (likeItem.classList.contains('on')) return; likeItem.classList.add('on');
    var cnt = likeItem.querySelector('[data-bind="likes"]'); if (cnt) { var n = parseInt(String(cnt.textContent).replace(/[^0-9]/g, ''), 10) || 0; cnt.textContent = (n + 1).toLocaleString(); }
  });

  // 9. 댓글 바텀시트 렌더링
  const sheetComments = document.querySelector('[data-bind="sheet-comments"]');
  if (sheetComments && config.comments?.length) {
    sheetComments.innerHTML = config.comments.map(c => {
      const avatarInner = c.profile_image
        ? '<img src="' + c.profile_image + '" alt="">'
        : '';
      return '<div class="comment_sheet_item' + (c.reply ? ' comment_reply' : '') + '">' +
        '<div class="comment_sheet_profile">' +
          (c.reply ? '<span class="comment_reply_mark">ㄴ</span>' : '') +
          '<div class="comment_sheet_avatar comment_avatar_default">' + avatarInner + '</div>' +
          '<span class="comment_sheet_author">' + c.author + '</span>' + (c.owner ? '<span class="comment_owner">작성자</span>' : '') +
        '</div>' +
        '<div class="comment_sheet_text">' + c.text + '</div>' +
        '<div class="comment_sheet_meta">' +
          '<div class="comment_sheet_meta_left">' +
            '<span class="comment_sheet_date">' + c.time + '</span>' +
            '<span class="comment_sheet_report">신고</span>' +
          '</div>' +
          '<div style="display:flex;align-items:center;gap:12px;">' +
            '<button class="comment_sheet_reply_btn">' +
              '<svg viewBox="0 0 20 20" fill="none"><path d="M10 2c4.418 0 8 3.582 8 8s-3.582 8-8 8a7.96 7.96 0 01-4.17-1.17l-2.7.71a.22.22 0 01-.27-.27l.71-2.7A7.96 7.96 0 012 10c0-4.418 3.582-8 8-8z" stroke="#bbb" stroke-width="1.4"/></svg>' +
              '<span>답글</span>' +
            '</button>' +
            '<button class="comment_sheet_like_btn">' +
              '<svg viewBox="0 0 18 18" fill="none"><path d="M9 15.3l-1.05-.96C4.2 11.04 2 9.07 2 6.65 2 4.68 3.57 3.1 5.5 3.1c1.13 0 2.21.53 2.93 1.37h1.14c.72-.84 1.8-1.37 2.93-1.37C14.43 3.1 16 4.68 16 6.65c0 2.42-2.2 4.39-5.95 7.69L9 15.3z" stroke="#bbb" stroke-width="1.2" fill="none"/></svg>' +
              '<span>' + (c.likes || 0) + '</span>' +
            '</button>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join('');
  }

  // 10. 댓글 바텀시트 열기/닫기
  const overlay = document.getElementById('commentOverlay');
  const sheet = document.getElementById('commentSheet');
  if (overlay && sheet) {
    // 소셜바 댓글 버튼 클릭 → 바텀시트 열기
    const commentBtn = document.querySelector('.social_item.comment');
    if (commentBtn) {
      commentBtn.addEventListener('click', function () {
        overlay.classList.add('active');
        sheet.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    }

    // 오버레이 클릭 → 닫기
    overlay.addEventListener('click', function () {
      overlay.classList.remove('active');
      sheet.classList.remove('active');
      document.body.style.overflow = '';
    });

    // 바텀시트 핸들 드래그 다운 → 닫기 (간단 버전)
    const handle = sheet.querySelector('.comment_sheet_handle');
    if (handle) {
      let startY = 0;
      handle.addEventListener('touchstart', function (e) {
        startY = e.touches[0].clientY;
      });
      handle.addEventListener('touchmove', function (e) {
        const dy = e.touches[0].clientY - startY;
        if (dy > 60) {
          overlay.classList.remove('active');
          sheet.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
    }
  }

  // 11. CTA 링크 설정
  if (config.cta?.url) {
    document.querySelectorAll('a[data-cta]').forEach(el => {
      el.href = config.cta.url;
      if (config.cta.text && !el.textContent.trim()) {
        el.textContent = config.cta.text;
      }
    });
  }
})();
