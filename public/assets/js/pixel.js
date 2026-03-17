// pixel.js — Meta Pixel + 스크롤 깊이 + CTA 클릭 추적
(async function () {
  let config;
  try {
    config = await fetch('./config.json').then(r => r.json());
  } catch (e) { return; }

  const t = config.tracking || {};
  const pid = t.meta_pixel_id;

  // 1. Meta Pixel 초기화
  if (pid && pid !== 'YOUR_META_PIXEL_ID') {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', pid);
    fbq('track', 'PageView');
  }

  // 2. GA4 (선택)
  const gid = t.ga_id;
  if (gid && gid !== 'YOUR_GA_ID' && gid !== '') {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + gid;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', gid);
  }

  // 3. 스크롤 깊이 추적
  const thresholds = t.scroll_events || [25, 50, 75, 100];
  const fired = new Set();

  function checkScroll() {
    const docH = document.documentElement.scrollHeight - window.innerHeight;
    if (docH <= 0) return;
    const pct = Math.round((window.scrollY / docH) * 100);

    for (const th of thresholds) {
      if (pct >= th && !fired.has(th)) {
        fired.add(th);
        if (typeof fbq === 'function') {
          fbq('trackCustom', 'ScrollDepth', { percent: th });
        }
        if (typeof gtag === 'function' && gid) {
          gtag('event', 'scroll_depth', { percent: th });
        }
      }
    }
  }

  let ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () { checkScroll(); ticking = false; });
      ticking = true;
    }
  }, { passive: true });

  // 4. CTA 클릭 추적
  const ctaEvent = t.cta_event_name || 'Lead';
  document.querySelectorAll('a[data-cta]').forEach(function (el) {
    el.addEventListener('click', function () {
      if (typeof fbq === 'function') {
        fbq('track', ctaEvent);
      }
      if (typeof gtag === 'function' && gid) {
        gtag('event', 'cta_click', { event_category: 'conversion' });
      }
    });
  });
})();
