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
# 전부 화자 1명 일치 (손=마스터핸드 / 얼굴=hf_ 앵커) · POV 자가촬영 · 저화질 톤
def _dl(n): return os.path.join(DL, n)
IMAGE_SRC = {
    # 🔁 얼굴 (눈크롭/거울셀카)
    's01-beforeafter.jpg': _dl('tc_face_before_after_lowq.jpg'),
    's10-dieoff.jpg':      _dl('tc_face_dieoff_lowq.jpg'),
    's12-progress.jpg':    _dl('tc_face_progression_lowq.jpg'),
    # 🎬 장면 (손 일치 · POV)
    's05-towelmirror.jpg': _dl('tc_scene_towelmirror_lowq.jpg'),
    's05-mirrorred.jpg':   _dl('tc_scene_mirror_red_lowq.jpg'),
    's05-makeup.jpg':      _dl('tc_scene_makeup_lowq.jpg'),
    's05-gallery.jpg':     _dl('tc_scene_gallery_lowq.jpg'),
    's05-blank.jpg':       _dl('tc_scene_blank_lowq.jpg'),
    's06-meds.jpg':        _dl('tc_scene_meds_lowq.jpg'),
    's06-receipts.jpg':    _dl('tc_scene_receipts_lowq.jpg'),
    's08-night.jpg':       _dl('tc_scene_nightsearch_lowq.jpg'),
    's08-realize.jpg':     _dl('tc_scene_realize_lowq.jpg'),
    's12-wash.jpg':        _dl('tc_scene_wash_lowq.jpg'),
    's12-walk.jpg':        _dl('tc_scene_walk_lowq.jpg'),
    's12-event.jpg':       _dl('tc_scene_eventphoto_lowq.jpg'),
    # 📊 도식 (.png · "받은 자료" 질감)
    's08-mosquito.png':    _dl('tc_dia_redness.png'),
    's08-order.png':       _dl('tc_dia_paths.png'),
    's09-rebound.png':     _dl('tc_dia_rebound.png'),
    's10-barrier.png':     _dl('tc_dia_barrier.png'),
    's10-demodex.png':     _dl('tc_dia_demodex.png'),
    's10-mold.png':        _dl('tc_dia_mold.png'),
    's11-ppm.png':         _dl('tc_dia_ppm.png'),
    's11-table.png':       _dl('tc_dia_table.png'),
    # 🎬 효능 GIF (모낭충 못 살게 — 환경)
    's11-efficacy.gif':    _dl('tc_efficacy_mites.gif'),
    # 🗂️ 카드 (Canva 기존)
    's04-checklist.png':   os.path.join(IMG_GEN, 's4_checklist.png'),
    # 📸 신규 found-document (피드백 반영)
    's06-diagnosis.jpg':   _dl('tc_scene_diagnosis_lowq.jpg'),
    's08-pharmacy.jpg':    _dl('tc_scene_pharmacy_lowq.jpg'),
    's08-overseas.jpg':    _dl('tc_scene_overseas_lowq.jpg'),
    's10-demodextest.jpg': _dl('tc_scene_demodextest_lowq.jpg'),
    's11-teatree.jpg':     _dl('tc_scene_teatree_lowq.jpg'),
}

# ===== Group A 이미지 트리거 (트리거 문자열 직후 삽입) =====
GROUPA_TRIGGERS = [
    # §1
    ("혈관레이저까지 받았는데도.",                              's01-beforeafter.jpg', "5년 빨갰던 얼굴, 지금"),
    # §4
    ("괜히 시간 버리지 않길 바란다.",                          's04-checklist.png',   "이런 분만 읽어주세요"),
    # §5
    ("이게 심해지니 언젠가부턴 현관 거울도 수건으로 덮어두게 됐다.", 's05-towelmirror.jpg', "수건으로 덮어둔 거울"),
    ("어두우면 그나마 덜 보이니까.",                            's05-mirrorred.jpg',   "불 꺼야 덜 보이던 볼"),
    ("그래도 비치는 덴 컨실러로 콕콕.",                          's05-makeup.jpg',      "매일 아침 가리는 30분"),
    ("나는 늘 카메라 뒤에 있었으니까.",                          's05-gallery.jpg',     "사진첩엔 늘 아이만"),
    ("한참을 가만히 있었다.",                                    's05-blank.jpg',       "화장솜 쥔 채 멍하니"),
    # §6
    ("약산성에 진정크림에, 좋다는 건 다 발라봤다.",              's06-meds.jpg',        "안 해본 게 없던 약·연고"),
    ("레이저값만 천만 원에 가까웠다.",                          's06-receipts.jpg',    "쌓인 영수증"),
    # §8
    ("식구들 다 자는 새벽, 나 혼자 핸드폰을 붙들고 밤을 새웠다.", 's08-night.jpg',       "그날 밤"),
    ("다친 데나 모기 물린 자리를 보면, 빨갛게 부어오른다.",      's08-mosquito.png',    "자극 → 피 몰림 → 부풂"),
    ("안 꺼지는 염증이, 그 혈관을 계속 부풀려온 거였다.",        's08-order.png',       "혈관은 결과, 염증이 원인"),
    ("핸드폰을 든 채로 한참을 멍하니 앉아 있었다.",              's08-realize.jpg',     "그래서였구나"),
    # §9
    ("낫는 게 아니라, 못 끊게 되는 거였다.",                    's09-rebound.png',     "스테로이드 악순환"),
    # §10
    ("그래서 별것 아닌 데도, 염증이 가라앉질 않는 거다.",        's10-barrier.png',     "무너진 피부 장벽"),
    ("이때 확 늘어나서, 그 염증을 더 들쑤신다고 했다.",          's10-demodex.png',     "약한 장벽에서 늘어나는 모낭충"),
    ("시뻘게지고, 더 화끈거리고.",                              's10-dieoff.jpg',      "죽이려다 더 뒤집어진 얼굴"),
    ("내 얼굴도 딱 그거였다.",                                  's10-mold.png',        "닦아도 또 생기는 곰팡이"),
    # §11
    ("이름만 어렵지, 그냥 모낭충이 못 늘게 만드는 거다.",        's11-efficacy.gif',    "환경이 바뀌니 모낭충이 못 버틴다"),
    ("10,670ppm.",                                             's11-ppm.png',         "티트리 농도 비교"),
    ("그래서 이 기준으로, 시중에 있는 걸 다 뒤졌다.",            's11-table.png',       "성분 기준 비교표"),
    # §12
    ("빨갛던 날이, 눈에 띄게 줄어갔다.",                        's12-progress.jpg',    "천천히 줄어든 시간"),
    ("눈만 빼꼼 보던 그 버릇이, 어느새 없어졌다.",              's12-wash.jpg',        "아무렇지 않게 세수"),
    ("이젠 선크림 하나 바르고 나간다.",                        's12-walk.jpg',        "맨얼굴로 등원"),
    ("처음으로 사진을 안 피하고 같이 찍었다.",                  's12-event.jpg',       "드디어 같이 찍힌 사진"),
    # 📸 신규 found-document (피드백 반영)
    ("내 얼굴은 하난데, 의사마다 말이 다르더라.",               's06-diagnosis.jpg',   "병원마다 다른 진단"),
    ("5년을 같은 약국만 다니다 보니, 약사님도 내 얼굴을 안다.",  's08-pharmacy.jpg',    "쌓인 약봉투"),
    ("외국의 어느 피부과 의사가 한 말이었다.",                 's08-overseas.jpg',    "해외 연구 자료"),
    ("나도 예전에 모낭충 검사를 해봤는데, 0마리였거든.",        's10-demodextest.jpg', "모낭충 검사 결과 — 0마리"),
    ("호주에선 옛날부터 상처나 벌레 물린 데 발라온 풀이고.",     's11-teatree.jpg',     "호주 티트리 원물"),
]

# ===== Group B 플레이스홀더 트리거 (비-AI 자산: 실제캡처/제품컷/카드/스티커) =====
GROUPB_TRIGGERS = [
    # §3
    ("그건 절대 아니다.", "💬 스티커 (놀람/물음) [네이버]"),
    # §5
    ("웃으면서 돌아섰지만 사실 마음은 찢어졌다.", "💬 스티커 (걱정/슬픔) — '어디 아파요?' 비트 [네이버]"),
    ("그렇게 처발라도 결국은 티가 난다.", "💬 스티커 (슬픔) [네이버]"),
    # §6
    ("혈관이 늘어나서, 영구적이다.", "🗂️ '평생 관리' 선고 카드 [Canva]"),
    ("어느 순간부턴 내 생활 습관 모든 걸 의심하며 스스로를 한심하게 바라봤다.", "💬 스티커 (자책 바닥) [네이버]"),
    # §8 후기
    ("나 같은 사람들 글을 한참 찾아 읽었다.", "📸 실제 후기 글 캡처 [운영자·실제]"),
    # §9
    ("원인을 안 보니, 고칠 수가 없던 거다.", "🗂️ '평생관리=자백' 카드 [Canva]"),
    ("다들 나처럼, 빨간 것만 쫓느라 몇 년씩 빙빙 돌고 있었다.", "💬 스티커 (분노) [네이버]"),
    # §10
    ("죽이는 게 아니라, 못 살게.", "🗂️ '죽이지 말고, 못 살게' 카드 [Canva]"),
    # §11
    ("독한 약처럼 뒤집어지진 않는다.", "📦 티트리셀 제품 컷 [실제 제품]"),
    ("진짜 되려면, 딱 세 가지가 맞아야 했다.", "🗂️ 핵심3 기준 카드 [Canva]"),
    # §12
    ("좀 지나선 토너랑 패드도 같이 챙겼다.", "📦 티트리셀 크림+토너+패드 [실제 제품]"),
    ("그 말 듣고, 좀 울컥했다.", "💬 스티커 (밝음/반가움) — '좋아졌네요?' 비트 [네이버]"),
    ("그 평범한 게, 5년 만에 됐다.", "💬 스티커 (벅참/안도) [네이버]"),
    # §13
    ("5년 헤매고 안 게, 딱 이거였다.", "🗂️ 결론 카드 (빨간건 결과/염증/못살게) [Canva]"),
    ("마지막 하나는, 그 고생 이미 다 한 사람이 찾은 걸 그냥 한 통 써보는 거.", "📊 세 갈래 길 도식 [GPT]"),
    ("밑져야 본전인 거다.", "🗂️ 28일 환불 카드 [Canva]"),
    ("(다음에 들어오면 또 언제 풀릴지 모른다.)", "🗂️ 품절·기한 카드 [Canva]"),
]

THUMB_LABEL = "대표 사진 — 약·레이저 없이 호전된 현재 얼굴"


# ===== SE 블록 헬퍼 =====
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def p_tag(text, fs='fs15', bold=False, color=None):
    if not text.strip():
        return '      <p class="se-text-paragraph se-blank se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system"><br></span>\n      </p>'
    inner = esc(text)
    if bold:
        inner = f'<b>{inner}</b>'
    style = f' style="color:{color};"' if color else ''
    return f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span{style} class="se-fs-{fs} se-ff-system">{inner}</span>\n      </p>'

# ===== 강조 시스템 (레퍼런스 네이버 어드버토리얼 시각 위계 이식) =====
HEADING_LINES = [
    "그 5년 동안, 안 해본 게 없다.",
    "내 얼굴은 고장난 게 아니었다.",
    "죽이지 말고, 못 살게.",
    "티트리였다.",
    "그 평범한 게, 5년 만에 됐다.",
]
HIGHLIGHT_LINES = [
    "빨간 거 그거, 그 밑에 염증이 자꾸 건드려서 그래.",
    "빨간 게 가라앉을 틈이 없었던 거다.",
    "그 염증이 혈관을 건드려서 → 빨개지는 거.",
    "그냥 모낭충이 못 견디는 환경을 만들어주는 거다.",
    "10,670ppm.",
    "빨간 건 원인이 아니라 결과라는 거.",
]
BOLD_LINES = [
    "지금 내 얼굴이다.",
    "그건 아니다.",
    "5년째, 똑바로 못 보고 살았다.",
    "혈관이 늘어나서, 영구적이다.",
    "근데 그게 — 하나였다.",
    "그래서였구나.",
    "혈관은 결과다.",
]
RED_PHRASES = [
    "평생 관리하셔야 돼요", "자릿수가 아예 달랐다", "모세혈관이 늘어나서",
    "완치는 없고", "고장난 거구나", "또 광고겠지",
    "영구적이다", "리바운드", "한심했다", "천만 원", "30만 원",
]

def _norm(x):
    return x.strip().strip('“”"\' ')

_HEADING_N = {_norm(x) for x in HEADING_LINES}
_HIGHLIGHT_N = {_norm(x) for x in HIGHLIGHT_LINES}
_BOLD_N = {_norm(x) for x in BOLD_LINES}
_RED_SORTED = sorted(RED_PHRASES, key=len, reverse=True)

def styled_paragraph(s):
    n = _norm(s)
    if n in _HEADING_N:
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-ff-system" style="font-size:22px;font-weight:800;line-height:1.5;">' + esc(s) + '</span>\n'
                '      </p>')
    if s.startswith('(') and s.endswith(')'):
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-fs-fs13 se-ff-system" style="color:#8a9098;font-size:15px;">' + esc(s) + '</span>\n'
                '      </p>')
    inner = esc(s)
    for ph in _RED_SORTED:
        e = esc(ph)
        if e in inner:
            inner = inner.replace(e, '<span style="color:#ff0010;font-weight:700;">' + e + '</span>')
    if n in _HIGHLIGHT_N:
        inner = '<span style="background-color:#fff8b2;font-weight:700;">' + inner + '</span>'
    elif n in _BOLD_N or (s.startswith('"') and s.endswith('"') and len(s) < 45):
        inner = '<b>' + inner + '</b>'
    return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
            '        <span class="se-fs-fs15 se-ff-system" style="font-size:18px;line-height:1.85;">' + inner + '</span>\n'
            '      </p>')


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
      <div style="font-size:11px;color:#b8bdc2;margin-top:8px;">이미지 자리 · 생성/확보 후 교체</div>
    </div>
  </div>
</div>'''

def section_break_block():
    return '''<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- "><span class="se-ff-system" style="display:block;height:44px;line-height:44px;">&#8203;</span></p>
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
    # §1 헤더는 제거(맨 앞 섹션 브레이크 방지), §2~13 헤더는 섹션 브레이크 마커로
    body = re.sub(r'^##\s*§1[^\n]*$', '', body, count=1, flags=re.MULTILINE)
    body = re.sub(r'^##\s*§[^\n]*$', '\n___SECTION___\n', body, flags=re.MULTILINE)
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

        if s == '___SECTION___':
            if paras and 'se-blank' in paras[-1]:   # 앞 빈 줄 제거
                paras.pop()
            flush()
            blocks.append(section_break_block())
            last_br = True                          # 뒤 빈 줄 1개 suppress
            continue

        if s == '':
            if not last_br:
                paras.append(p_tag(''))
                last_br = True
            continue
        last_br = False
        paras.append(styled_paragraph(s))

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
         'text': '저도 거울 보기 싫어서 화장실 불도 잘 안 켜고 살았어요.. 읽다가 울컥했네요. 화장으로 덮어도 오후되면 올라오는 것도 똑같고요 ㅠ', 'likes': 58},
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
