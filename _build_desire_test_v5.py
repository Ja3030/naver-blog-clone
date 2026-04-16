#!/usr/bin/env python3
"""Desire Test v5 어드버토리얼 빌드 — v5 마크다운 → 네이버 블로그 HTML 자동 변환"""

import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
POST_DIR = os.path.join(BASE, 'public', 'posts', 'desire-test-v5')
MD_PATH = os.path.join(os.path.dirname(BASE), 'demodex-rosacea', '05_COPY', 'advertorial_desire_test_v5.md')

# 이미지 매핑 — [이미지: 설명] → 실제 파일
# TODO: 유저가 이미지를 images/ 폴더에 넣은 후 여기 매핑
IMG_BASE = '/posts/desire-test-v5/images/'
DEMODEX_IMG = '/posts/demodex-rosacea/images/'
IMAGE_MAP = {
    'Before — 가장 심했을 때 볼 사진': 'before.jpg',
    'After — 마스크 없이 밖. 얼굴 안 나오게 옆모습': 'after_mask_off.jpg',
    '약 봉투': 'pill_bag.jpg',
    '수란트라 튜브': 'soolantra_tube.jpg',
    '세면대 위 크림 여러 개': DEMODEX_IMG + '1775151631403_image4.png',
    '마스크 여러 개 쌓여있는 서랍': 'masks_drawer.jpg',
    '크림 성분 비교 메모': 'ingredient_comparison.jpg',
    '크림 하나. 세면대 위에 하나만': DEMODEX_IMG + '1775154473754_hf_20260402_182401_d837551c-7bbd-45e3-bc4d-dd2216eacb01.png',
    '마스크 없이 밖. 자연광': 'outside_natural_light.jpg',
    '4개월째 근황': 'month4_update.jpg',
    '카페 7년차 글 캡처 일부': 'cafe_7year_post.jpg',
    '곰팡이 비유 도식 — 닦기만 vs 닦기+안생기게': 'mold_diagram.jpg',
    '첫 주~1개월 피부 변화 타임라인': 'skin_timeline.jpg',
    '카페 쪽지 대화 캡처': 'cafe_dm_screenshot.jpg',
}

CTA_URL = "https://soricare.com/product/detail.html?product_no=64&utm_source=meta&utm_medium=cpc&utm_campaign=desire_test_v5"


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def p_tag(text, fs='fs15', bold=False, color=None):
    if not text.strip():
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-fs-fs15 se-ff-system"><br></span>\n'
                '      </p>')
    # Handle inline **bold** markdown
    def replace_bold(m):
        return f'<b>{m.group(1)}</b>'
    processed = esc(text)
    # Re-apply bold after escaping (bold markers were stripped by esc)
    # Actually we need to handle bold BEFORE escaping
    pass  # handled in parse_line

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

    # Split by **..** and build spans
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
            f'        <div class="se-og-title">티트리셀 카밍 크림 80ml</div>\n'
            f'        <div class="se-og-description">TTO 1.07% · 밤새 잔류 · 매일 사용 가능</div>\n'
            f'        <div class="se-og-site-name">soricare.com</div>\n'
            f'      </a>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</div>')


BR = p_tag('')

# Korean natural break points for line splitting
BREAK_AFTER = re.compile(
    r'(는데|은데|았는데|었는데|했는데|봤는데|갔는데'  # ~는데/은데 connectors
    r'|으니까|니까|길래'                              # reason connectors
    r'|거든요?|더라고요?|잖아요?|더라'                # reported/reason
    r'|어서|아서|여서'                                # ~아서/어서 connectors
    r'|했다|었다|였다|났다|왔다|갔다|봤다|됐다|않았다' # past tense
    r'|해요|돼요|써요|와요'                           # polite endings
    r'|ㅋㅋ|하\.\.)'                                 # ㅋㅋ, 한숨
    r' '                                              # must be followed by space
)

def split_long_line(line, max_chars=40):
    """Split a long Korean line into shorter segments for mobile readability.
    Min segment: 15 chars. Max target: 40 chars."""
    if len(line) <= max_chars:
        return [line]

    segments = []
    remaining = line

    while len(remaining) > max_chars:
        # Find all possible break points in the search zone
        search_zone = remaining[:max_chars + 15]
        candidates = []
        for m in BREAK_AFTER.finditer(search_zone):
            pos = m.end()  # position right after the break pattern + space
            if pos >= 15:  # min 15 chars per segment
                candidates.append(pos)

        if candidates:
            # Pick the break point closest to max_chars (fill the line)
            best = min(candidates, key=lambda p: abs(p - max_chars))
            segments.append(remaining[:best].rstrip())
            remaining = remaining[best:].lstrip()
        else:
            # Fallback: split at last space near midpoint
            mid = len(remaining) // 2
            space_positions = [i for i, c in enumerate(remaining) if c == ' ' and i >= 15]
            if space_positions:
                best_sp = min(space_positions, key=lambda p: abs(p - mid))
                segments.append(remaining[:best_sp].rstrip())
                remaining = remaining[best_sp:].lstrip()
            else:
                break

    if remaining:
        # Don't create tiny fragments (< 10 chars)
        if segments and len(remaining) < 10:
            segments[-1] = segments[-1] + ' ' + remaining
        else:
            segments.append(remaining)

    return segments


def parse_markdown(md_text):
    """Parse v5 markdown into HTML blocks.
    Key: text_blocks are kept SMALL (3-7 lines) to match reference blog formatting.
    Flush triggers: blank lines, bold lines, images, hrs, max 6 text lines."""
    lines = md_text.split('\n')
    blocks = []
    current_paras = []
    text_line_count = 0  # count of actual text lines (not BR) in current block

    consecutive_text = 0  # consecutive text lines without BR

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

        # Skip title (# ...)
        if line.startswith('# '):
            i += 1
            continue

        # Horizontal rule
        if line.strip() == '---':
            flush_paras()
            blocks.append(hr_block())
            i += 1
            continue

        # Image marker
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
            i += 1
            continue

        # CTA link
        if line.strip() == '[CTA 링크]':
            flush_paras()
            blocks.append(oglink_block())
            i += 1
            continue

        # Hashtags
        if line.startswith('#') and not line.startswith('# '):
            flush_paras()
            current_paras.append(BR)
            current_paras.append(p_tag(line, fs='fs13', color='#00a832'))
            flush_paras()
            i += 1
            continue

        # Empty line → BR + reset consecutive counter
        if not line.strip():
            current_paras.append(BR)
            consecutive_text = 0  # reset: BR breaks consecutive run
            # Flush after every blank line if we have 4+ text lines
            if text_line_count >= 4:
                current_paras.append(BR)
                flush_paras()
            i += 1
            continue

        # Bold line (entire line is **bold**) → RED + fs19 + flush after
        bold_match = re.match(r'^\*\*(.+)\*\*$', line)
        if bold_match:
            current_paras.append(p_tag(bold_match.group(1), fs='fs19', bold=True, color='rgb(255, 0, 16)'))
            current_paras.append(BR)
            current_paras.append(BR)
            flush_paras()  # Always flush after bold/RED line (reference pattern)
            i += 1
            continue

        # Line with inline **bold** → bold parts get RED + fs19
        if '**' in line:
            current_paras.append(p_tag_with_inline_bold(line, fs='fs15'))
            current_paras.append(BR)
            current_paras.append(BR)
            flush_paras()  # Flush after inline bold too
            i += 1
            continue

        # +++ section header → large bold with generous spacing
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

        # Regular text — split long lines for mobile readability
        segments = split_long_line(line, max_chars=40)
        for seg in segments:
            current_paras.append(p_tag(seg))
            consecutive_text += 1
            text_line_count += 1

            # Reference pattern: BR after every 2 consecutive text lines
            if consecutive_text >= 2:
                current_paras.append(BR)
                consecutive_text = 0

        # Auto-flush if we hit 8 text lines (prevent huge blocks)
        if text_line_count >= 8:
            current_paras.append(BR)
            flush_paras()

        i += 1

    flush_paras()
    return blocks


def build():
    # Read markdown
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Read template
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    # Read config
    config_path = os.path.join(POST_DIR, 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Parse markdown to HTML blocks
    blocks = parse_markdown(md_text)
    content_html = '\n\n'.join(blocks)

    # Insert into template
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

    # Apply config bindings
    html = html.replace('data-bind="title">블로그 글', f'data-bind="title">{esc(config["post"]["title"])}')
    html = html.replace('data-bind="blog-title">블로그 이름', f'data-bind="blog-title">{esc(config["blog"]["title"])}')
    html = html.replace('data-bind="title">글 제목', f'data-bind="title">{esc(config["post"]["title"])}')
    html = html.replace('data-bind="category">카테고리', f'data-bind="category">{esc(config["post"]["category"])}')
    html = html.replace('<strong class="ell">작성자</strong>', f'<strong class="ell">{esc(config["blog"]["name"])}</strong>')
    html = html.replace('<p class="blog_date">날짜</p>', f'<p class="blog_date">{esc(config["post"]["date"])}</p>')
    html = html.replace('data-bind="likes">0', f'data-bind="likes">{config["social"]["likes"]}')
    html = html.replace('data-bind="shares">0', f'data-bind="shares">{config["social"]["shares"]}')

    # Comments count
    comment_count = len(config.get('comments', []))
    html = html.replace('data-bind="comments-count">0', f'data-bind="comments-count">{comment_count}')

    # Profile color
    if config['blog'].get('profile_color'):
        html = html.replace(
            '<span class="img"></span>',
            f'<span class="img" style="background-color:{config["blog"]["profile_color"]};"></span>'
        )

    # Write output
    out_path = os.path.join(POST_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✅ Built: {out_path}')
    print(f'   Lines: {len(html.splitlines())}')
    print(f'   Size: {len(html.encode("utf-8")) / 1024:.1f} KB')

    # Report missing images
    print('\n📷 이미지 상태:')
    for desc, path in IMAGE_MAP.items():
        if path.startswith('/posts/demodex-rosacea/'):
            full = os.path.join(BASE, 'public', path.lstrip('/'))
            status = '✅ 기존' if os.path.exists(full) else '❌ 없음'
        else:
            full = os.path.join(POST_DIR, 'images', path)
            status = '✅ 있음' if os.path.exists(full) else '⚠️  필요'
        print(f'   {status} [{desc}] → {path}')


if __name__ == '__main__':
    build()
