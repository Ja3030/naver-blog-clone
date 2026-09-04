"""흰머리 어드버토리얼 v7 → 네이버 블로그 모바일 UI HTML
- 본문: anti-gray-hair/05_ADVERTORIAL/_draft/v9_전문_2026-09-02.txt
- 📷 [라벨]  → 확보 이미지는 실제 삽입, 미확보는 점선 플레이스홀더
- [인용구]  → 네이버 인용구 블록 (다음 스탠자를 감쌈)
"""
import os, re, json, shutil
from _deploy import auto_deploy

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
SRC = '/Users/juan/Brand Manager/anti-gray-hair/05_ADVERTORIAL/_draft/v9_전문_2026-09-02.txt'
SLUG = 'graywhite-v7'
POST_DIR = os.path.join(BASE, 'public', 'posts', SLUG)
IMG_REL = f'/posts/{SLUG}/images/'
PRODUCT_URL = "https://www.momsaju.com/product/%EB%89%B4%ED%8A%B8%EB%A6%AC%EB%9E%A9-%EA%B1%B4%ED%9A%A8%EB%AA%A8%ED%99%98/18/category/43/display/1/"
CTA_URL = PRODUCT_URL + "?utm_source=naver&utm_medium=blog&utm_campaign=graywhite_v7"
# 링크 카드에 뜨는 값 = momsaju 상품 페이지의 실제 og 태그
OG_TITLE  = "뉴트리랩 건효모환 - NutriLab"
OG_DESC   = "건조맥주효모·판토텐산·산화아연·셀레늄 · 뒷면 성분표로 확인하세요"
OG_DOMAIN = "momsaju.com"

IMGSRC = '/Users/juan/Brand Manager/anti-gray-hair/05_ADVERTORIAL/_images'
# 📷 라벨 → [(파일명, 원본경로), ...]  ※ 리스트 = 연속 삽입 / 없는 건 자동 플레이스홀더
def R(n): return f'{IMGSRC}/raw/{n}'
def F(n): return f'{IMGSRC}/final/{n}'

IMAGE_MAP = {
    '비포 애프터 영상':        [('a_before.gif', f'{IMGSRC}/gif/A_before_500.gif'), ('a_after.gif', f'{IMGSRC}/gif/A_after_500.gif')],
    '비포 애프터 사진':        [('a1.jpg', f'{IMGSRC}/A1_final.jpg'), ('a2.jpg', f'{IMGSRC}/A2_final.jpg')],
    '정수리 가르마 사진':      [('b13.jpg', R('B13.jpg'))],
    '시도했던 것들 사진':      [('b14.jpg', R('B14.jpg'))],
    '뿌리 경계선 사진':        [('b16.jpg', R('B16.jpg'))],
    '검색결과 비교 캡처':      [('e5.jpg',  R('E5.jpg'))],
    '논문 캡처':              [('e15b.jpg', F('E15_bradford.jpg'))],
    '약사님 옛날 사진':        [('e12a.jpg', R('E12a.jpg'))],
    '약사님 카톡 캡처':        [('e4.jpg',  R('E4.jpg'))],
    '현재 뿌리 사진':          [('c24.jpg', R('C24.jpg'))],
    '컬럼비아 논문 캡처':      [('e15c.jpg', F('E15_columbia.jpg')), ('e15p.png', R('E15_hair_panel.png'))],
    '모발 단면 현미경 사진':   [('e8.jpg',  R('E8.jpg'))],
    '2제 통 사진':            [('c2.jpg',  R('C2.jpg'))],
    '검은머리 탈색 실험 사진': [('e1a.jpg', R('E1a.jpg')), ('e1b.jpg', R('E1b.jpg'))],
    '정상 vs 쌓임 도해':       [('c4.jpg',  F('C4.jpg'))],
    '계단 그래프 도해':        [('c5v.jpg', R('C5v.jpg')), ('c5d.jpg', R('C5d.jpg'))],
    '효모 함량 비교 그래프':   [('e6.png',  R('E6.png'))],
    '이스트 거품 실험 사진':   [('c16.jpg', R('C16.jpg'))],
    '해외 학교 실험 캡처':     [('e9.jpg',  R('E9.jpg'))],
    '성분표 뒷면 사진':        [('c19.jpg', F('C19.jpg'))],
    '3단 분해 도해':           [('c20.jpg', R('C20.jpg'))],
    '따로 산 네 통 사진':      [('e13s.jpg', R('E13s.jpg')), ('e13.jpg', R('E13.jpg'))],
    '12주 변화 기록 사진':     [('e3.jpg',  R('E3.jpg'))],
    '손님 뿌리 관찰 사진':     [('b17a.jpg', R('B17a.jpg')), ('b17b.jpg', R('B17b.jpg')), ('b17c.jpg', R('B17c.jpg'))],
    '성분표 비교 사진':        [('d1.png',  R('D1.png'))],
    '쇼핑 검색결과 캡처':      [('c18.png', R('C18.png'))],
    '탈락 제품 뒷면 사진':     [('c22.jpg', R('C22.jpg'))],
    '검증 3단 카드':           [('e14.jpg', R('E14.jpg'))],
    '가게 거울 사진':          [('b4.jpg',  R('B4.jpg'))],
    '원장님 단톡방 캡처':      [('e10.jpg', R('E10.jpg'))],
    '댓글 문의 캡처':          [('e16.jpg', R('E16.jpg'))],
'주문내역 캡처':           [('d3.jpg',  R('D3.jpg'))],
    '품절 캡처':               [('e11.jpg', R('E11.jpg'))],
    '잘못 산 제품 모자이크 사진': [('d4.jpg', F('D4.jpg'))],
    '쪽지함 메일함 캡처':      [('a4.jpg', R('A4.jpg'))],
    '뽑은 머리카락 사진':      [('b6b.jpg', R('B6b.jpg'))],
    '468 계산 수첩':           [('b7.jpg',  R('B7.jpg'))],
    '욕실 선반 사진':          [('b8.jpg',  R('B8.jpg'))],
    '가방 속 모자 사진':       [('b10.jpg', R('B10.jpg'))],
    '장바구니 뒷모습 사진':    [('b23.jpg', R('B23.jpg'))],
    '약 갠 볼 사진':           [('c12.jpg', R('C12.jpg'))],
    '검은콩 사진':             [('c10.jpg', R('C10.jpg'))],
    '냉장고 두유 사진':        [('b24.jpg', R('B24.jpg'))],
    '헤나 당근색 사진':        [('b25.jpg', R('B25.jpg'))],
    '미용실 가격표 사진':      [('b15.jpg', R('B15.jpg'))],
    '카페 글 캡처':            [('b18.jpg', R('B18.jpg'))],
    '댓글 캡처':               [('b19.jpg', R('B19.jpg'))],
    '지분 80% 캡처':           [('b20.jpg', F('B20.jpg'))],
    '유튜브 캡처 과산화수소':  [('y1.jpg', R('Y1.jpg'))],
    '해외 유튜브 유전':        [('y2.jpg', R('Y2.jpg'))],
    '유튜브 캡처 효소':        [('y3.jpg', R('Y3.jpg'))],
    '해외 유튜브 판토텐산':    [('y4.jpg', R('Y4.jpg'))],
    '유튜브 캡처 셀레늄':      [('y5.jpg', R('Y5.jpg'))],
    '유튜브 캡처 안돌아옴':    [('y6.jpg', R('Y6.jpg'))],
    '탈색 실험 영상':          [('s0.gif', f'{IMGSRC}/gif/S0_600.gif')],
    '1단계 영상':              [('s1.gif', f'{IMGSRC}/gif/S1_600.gif')],
    '2단계 영상':              [('s2.gif', f'{IMGSRC}/gif/S2_600.gif')],
    '3단계 영상':              [('s3.gif', f'{IMGSRC}/gif/S3_600.gif')],
    '검어짐 영상':             [('s4.gif', f'{IMGSRC}/gif/S4_600.gif')],
}

# ===== 시각 위계 =====
HEADING_LINES = [
    "흰머리는 조금씩 늘지 않는다",
    "하나", "둘", "셋",
    "흰머리는 왜 하얗게 나오나",
    "그동안 먹은 건",
    "그럼 뭘 보고 골라야 하나",
    "마치며",
]
HIGHLIGHT_LINES = [
    "뚝. 하고 계단처럼 훅 늘어난다",
    "기미는 왜 까매지나??",
    "만들긴 만드는데",
    "나오면서 지워지는 거다..",
    "결국엔 영양소 부족이다",
    "유전이 정하는 건",
    "흰머리가 아니라 속도다",
    "이미 하얗게 나온 머리카락은",
    "안 돌아온다",
]
BOLD_LINES = [
    "내가 바로", "그 소리 하는 사람이다", "작년까지는.",
    "그럼 뭐가 지우냐?", "바로, 과산화수소다",
    "그래서 더 빨리", "시작하는 수밖에 없다",
    "백만원이다",
]
RED_PHRASES = ["과산화수소", "468번", "백만원", "3단 분해", "건조맥주효모", "판토텐산", "산화아연", "셀레늄"]

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def _n(x): return x.strip().strip('“”"\' ')
_H = {_n(x) for x in HEADING_LINES}
_HL = {_n(x) for x in HIGHLIGHT_LINES}
_B = {_n(x) for x in BOLD_LINES}
_RED = sorted(RED_PHRASES, key=len, reverse=True)

def p_blank():
    return '      <p class="se-text-paragraph se-blank se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system"><br></span>\n      </p>'

def styled_paragraph(s):
    n = _n(s)
    if n in _H:
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-ff-system" style="font-size:22px;font-weight:800;line-height:1.5;">'+esc(s)+'</span>\n      </p>')
    if s.startswith('(') and s.endswith(')'):
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-ff-system" style="color:#8a9098;font-size:15px;">'+esc(s)+'</span>\n      </p>')
    inner = esc(s)
    for ph in _RED:
        e = esc(ph)
        if e in inner:
            inner = inner.replace(e, '<span style="color:#ff0010;font-weight:700;">'+e+'</span>')
            break
    if n in _HL:
        inner = '<span style="background-color:#fff8b2;font-weight:700;">'+inner+'</span>'
    elif n in _B:
        inner = '<b>'+inner+'</b>'
    return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
            '        <span class="se-ff-system" style="font-size:18px;line-height:1.9;">'+inner+'</span>\n      </p>')

def text_block(paras):
    return ('<div class="se-component se-text se-l-default">\n  <div class="se-section se-section-text se-l-default">\n'
            '    <div class="se-module se-module-text">\n'+'\n'.join(paras)+'\n    </div>\n  </div>\n</div>')

def quote_block(lines):
    inner = '\n'.join(
        '      <p class="se-text-paragraph se-text-paragraph-align-center">\n'
        '        <span class="se-ff-system" style="font-size:19px;font-weight:600;line-height:1.75;">'+esc(l)+'</span>\n      </p>'
        for l in lines)
    return ('<div class="se-component se-quotation se-l-quotation_line">\n'
            '  <div class="se-section se-section-quotation se-l-quotation_line">\n'
            '    <blockquote class="se-quotation-container" style="border-left:3px solid #222;padding:6px 0 6px 18px;margin:26px 0;">\n'
            '      <div class="se-module se-module-text se-quote">\n'+inner+'\n      </div>\n'
            '    </blockquote>\n  </div>\n</div>')

def img_block(src, alt=''):
    return ('<div class="se-component se-image se-l-default">\n  <div class="se-section se-section-image se-l-default">\n'
            '    <div class="se-module se-module-image">\n      <a class="se-module-image-link">\n'
            f'        <img src="{esc(src)}" alt="{esc(alt)}" class="se-image-resource">\n'
            '      </a>\n    </div>\n  </div>\n</div>')

def placeholder_block(label):
    return ('<div class="se-component se-image se-l-default">\n  <div class="se-section se-section-image se-l-default">\n'
            '    <div class="se-module" style="border:2px dashed #c9ccd1;background:#f5f6f7;border-radius:6px;padding:54px 20px;text-align:center;">\n'
            '      <div style="font-size:13px;font-weight:800;letter-spacing:2px;color:#aeb4ba;">📷 사진 자리</div>\n'
            f'      <div style="font-size:15px;font-weight:700;color:#6b7178;margin-top:10px;">{esc(label)}</div>\n'
            '      <div style="font-size:11px;color:#b8bdc2;margin-top:8px;">이미지 자리 · 생성/확보 후 교체</div>\n'
            '    </div>\n  </div>\n</div>')

def hr_block():
    return ('<div class="se-component se-horizontalLine se-l-default">\n  <div class="se-section se-section-horizontalLine se-l-default">\n'
            '    <div class="se-module se-module-horizontalLine">\n      <hr class="se-hr">\n    </div>\n  </div>\n</div>')

def oglink_block():
    return ('<div class="se-component se-oglink se-l-default">\n  <div class="se-section se-section-oglink">\n'
            '    <div class="se-module se-module-oglink">\n'
            f'      <a href="{CTA_URL}" class="se-oglink-info __se_link" target="_blank" rel="noopener" '
            "onclick=\"if(typeof fbq==='function'){fbq('track','Lead');}\">\n"
            '        <div class="se-og-title">내가 먹는 것 — 3단 분해 성분표</div>\n'
            '        <div class="se-og-description">건조맥주효모·판토텐산·산화아연·셀레늄 · 뒷면 성분표로 확인하세요</div>\n'
            '        <div class="se-og-site-name">soricare.com</div>\n'
            '      </a>\n    </div>\n  </div>\n</div>')

LINK_IMG = []

def link_text_block():
    """네이버 링크 카드 — og:image 썸네일 + 제목 + 설명 + 도메인 (스마트에디터 se-oglink 재현)"""
    fn = 'og1.jpg'
    src = IMGSRC + '/raw/OG1.jpg'
    if os.path.exists(src):
        LINK_IMG.append((fn, src))
    return ('<div class="se-component se-oglink se-l-default">\n'
            '  <div class="se-section se-section-oglink">\n'
            '    <div class="se-module se-module-oglink">\n'
            f'      <a href="{CTA_URL}" class="se-oglink-card __se_link" target="_blank" rel="noopener" '
            "onclick=\"if(typeof fbq==='function'){fbq('track','Lead');}\">\n"
            f'        <img src="{IMG_REL}{fn}" alt="" class="se-oglink-thumb">\n'
            '        <div class="se-oglink-body">\n'
            f'          <div class="se-oglink-title">{esc(OG_TITLE)}</div>\n'
            f'          <div class="se-oglink-desc">{esc(OG_DESC)}</div>\n'
            f'          <div class="se-oglink-domain">{esc(OG_DOMAIN)}</div>\n'
            '        </div>\n      </a>\n    </div>\n  </div>\n</div>')

def build():
    raw = open(SRC, encoding='utf-8').read()
    lines = raw.split('\n')
    blocks, paras, last_blank = [], [], True
    used_img, missing = [], []
    pending_quote = False
    quote_buf = []
    def flush():
        nonlocal paras
        if paras:
            blocks.append(text_block(paras)); paras = []
    def flush_quote():
        nonlocal quote_buf, pending_quote
        if quote_buf:
            flush(); blocks.append(quote_block(quote_buf)); quote_buf = []
        pending_quote = False

    i = 0
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r'^📷 \[(.+?)\]$', s)
        if m:
            flush_quote(); flush(); last_blank = True
            label = m.group(1)
            entries = IMAGE_MAP.get(label, [])
            ok = [(fn, src) for fn, src in entries if os.path.exists(src)]
            if ok:
                for fn, src in ok:
                    used_img.append((fn, src))
                    blocks.append(img_block(IMG_REL+fn, label))
            else:
                missing.append(label); blocks.append(placeholder_block(label))
            i += 1; continue
        if s == '[인용구]':
            flush(); pending_quote = True; quote_buf = []; last_blank = True
            i += 1; continue
        if s == '---':
            flush_quote(); flush(); blocks.append(hr_block()); last_blank = True
            i += 1; continue
        if s == '[제품 링크]':
            flush_quote(); flush(); blocks.append(link_text_block()); last_blank = True
            i += 1; continue
        if s == '':
            if pending_quote and quote_buf: flush_quote()
            elif not last_blank:
                paras.append(p_blank()); last_blank = True
            i += 1; continue
        last_blank = False
        if pending_quote: quote_buf.append(s)
        else: paras.append(styled_paragraph(s))
        i += 1
    flush_quote(); flush()
    blocks.append(hr_block()); blocks.append(text_block([p_blank()]))
    print(f"🖼  실제 이미지 {len(used_img)}장 · 플레이스홀더 {len(missing)}개")
    for lb in missing: print(f"   · {lb}")
    if LINK_IMG: print(f"🔗  링크 썸네일 {len(LINK_IMG)}장")
    return '\n\n'.join(blocks), used_img + LINK_IMG

def copy_images(used):
    d = os.path.join(POST_DIR, 'images'); os.makedirs(d, exist_ok=True)
    for fn, src in used: shutil.copy2(src, os.path.join(d, fn))

# ── 댓글 197개 전부 비밀 댓글 (2026-09-04 유저 지시) ──
def secret_comments(n=197, seed=11):
    import random
    rnd = random.Random(seed)
    ko_a = ['봄날','오늘도','뿌리','새치','염색','은퇴','미시','사십','오십','부천','인천','수원','마흔','둘째','워킹','흰머리','거울','정수리','아침','커피','산책','하늘','바다','별빛','달빛','꽃길','햇살','구름','민트','라떼','두딸','세아이','막내','큰딸','주말','평일','퇴근','출근','우리','동네','골목','이층','옥상','창가','텃밭','바람','소나기','안개','노을','새벽']
    ko_b = ['맘','님','씨','지기','언니','이모','살림','일기','하루','러버','홀릭','스토리','로그','엄마','아줌마','생각','기록','노트','집','방','씨앗','정원','산책러','수다','고민','걱정','다이어리','부인','댁','네']
    en = ['sunny','cherry','jenny','hana','mina','lily','coco','yuni','bomi','soo','kimmy','leeh','parkj','yj','sj','hj','mj','eun','jin','ara','dana','rosa','anna','yena','sora','nari','jiyo','haru','moon','star']
    names=set(); out=[]
    while len(out)<n:
        r=rnd.random()
        if r<0.55: nm=rnd.choice(ko_a)+rnd.choice(ko_b)+(str(rnd.randint(1,99)) if rnd.random()<0.35 else '')
        elif r<0.8: nm=rnd.choice(en)+rnd.choice(['','_','.'])+str(rnd.choice([rnd.randint(1,99), rnd.randint(1970,1985), rnd.randint(100,9999)]))
        else: nm=rnd.choice(ko_a)+str(rnd.randint(70,85))+rnd.choice(['','년생','s'])
        if nm in names: continue
        names.add(nm); out.append(nm)
    # 시간: 최신순. 앞 30개 = 오늘, 다음 90개 = 1~5일 전(폭주), 나머지 = 6~18일 전
    times=[]
    for i in range(n):
        if i<3: times.append(rnd.choice(['방금 전','1분 전','3분 전']))
        elif i<12: times.append(f'{rnd.randint(5,58)}분 전')
        elif i<30: times.append(f'{rnd.randint(1,23)}시간 전')
        elif i<120: times.append(f'{rnd.randint(1,5)}일 전')
        else: times.append(f'{rnd.randint(6,18)}일 전')
    # 정렬 보정: 같은 단위 안에서 숫자 오름차순
    def key(s):
        if s=='방금 전': return 0
        v=int(s.split()[0].rstrip('분시간일')) if s[0].isdigit() else 0
        u=s.split()[0]
        return v*(1 if '분' in u else 60 if '시간' in u else 1440)
    times.sort(key=key)
    lock=('<span style="color:#888;display:inline-flex;align-items:center;gap:4px">'
          '<svg width="13" height="13" viewBox="0 0 14 14" fill="none"><rect x="2.5" y="6" width="9" height="6.5" rx="1.2" stroke="#999" stroke-width="1.2"/>'
          '<path d="M4.5 6V4.2a2.5 2.5 0 015 0V6" stroke="#999" stroke-width="1.2"/></svg>비밀 댓글입니다.</span>')
    return [{'author': out[i], 'time': times[i], 'text': lock, 'likes': (rnd.randint(1,3) if rnd.random()<0.08 else 0)} for i in range(n)]

CONFIG = {
    'blog': {'name': '뿌리만보는사람', 'title': '19년차 미용실 원장의 기록',
             'profile_image': '', 'profile_color': '#d9c7a8'},
    'post': {'title': "19년을 2주마다 염색하던 미용실 원장이 두 달에 한 번으로 줄인 이야기",
             'category': '헤어', 'date': '2026. 8. 27. 21:14'},
    'social': {'likes': 2041, 'shares': 168, 'views': 18720},
    'comments': secret_comments(197),
    'tracking': {'meta_pixel_id': '1727184084578989', 'ga_id': '',
                 'scroll_events': [25, 50, 75, 100], 'cta_event_name': 'Lead'},
    'cta': {'url': CTA_URL, 'text': '성분표 확인하기'},
}

def save(se_html, used):
    os.makedirs(os.path.join(POST_DIR, 'images'), exist_ok=True)
    t = open(TEMPLATE, encoding='utf-8').read()
    a, b = '<!-- POST CONTENT START -->', '<!-- POST CONTENT END -->'
    si, ei = t.index(a), t.index(b)
    html = t[:si+len(a)] + '\n\n' + se_html + '\n\n' + t[ei:]
    open(os.path.join(POST_DIR, 'index.html'), 'w', encoding='utf-8').write(html)
    json.dump(CONFIG, open(os.path.join(POST_DIR, 'config.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print('🚀 흰머리 v7 빌드\n')
    se, used = build()
    copy_images(used)
    save(se, used)
    print(f'\n✅ public/posts/{SLUG}/index.html')
