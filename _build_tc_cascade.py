#!/usr/bin/env python3
"""티트리셀 Cascade Reset 어드버토리얼 → 네이버 블로그
- 본문: demodex-rosacea/Final/_s1~_s11_check.txt (+ _s7b_check.txt)
- 이미지 38장: Final/images/§*.png (slot_id 매칭)
- 가독성: 28px 빨강 제목 / 19px 본문 / line-height 1.0 / 빈 단락 호흡
"""

import os, re, json, shutil

BASE_BLOG = '/Users/juan/Brand Manager/naver-blog-clone'
BASE_AD = '/Users/juan/Brand Manager/demodex-rosacea'
TEMPLATE = os.path.join(BASE_BLOG, 'templates', 'post-template.html')
SLUG = 'tc-rosacea-cascade'
POST_DIR = os.path.join(BASE_BLOG, 'public', 'posts', SLUG)
IMG_REL = f'/posts/{SLUG}/images/'
IMG_SRC_DIR = os.path.join(BASE_AD, 'Final', 'images')

CTA_URL = "https://soricare.com/product/detail.html?product_no=64&utm_source=naver&utm_medium=blog&utm_campaign=tc_cascade_v1"

# ===== 본문 파일 순서 =====
SECTION_FILES = [
    ('§1',  '_s1_check.txt'),
    ('§2',  '_s2_check.txt'),
    ('§3',  '_s3_check.txt'),
    ('§4',  '_s4_check.txt'),
    ('§5',  '_s5_check.txt'),
    ('§6',  '_s6_check.txt'),
    ('§7',  '_s7_check.txt'),
    ('§7b', '_s7b_check.txt'),
    ('§8',  '_s8_check.txt'),
    ('§9',  '_s9_check.txt'),
    ('§10', '_s10_check.txt'),
    ('§11', '_s11_check.txt'),
]

# ===== Slot ID → 이미지 파일 매핑 =====
# para_id (slot이 들어갈 본문 단락) → 이미지 파일명
# (실제 다운로드 받은 38장)
IMAGE_MAP = {
    # §1
    ('§1', 0):  '§1_0_약품_3종_amateur.png',
    ('§1', 2):  '§1_사촌카톡.png',
    ('§1', 4):  '§1_4_학술지콜라주.png',
    ('§1', 5):  '§1_네이버메일999.png',
    # §2
    ('§2', 2):  '§2_slot_2_진료확인서.png',
    # §5
    ('§5', 1):  '§5_slot_1_약5종.png',
    ('§5', 2):  '§5_slot_3_KB카드문자.png',
    ('§5', 3):  '§5_slot_4_화장품카오스.png',
    ('§5', 4):  '§5_slot_5_영수증.png',
    # §6
    ('§6', 3):  '§6_slot_2_책상영문책.png',
    ('§6', 4):  '§6_slot_3_논문stack.png',
    ('§6', 5):  '§6_slot_tweets.png',
    ('§6', 10): '§6_slot_6_reddit.png',
    ('§6', 12): '§6_slot_7_reddit댓글.png',
    ('§6', 14): '§6_slot_8_instagram.png',
    # §7
    ('§7', 2):  '§7_slot_1_tv학명박스.png',
    ('§7', 3):  '§7_slot_2_cascade큐브.png',
    ('§7', 6):  '§7_slot_5_학술논문.png',
    ('§7', 8):  '§7_slot_6_식약처.png',
    # §7b
    ('§7b', 4): '§7b_slot_2_reddit_erythema.png',
    ('§7b', 6): '§7b_6_slot_user_tv25년.png',
    # §8
    ('§8', 0):  '§8_0_slot_user_여성의사.png',
    ('§8', 1):  '§8_1_slot_user_여성의사위험.png',
    ('§8', 3):  '§8_slot_1_3pillar.png',
    ('§8', 6):  '§8_slot_user_7_한국의사.png',
    ('§8', 9):  '§8_slot_user_10_TEDMED.png',
    ('§8', 11): '§8_slot_4_유튜브검색.png',
    ('§8', 12): '§8_slot_5_reddit댓글.png',
    # §9
    ('§9', 3):  '§9_slot_1_13개비교표.png',
    ('§9', 4):  '§9_slot_3_reddit300k.png',
    ('§9', 5):  '§9_slot_4_학술지콜라주.png',
    ('§9', 6):  '§9_slot_6_sigma.png',
    ('§9', 7):  '§9_slot_7_4주임상.png',
    ('§9', 9):  '§9_slot_8_cro보고서.png',
    ('§9', 10): '§9_slot_9_임상.png',
    # §10
    ('§10', 11): '§10_slot_8_남편카톡.png',
    ('§10', 14): '§10_slot_9_드첸트윗.png',
    # §11
    ('§11', 5):  '§11_slot_1_메일함.png',
}

# ===== 강조 색 시스템 =====
# 빨강 강조 단락 (반복적으로 등장하는 통점 또는 핵심 메시지)
RED_LINES_PARTIAL = [
    "5년", "별짓 다 해본", "5년 동안 매일 아침",
    "평생 관리하는 거예요", "5년 내내", "5년 만에",
    "광고 0", "협찬 의뢰는 다 거절",
    "정말 답이 없었", "정말 없었", "정말 0개", "0개",
    "또 뒤집어진", "또 도진",
    "Demodex-Malassezia", "cascade", "Cascade Reset", "캐스케이드 리셋",
    "98%", "78%", "89%", "100편",
    "Sigma-Aldrich", "kg당 200만원",
    "AAD 가이드라인", "식약처",
    "Dr. Sarah Chen", "Dr. Chen",
    "내 잘못이 아니다", "본인 잘못이 절대 아니다",
    "한국 시장에 답이 없", "한국에 들어오는 게 늦",
]

# ===== HTML 헬퍼 =====
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def blank_p():
    return '      <p class="se-text-paragraph se-blank se-text-paragraph-align- "><span class="se-fs-fs19 se-ff-system"><br></span></p>'

def big_red_p(text):
    """28px 빨강 (대제목)"""
    return (
        '      <p class="se-text-paragraph se-text-paragraph-align- ">'
        f'<span class="se-fs-fs28 se-ff-system" style="font-size:28px;color:#ff0010;line-height:1.0;">{esc(text)}</span>'
        '</p>'
    )

def body_p(text, red=False):
    """19px 본문 (검정 기본, red=True면 빨강)"""
    inner = esc(text)
    # 부분 빨강 강조: 본문 내에 RED_LINES_PARTIAL 단어가 있으면 그 부분만 빨강
    if not red:
        for w in sorted(RED_LINES_PARTIAL, key=len, reverse=True):
            we = esc(w)
            if we in inner:
                inner = inner.replace(we, f'<span style="color:#ff0010;">{we}</span>')
    color_style = 'color:#ff0010;' if red else ''
    return (
        '      <p class="se-text-paragraph se-text-paragraph-align- ">'
        f'<span class="se-fs-fs19 se-ff-system" style="font-size:19px;{color_style}line-height:1.0;">{inner}</span>'
        '</p>'
    )

def text_block(paragraphs_html):
    return (
        '<div class="se-component se-text se-l-default">\n'
        '  <div class="se-section se-section-text se-l-default">\n'
        '    <div class="se-module se-module-text">\n'
        + '\n'.join(paragraphs_html) + '\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )

def img_block(src, alt=''):
    return (
        '<div class="se-component se-image se-l-default">\n'
        '  <div class="se-section se-section-image se-l-default">\n'
        '    <div class="se-module se-module-image">\n'
        '      <a class="se-module-image-link">\n'
        f'        <img src="{esc(src)}" alt="{esc(alt)}" class="se-image-resource">\n'
        '      </a>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )

def hr_block():
    return (
        '<div class="se-component se-horizontalLine se-l-default">\n'
        '  <div class="se-section se-section-horizontalLine se-l-default">\n'
        '    <div class="se-module se-module-horizontalLine">\n'
        '      <hr class="se-hr">\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )

def oglink_block():
    return (
        '<div class="se-component se-oglink se-l-default">\n'
        '  <div class="se-section se-section-oglink">\n'
        '    <div class="se-module se-module-oglink">\n'
        f'      <a href="{CTA_URL}" class="se-oglink-info __se_link" target="_blank" rel="noopener" onclick="if(typeof fbq===\'function\'){{fbq(\'track\',\'Lead\');}}">\n'
        '        <div class="se-og-title">티트리셀 — Cascade Reset 크림</div>\n'
        '        <div class="se-og-description">티트리 1.07% 고농도 · 항진균 식물 추출 · 세라마이드·판테놀 · 28일 환불</div>\n'
        '        <div class="se-og-site-name">soricare.com</div>\n'
        '      </a>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>'
    )

# ===== 본문 파싱 =====
def load_section(filename):
    """단락 리스트 반환 (빈 줄 제외)"""
    path = os.path.join(BASE_AD, 'Final', filename)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = [line.strip() for line in text.split('\n') if line.strip()]
    return paragraphs

def is_first_paragraph_of_section(idx_in_section, section_label, paragraphs):
    """§1 첫 단락 (제목 톤) 판단 — 보통 §의 1번째 단락만 28px 빨강 대제목"""
    return idx_in_section == 0 and section_label in ('§1',)

# ===== build =====
def build():
    blocks = []

    for section_label, filename in SECTION_FILES:
        paragraphs = load_section(filename)

        # 단락별 처리
        current_text_paras = []
        for idx, para in enumerate(paragraphs):
            # 첫 단락 = 28px 빨강 (§1만)
            if section_label == '§1' and idx == 0:
                # 빈 줄로 호흡 1회
                if current_text_paras:
                    current_text_paras.append(blank_p())
                current_text_paras.append(big_red_p(para))
                current_text_paras.append(blank_p())
                current_text_paras.append(blank_p())
            else:
                current_text_paras.append(body_p(para))
                current_text_paras.append(blank_p())

            # 이미지 자리 체크
            if (section_label, idx) in IMAGE_MAP:
                # 현재까지의 text block flush
                blocks.append(text_block(current_text_paras))
                current_text_paras = []
                # 이미지 삽입
                fname = IMAGE_MAP[(section_label, idx)]
                blocks.append(img_block(IMG_REL + fname, alt=f'{section_label} 단락 {idx}'))
                # 이미지 다음 빈 줄 호흡
                current_text_paras.append(blank_p())

        # 섹션 마지막 text block flush
        if current_text_paras:
            blocks.append(text_block(current_text_paras))

        # 섹션 사이 빈 줄 + 구분선 X (네이버 스타일은 연속)
        blocks.append(text_block([blank_p(), blank_p()]))

    # CTA
    blocks.append(hr_block())
    blocks.append(text_block([blank_p()]))
    blocks.append(oglink_block())
    blocks.append(text_block([blank_p()]))

    return '\n\n'.join(blocks)


def copy_images():
    img_dir = os.path.join(POST_DIR, 'images')
    os.makedirs(img_dir, exist_ok=True)
    ok = 0
    missing = []
    for (_, _), fname in IMAGE_MAP.items():
        src = os.path.join(IMG_SRC_DIR, fname)
        dst = os.path.join(img_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            ok += 1
        else:
            missing.append(fname)
    print(f"🖼  이미지 복사: {ok}/{len(IMAGE_MAP)} → {img_dir}")
    for m in missing:
        print(f"  ⚠️ 누락: {m}")


# ===== Cascade 전용 가독성 override (네이버 모바일 원본 정확 매칭) =====
CASCADE_STYLE = """
<style>
/* line-height 1.0 / margin 0 — 네이버 column_wrinkle 패턴 매칭 */
.se-viewer .se-text-paragraph { line-height: 1.0 !important; margin: 0 !important; padding: 0 !important; }
.se-viewer .se-text-paragraph.se-blank { margin-top: 0 !important; padding: 0 !important; }
.se-viewer .se-text-paragraph span { line-height: 1.0 !important; }
/* 폰트 모바일 기본 */
.se-viewer .se-ff-system { font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "HelveticaNeue", "Helvetica Neue", helvetica, sans-serif !important; }
/* 좌측 정렬 */
.se-viewer .se-text-paragraph-align- { text-align: left; }
/* 컴포넌트 간격 — 네이버 원본 컴포넌트 마진 작게 */
.se-viewer .se-component { margin: 0 !important; padding: 0 !important; }
.se-viewer .se-component.se-text { margin: 0 !important; }
.se-viewer .se-component.se-image { margin: 14px 0 !important; }
.se-viewer .se-section { margin: 0 !important; padding: 0 !important; }
.se-viewer .se-module { margin: 0 !important; padding: 0 !important; }
/* 빈 단락 높이 — 19.8px (원본 line-height) */
.se-viewer .se-text-paragraph.se-blank { min-height: 19.8px; height: 19.8px; }
.se-viewer .se-text-paragraph.se-blank span { display: inline-block; height: 19.8px; line-height: 19.8px !important; }
</style>
"""

def inject_and_save(se_html, config_data):
    os.makedirs(POST_DIR, exist_ok=True)
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()
    # head에 cascade 전용 style 주입
    template = template.replace('</head>', CASCADE_STYLE + '</head>')
    start = '<!-- POST CONTENT START -->'
    end = '<!-- POST CONTENT END -->'
    si = template.index(start)
    ei = template.index(end)
    html = template[:si + len(start)] + '\n\n' + se_html + '\n\n' + template[ei:]
    with open(os.path.join(POST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(POST_DIR, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {SLUG}/index.html — {os.path.getsize(os.path.join(POST_DIR, 'index.html')):,} bytes")


config_data = {
    'blog': {
        'name': '서연ㅣ주사피부염 cascade 회복기',
        'title': '서연ㅣ주사피부염 cascade 회복기',
        'profile_image': '',
        'profile_color': '#f3d4d4',
    },
    'post': {
        'title': '주사피부염 5년 만성 — Cascade Reset으로 4달 만에 잡은 이야기',
        'category': '건강·뷰티',
        'date': '2026. 6. 28. 14:30',
    },
    'social': {'likes': 2143, 'shares': 187, 'views': 18420},
    'comments': [
        {'author': '주사피부염5년차', 'profile_color': '#f0d6e8', 'time': '2시간 전',
         'text': '저랑 너무 똑같아요.. 수란트라 발랐다 끊으면 또 도지고. 결국 평생 관리라는 말만 들었거든요. cascade 얘기 처음 들어요', 'likes': 89},
        {'author': '40대워킹맘', 'profile_color': '#d6e8f0', 'time': '4시간 전',
         'text': '저도 5년차예요.. 거울 보기 싫어서 화장 두껍게 발라도 오후되면 또 빨개지고. 읽다가 울컥했네요', 'likes': 67},
        {'author': '맨얼굴이소원', 'profile_color': '#e8f0d6', 'time': '7시간 전',
         'text': '항생제 이소티논 다 해봤는데 끊으면 더 시뻘게져서 무서워서 또 바르고.. cascade 환경 얘기 더 알고싶어요', 'likes': 54},
        {'author': '천만원날린사람', 'profile_color': '#f0e0d6', 'time': '11시간 전',
         'text': '카드 명세서 부분.. 저도 세다가 그만뒀어요. 5년 만성으로 헛돈 쓴 거 진짜 답답해요', 'likes': 48},
        {'author': '복직앞두고', 'profile_color': '#d6f0e0', 'time': '1일 전',
         'text': '곰팡이 비유 진짜 찰떡이네요. 죽이는 게 아니라 환경을 바꾼다 — 이제야 이해돼요', 'likes': 37},
        {'author': '아이엄마지수', 'profile_color': '#e0d6f0', 'time': '1일 전',
         'text': '사진에 늘 본인만 없다는 거.. 저도 그래서 댓글 남겨요. 지금은 화장 30분 만에 끝나신다니 제일 부럽습니다', 'likes': 31},
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
    print('🚀 티트리셀 Cascade Reset 빌드 시작\n')
    se_html = build()
    copy_images()
    inject_and_save(se_html, config_data)
    print('\n✅ 빌드 완료')
    print(f'  로컬 미리보기: open public/posts/{SLUG}/index.html')
