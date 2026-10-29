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
MIRROR = '/Users/juan/Brand Manager/blog-note/public/posts'   # 광고 도착지(프로젝트 blog-note) — 주소에 naver 없음.
# 루트 /는 글 1개만 노출(흰머리 blog-kr과 같은 방식). 이 폴더가 광고가 실제로 가는 곳이다.
GIF_LOCAL = '/Users/juan/Brand Manager/tonsil-stone-spray/03_COPY/유튜버판_2026-08-31/발행패키지_2026-09-01'

POSTS = {
    'tonsil-hyg-v6b': dict(
        src=f'{BK}/여성개량판_juteacher0_224386080000_2026-09-20',
        origin='https://blog.naver.com/juteacher0/224386080000',
        title='편도결석 재발없이 완전 해결한 방법', date='2026. 8. 21. 22:27', category='.',
        cta='https://soricare.com/product/detail.html?product_no=53&utm_source=blog&utm_medium=post&utm_campaign=Avatar4&utm_content=clone_v6b',
        og_title='편도장벽제 - FarmBio',
        # V2 (유저 🟢 2026-09-20): V1 블록에 빠져 있던 가운데 고리(구역반사)를 채우고 자리를 옮겼다.
        # 「대충 본다」 바로 뒤로 — 의사가 두 번 더 시도하는 장면이 그 앞에 오면 어긋난다. VOC 336·655.
        # V3 (유저 🟢 2026-09-20): 제품 나열(A1 어휘 17줄) 앞에 몸 동작 나열을 얹는다 — A6는 제품이 아니라 동작을 센다.
        # VOC 286(원형) · 228 · 95 · 653 · 492 · 72. 제품 나열은 그대로 둔다(「10년간 돈 쓴 사람」 증거).
        inserts=[dict(after='그건 좀 다행이다 싶었다.', lines=[
            '', '처음엔 그냥 기다렸다', '한 번 나왔으니까', '또 나오겠지 싶었다', '',
            '안 나왔다', '',
            '일부러 기침도 해봤다', '가래 뱉듯이 켁켁거려 봤고', '캬악 소리까지 내봤다',
            '세면대 앞에서 혼자', '별 쇼를 다 했다', '',
            '나오는 건 헛구역질뿐이었다', '',
            '분명히 뭔가 걸려 있는데', '안 나온다']),
            dict(after='대~충 보는구나;;', lines=[
            '', '한 번은 눈에 걸리는 게 있다며', '그 자리에서 빼주신 적이 있다',
            '쟁반에 톡 하고', '생각보다 큰 게 떨어졌다', '',
            '근데 안쪽에 하나 더 있다며', '기구를 조금 더 넣는 순간', '내가 웩— 하고 고개를 돌려버렸다', '',
            '다시 해보려는데', '또 그랬다', '',
            '결국 내가 먼저', '됐다고, 그만하겠다고 했다', '의사 앞에서 그러고 있는 게', '너무 창피했다', '',
            '그날 밤,', '침을 삼키는데 알겠더라', '냄새가 그대로 있었다', '',
            '빼낸 건 앞쪽에 있던 거였고', '냄새는 못 뺀 쪽에서 났다', '',
            '결국 남은 건', '손이 안 닿는 자리에 있었다', '병원도, 나도'])],
        # V3 삽입으로 「그날」의 지시가 흐려지고 시제가 튀어 원문 한 줄 교체 (유저 🟢 2026-09-20)
        replaces=[('그날부터 나는,', '그러다 나는,')],
        social=dict(likes=1362, shares=97, views=21480),   # ⚠ 실측 아님 — 라이브 모바일 페이지에 수치가 안 실림. 유저 조정
    ),
    'tonsil-yt-v1': dict(
        src=f'{BK}/여성유튜버판_juteacher0_223935521383_2026-09-20',
        origin='https://blog.naver.com/juteacher0/223935521383',
        title='4년간 편도결석에 시달린 8만 먹방 유튜버가 3개월 동안 바꾼 것 (미국에선 이미 정설)',
        date='2025. 7. 16. 11:17', category='..',
        cta='https://soricare.com/product/detail.html?product_no=53&utm_source=blog&utm_medium=post&utm_campaign=Youtuber&utm_content=clone_v1',
        og_title='프로폴리스 스프레이 - FarmBio',
        # V4 (유저 🟢 2026-09-20): 원문의 A5 belief(「내 구멍이 커서」)는 그대로 두고 A6의 진짜 벽을 하나 더 얹는다.
        # VOC 72 `나올때까자 기다리는데 안나오네요` · 312 `가글 자주해주면 스스로 빠져나올까유`
        inserts=[dict(after='근데 구멍이 문제가 아니었던 거예요.', lines=[
            '', '그리고 하나 더요.', '',
            '저는 계속 기다렸어요.', '건드리면 안 좋다길래', '언젠가 알아서 나오겠지 하고.', '',
            '근데 기다리는 동안', '막은 그대로 있는 거잖아요.', '',
            '하나 빠져도', '그 안에서 또 만들어지고 있었던 거예요.', '',
            '기다려서 될 일이 아니었어요.']),
            dict(after='"불편하면 그때그때 오세요"', lines=[
            '', '사실 그날, 안쪽에 하나 더 있다고', '한 번 더 들어가셨는데',
            '제가 웩— 하고 고개를 돌려버렸어요.', '두 번 시도하다가', '제가 먼저 됐다고 했습니다.',
            '의사 선생님 앞에서 그러고 있는 게', '너무 민망했거든요.', '',
            '그날은 그래도 다 끝난 줄 알았어요.', '',
            '근데 집에 가는 길에', '침을 삼키는데 그대로더라고요.', '',
            '빼주신 건 앞에 보이던 거고', '냄새는 못 뺀 쪽에서 나고 있었어요.', '',
            '그때는 그냥', '덜 뺐나보다 했는데요.'])],
        social=dict(likes=2041, shares=188, views=38920),  # ⚠ 실측 아님 — 유저 조정
    ),
}
# β 첫 화면 변형 (유저 🟢 2026-09-20): 유튜버판 2막의 「"지금은 딱히 안 보이는데요"」 텍스트 블록 + 바로 앞 사진(IMG-13)을
# 맨 위로 복제해 올린다. 2막 자리의 원문은 그대로 둔다. 새 문장 0.
# L1 최초 원고 (224341868295) — ROAS 2.84. 현행 클론(개량판 224386080000)은 2.15였다.
# 첫 화면이 다르다: L1 = 10년째 파내는 습관 + 「진짜 원인을 알게 됐을 뿐」(궁금증 열고 끝) /
# L2 = 「안 보이는데요」 + 「숨어있었을 뿐이었다」(답을 먼저 말함). 본문 68% 동일.
POSTS['tonsil-hyg-L1'] = dict(
    src=f'{BK}/여성최초원고_juteacher0_224341868295_2026-09-24',
    origin='https://blog.naver.com/juteacher0/224341868295',
    title='편도결석 재발없이 완전 해결한 방법', date='2026. 7. 11. 20:14', category='.',
    cta='https://soricare.com/product/detail.html?product_no=53&utm_source=blog&utm_medium=post&utm_campaign=Avatar4&utm_content=clone_L1',
    og_title='프로폴리스 스프레이 - FarmBio',
    social=dict(likes=1362, shares=97, views=21480),   # ⚠ 실측 아님
)

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
.se-viewer .se-module-image video { width: 100%; height: auto; display: block; }
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


def _para(tpl, line):
    """표식 문단(tpl)의 서체·크기·색·정렬을 그대로 복사해 새 문단을 만든다. 빈 줄은 네이버와 같이 ZWSP"""
    m = re.search(r'>([^<>]*)</', tpl)
    pre, suf = tpl[:m.start() + 1], tpl[m.start() + 1 + len(m.group(1)):]
    if line:
        return pre + esc(line) + suf
    return pre.replace('background-color:#ffffff;', '') + '\u200b' + suf


def apply_edits(inner, specs, reps, hits):
    """inserts = 표식 <p> 뒤에 새 문단 끼워넣기 · replaces = 원문 <p> 한 줄 통째 교체.
    둘 다 표식 문단의 조판을 그대로 쓴다. (A6×β 조정 V1~V4 · 유저 🟢 2026-09-20)"""
    def one(m):
        p = m.group(0)
        t = re.search(r'>([^<>]*)</', p)
        txt = H.unescape(t.group(1)).strip() if t else ''
        if not txt:
            return p
        for old, new in reps:
            if txt == old:
                hits[old] = hits.get(old, 0) + 1
                p = _para(p, new)
                break
        for sp in specs:
            if txt == sp['after']:
                hits[sp['after']] = hits.get(sp['after'], 0) + 1
                return p + '\n' + '\n'.join(_para(p, L) for L in sp['lines'])
        return p
    return re.sub(r'<p\b.*?</p>', one, inner, flags=re.S)


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


def optimize(mirror, eager=2):
    """광고 도착지(미러)만 경량화. GIF→mp4 · PNG/JPEG→WebP(폭 900) · 2장 빼고 loading=lazy.
    원본 작업본(naver-blog-clone)은 건드리지 않는다 — 대조용으로 남긴다."""
    import subprocess
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    idir = os.path.join(mirror, 'images')
    idx = os.path.join(mirror, 'index.html')
    if not os.path.isdir(idir):
        return 0, 0
    html_txt = open(idx, encoding='utf-8').read()
    before = sum(os.path.getsize(os.path.join(idir, f)) for f in os.listdir(idir))
    ren = {}
    for f in sorted(os.listdir(idir)):
        src = os.path.join(idir, f)
        if not os.path.isfile(src):
            continue
        stem, ext = os.path.splitext(f)
        if ext.lower() == '.gif':
            out = stem + '.mp4'
            r = subprocess.run(['ffmpeg', '-y', '-i', src, '-movflags', 'faststart', '-pix_fmt', 'yuv420p',
                                '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-crf', '28', '-an',
                                os.path.join(idir, out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if r.returncode == 0:
                ren[f] = out
                os.remove(src)
        elif ext.lower() in ('.png', '.jpg', '.jpeg'):
            out = stem + '.webp'
            try:
                im = Image.open(src).convert('RGB')
                if im.width > 900:
                    im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
                im.save(os.path.join(idir, out), 'WEBP', quality=80, method=5)
                ren[f] = out
                os.remove(src)
            except Exception:
                pass
    for old, new in ren.items():
        if new.endswith('.mp4'):
            html_txt = re.sub(r'<img src="([^"]*?' + re.escape(old) + r')"[^>]*>',
                              lambda m: f'<video src="{m.group(1).replace(old, new)}" autoplay muted loop playsinline></video>',
                              html_txt)
        else:
            html_txt = html_txt.replace(old, new)
    parts = html_txt.split('<img ')                      # 앞 eager장 빼고 lazy
    html_txt = parts[0] + ''.join(('<img ' if i <= eager else '<img loading="lazy" ') + x
                                  for i, x in enumerate(parts[1:], 1))
    open(idx, 'w', encoding='utf-8').write(html_txt)
    after = sum(os.path.getsize(os.path.join(idir, f)) for f in os.listdir(idir))
    return before, after


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

    blocks, n_img, stats, used, hits = [], 0, {}, [], {}
    for kind, comp in components(main):
        stats[kind] = stats.get(kind, 0) + 1
        if kind == 'se-text':
            inner = clean_text_inner(comp)
            if P.get('inserts') or P.get('replaces'):
                inner = apply_edits(inner, P.get('inserts', []), P.get('replaces', []), hits)
            blocks.append(text_block(inner))
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
    for mk in [sp['after'] for sp in P.get('inserts', [])] + [r[0] for r in P.get('replaces', [])]:
        if hits.get(mk) != 1:
            raise SystemExit(f'표식 {mk!r} 매칭 {hits.get(mk, 0)}회 (1회여야 함)')
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
    mirror = os.path.join(MIRROR, slug)
    shutil.rmtree(mirror, ignore_errors=True)
    shutil.copytree(post_dir, mirror, ignore=shutil.ignore_patterns('_source.json'))   # 빌드 기록(원본 네이버 주소 포함) 공개 금지
    for f in ('index.html', 'config.json'):   # css 이름에서 naver 제거 (흰머리 blog-kr과 같은 이름 규칙)
        fp = os.path.join(mirror, f)
        txt = open(fp, encoding='utf-8').read()
        txt = txt.replace('/assets/css/naver-blog.css', '/assets/css/blog.css')
        open(fp, 'w', encoding='utf-8').write(txt)
        if 'naver' in txt.lower():
            raise SystemExit(f'{slug}: 미러 {f}에 naver 문자열 남음')
    ob, oa = optimize(mirror)
    if ob:
        print(f'   ↓ 경량화 {ob/1e6:.1f}MB → {oa/1e6:.1f}MB ({oa/ob*100:.0f}%)')
    for root, _, fs in os.walk(mirror):   # 미러 전체 최종 검사
        for f in fs:
            if f.rsplit('.', 1)[-1] in ('html', 'json', 'css', 'js', 'txt'):
                if 'naver' in open(os.path.join(root, f), encoding='utf-8', errors='ignore').read().lower():
                    raise SystemExit(f'{slug}: 미러에 naver 남음 → {os.path.join(root, f)}')
    print(f'✅ {slug}: 컴포넌트 {stats} · 이미지 {len(used)} · 본문 글자 {n_chars:,} · 미러 → blog-note')
    return post_dir


if __name__ == '__main__':
    for slug in (sys.argv[1:] or POSTS):
        build(slug)
