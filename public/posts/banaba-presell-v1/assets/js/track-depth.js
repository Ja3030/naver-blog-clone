/* track-depth.js — 랜딩 읽기 깊이 정밀 측정 (2026-09-28)
   이벤트는 전부 Meta 픽셀 맞춤 이벤트(trackCustom). 픽셀 통계 API가 파라미터로 나눠 세지 못하므로
   값을 이벤트 이름에 넣는다 → 이벤트 이름별 건수만으로 이탈 곡선이 나온다.
   ① SD010~SD100 : 본문(.se-main-container) 10% 단위 도달
   ② SECnn_이름  : 이야기 구간 도착 (본문 문장 기준 33곳 + 제품 카드, 문서 순서 · 화면 아래 끝이 지나면 도착)
                   2026-09-30 추가: 도입부 SEC00a~c · 3단 분해 안 SEC16a~f · 카드 직전 SEC19a~d (이름 정렬 = 문서 순서)
   ③ TM015~TM600 : 화면을 보고 있던 시간 누적 (탭이 가려지면 멈춤)
   ④ ENGAGED     : 15초 이상 + 본문 10% 이상
   ⑤ SCROLLED    : 화면 1/4 이상 내림 (2026-09-30 · 스크롤도 안 하고 나간 사람과 가르기)
   한 번 방문에 이벤트마다 1회만 보낸다. 제품 카드 클릭 Lead는 원래대로 onclick에서 나간다 */
(function () {
  var sent = {};
  function send(name) {
    if (sent[name]) return;
    sent[name] = 1;
    if (typeof window.fbq === 'function') window.fbq('trackCustom', name);
    if (window.__depthLog) window.__depthLog.push(name);
  }

  /* 이야기 구간 — 본문 문장이 바뀌면 여기만 고친다 (못 찾은 구간은 조용히 건너뜀) */
  var SECTIONS = [
    ['SEC00a_photo_warn', '사진은 위에 올려두는데'],
    ['SEC00b_too_long', '글이 깁니다'],
    ['SEC00c_no_ads', '광고 문의 사절'],
    ['SEC01_no_reverse', '그런 건 없습니다'],
    ['SEC02_every_2weeks', '2주에 한 번.'],
    ['SEC03_childhood', '초등학교 4학년'],
    ['SEC04_q_agassi', '얼굴은 아가씬데'],
    ['SEC05_perm_failed', '파마까지 안 걸렸다'],
    ['SEC06_q_nobody_knows', '겪어보지 않은 사람들은 몰라요'],
    ['SEC07_science', '브래드포드'],
    ['SEC08_q_forty', '나도 마흔 넘어서'],
    ['SEC09_q_tried', '흰머리에 좋다는 것들은'],
    ['SEC10_q_thats_it', '그래 그거'],
    ['SEC11_columbia', '미국 컬럼비아 대학도'],
    ['SEC12_material_cutoff', '몸에서 재료가 끊기는 날'],
    ['SEC13_born_gray', '흰머리로 태어난 애기'],
    ['SEC14_yeast_test', '이스트 한 숟갈에'],
    ['SEC15_how_to_choose', '그럼 뭘 보고 골라야 하나'],
    ['SEC16_q_3step', '3단 분해만 기억하면 된다'],
    ['SEC16a_step1', '1단계'],
    ['SEC16b_step2', '2단계'],
    ['SEC16c_step3', '3단계'],
    ['SEC16d_four_bottles', '네 개를 따로 샀다'],
    ['SEC16e_not_human', '사람이 할 짓이 아니다'],
    ['SEC16f_three_types', '세 부류였다'],
    ['SEC17_one_product', '셋 다 제대로 든 건'],
    ['SEC18_result', '두 달째에 염색 주기가'],
    ['SEC19_q_good_time', '지금이 좋을 때야'],
    ['SEC19a_summary', '네 줄로 줄이면'],
    ['SEC19b_verify', '확인하는 법을 적어둔다'],
    ['SEC19c_closing', '마치며'],
    ['SEC19d_update', '8월 14일 추가'],
    ['SEC20_before_card', '일주일만 아래에 걸어둡니다']
  ];

  function start() {
    var main = document.querySelector('.se-main-container') || document.body;

    /* ② 구간 도착 */
    var paras = main.querySelectorAll('p.se-text-paragraph, .se-quotation-line, .se-quote');
    var targets = [], from = 0, missing = [];
    for (var s = 0; s < SECTIONS.length; s++) {
      var hit = -1;
      for (var i = from; i < paras.length; i++) {
        if ((paras[i].textContent || '').indexOf(SECTIONS[s][1]) >= 0) { hit = i; break; }
      }
      if (hit < 0) { missing.push(SECTIONS[s][0]); continue; }
      targets.push([paras[hit], SECTIONS[s][0]]);
      from = hit + 1;
    }
    var card = main.querySelector('.se-oglink-card, a.__se_link');
    if (card) targets.push([card, 'SEC21_card_seen']);
    window.__depthSections = { found: targets.length, missing: missing };

    /* 구간은 「화면 아래 끝이 그 문장을 지났는가」로 판정 — 빠르게 넘겨도 빠지지 않는다 */
    function checkSections() {
      var vh = window.innerHeight;
      for (var k = 0; k < targets.length; k++) {
        var t = targets[k];
        if (sent[t[1]]) continue;
        if (t[0].getBoundingClientRect().top < vh) send(t[1]);
      }
    }

    /* ① 본문 10% 단위 */
    var maxPct = 0;
    function checkDepth() {
      if (window.scrollY > window.innerHeight * 0.25) send('SCROLLED');
      var r = main.getBoundingClientRect();
      if (r.height <= 0) return;
      var seen = (window.innerHeight - r.top) / r.height;   // 화면 아래 끝까지 본 본문 비율
      var pct = Math.max(0, Math.min(100, Math.floor(seen * 100)));
      if (pct > maxPct) maxPct = pct;
      for (var p = 10; p <= 100; p += 10) {
        if (maxPct >= p) send('SD' + ('00' + p).slice(-3));
      }
      checkSections();
      if (maxPct >= 10 && active >= 15) send('ENGAGED');
    }
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () { ticking = false; checkDepth(); });
    }, { passive: true });
    window.addEventListener('resize', checkDepth);

    /* ③ 보고 있던 시간 */
    var active = 0, MARKS = [15, 30, 60, 120, 180, 300, 600];
    setInterval(function () {
      if (document.visibilityState !== 'visible') return;
      active += 1;
      for (var m = 0; m < MARKS.length; m++) if (active >= MARKS[m]) send('TM' + ('00' + MARKS[m]).slice(-3));
      if (active === 15) checkDepth();
    }, 1000);

    checkDepth();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
