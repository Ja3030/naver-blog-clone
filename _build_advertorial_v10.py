#!/usr/bin/env python3
"""티트리셀 어드버토리얼 v10 → 네이버 블로그 모바일 UI HTML
- 본문: /Users/juan/Brand Manager/티트리셀/_working/advertorial_v3_final.md
- 이미지: public/posts/sa-advertorial-v10/images/IMG-{N:02d}-chatgpt.png (21장)
- 트리거 텍스트 매칭으로 이미지 삽입
"""

import os, re, json, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
POSTS_DIR = os.path.join(BASE, 'public', 'posts')
SRC_MD = '/Users/juan/Brand Manager/티트리셀/_working/advertorial_v3_final.md'

SLUG = 'sa-advertorial-v10'
POST_DIR = os.path.join(POSTS_DIR, SLUG)
IMG_REL = f'/posts/{SLUG}/images/'

CTA_URL = "https://soricare.com/product/detail.html?product_no=64&utm_source=google&utm_medium=cpc&utm_campaign=sa_advertorial_v10"

# ===== 이미지 삽입 트리거 (본문 텍스트 매칭, 트리거 직후 삽입) =====
# (트리거 substring, IMG 번호, alt)
IMAGE_TRIGGERS = [
    ("약통은 매일 늘어났고", 1, "약통 한 가득"),
    ("카드값은 3000만원을 넘겼다", 2, "카드 명세서 누적"),
    ('"아 됐다"', 7, "동네 피부과 처방"),
    ("정말로 매끈했다", 8, "대학병원 처방"),
    ("동료들이 흘끗 보는 게 느껴졌다", 9, "회의실 형광등"),
    ("네 가지를 한꺼번에 처방받았다", 10, "오월의아침 4종"),
    ("울었다", 11, "세면대 약통 더미"),
    ("친구한테 들었던 한방원 갔다", 12, "한방원 한약+침"),
    ("매주 한 번씩 갔다", 13, "강남 시술실"),
    ("월 30만원씩 일 년", 14, "영양제 풀스택"),
    ("라로슈포제 아벤느 듀크레이", 15, "해외 직구 박스"),
    ("알러지 매트리스 공기청정기", 16, "식단·매트리스"),
    ("세다가 손이 멈췄다", 17, "카드 명세서 정점"),
    ("새벽 한두 시까지", 19, "노트북 새벽 자가 진단"),
    ("Demodex folliculorum", 20, "모낭충 다이어그램"),
    ("일본 피부과 학회 — 1.0~1.5% 농도 권장", 21, "해외 TTO 임상 자료"),
    ("이게 호주가 100년 전부터 가지고 있던 답이었다", 23, "비유 그래픽"),
    ("이 네 가지가 다 맞는 건 딱 하나였다", 24, "4종 비교"),
    ("호호바 오일 베이스", 22, "티트리셀 제품"),
    ("개인 답장은 더 이상 못 드리니까", 27, "쪽지 캡처"),
    ("soricare.com/product/detail.html?product_no=64", 28, "티트리셀 CTA 배너"),
]


# ===== SE 블록 헬퍼 =====
def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

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
        <div class="se-og-title">티트리셀 — TTO 1.067% 호호바 베이스</div>
        <div class="se-og-description">호주산 / 10,670ppm / 모낭 침투 오일 베이스</div>
        <div class="se-og-site-name">soricare.com</div>
      </a>
    </div>
  </div>
</div>'''


# ===== 마크다운 본문 파싱 =====
def load_body():
    with open(SRC_MD, 'r', encoding='utf-8') as f:
        md = f.read()
    body_start = md.find('## 단계 1')
    body_end = md.find('# 검증 필요')
    body = md[body_start:body_end]
    body = re.sub(r'^## 단계 \d+[^\n]*\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^---\s*$', '', body, flags=re.MULTILINE)
    return body


# ===== 빌드 =====
def build():
    body = load_body()
    lines = body.split('\n')

    # 이미지 트리거 placeholder 삽입
    full_text = '\n'.join(lines)
    placeholder = '___IMG_{n}___'
    inserted = 0
    for trigger, n, alt in IMAGE_TRIGGERS:
        marker = f"\n\n{placeholder.format(n=n)}\n"
        if trigger in full_text:
            full_text = full_text.replace(trigger, trigger + marker, 1)
            inserted += 1
        else:
            print(f"  ⚠️ 트리거 매칭 실패: IMG {n} ({trigger[:30]})")
    print(f"\n📷 이미지 삽입: {inserted}/{len(IMAGE_TRIGGERS)}")

    lines = full_text.split('\n')

    # SE 블록 생성
    blocks = []
    paras = []  # 누적 paragraph 버퍼

    def flush_paras():
        nonlocal paras
        if paras:
            blocks.append(text_block(paras))
            paras = []

    img_pattern = re.compile(r'^___IMG_(\d+)___$')

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        # 이미지 마커
        m = img_pattern.match(stripped)
        if m:
            flush_paras()
            n = int(m.group(1))
            blocks.append(img_block(f'{IMG_REL}IMG-{n:02d}-chatgpt.png', alt=f'IMG {n}'))
            continue

        # 빈 줄 또는 zero-width space = 단락 break (BR)
        if stripped == '' or stripped == '\u200b':
            paras.append(p_tag(''))
            continue

        # CTA URL 줄은 그냥 텍스트로 (oglink는 별도 처리)
        # 일반 텍스트
        # 시간 marker / 목차 / 박스 류 스타일링
        if stripped.startswith('['):
            # 박스(시각 BA) / 목차 — bold + 큰 글자
            paras.append(p_tag(stripped, fs='fs15', bold=True))
        elif stripped.startswith('⬇'):
            paras.append(p_tag(stripped, fs='fs15', bold=True))
        elif stripped == '↓':
            paras.append(p_tag(stripped, fs='fs15', bold=True, color='#999'))
        elif stripped.startswith('※'):
            paras.append(p_tag(stripped, fs='fs15', bold=True, color='rgb(255, 0, 16)'))
        elif stripped.startswith('🔗'):
            paras.append(p_tag(stripped, fs='fs15', bold=True, color='rgb(0, 0, 255)'))
        elif stripped.startswith('"') and stripped.endswith('"') and len(stripped) < 40:
            # 짧은 따옴표 발화 = 강조
            paras.append(p_tag(stripped, fs='fs15', bold=True))
        elif stripped in ('울었다', '평생 매일 발라야 한다고 생각하셔야 해요', '삼천만원', '"이거 평생 가는 건가"'):
            paras.append(p_tag(stripped, fs='fs19', bold=True, color='rgb(255, 0, 16)'))
        else:
            paras.append(p_tag(stripped))

    flush_paras()

    # 마지막에 oglink CTA 카드 추가 (단계 15 끝)
    blocks.append(hr_block())
    blocks.append(text_block([p_tag('')]))
    blocks.append(oglink_block())
    blocks.append(text_block([p_tag('')]))

    return '\n\n'.join(blocks)


# ===== 템플릿 inject + 저장 =====
def inject_and_save(slug, se_html, config_data):
    post_dir = os.path.join(POSTS_DIR, slug)
    os.makedirs(os.path.join(post_dir, 'images'), exist_ok=True)

    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    start = '<!-- POST CONTENT START -->'
    end = '<!-- POST CONTENT END -->'
    si = template.index(start)
    ei = template.index(end)
    before = template[:si + len(start)]
    after = template[ei:]
    html = before + '\n\n' + se_html + '\n\n' + after

    with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(post_dir, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print(f'  ✅ {slug}/')
    print(f'  📄 index.html — {os.path.getsize(os.path.join(post_dir, "index.html")):,} bytes')


# ===== 실행 =====
print('🚀 어드버토리얼 v10 빌드 시작\n')

se_html = build()

config_data = {
    'blog': {
        'name': '혜원이의 피부 회복 일기',
        'title': '혜원이의 피부 회복 일기',
        'profile_image': '',
        'profile_color': '#f5c6c6',
    },
    'post': {
        'title': '주사피부염 4년 3000만원 헛돈 쓰다가 호주 친구가 보내준 메일 한 통으로 1년 만에 답 찾은 이야기',
        'category': '건강·의학',
        'date': '2025. 11. 18. 23:47',
    },
    'social': {
        'likes': 2184,
        'shares': 167,
        'views': 18432,
    },
    'comments': [
        {'author': '주사피부염4년차', 'profile_color': '#f0d6e8', 'time': '2시간 전',
         'text': '저도 정확히 똑같아요.. 수란트라 끊으면 다시 올라오고. Forton 박사 자료 더 알려주실 수 있나요?', 'likes': 87},
        {'author': '40대워킹맘피부', 'profile_color': '#d6e8f0', 'time': '6시간 전',
         'text': '아침마다 거울 보는 게 무섭다는 거 진짜 공감.. 화장하는데 1시간씩 걸리고요 ㅠ', 'likes': 64},
        {'author': '오월의아침5년차', 'profile_color': '#e8f0d6', 'time': '10시간 전',
         'text': '저도 오월의아침 다녔는데 한 달에 한 번씩 가도 나아지질 않아서.. 호주 100년이라는 말 처음 들어요', 'likes': 52},
        {'author': '강남시술800만원', 'profile_color': '#f0e0d6', 'time': '14시간 전',
         'text': 'LDM 인모드 저도 받았는데 결국 도로 원점인 거 똑같았어요. 표면만 건드린다는 말 너무 와닿네요', 'likes': 41},
        {'author': '복직첫날공포', 'profile_color': '#d6f0e0', 'time': '1일 전',
         'text': '복직 첫날 회의실 형광등 ㅠㅠ 그 장면이 너무 생생해서 댓글 남기게 됐어요. 1년이 지난 지금 정말 안정이세요?', 'likes': 38},
        {'author': '시어머니갱년기', 'profile_color': '#e0d6f0', 'time': '1일 전',
         'text': '시어머니께도 도움 됐다니 부럽네요.. 저희 시어머니 갱년기 홍조로 고생 중이신데 한번 권유해 봐도 될지', 'likes': 33},
    ],
    'tracking': {
        'meta_pixel_id': '1727184084578989',
        'ga_id': '',
        'scroll_events': [25, 50, 75, 100],
        'cta_event_name': 'Lead',
    },
    'cta': {
        'url': CTA_URL,
        'text': '티트리셀 자세히 보기',
    },
}

inject_and_save(SLUG, se_html, config_data)

print('\n✅ 빌드 완료')
print(f'  로컬 미리보기: open public/posts/{SLUG}/index.html')
