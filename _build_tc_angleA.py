#!/usr/bin/env python3
"""티트리셀 AngleA 어드버토리얼(§1-13) → 네이버 블로그 모바일 UI HTML
- 본문: demodex-rosacea/03_ADVERTORIAL/advertorial_AngleA_prose_2026-06-13.md
- Group A 이미지 12장: 실제 삽입 (GPT 7 + HTML figure 5)
- Group B 6곳: 점선 '사진 자리' 플레이스홀더 (실제 사진 필요)
"""

import os, re, json, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
POSTS_DIR = os.path.join(BASE, 'public', 'posts')
SRC_MD = '/Users/juan/Brand Manager/demodex-rosacea/03_ADVERTORIAL/advertorial_AngleA_prose_2026-06-13.md'

SLUG = 'tc-rosacea-angleA'
POST_DIR = os.path.join(POSTS_DIR, SLUG)
IMG_REL = f'/posts/{SLUG}/images/'

CTA_URL = "https://soricare.com/product/detail.html?product_no=64&utm_source=naver&utm_medium=blog&utm_campaign=tc_angleA_v1"

IMG_GEN = '/Users/juan/Brand Manager/demodex-rosacea/03_ADVERTORIAL/_working/img_gen'
DL = '/Users/juan/Downloads'

# ===== 이미지 파일 소스 (canonical 이름 → 원본 경로) =====
IMAGE_SRC = {
    's05-vanity.png':    os.path.join(DL, 'ChatGPT Image 2026년 6월 16일 오후 11_09_16.png'),
    's05-mirror.png':    os.path.join(DL, 'ChatGPT Image 2026년 6월 16일 오후 11_09_21.png'),
    's06-meds.png':      os.path.join(DL, 'ChatGPT Image 2026년 6월 16일 오후 11_09_11.png'),
    's06-statement.png': os.path.join(DL, 'ChatGPT Image 2026년 6월 17일 오전 12_27_32.png'),
    's08-mosquito.png':  os.path.join(DL, 'ChatGPT Image 2026년 6월 16일 오후 11_09_25.png'),
    's10-mold.png':      os.path.join(DL, 'ChatGPT Image 2026년 6월 16일 오후 11_09_30.png'),
    's11-teatree.png':   os.path.join(DL, 'ChatGPT Image 2026년 6월 17일 오전 12_11_05.png'),
    's04-checklist.png': os.path.join(IMG_GEN, 's4_checklist.png'),
    's07-search.png':    os.path.join(IMG_GEN, 's7_yt_search.png'),
    's10-pathway.png':   os.path.join(IMG_GEN, 'p10_figure.png'),
    's11-ppm.png':       os.path.join(IMG_GEN, 'p11_figure.png'),
    's12-timeline.png':  os.path.join(IMG_GEN, 's12_timeline.png'),
}

# ===== Group A 이미지 트리거 (트리거 문자열 직후 삽입) =====
GROUPA_TRIGGERS = [
    ("괜히 시간 버릴 것 없다.",                          's04-checklist.png', "이런 분만 읽어주세요 체크리스트"),
    ("언젠가부턴 현관 거울도 수건으로 반쯤 덮어놨다.",    's05-mirror.png',    "수건으로 반쯤 덮어둔 거울"),
    ("그래도 비치는 덴 컨실러로 콕콕.",                  's05-vanity.png',    "매일 아침 30분 떡칠"),
    ("약산성에 진정크림에, 좋다는 건 다 발라봤다.",      's06-meds.png',      "안 해본 게 없던 약·연고 더미"),
    ("레이저값만 천만 원에 가까웠다.",                  's06-statement.png', "5년치 카드 명세서"),
    ("몇 시간 동안 밤을 새며 찾아봤다.",                's07-search.png',    "그날 밤 검색 기록"),
    ("빨간 게 가라앉을 틈이 없었던 거다.",              's08-mosquito.png',  "안 떨어지는 모기처럼"),
    ("그 염증이 혈관을 건드려서 → 빨개지는 거.",         's10-pathway.png',   "[그림1] 주사피부염 발생 경로"),
    ("내 얼굴도 딱 그랬다.",                            's10-mold.png',      "닦아도 또 생기는 곰팡이"),
    ("거기선 옛날부터 상처나 벌레 물린 데 발라왔다더라.", 's11-teatree.png',   "호주 티트리 원물"),
    ("10,670ppm.",                                     's11-ppm.png',       "[그림2] 티트리 농도 비교"),
    ("그렇게 천천히, 빨갛던 날이 하루하루 줄었다.",      's12-timeline.png',  "천천히 줄어든 시간"),
]

# ===== Group B 플레이스홀더 트리거 (실제 사진 필요) =====
GROUPB_TRIGGERS = [
    ("아침저녁으로 그냥 발라주기만 하면 됐다.", "티트리셀 제품 사진"),
    ("나 같은 사람들 글을 한참 찾아 읽었다.",   "실제 후기 글 캡처 (나 같은 사람들 글)"),
    ("처음으로 사진 안 피하고 같이 찍었다.",     "맨얼굴 등원 / 아이와 함께 찍은 사진"),
]

THUMB_LABEL = "대표 사진 — 약·레이저 없이 호전된 현재 얼굴"


# ===== SE 블록 헬퍼 =====
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def p_tag(text, fs='fs15', bold=False, color=None):
    if not text.strip():
        return '      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system"><br></span>\n      </p>'
    inner = esc(text)
    if bold:
        inner = f'<b>{inner}</b>'
    style = f' style="color:{color};"' if color else ''
    return f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span{style} class="se-fs-{fs} se-ff-system">{inner}</span>\n      </p>'

def text_block(paras):
    return f'''<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
{chr(10).join(paras)}
    </div>
  </div>
</div>'''

def img_block(src, alt=''):
    return f'''<div class="se-component se-image se-l-default">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a class="se-module-image-link">
        <img src="{esc(src)}" alt="{esc(alt)}" class="se-image-resource">
      </a>
    </div>
  </div>
</div>'''

def placeholder_block(label):
    return f'''<div class="se-component se-image se-l-default">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module" style="border:2px dashed #c9ccd1;background:#f5f6f7;border-radius:6px;padding:54px 20px;text-align:center;">
      <div style="font-size:13px;font-weight:800;letter-spacing:2px;color:#aeb4ba;">📷 사진 자리</div>
      <div style="font-size:15px;font-weight:700;color:#6b7178;margin-top:10px;">{esc(label)}</div>
      <div style="font-size:11px;color:#b8bdc2;margin-top:8px;">실제 사진 필요 · AI 생성 불가 (Group B)</div>
    </div>
  </div>
</div>'''

def hr_block():
    return '''<div class="se-component se-horizontalLine se-l-default">
  <div class="se-section se-section-horizontalLine se-l-default">
    <div class="se-module se-module-horizontalLine">
      <hr class="se-hr">
    </div>
  </div>
</div>'''

def oglink_block():
    return f'''<div class="se-component se-oglink se-l-default">
  <div class="se-section se-section-oglink">
    <div class="se-module se-module-oglink">
      <a href="{CTA_URL}" class="se-oglink-info __se_link" target="_blank" rel="noopener" onclick="if(typeof fbq==='function'){{fbq('track','Lead');}}">
        <div class="se-og-title">티트리셀 — 티트리 10,670ppm 크림</div>
        <div class="se-og-description">호주 티트리 고함량 · 병풀·판테놀 진정 · 아침저녁 발라주는 크림</div>
        <div class="se-og-site-name">soricare.com</div>
      </a>
    </div>
  </div>
</div>'''


# ===== 본문 파싱 =====
def load_body():
    with open(SRC_MD, 'r', encoding='utf-8') as f:
        md = f.read()
    start = md.find('## §1')
    body = md[start:]
    # 섹션 헤더 / 구분선 제거
    body = re.sub(r'^##\s*§[^\n]*$', '', body, flags=re.MULTILINE)
    body = re.sub(r'^\s*---\s*$', '', body, flags=re.MULTILINE)
    return body


def build():
    full_text = load_body()

    phb = []   # placeholder labels
    imga = []  # (filename, alt)

    # 1) 본문 내 [이미지: ...] 마커 → Group B 플레이스홀더
    def repl_bracket(m):
        raw = m.group(1)
        label = re.split(r'[—\-–]', raw)[0].strip()
        idx = len(phb); phb.append(label)
        return f"\n\n___PHB_{idx}___\n"
    full_text = re.sub(r'\[이미지:([^\]]*)\]', repl_bracket, full_text)

    # 2) Group A 이미지 트리거 삽입
    a_hit = 0
    for trigger, fname, alt in GROUPA_TRIGGERS:
        if trigger in full_text:
            k = len(imga); imga.append((fname, alt))
            full_text = full_text.replace(trigger, trigger + f"\n\n___IMGA_{k}___\n", 1)
            a_hit += 1
        else:
            print(f"  ⚠️ [A] 트리거 매칭 실패: {fname} ({trigger[:24]})")

    # 3) Group B 트리거 삽입
    b_hit = 0
    for trigger, label in GROUPB_TRIGGERS:
        if trigger in full_text:
            idx = len(phb); phb.append(label)
            full_text = full_text.replace(trigger, trigger + f"\n\n___PHB_{idx}___\n", 1)
            b_hit += 1
        else:
            print(f"  ⚠️ [B] 트리거 매칭 실패: {label} ({trigger[:24]})")

    # 4) 맨 위 대표 썸네일 플레이스홀더
    tidx = len(phb); phb.append(THUMB_LABEL)
    full_text = f"___PHB_{tidx}___\n\n" + full_text

    print(f"\n📷 Group A 삽입: {a_hit}/{len(GROUPA_TRIGGERS)}  |  Group B 플레이스홀더: {len(phb)}")

    # ===== 블록 생성 =====
    lines = full_text.split('\n')
    blocks = []
    paras = []
    last_br = False

    def flush():
        nonlocal paras
        if paras:
            blocks.append(text_block(paras))
            paras = []

    re_a = re.compile(r'^___IMGA_(\d+)___$')
    re_b = re.compile(r'^___PHB_(\d+)___$')

    for raw in lines:
        s = raw.strip()

        ma = re_a.match(s)
        if ma:
            flush(); last_br = False
            fname, alt = imga[int(ma.group(1))]
            blocks.append(img_block(IMG_REL + fname, alt))
            continue
        mb = re_b.match(s)
        if mb:
            flush(); last_br = False
            blocks.append(placeholder_block(phb[int(mb.group(1))]))
            continue

        if s == '':
            if not last_br:
                paras.append(p_tag(''))
                last_br = True
            continue
        last_br = False

        # 가벼운 스타일링
        if s.startswith('(') and s.endswith(')'):
            paras.append(p_tag(s, fs='fs13', color='#8a9098'))
        elif s.startswith('"') and s.endswith('"') and len(s) < 45:
            paras.append(p_tag(s, bold=True))
        elif s.startswith('※'):
            paras.append(p_tag(s, bold=True, color='rgb(255,0,16)'))
        else:
            paras.append(p_tag(s))

    flush()

    # CTA
    blocks.append(hr_block())
    blocks.append(text_block([p_tag('')]))
    blocks.append(oglink_block())
    blocks.append(text_block([p_tag('')]))

    return '\n\n'.join(blocks)


# ===== 이미지 복사 =====
def copy_images():
    img_dir = os.path.join(POST_DIR, 'images')
    os.makedirs(img_dir, exist_ok=True)
    ok = 0
    for name, src in IMAGE_SRC.items():
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(img_dir, name))
            ok += 1
        else:
            print(f"  ⚠️ 이미지 원본 없음: {name} ← {src}")
    print(f"🖼  이미지 복사: {ok}/{len(IMAGE_SRC)} → {img_dir}")


# ===== 저장 =====
def inject_and_save(se_html, config_data):
    os.makedirs(os.path.join(POST_DIR, 'images'), exist_ok=True)
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()
    start = '<!-- POST CONTENT START -->'
    end = '<!-- POST CONTENT END -->'
    si = template.index(start); ei = template.index(end)
    html = template[:si + len(start)] + '\n\n' + se_html + '\n\n' + template[ei:]
    with open(os.path.join(POST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(POST_DIR, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {SLUG}/index.html — {os.path.getsize(os.path.join(POST_DIR, 'index.html')):,} bytes")


config_data = {
    'blog': {
        'name': '지영ㅣ주사피부염 회복일기',
        'title': '지영ㅣ주사피부염 회복일기',
        'profile_image': '',
        'profile_color': '#f3d4d4',
    },
    'post': {
        'title': '주사피부염 홍조 극복 후기',
        'category': '건강·뷰티',
        'date': '2026. 5. 14. 22:18',
    },
    'social': {'likes': 1873, 'shares': 142, 'views': 15604},
    'comments': [
        {'author': '주사피부염5년차', 'profile_color': '#f0d6e8', 'time': '3시간 전',
         'text': '저랑 너무 똑같아요.. 레이저 받으면 잠깐 빠졌다가 며칠이면 또 올라오고. 결국 완치는 없다는 말만 들었거든요. 염증부터라는 말 처음 들어요', 'likes': 73},
        {'author': '40대워킹맘', 'profile_color': '#d6e8f0', 'time': '5시간 전',
         'text': '아침마다 거울 눈만 보고 볼은 안 본다는 거.. 읽다가 울컥했네요. 화장으로 덮어도 오후되면 올라오는 것도 똑같고요 ㅠ', 'likes': 58},
        {'author': '맨얼굴이소원', 'profile_color': '#e8f0d6', 'time': '8시간 전',
         'text': '스테로이드 끊으면 더 시뻘게져서 무서워서 또 바르고.. 그 굴레 너무 공감돼요. 모낭충 환경 얘기 더 알고싶어요', 'likes': 49},
        {'author': '천만원날린사람', 'profile_color': '#f0e0d6', 'time': '12시간 전',
         'text': '카드 명세서 더해보다 손 멈췄다는 부분.. 저도 세다가 그만뒀어요. 표면만 지진다는 말이 너무 와닿네요', 'likes': 41},
        {'author': '복직앞두고', 'profile_color': '#d6f0e0', 'time': '1일 전',
         'text': '곰팡이 비유 진짜 찰떡이네요. 죽이는 게 아니라 환경을 바꾼다 — 이제야 이해가 돼요. 혹시 처음에 따끔한 건 얼마나 가나요?', 'likes': 34},
        {'author': '아이엄마지수', 'profile_color': '#e0d6f0', 'time': '1일 전',
         'text': '사진에 늘 본인만 없다는 거.. 저도 그래서 댓글 남겨요. 지금은 아이랑 같이 찍으신다니 그게 제일 부럽습니다', 'likes': 29},
    ],
    'tracking': {
        'meta_pixel_id': '1727184084578989',
        'ga_id': '',
        'scroll_events': [25, 50, 75, 100],
        'cta_event_name': 'Lead',
    },
    'cta': {'url': CTA_URL, 'text': '티트리셀 자세히 보기'},
}


if __name__ == '__main__':
    print('🚀 티트리셀 AngleA 빌드 시작\n')
    se_html = build()
    copy_images()
    inject_and_save(se_html, config_data)
    print('\n✅ 빌드 완료')
    print(f'  로컬 미리보기: open public/posts/{SLUG}/index.html')
