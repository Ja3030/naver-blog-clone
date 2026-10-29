#!/usr/bin/env python3
"""편도(프로폴리스 스프레이) 블로그판 2편 — 입마름 `tonsil-dry-v1` · 백태 `tonsil-tongue-v1` (2026-10-27)

본문 = tonsil-stone-spray/03_COPY/블로그판_입마름백태_2026-10-27/10_입마름_본문_v1.md · 20_백태_본문_v1.md
  (`---` 첫 줄 뒤 ~ `## 제목 후보` 앞 · 빈 줄 = 문단 경계 · 〔사진 #N …〕 = 이미지 · `## [1] …` = 큰 글씨 · **…** = 굵게 · → 〔링크 카드 …〕 = 링크 카드)
이미지 = 같은 폴더 img/final/<슬롯>.jpg|gif (없으면 HIDE_MISSING에 따라 점선 자리 또는 생략)
결정 = 00_결정목록.md (D9 blog-note · utm_source=presell&utm_medium=blog → 상품페이지 2+1 기본)
빌드 → public/posts/<slug>/ → 미러 blog-note/public/posts/<slug>/ (naver 문자열 0 · 경량화). 배포는 따로.
사용: python3 _build_tonsil_dry_tongue.py [dry|tongue] [--review]   (--review = 빠진 사진을 점선 자리로 보이게)
"""
import json, os, re, shutil, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _build_gout_entry1 as G                 # 문단·인용·이미지·링크 블록 꼴 재사용
from _build_tonsil_live_clone import optimize   # 미러 경량화

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
SRC_DIR = '/Users/juan/Brand Manager/tonsil-stone-spray/03_COPY/블로그판_입마름백태_2026-10-27'
FINAL = f'{SRC_DIR}/img/final'
MIRROR = '/Users/juan/Brand Manager/blog-note/public/posts'
THUMB = '/Users/juan/Brand Manager/tonsil-stone-spray/07_LIVE_BACKUP/_product_thumb/soricare_53_big.png'
PIXEL_ID = '1727184084578989'   # 편도 픽셀(템플릿 기본값)
REVIEW = '--review' in sys.argv

POSTS = {
    'dry': dict(
        slug='tonsil-dry-v1', md=f'{SRC_DIR}/10_입마름_본문_v1.md', prefix='dry', ev='Dry',
        title='입마름 입냄새, 물 2리터 마셔도 안 됐던 이유 (4년 만에 해결)', date='2026. 10. 21. 23:12',
        blog=dict(name='말하는직업', title='12년차 영어쌤의 기록장', profile_color='#c9b8a6'),
        social=dict(likes=1426, shares=118, views=19870),
        cta='https://soricare.com/product/detail.html?product_no=53&utm_source=presell&utm_medium=blog&utm_campaign=dry&utm_content=v1',
        H=['혀가 입천장에 쩍쩍 달라붙었다', '1분쯤 지나니까 올라왔다. 덜 마른 걸레 냄새.', '그 애가 고개를 홱 돌렸다. 그리고 손으로 코를 막았다.',
           '말하는 게 직업인 사람이, 말을 줄이고 있었다.', '"엄마 입에서 이상한 냄새 나."', '"입술 트면 물 바르냐? 립밤 바르지. 입안도 똑같아."',
           '입이 마르는 건 물이 모자라서가 아니었다. 침이 덜 나와서였다.', '입안에도 바르고 나서 남아 있는 게 필요했다. 입안에 바르는 립밤 같은 거.',
           '일주일째 되던 날, 3교시 끝나고 보니 물병이 반도 안 줄어 있었다. 혀도 입천장에 안 붙어 있었다.',
           '근데 아니었다. 물을 덜 마신 것도, 덜 닦은 것도 아니었다. 아무도 침 얘기를 해 주지 않았을 뿐이다.'],
        R=['4년', '2리터', '하루 다섯 번', '10분도 안 돼서', '6개월치', '두달', '30초', '석달', '1분'],
    ),
    'tongue': dict(
        slug='tonsil-tongue-v1', md=f'{SRC_DIR}/20_백태_본문_v1.md', prefix='tg', ev='Tg',
        title='혀 백태, 6년 동안 매일 긁어도 다시 하얘졌던 이유', date='2026. 10. 20. 22:41',
        blog=dict(name='혀긁기6년차', title='7년차 직장인의 사소한 기록', profile_color='#b9c4cf'),
        social=dict(likes=1688, shares=131, views=22310),
        cta='https://soricare.com/product/detail.html?product_no=53&utm_source=presell&utm_medium=blog&utm_campaign=tongue&utm_content=v1',
        H=['가운데는 긁고도 저랬다', '긁은 직후엔 혀끝만 잠깐 분홍빛이 보였다. 그 분홍이 너무 반가워서 더 긁었다.',
           '"너 혀 왜 이렇게 하얘?"', '그날 퇴근길 지하철에서 마스크 안으로 혼자 울었다.',
           '"야, 냄비 긁지 말고 물 부어서 불려 놔. 내일 아침이면 쑥 떨어져."', "'혹시 혀도, 긁어서 될 게 아니었나?'",
           '근데 혀클리너는 원래 돌기 끝만 긁게 생겼다. 납작한 날이 위를 쓸고 지나가니까.',
           '그 분홍이 원래 내 혀 색이었다. 하얀 건 그 위에 덮여 있던 거다. 남자친구 혀랑 다를 게 없었다.',
           '사흘째 아침, 거울 앞에서 혀를 내밀었는데 앞쪽이 분홍빛이었다.',
           '10월 첫 주 아침이었다. 거울 앞에서 혀를 내밀었는데 통째로 분홍이었다. 긁지도 않았는데. 휴대폰을 들고 맨 위에 올린 사진을 찍었다.'],
        R=['6년', '10분', '일곱 개', '석달', '두달', '사흘째', '일주일', '2주째', '5분'],
    ),
}

OG_TITLE = '프로폴리스 스프레이 - FarmBio'
OG_DESC = '물에 녹인 호주산 프로폴리스 · 꿀 · 주머니에 들어가는 30ml'
OG_DOMAIN = 'soricare.com'


def img_for(prefix, num):
    """〔사진 #N〕 → final/<prefix>_NN(.jpg|.gif) · #2-1 → <prefix>_02s"""
    key = f'{prefix}_{int(num.split("-")[0]):02d}' + ('s' if '-' in num else '')
    for ext in ('.gif', '.jpg', '.png'):
        p = f'{FINAL}/{key}{ext}'
        if os.path.exists(p):
            return key, p
    return key, None


def para(s, P):
    """한 문단 → <p> · 형광(H) · 굵게(**) · 빨강(R)"""
    bold = s.startswith('**') and s.endswith('**')
    t = s.strip('*').replace('\\*', '*') if bold else s
    inner = G.esc(t)
    hit = next((h for h in P['H'] if h in t), None)   # 형광 = 문단 안의 그 구절만
    if hit:
        e = G.esc(hit)
        inner = inner.replace(e, '\x00' + e + '\x01', 1)
    for ph in sorted(P['R'], key=len, reverse=True):
        e = G.esc(ph)
        if e in inner and ('>' + e + '<') not in inner:
            inner = inner.replace(e, '<span style="color:#ff0010;font-weight:700;">' + e + '</span>', 1)
    inner = inner.replace('\x00', '<span style="background-color:#fff8b2;font-weight:700;">').replace('\x01', '</span>')
    if bold:
        inner = '<b>' + inner + '</b>'
    return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
            '        <span class="se-ff-system" style="font-size:18px;line-height:1.9;">' + inner + '</span>\n      </p>')


def big(s):
    return G.text_block(['      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                         '        <span class="se-ff-system" style="font-size:22px;font-weight:800;line-height:1.5;">' + G.esc(s) + '</span>\n      </p>',
                         G.p_blank()])


def link_card(P, used):
    fn = 'og1.jpg'
    im = Image.open(THUMB).convert('RGB'); im.thumbnail((600, 600)); os.makedirs('/tmp', exist_ok=True)
    used.append((fn, THUMB))
    return ('<div class="se-component se-oglink se-l-default">\n  <div class="se-section se-section-oglink">\n    <div class="se-module se-module-oglink">\n'
            f'      <a href="{P["cta"]}" class="se-oglink-card __se_link" target="_blank" rel="noopener" '
            "onclick=\"if(typeof fbq==='function'){fbq('track','Lead');}\">\n"
            f'        <img src="/posts/{P["slug"]}/images/{fn}" alt="" class="se-oglink-thumb" loading="lazy" decoding="async">\n'
            '        <div class="se-oglink-body">\n'
            f'          <div class="se-oglink-title">{G.esc(OG_TITLE)}</div>\n'
            f'          <div class="se-oglink-desc">{G.esc(OG_DESC)}</div>\n'
            f'          <div class="se-oglink-domain">{G.esc(OG_DOMAIN)}</div>\n'
            '        </div>\n      </a>\n    </div>\n  </div>\n</div>')


TRACK_JS = """<script>
(function(){
  var EV='__EV__';
  function fire(n){ try{ if(typeof fbq==='function'){ fbq('trackCustom', EV+n); } }catch(e){} }
  var once={}; function one(n){ if(once[n]) return; once[n]=1; fire(n); }
  var marks=[];
  function check(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    if(h>0){ var p=window.scrollY/h; [25,50,75,100].forEach(function(k){ if(p>=k/100-0.001) one('S'+k); }); }
    var line=window.innerHeight*0.9;
    marks.forEach(function(m){ if(!once[m[1]] && m[0].getBoundingClientRect().top<=line) one(m[1]); });
  }
  var tick=false;
  window.addEventListener('scroll',function(){ if(!tick){ tick=true; requestAnimationFrame(function(){ check(); tick=false; }); } },{passive:true});
  function init(){
    setTimeout(function(){ one('T10'); }, 10000);
    var hs=document.querySelectorAll('.nl-sec'); for(var i=0;i<hs.length;i++){ marks.push([hs[i],'H'+(i+1)]); }
    var c=document.querySelector('a.se-oglink-card'); if(c) marks.push([c,'CardView']);
    check();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>"""


def build(key):
    P = POSTS[key]
    text = open(P['md'], encoding='utf-8').read()
    body = text.split('\n---\n', 1)[1].split('\n## 제목 후보')[0]
    blocks, paras, used, missing, n_sec = [], [], [], [], 0

    def flush():
        nonlocal paras
        if paras:
            blocks.append(G.text_block(paras)); paras = []

    for raw in body.split('\n'):
        s = raw.strip()
        if not s:
            continue
        m = re.match(r'^〔사진 #([\d-]+)', s)
        if m:
            flush()
            k, p = img_for(P['prefix'], m.group(1))
            if p:
                fn = os.path.basename(p); used.append((fn, p))
                with Image.open(p) as im: sz = im.size
                blocks.append(G.img_block(f'/posts/{P["slug"]}/images/{fn}', '', sz, lazy=len(used) > 2))
            else:
                missing.append(k)
                if REVIEW:
                    blocks.append(G.placeholder_block(f'{k} · {s[1:40]}'))
            continue
        if s.startswith('→ 〔링크 카드'):
            flush(); blocks.append(link_card(P, used)); continue
        if s == '---':
            flush(); blocks.append(G.hr_block()); continue
        if s.startswith('## '):
            flush(); n_sec += 1
            blocks.append(big(s[3:]).replace('class="se-component se-text se-l-default"', 'class="se-component se-text se-l-default nl-sec"', 1)); continue
        paras.append(para(s, P)); paras.append(G.p_blank())
    flush()
    blocks.append(G.hr_block()); blocks.append(G.text_block([G.p_blank()]))
    se_html = '\n\n'.join(blocks)

    post_dir = os.path.join(BASE, 'public', 'posts', P['slug'])
    shutil.rmtree(post_dir, ignore_errors=True); os.makedirs(os.path.join(post_dir, 'images'))
    for fn, src in used:
        if fn == 'og1.jpg':
            im = Image.open(src).convert('RGB'); im.thumbnail((600, 600)); im.save(os.path.join(post_dir, 'images', fn), quality=88)
        else:
            shutil.copy2(src, os.path.join(post_dir, 'images', fn))
    t = open(TEMPLATE, encoding='utf-8').read()
    a, b = '<!-- POST CONTENT START -->', '<!-- POST CONTENT END -->'
    si, ei = t.index(a), t.index(b)
    html = t[:si + len(a)] + '\n\n' + se_html + '\n\n' + t[ei:]
    html = html.replace('</body>', TRACK_JS.replace('__EV__', P['ev']) + '\n</body>')
    open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8').write(html)
    cfg = {'blog': dict(P['blog'], profile_image=''), 'post': {'title': P['title'], 'category': '일상', 'date': P['date']},
           'social': P['social'], 'comments': G.secret_comments(n=96 if key == 'dry' else 112, seed=11 if key == 'dry' else 23),
           'tracking': {'meta_pixel_id': PIXEL_ID, 'ga_id': '', 'scroll_events': [25, 50, 75, 100], 'cta_event_name': 'Lead'},
           'cta': {'url': P['cta'], 'text': '여기서 확인해보세요'}}
    json.dump(cfg, open(os.path.join(post_dir, 'config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    # 형광 줄 대조 — 원고에 없는 줄이면 알린다
    miss_h = [h for h in P['H'] if h not in body]
    n_chars = len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', se_html)))
    print(f'{P["slug"]}: 이미지 {len(used)} · 빠진 사진 {len(missing)} {missing} · 큰 제목 {n_sec} · 형광 {se_html.count("fff8b2")} · 본문 {n_chars:,}자')
    if miss_h: print('  ⚠ 원고에 없는 형광 줄:', miss_h)

    if not REVIEW:
        mirror = os.path.join(MIRROR, P['slug'])
        shutil.rmtree(mirror, ignore_errors=True); shutil.copytree(post_dir, mirror)
        for f in ('index.html', 'config.json'):
            fp = os.path.join(mirror, f); x = open(fp, encoding='utf-8').read().replace('/assets/css/naver-blog.css', '/assets/css/blog.css')
            open(fp, 'w', encoding='utf-8').write(x)
        ob, oa = optimize(mirror)
        for root, _, fs in os.walk(mirror):
            for f in fs:
                if f.rsplit('.', 1)[-1] in ('html', 'json', 'css', 'js', 'txt') and 'naver' in open(os.path.join(root, f), encoding='utf-8', errors='ignore').read().lower():
                    raise SystemExit(f'미러에 naver 남음 → {os.path.join(root, f)}')
        print(f'  미러 → blog-note/public/posts/{P["slug"]}/' + (f' · 경량화 {ob/1e6:.1f}→{oa/1e6:.1f}MB' if ob else ''))


if __name__ == '__main__':
    keys = [a for a in sys.argv[1:] if not a.startswith('--')] or list(POSTS)
    for k in keys:
        build(k)
