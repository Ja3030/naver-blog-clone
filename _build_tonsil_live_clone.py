"""편도 랜딩 2종 — 네이버 블로그 라이브 HTML을 그대로 클론으로 옮긴다 (2026-09-20).

원본 = 07_LIVE_BACKUP/<폴더>/_원본페이지.html (m.blog.naver.com 모바일 렌더, curl로 받은 것)
       + images/ (모듈 등장 순서대로 번호 매긴 파일) + _이미지_매니페스트.json
방식 = se-main-container 안의 컴포넌트를 순서대로 읽어 본문 조판(굵기·크기·색·정렬·빈 줄)을
       그대로 두고, 이미지 src만 로컬 파일로 바꾼다. 글자는 한 자도 새로 쓰지 않는다.
       GIF(원본은 <video>)는 <img .gif>로. 링크 카드는 우리 CTA 링크 + 로컬 썸네일.

  tonsil-hyg-v6b  치위생사판 개량(A4/A6판)  ← juteacher0/224386080000 (9/20 라이브)
  tonsil-yt-v1    여성 유튜버판(혜밥투어)     ← juteacher0/223935521383 (9/20 라이브)

사용: python3 _build_tonsil_live_clone.py [slug ...]   (인자 없으면 둘 다)
배포는 이 스크립트가 하지 않는다 (_deploy.py 별도).
"""
import html as H
import json
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
BK = '/Users/juan/Brand Manager/tonsil-stone-spray/07_LIVE_BACKUP'
PIXEL_ID = '1727184084578989'   # 편도장벽제 픽셀 (템플릿 하드코딩과 동일)
THUMB_SRC = f'{BK}/_product_thumb/soricare_53_big.png'
GIF_LOCAL = '/Users/juan/Brand Manager/tonsil-stone-spray/03_COPY/유튜버판_2026-08-31/발행패키지_2026-09-01'

POSTS = {
    'tonsil-hyg-v6b': dict(
        src=f'{BK}/여성개량판_juteacher0_224386080000_2026-09-20',
        origin='https://blog.naver.com/juteacher0/224386080000',
        title='편도결석 재발없이 완전 해결한 방법', date='2026. 8. 21. 22:27', category='.',
        cta='https://soricare.com/product/detail.html?product_no=53&utm_source=naver_blog&utm_medium=advertorial&utm_campaign=Avatar4&utm_content=clone_v6b',
        og_title='편도장벽제 - FarmBio',
        social=dict(likes=1362, shares=97, views=21480),   # ⚠ 실측 아님 — 라이브 모바일 페이지에 수치가 안 실림. 유저 조정
    ),
    'tonsil-yt-v1': dict(
        src=f'{BK}/여성유튜버판_juteacher0_223935521383_2026-09-20',
        origin='https://blog.naver.com/juteacher0/223935521383',
        title='4년간 편도결석에 시달린 8만 먹방 유튜버가 3개월 동안 바꾼 것 (미국에선 이미 정설)',
        date='2025. 7. 16. 11:17', category='..',
        cta='https://soricare.com/product/detail.html?product_no=53&utm_source=naver_blog&utm_medium=advertorial&utm_campaign=Youtuber&utm_content=clone_v1',
        og_title='프로폴리스 스프레이 - FarmBio',
        social=dict(likes=2041, shares=188, views=38920),  # ⚠ 실측 아님 — 유저 조정
    ),
}
# β 첫 화면 변형 (유저 🟢 2026-09-20): 유튜버판 2막의 「"지금은 딱히 안 보이는데요"」 텍스트 블록 + 바로 앞 사진(IMG-13)을
# 맨 위로 복제해 올린다. 2막 자리의 원문은 그대로 둔다. 새 문장 0.
POSTS['tonsil-yt-v1b'] = dict(POSTS['tonsil-yt-v1'],
    cta=POSTS['tonsil-yt-v1']['cta'].replace('clone_v1', 'clone_v1b'),
    atf_marker='지금은 딱히 안 보이는데요')
OG_DESC = ('임상 데이터 기반 설계 10,670 ppm 티트리 유효농도 학술 연구 확인 구간 · 시중 대비 5배 18 × 문제성 피부의 '
           '트러블 지수 정상 피부 대비 배율 12.8 민감성 홍조 피부 기준 정상 대비 트러블 빈도 REVIEWS 고객 후기 * 개인의 '
           '주관적 체험에 의한 후기이며, 효과는 개인차가 있을 수 있습니다')   # 라이브 링크 카드 문구 그대로(스토어 og 설명)

EXTRA_CSS = '''
/* 라이브 클론 보정 — 원본 SE 클래스 중 클론 CSS에 없던 것 */
.se-fs-fs16 { font-size: 16px; }
.se-text-paragraph-align-center { text-align: center; }
.se-text-paragraph-align-right { text-align: right; }
.se-viewer .se-component.se-imageStrip { margin: 26px 0; }
.se-imageStrip-container { display: flex; gap: 3px; }
.se-imageStrip-container .se-module-image { flex: 1 1 0; min-width: 0; }
.se-imageStrip-container img { width: 100%; height: auto; display: block; }
.se-viewer .se-text-paragraph span { background-color: transparent !important; }
'''


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def balanced_div(h, start):
    """h[start:]가 '<div'로 시작 — 짝이 맞는 </div>까지의 끝 인덱스"""
    depth, i, n = 0, start, len(h)
    tag = re.compile(r'<div\b|</div\s*>', re.I)
    for m in tag.finditer(h, start):
        if m.group(0).lower().startswith('</'):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    return n


def components(main):
    """se-main-container 직속 컴포넌트를 순서대로 (type, html)"""
    out, pos = [], 0
    pat = re.compile(r'<div class="se-component (se-[A-Za-z]+)[^"]*"')
    while True:
        m = pat.search(main, pos)
        if not m:
            break
        end = balanced_div(main, m.start())
        out.append((m.group(1), main[m.start():end]))
        pos = end
    return out


def clean_text_inner(comp):
    m = re.search(r'<div class="se-module se-module-text"[^>]*>', comp)
    inner = comp[m.end():balanced_div(comp, m.start()) - len('</div>')]
    inner = re.sub(r'\s*id="SE-[0-9a-f-]+"', '', inner)
    inner = re.sub(r'<!--\s*\}?\s*SE-TEXT\s*\{?\s*-->', '', inner)
    inner = re.sub(r'<!--\s*-->', '', inner)
    return inner.strip()


def text_block(inner):
    return ('<div class="se-component se-text se-l-default">\n  <div class="se-section se-section-text se-l-default">\n'
            '    <div class="se-module se-module-text">\n' + inner + '\n    </div>\n  </div>\n</div>')


def img_block(src):
    return ('<div class="se-component se-image se-l-default">\n  <div class="se-section se-section-image se-l-default">\n'
            '    <div class="se-module se-module-image">\n      <a class="se-module-image-link">\n'
            f'        <img src="{esc(src)}" alt="" class="se-image-resource">\n'
            '      </a>\n    </div>\n  </div>\n</div>')


def strip_block(srcs):
    mods = ''.join(f'      <div class="se-module se-module-image"><a class="se-module-image-link"><img src="{esc(s)}" alt="" class="se-image-resource"></a></div>\n' for s in srcs)
    return ('<div class="se-component se-imageStrip se-l-default">\n  <div class="se-section se-section-imageStrip se-l-default">\n'
            f'    <div class="se-imageStrip-container">\n{mods}    </div>\n  </div>\n</div>')


def hr_block():
    return ('<div class="se-component se-horizontalLine se-l-default">\n  <div class="se-section se-section-horizontalLine se-l-default">\n'
            '    <div class="se-module se-module-horizontalLine">\n      <hr class="se-hr">\n    </div>\n  </div>\n</div>')


def oglink_block(cta, thumb_rel, title):
    return ('<div class="se-component se-oglink se-l-default">\n  <div class="se-section se-section-oglink">\n    <div class="se-module se-module-oglink">\n'
            f'      <a href="{esc(cta)}" class="se-oglink-card __se_link" target="_blank" rel="noopener" data-cta '
            "onclick=\"if(typeof fbq==='function'){fbq('track','Lead');}\">\n"
            f'        <img src="{esc(thumb_rel)}" alt="" class="se-oglink-thumb">\n'
            '        <div class="se-oglink-body">\n'
            f'          <div class="se-oglink-title">{esc(title)}</div>\n'
            f'          <div class="se-oglink-desc">{esc(OG_DESC)}</div>\n'
            '          <div class="se-oglink-domain">soricare.com</div>\n'
            '        </div>\n      </a>\n    </div>\n  </div>\n</div>')


def image_modules(comp):
    """컴포넌트 안 이미지 모듈들 → [('gif'|'img', 원본 URL)]"""
    out = []
    for mod in re.findall(r'<div class="se-module se-module-image"[^>]*>(.*?)</div>\s*</div>', comp, flags=re.S):
        g = re.search(r'data-gif-url="([^"]+)"', mod)
        if g:
            out.append(('gif', H.unescape(g.group(1))))
            continue
        im = re.search(r'<img[^>]*(?:data-lazy-src|src)="([^"]+)"', mod)
        if im:
            out.append(('img', H.unescape(im.group(1))))
    return out


def build(slug):
    P = POSTS[slug]
    post_dir = os.path.join(BASE, 'public', 'posts', slug)
    img_dir = os.path.join(post_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)
    rel = f'/posts/{slug}/images/'
    h = open(os.path.join(P['src'], '_원본페이지.html'), encoding='utf-8', errors='ignore').read()
    s = h.find('<div class="se-main-container')
    main = h[s:balanced_div(h, s)]
    man = json.load(open(os.path.join(P['src'], '_이미지_매니페스트.json'), encoding='utf-8'))
    files = {m['n']: m['file'] for m in man}
    by_base = {H.unescape(m['url']).split('?')[0].rsplit('/', 1)[-1]: m['file'] for m in man if m.get('url') and m.get('file')}

    def lookup(n, url):
        """모듈 순번(n)이 매니페스트와 어긋나면(유튜버판: GIF가 img 목록에 없음) URL 파일명으로 찾는다"""
        base = url.split('?')[0].rsplit('/', 1)[-1]
        return by_base.get(base) or files.get(n)
    thumb = 'og_thumb.png'
    shutil.copy2(THUMB_SRC, os.path.join(img_dir, thumb))

    blocks, n_img, stats, used = [], 0, {}, []
    for kind, comp in components(main):
        stats[kind] = stats.get(kind, 0) + 1
        if kind == 'se-text':
            blocks.append(text_block(clean_text_inner(comp)))
        elif kind in ('se-image', 'se-imageStrip'):
            srcs = []
            for t, url in image_modules(comp):
                n_img += 1
                fn = lookup(n_img, url)
                if t == 'gif':   # 유튜버판 GIF는 발행패키지 원본이 있으면 그것을 쓴다 (네이버 w800 압축본보다 좋다)
                    base = url.split('?')[0].rsplit('/', 1)[-1]
                    local = os.path.join(GIF_LOCAL, base)
                    if os.path.exists(local):
                        fn = f'{n_img:02d}_{base}'
                        shutil.copy2(local, os.path.join(img_dir, fn))
                        used.append(fn)
                        srcs.append(rel + fn)
                        continue
                if not fn:
                    raise SystemExit(f'이미지 {n_img} 파일 없음 ({url[:80]})')
                shutil.copy2(os.path.join(P['src'], 'images', fn), os.path.join(img_dir, fn))
                used.append(fn)
                srcs.append(rel + fn)
            blocks.append(img_block(srcs[0]) if kind == 'se-image' and len(srcs) == 1 else strip_block(srcs))
        elif kind == 'se-horizontalLine':
            blocks.append(hr_block())
        elif kind == 'se-oglink':
            blocks.append(oglink_block(P['cta'], rel + thumb, P['og_title']))
        elif kind == 'se-documentTitle':
            continue
        else:
            print('  ! 미처리 컴포넌트', kind)
    if P.get('atf_marker'):   # 첫 화면 변형: 표식 문장이 든 텍스트 블록 + 바로 앞 이미지 블록을 맨 위로 복제
        i = next(k for k, blk in enumerate(blocks) if blk.startswith('<div class="se-component se-text') and P['atf_marker'] in blk)
        assert blocks[i - 1].startswith('<div class="se-component se-image'), '표식 블록 앞이 이미지가 아님'
        blocks = [blocks[i], blocks[i - 1]] + blocks
        print(f'   ↑ 첫 화면 변형: 블록 {i}(텍스트)·{i - 1}(이미지)을 맨 위로 복제')
    se_html = '\n\n'.join(blocks)

    t = open(TEMPLATE, encoding='utf-8').read()
    t = t.replace('</style>', EXTRA_CSS + '</style>', 1)
    a, b = '<!-- POST CONTENT START -->', '<!-- POST CONTENT END -->'
    si, ei = t.index(a), t.index(b)
    html_out = t[:si + len(a)] + '\n\n' + se_html + '\n\n' + t[ei:]
    open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8').write(html_out)
    cfg = {
        'blog': {'name': '기록', 'title': 'dr 피부 약학', 'profile_image': '', 'profile_color': '#a8d8ea'},
        'post': {'title': P['title'], 'category': P['category'], 'date': P['date']},
        'social': P['social'],
        'comments': [],   # 라이브 = 댓글 닫힘 (7.11 추가 공지)
        'tracking': {'meta_pixel_id': PIXEL_ID, 'ga_id': '', 'scroll_events': [25, 50, 75, 100], 'cta_event_name': 'Lead'},
        'cta': {'url': P['cta'], 'text': '제품 보러가기'},
    }
    json.dump(cfg, open(os.path.join(post_dir, 'config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump({'origin': P['origin'], 'fetched': '2026-09-20', 'source_dir': P['src'], 'images': used, 'components': stats},
              open(os.path.join(post_dir, '_source.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    txt = re.sub(r'<[^>]+>', '', se_html)
    n_chars = len(re.sub(r'\s', '', txt))
    print(f'✅ {slug}: 컴포넌트 {stats} · 이미지 {len(used)} · 본문 글자 {n_chars:,}')
    return post_dir


if __name__ == '__main__':
    for slug in (sys.argv[1:] or POSTS):
        build(slug)
