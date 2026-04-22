#!/usr/bin/env python3
"""질활성균 v1 어드버토리얼 빌드 — MD → 네이버 블로그 HTML 자동 변환"""

import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
POST_DIR = os.path.join(BASE, 'public', 'posts', 'jilhwalseonggyun-v1')
MD_PATH = os.path.join(os.path.dirname(BASE), '낫지않는질염', '03_ADVERTORIAL', 'advertorial_jilhwalseonggyun_v1.md')

# 이미지 매핑 — [이미지: 설명] → 실제 파일
IMG_BASE = '/posts/jilhwalseonggyun-v1/images/'
IMAGE_MAP = {
    '처방전 3장 겹쳐 쌓인 사진 — 안젤릭·리비알·페모스톤': '01_prescriptions.jpg',
    '유방외과 초음파 화면 or 샤워 후 거울 앞 흐릿한 실루엣': '02_breast_ultrasound.jpg',
    '체중계 숫자 + 정강이 누른 손자국 클로즈업': '03_weight_edema.jpg',
    '쌓인 영양제 박스 + 한약 팩 + 택배 상자들': '04_supplements_pile.jpg',
    '노트에 손글씨로 적은 7년 지출 계산 — "HRT 270만 / 영양제 180만 / 한약 200만 / 합계 650만"': '05_spending_note.jpg',
    '어두운 주차장 차 안에서 약통을 손에 쥔 클로즈업 — 흐릿한 창문 너머 불빛': '06_parking_lot_night.jpg',
    '간-장-질 호르몬 재활용 회로 인포그래픽 — 화살표로 순환 흐름': '07_hormone_recycle_diagram.jpg',
    '19종 다균주 성분표 + FOS 강조 인포그래픽': '08_19strains_fos.jpg',
    'HRT vs 이소플라본 vs 질활성균 3축 비교표 — 완제품 / 흉내 / 공장 복원': '09_comparison_3axis.jpg',
    '28일 달력 — 주차별 체크 표시': '10_28day_calendar.jpg',
    '딸 카톡 캡처 "엄마 요즘 목소리가 달라"': '11_daughter_kakao.jpg',
    'FarmBio 질활성균 패키지 + 정기구독 29,967원 + 28일 체감 보증 그래픽': '12_farmbio_package_cta.jpg',
}

CTA_URL = "https://soricare.com/product/detail.html?product_no=68&utm_source=meta&utm_medium=cpc&utm_campaign=adv_jilhwalseonggyun_v1"


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def p_tag(text, fs='fs15', bold=False, color=None):
    if not text.strip():
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-fs-fs15 se-ff-system"><br></span>\n'
                '      </p>')
    processed = esc(text)
    if bold:
        processed = f'<b>{processed}</b>'
    style = f' style="color:{color};"' if color else ''
    return (f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
            f'        <span{style} class="se-fs-{fs} se-ff-system">{processed}</span>\n'
            f'      </p>')


def p_tag_with_inline_bold(text, fs='fs15'):
    """Handle **bold** inline markers within a line. Bold parts get RED + fs19."""
    if not text.strip():
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-fs-fs15 se-ff-system"><br></span>\n'
                '      </p>')

    parts = re.split(r'\*\*(.+?)\*\*', text)
    spans = []
    for i, part in enumerate(parts):
        if not part:
            continue
        escaped = esc(part)
        if i % 2 == 1:  # bold part → RED + larger
            spans.append(f'<span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>{escaped}</b></span>')
        else:
            spans.append(f'<span class="se-fs-{fs} se-ff-system">{escaped}</span>')

    inner = ''.join(spans)
    return (f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
            f'        {inner}\n'
            f'      </p>')


def text_block(paras):
    return (f'<div class="se-component se-text se-l-default">\n'
            f'  <div class="se-section se-section-text se-l-default">\n'
            f'    <div class="se-module se-module-text">\n'
            f'{chr(10).join(paras)}\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</div>')


def img_block(src, alt=''):
    return (f'<div class="se-component se-image se-l-default">\n'
            f'  <div class="se-section se-section-image se-l-default">\n'
            f'    <div class="se-module se-module-image">\n'
            f'      <a class="se-module-image-link">\n'
            f'        <img src="{esc(src)}" alt="{esc(alt)}" class="se-image-resource">\n'
            f'      </a>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</div>')


def hr_block():
    return ('<div class="se-component se-horizontalLine se-l-default">\n'
            '  <div class="se-section se-section-horizontalLine se-l-default">\n'
            '    <div class="se-module se-module-horizontalLine">\n'
            '      <hr class="se-hr">\n'
            '    </div>\n'
            '  </div>\n'
            '</div>')


def oglink_block():
    return (f'<div class="se-component se-oglink se-l-default">\n'
            f'  <div class="se-section se-section-oglink">\n'
            f'    <div class="se-module se-module-oglink">\n'
            f'      <a href="{CTA_URL}" class="se-oglink-info __se_link" target="_blank" rel="noopener"'
            f' onclick="if(typeof fbq===\'function\'){{fbq(\'track\',\'Lead\');}}">\n'
            f'        <div class="se-og-title">FarmBio 질활성균 19종 다균주</div>\n'
            f'        <div class="se-og-description">L.plantarum · L.rhamnosus · B.lactis + FOS · 28일 체감 환불</div>\n'
            f'        <div class="se-og-site-name">soricare.com</div>\n'
            f'      </a>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</div>')


BR = p_tag('')

BREAK_AFTER = re.compile(
    r'(는데|은데|았는데|었는데|했는데|봤는데|갔는데'
    r'|으니까|니까|길래'
    r'|거든요?|더라고요?|잖아요?|더라'
    r'|어서|아서|여서'
    r'|했다|었다|였다|났다|왔다|갔다|봤다|됐다|않았다'
    r'|해요|돼요|써요|와요'
    r'|ㅋㅋ|하\.\.)'
    r' '
)


def split_long_line(line, max_chars=40):
    if len(line) <= max_chars:
        return [line]

    segments = []
    remaining = line

    while len(remaining) > max_chars:
        search_zone = remaining[:max_chars + 15]
        candidates = []
        for m in BREAK_AFTER.finditer(search_zone):
            pos = m.end()
            if pos >= 15:
                candidates.append(pos)

        if candidates:
            best = min(candidates, key=lambda p: abs(p - max_chars))
            segments.append(remaining[:best].rstrip())
            remaining = remaining[best:].lstrip()
        else:
            mid = len(remaining) // 2
            space_positions = [i for i, c in enumerate(remaining) if c == ' ' and i >= 15]
            if space_positions:
                best_sp = min(space_positions, key=lambda p: abs(p - mid))
                segments.append(remaining[:best_sp].rstrip())
                remaining = remaining[best_sp:].lstrip()
            else:
                break

    if remaining:
        if segments and len(remaining) < 10:
            segments[-1] = segments[-1] + ' ' + remaining
        else:
            segments.append(remaining)

    return segments


def parse_markdown(md_text):
    lines = md_text.split('\n')
    blocks = []
    current_paras = []
    text_line_count = 0
    consecutive_text = 0

    def flush_paras():
        nonlocal current_paras, text_line_count, consecutive_text
        if current_paras:
            blocks.append(text_block(current_paras))
            current_paras = []
            text_line_count = 0
            consecutive_text = 0

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith('# '):
            i += 1
            continue

        if line.strip() == '---':
            flush_paras()
            blocks.append(hr_block())
            i += 1
            continue

        img_match = re.match(r'\[이미지:\s*(.+?)\]', line)
        if img_match:
            flush_paras()
            desc = img_match.group(1).strip()
            if desc in IMAGE_MAP:
                src = IMAGE_MAP[desc]
                if not src.startswith('/'):
                    src = IMG_BASE + src
            else:
                src = IMG_BASE + 'placeholder.jpg'
            blocks.append(img_block(src, desc))
            # CTA block right after the final image (12th image)
            if desc.startswith('FarmBio 질활성균 패키지'):
                blocks.append(oglink_block())
            i += 1
            continue

        if line.strip() == '[CTA 링크]':
            flush_paras()
            blocks.append(oglink_block())
            i += 1
            continue

        if line.startswith('#') and not line.startswith('# '):
            flush_paras()
            current_paras.append(BR)
            current_paras.append(p_tag(line, fs='fs13', color='#00a832'))
            flush_paras()
            i += 1
            continue

        if not line.strip():
            current_paras.append(BR)
            consecutive_text = 0
            if text_line_count >= 4:
                current_paras.append(BR)
                flush_paras()
            i += 1
            continue

        bold_match = re.match(r'^\*\*(.+)\*\*$', line)
        if bold_match:
            current_paras.append(p_tag(bold_match.group(1), fs='fs19', bold=True, color='rgb(255, 0, 16)'))
            current_paras.append(BR)
            current_paras.append(BR)
            flush_paras()
            i += 1
            continue

        if '**' in line:
            current_paras.append(p_tag_with_inline_bold(line, fs='fs15'))
            current_paras.append(BR)
            current_paras.append(BR)
            flush_paras()
            i += 1
            continue

        if line.startswith('+++'):
            flush_paras()
            current_paras.append(BR)
            current_paras.append(BR)
            current_paras.append(BR)
            current_paras.append(p_tag(line, fs='fs19', bold=True, color='#333'))
            current_paras.append(BR)
            current_paras.append(BR)
            flush_paras()
            i += 1
            continue

        segments = split_long_line(line, max_chars=40)
        for seg in segments:
            current_paras.append(p_tag(seg))
            consecutive_text += 1
            text_line_count += 1
            if consecutive_text >= 2:
                current_paras.append(BR)
                consecutive_text = 0

        if text_line_count >= 8:
            current_paras.append(BR)
            flush_paras()

        i += 1

    flush_paras()
    return blocks


def build():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    config_path = os.path.join(POST_DIR, 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    blocks = parse_markdown(md_text)
    content_html = '\n\n'.join(blocks)

    html = template.replace(
        '<!-- POST CONTENT START -->\n<div class="se-component se-text se-l-default">\n'
        '  <div class="se-section se-section-text se-l-default">\n'
        '    <div class="se-module se-module-text">\n'
        '      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
        '        <span class="se-fs-fs15 se-ff-system">본문 내용을 여기에 작성하세요</span>\n'
        '      </p>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'
        '<!-- POST CONTENT END -->',
        f'<!-- POST CONTENT START -->\n{content_html}\n<!-- POST CONTENT END -->'
    )

    html = html.replace('data-bind="title">블로그 글', f'data-bind="title">{esc(config["post"]["title"])}')
    html = html.replace('data-bind="blog-title">블로그 이름', f'data-bind="blog-title">{esc(config["blog"]["title"])}')
    html = html.replace('data-bind="title">글 제목', f'data-bind="title">{esc(config["post"]["title"])}')
    html = html.replace('data-bind="category">카테고리', f'data-bind="category">{esc(config["post"]["category"])}')
    html = html.replace('<strong class="ell">작성자</strong>', f'<strong class="ell">{esc(config["blog"]["name"])}</strong>')
    html = html.replace('<p class="blog_date">날짜</p>', f'<p class="blog_date">{esc(config["post"]["date"])}</p>')
    html = html.replace('data-bind="likes">0', f'data-bind="likes">{config["social"]["likes"]}')
    html = html.replace('data-bind="shares">0', f'data-bind="shares">{config["social"]["shares"]}')

    comment_count = len(config.get('comments', []))
    html = html.replace('data-bind="comments-count">0', f'data-bind="comments-count">{comment_count}')

    if config['blog'].get('profile_color'):
        html = html.replace(
            '<span class="img"></span>',
            f'<span class="img" style="background-color:{config["blog"]["profile_color"]};"></span>'
        )

    out_path = os.path.join(POST_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✅ Built: {out_path}')
    print(f'   Lines: {len(html.splitlines())}')
    print(f'   Size: {len(html.encode("utf-8")) / 1024:.1f} KB')

    print('\n📷 이미지 상태:')
    for desc, path in IMAGE_MAP.items():
        full = os.path.join(POST_DIR, 'images', path)
        status = '✅ 있음' if os.path.exists(full) else '⚠️  필요'
        print(f'   {status} [{desc[:50]}...] → {path}')


if __name__ == '__main__':
    build()
