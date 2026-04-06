#!/usr/bin/env python3
"""SA 어드버토리얼 5개 — MD → SE HTML → post-template.html 주입"""

import os, re, json, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
POSTS_DIR = os.path.join(BASE, 'public', 'posts')

CTA_URL = "https://soricare.com/product/detail.html?product_no=64&utm_source=google&utm_medium=cpc&utm_campaign=sa_{slug}"
CTA_TEXT = "티트리셀 카밍 크림 자세히 보기"

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def p(text, bold=False, fs='fs15', color=None):
    """align은 항상 공백 (네이버 원본 CSS 호환)"""
    if not text.strip():
        return '      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system"><br></span>\n      </p>'
    inner = esc(text)
    if bold:
        inner = f'<b>{inner}</b>'
    style = f' style="color:{color};"' if color else ''
    return f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span{style} class="se-fs-{fs} se-ff-system">{inner}</span>\n      </p>'

def text_block(paragraphs):
    paras = '\n'.join(paragraphs)
    return f'''<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
{paras}
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

def oglink_block(slug):
    url = CTA_URL.format(slug=slug)
    return f'''<div class="se-component se-oglink se-l-default">
  <div class="se-section se-section-oglink">
    <div class="se-module se-module-oglink">
      <a href="{url}" class="se-oglink-info __se_link" target="_blank" rel="noopener" onclick="if(typeof fbq==='function'){{fbq('track','Lead');}}">
        <div class="se-og-title">티트리셀 카밍 크림 80ml</div>
        <div class="se-og-description">TTO 1.07% · 밤새 모공 안 환경 변경 · 바이옴 복원</div>
        <div class="se-og-site-name">soricare.com</div>
      </a>
    </div>
  </div>
</div>'''


# 강조 라인 키워드 — 이 패턴이 포함된 줄은 fs19로 표시
EMPHASIS_PATTERNS = [
    # 오프닝
    '검색하다가 여기까지',
    '저도 그랬어요',
    # 전환점 / 핵심 발견
    '알게 된 게',
    '알게 된 건데요',
    '밤에만 활동',
    '환경을 바꾸는 거',
    '환경을 만드는 거',
    '이해가 됐어요',
    '이해가 되는 거',
    '전환점이었어요',
    '모낭충이라는 걸',
    '모낭충이라는 거요',
    # 제품 특징
    '1.07%',
    '8시간 동안',
    '비누 30초 vs',
    # 결과
    '안 뜨거운 거예요',
    '확실히 덜했어요',
    '괜찮아진 거 아니야',
    # 감정
    '울었어요',
    '결국 끊었어요',
    # C4 특화
    '모낭염이 아니었어요',
    '모낭충이었던 거예요',
    # C5 특화
    '끊으면 돌아오는',
    '다시 돌아왔어요',
]

def should_emphasize(text):
    for pat in EMPHASIS_PATTERNS:
        if pat in text:
            return True
    return False

def md_to_se(md_text, slug):
    """마크다운 텍스트를 SE HTML 블록으로 변환"""
    lines = md_text.strip().split('\n')
    blocks = []
    current_paras = []

    for line in lines:
        stripped = line.strip()

        # 메타 헤더 스킵
        if stripped.startswith('#') or stripped.startswith('>') or stripped.startswith('---'):
            continue
        if stripped.startswith('## 본문') or stripped.startswith('## 메타'):
            continue

        # ㅣ (구분선)
        if stripped == 'ㅣ':
            if current_paras:
                blocks.append(text_block(current_paras))
                current_paras = []
            blocks.append(hr_block())
            continue

        # [상세페이지 링크] → OG link
        if '[상세페이지 링크]' in stripped:
            if current_paras:
                blocks.append(text_block(current_paras))
                current_paras = []
            blocks.append(oglink_block(slug))
            continue

        # 빈 줄
        if not stripped:
            current_paras.append(p(''))
            continue

        # "추가)" "수정)" 섹션 — 약간 작은 글씨, 회색
        if stripped.startswith('추가)') or stripped.startswith('수정)'):
            current_paras.append(p(stripped, bold=True, fs='fs13', color='#666'))
            continue

        # 강조 라인 → fs19
        if should_emphasize(stripped):
            current_paras.append(p(stripped, fs='fs19'))
            continue

        # 일반 텍스트
        current_paras.append(p(stripped))

    if current_paras:
        blocks.append(text_block(current_paras))

    return '\n\n'.join(blocks)

def build_post(slug, md_path, config_data):
    """포스트 디렉토리 생성 + index.html + config.json"""
    post_dir = os.path.join(POSTS_DIR, slug)
    os.makedirs(os.path.join(post_dir, 'images'), exist_ok=True)

    # MD 읽기
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # "## 본문" 이후만 추출
    if '## 본문' in md_text:
        md_text = md_text.split('## 본문', 1)[1]
        if '## 메타' in md_text:
            md_text = md_text.split('## 메타', 1)[0]

    # SE HTML 변환
    se_html = md_to_se(md_text, slug)

    # 템플릿 읽기
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    # 본문 주입
    html = template.replace(
        '<!-- POST CONTENT START -->\n<div class="se-component se-text se-l-default">\n  <div class="se-section se-section-text se-l-default">\n    <div class="se-module se-module-text">\n      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system">본문 내용을 여기에 작성하세요</span>\n      </p>\n    </div>\n  </div>\n</div>\n<!-- POST CONTENT END -->',
        f'<!-- POST CONTENT START -->\n{se_html}\n<!-- POST CONTENT END -->'
    )

    # 저장
    with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    with open(os.path.join(post_dir, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print(f"  ✅ {slug}/ — index.html + config.json")

# ===== 5개 포스트 설정 =====

MD_DIR = os.path.join(os.path.dirname(BASE), 'demodex-rosacea', '03_ADVERTORIAL')

posts = [
    {
        'slug': 'sa-demodex-direct',
        'md': os.path.join(MD_DIR, 'sa_c1_demodex_direct.md'),
        'config': {
            'blog': {'name': '피부고민 수진', 'title': '수진이의 피부 이야기', 'profile_image': '', 'profile_color': '#a8d8ea'},
            'post': {'title': '모낭충 3년째 달고 사는 사람이 알게 된 것', 'category': '건강·의학', 'date': '2026. 4. 5. 23:14'},
            'social': {'likes': 632, 'shares': 38, 'views': 4821},
            'comments': [
                {'author': '피부맘일기', 'profile_color': '#f0d6e8', 'time': '3시간 전', 'text': '저도 모낭충 비누 한 달 넘게 써봤는데 안 됐거든요.. 밤에만 활동한다는 거 처음 알았어요', 'likes': 23},
                {'author': '주사3년차극복중', 'profile_color': '#d6e8f0', 'time': '8시간 전', 'text': '수란트라 끊으면 돌아오는 이유가 이거였구나.. 환경이 안 바뀌니까', 'likes': 41},
                {'author': '올리브영탐험가', 'profile_color': '#e8f0d6', 'time': '1일 전', 'text': '에스트라 제로이드 닥터지 저도 다 써봤어요 ㅠㅠ 세면대에 크림만 쌓이는 거 완전 공감', 'likes': 35},
            ],
            'tracking': {'meta_pixel_id': '1727184084578989', 'ga_id': '', 'scroll_events': [25,50,75,100], 'cta_event_name': 'Lead'},
            'cta': {'url': CTA_URL.format(slug='c1_demodex'), 'text': '티트리셀 카밍 크림 자세히 보기'},
        }
    },
    {
        'slug': 'sa-soolantra-alt',
        'md': os.path.join(MD_DIR, 'sa_c5_soolantra_alternative.md'),
        'config': {
            'blog': {'name': '피부고민 수진', 'title': '수진이의 피부 이야기', 'profile_image': '', 'profile_color': '#a8d8ea'},
            'post': {'title': '수란트라 3개월 쓰고 끊었더니 다시 돌아온 사람', 'category': '건강·의학', 'date': '2026. 4. 3. 21:38'},
            'social': {'likes': 891, 'shares': 52, 'views': 7234},
            'comments': [
                {'author': '수란트라졸업반', 'profile_color': '#f0e0d6', 'time': '2시간 전', 'text': '저도 수란트라 3개월 쓰고 끊었는데 2주 만에 원래대로 돌아왔어요.. 진짜 멘탈 나감', 'likes': 56},
                {'author': '새벽검색러', 'profile_color': '#d6f0e0', 'time': '5시간 전', 'text': '죽이기가 아니라 환경을 바꾸는 거라는 말이 진짜 와닿네요', 'likes': 38},
                {'author': '직장인피부고민', 'profile_color': '#e0d6f0', 'time': '1일 전', 'text': '수란트라 뒤집어지면서 회사 못 간 거 저도요 ㅠㅠ 그 상태로 출근을 어떻게 해요', 'likes': 44},
            ],
            'tracking': {'meta_pixel_id': '1727184084578989', 'ga_id': '', 'scroll_events': [25,50,75,100], 'cta_event_name': 'Lead'},
            'cta': {'url': CTA_URL.format(slug='c5_soolantra'), 'text': '티트리셀 카밍 크림 자세히 보기'},
        }
    },
    {
        'slug': 'sa-rosacea',
        'md': os.path.join(MD_DIR, 'sa_c2_rosacea.md'),
        'config': {
            'blog': {'name': '피부고민 수진', 'title': '수진이의 피부 이야기', 'profile_image': '', 'profile_color': '#a8d8ea'},
            'post': {'title': '주사피부염 2년차가 치료 다 해보고 알게 된 것', 'category': '건강·의학', 'date': '2026. 4. 1. 22:51'},
            'social': {'likes': 1247, 'shares': 89, 'views': 12450},
            'comments': [
                {'author': '홍조탈출일기', 'profile_color': '#f0d6d6', 'time': '4시간 전', 'text': '스테로이드 수란트라 레이저 한의원 저도 순서 똑같아요.. 다 일시적이었어요', 'likes': 67},
                {'author': '모낭충알게됨', 'profile_color': '#d6d6f0', 'time': '7시간 전', 'text': '겉만 건드리고 모공 안은 안 건드린 거라는 말에 소름 돋았어요', 'likes': 53},
                {'author': '엄마가알로에발라', 'profile_color': '#f0f0d6', 'time': '2일 전', 'text': '엄마한테 한의원 가봐 듣고 간 거 저도요 ㅋㅋ 돈만 날림', 'likes': 42},
            ],
            'tracking': {'meta_pixel_id': '1727184084578989', 'ga_id': '', 'scroll_events': [25,50,75,100], 'cta_event_name': 'Lead'},
            'cta': {'url': CTA_URL.format(slug='c2_rosacea'), 'text': '티트리셀 카밍 크림 자세히 보기'},
        }
    },
    {
        'slug': 'sa-facial-redness',
        'md': os.path.join(MD_DIR, 'sa_c3_facial_redness.md'),
        'config': {
            'blog': {'name': '피부고민 수진', 'title': '수진이의 피부 이야기', 'profile_image': '', 'profile_color': '#a8d8ea'},
            'post': {'title': '얼굴 빨개지는 이유 2년째 찾다가 알게 된 것', 'category': '건강·의학', 'date': '2026. 3. 28. 20:15'},
            'social': {'likes': 758, 'shares': 41, 'views': 5832},
            'comments': [
                {'author': '장벽크림5개째', 'profile_color': '#d6f0f0', 'time': '6시간 전', 'text': '진정 크림 시카 크림 다 발라봤는데 아침에 똑같은 거 진짜 공감.. 겉에서만 바르는 거였구나', 'likes': 29},
                {'author': '안면홍조10년', 'profile_color': '#f0d6f0', 'time': '12시간 전', 'text': '모낭충이라는 거 처음 알았어요 혈관 문제인 줄만 알았는데', 'likes': 47},
                {'author': '마라탕2년째못먹음', 'profile_color': '#f0e8d6', 'time': '1일 전', 'text': '매운 거 못 먹는 거 너무 공감 ㅠㅠ 친구들이랑 밥 먹을 때 제일 서러워요', 'likes': 31},
            ],
            'tracking': {'meta_pixel_id': '1727184084578989', 'ga_id': '', 'scroll_events': [25,50,75,100], 'cta_event_name': 'Lead'},
            'cta': {'url': CTA_URL.format(slug='c3_redness'), 'text': '티트리셀 카밍 크림 자세히 보기'},
        }
    },
    {
        'slug': 'sa-folliculitis',
        'md': os.path.join(MD_DIR, 'sa_c4_folliculitis.md'),
        'config': {
            'blog': {'name': '피부고민 수진', 'title': '수진이의 피부 이야기', 'profile_image': '', 'profile_color': '#a8d8ea'},
            'post': {'title': '모낭염 연고 3개월 발라도 재발하는 진짜 이유', 'category': '건강·의학', 'date': '2026. 3. 25. 19:42'},
            'social': {'likes': 543, 'shares': 29, 'views': 3941},
            'comments': [
                {'author': '에스로반3통째', 'profile_color': '#e0f0d6', 'time': '4시간 전', 'text': '항생제 연고 바르면 가라앉는데 끊으면 또 올라오는 거 3개월째 반복 중이에요..', 'likes': 28},
                {'author': '모낭염인줄알았음', 'profile_color': '#d6e0f0', 'time': '9시간 전', 'text': '저도 모낭염인 줄 알았는데 모낭충이었어요.. 항생제가 소용없었던 이유가 이거였구나', 'likes': 39},
                {'author': '얼굴좁쌀파티', 'profile_color': '#f0d6e0', 'time': '1일 전', 'text': '아침마다 좁쌀 올라오는 거 진짜 미치겠어요 이게 모낭충 때문이었을 수도 있다니', 'likes': 22},
            ],
            'tracking': {'meta_pixel_id': '1727184084578989', 'ga_id': '', 'scroll_events': [25,50,75,100], 'cta_event_name': 'Lead'},
            'cta': {'url': CTA_URL.format(slug='c4_folliculitis'), 'text': '티트리셀 카밍 크림 자세히 보기'},
        }
    },
]

print("🚀 SA demodex 어드버토리얼 빌드 시작\n")
for post in posts:
    build_post(post['slug'], post['md'], post['config'])

print(f"\n✅ 완료 — {len(posts)}개 포스트 생성")
print("\nVercel 배포:")
print("  cd naver-blog-clone && vercel --prod")
print("\nURL 목록:")
for post in posts:
    print(f"  /{post['slug']}/")
