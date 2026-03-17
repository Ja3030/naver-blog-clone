// render.js — config.json 기반 소셜 증거 + 프로필 렌더링
(async function () {
  let config;
  try {
    config = await fetch('./config.json').then(r => r.json());
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
        const color = config.blog?.profile_color || '#a8d8ea';
        const initial = (config.blog?.name || '?')[0];
        thumb.innerHTML = '<span class="avatar_fallback" style="background:' + color + ';width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;color:white;font-weight:bold;">' + initial + '</span>';
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

  // 8. 댓글 목록 렌더링
  const commentList = document.querySelector('[data-bind="comments"]');
  if (commentList && config.comments?.length) {
    commentList.innerHTML = config.comments.map(c => {
      const color = c.profile_color || '#ddd';
      const initial = (c.author || '?')[0];
      return '<div class="comment_item">' +
        '<div class="comment_profile">' +
          '<div class="comment_avatar" style="background:' + color + ';">' + initial + '</div>' +
          '<span class="comment_author">' + c.author + '</span>' +
          '<span class="comment_time">' + c.time + '</span>' +
        '</div>' +
        '<div class="comment_text">' + c.text + '</div>' +
        (c.likes ? '<div class="comment_like">♥ ' + c.likes + '</div>' : '') +
      '</div>';
    }).join('');
  }

  // 9. CTA 링크 설정
  if (config.cta?.url) {
    document.querySelectorAll('a[data-cta]').forEach(el => {
      el.href = config.cta.url;
      if (config.cta.text && !el.textContent.trim()) {
        el.textContent = config.cta.text;
      }
    });
  }
})();
