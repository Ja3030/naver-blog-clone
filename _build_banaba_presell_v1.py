# -*- coding: utf-8 -*-
"""혈당_바나바 프리셀 v1 → 네이버 블로그 모바일 UI 라이브 빌드 (2026-10-29)
원고 = 혈당_바나바/05_PRESELL/03_프리셀_본문_v1 · 겉모습 = uvola 06_LANDING 틀 (미리보기 build_preview.py와 동일 해석)
미리보기와 다른 점:
- 메타 픽셀·클래리티·읽기깊이 스크립트를 떼지 않고 실값으로 넣는다 (픽셀 = momsaju_new 1957044568277876, 스토어와 동일)
- [링크 카드 · 제품] = 진짜 상품 링크 카드 (surl/P/21 + utm)
- 못 채운 사진 자리(p06·p19)는 점선 상자 대신 아예 안 그린다 (HIDE_MISSING)
결과: public/posts/banaba-presell-v1/  →  python3 _deploy.py banaba-presell-v1
"""
import re, os, json, html, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
UV = '/Users/juan/Brand Manager/uvola/06_LANDING'
PRE = '/Users/juan/Brand Manager/혈당_바나바/05_PRESELL'
SRC = os.path.join(PRE, '03_프리셀_본문_v1_2026-10-27.md')
SLUG = 'banaba-presell-v1'
POST_DIR = os.path.join(BASE, 'public', 'posts', SLUG)

PIXEL_ID = '1957044568277876'   # momsaju_new — 스토어 픽셀과 동일 (유저 결정 2026-09-21)
PRODUCT_URL = 'https://momsaju.com/surl/P/21'
CTA_URL = PRODUCT_URL + '?utm_source=naver&utm_medium=blog&utm_campaign=banaba_presell_v1'
OG_TITLE = '뉴트리랩 바나바정 - NutriLab'
OG_DESC = '1일 1정 · 바나바잎 코로솔산 · 뒷면 성분표로 확인하세요'
OG_DOMAIN = 'momsaju.com'
LINKCARD_IMG = os.path.join(PRE, '..', '06_DETAIL_PAGE', '제품컷', 'BOTTLE_FRONT_REF.jpg')

raw = open(SRC, encoding='utf-8').read()
title = re.search(r'\*\*\[글 제목\]\*\* (.+)', raw).group(1).strip()
blog_name, blog_cat = re.search(r'\*\*\[블로그\]\*\* (.+?) · 분류 「(.+?)」', raw).groups()
a = raw.index('**[블로그]**'); a = raw.index('\n', a)
b = raw.index('\n---\n→ 관련')
L = raw[a:b].split('\n')

RED = 'color:#ff0010'
def fmt(line):
    big = '[크게]' in line; red = '[빨강]' in line
    t = line.replace('[크게]', '').replace('[빨강]', '').strip()
    t = re.sub(r'^\\([*+]+)', r'\1', t)
    css = []
    if red: css.append(RED)
    if big: css.append('font-size:min(24px,5.6vw)')
    if red or big: css.append('font-weight:700')
    e = html.escape(t)
    return f'<span style="{";".join(css)}">{e}</span>' if css else e

BL = '<p class="se-text-paragraph se-blank"><span class="se-ff-system"><br></span></p>'
def p(s): return f'<p class="se-text-paragraph uv-p">{s}</p>'
def text_comp(lines): return '<div class="se-component se-text"><div class="se-module se-module-text">' + ''.join(lines) + BL + '</div></div>\n'

IMGDIR = os.path.join(PRE, 'images', 'final'); USED = {}
def img_for(n):
    for ext in ('webp', 'jpg', 'png'):
        f = os.path.join(IMGDIR, f'p{n:02d}.{ext}')
        if os.path.exists(f): return f
def ph(line):
    """[사진 n · 설명] → images/final/pNN.* 있으면 이미지, 없으면 생략(라이브)"""
    m = re.match(r'\[사진 (\d+) · (.+)\]', line)
    n = int(m.group(1)) if m else 0
    f = img_for(n) if n else None
    if f:
        USED[n] = f
        return f'<div class="se-component se-image"><img class="bs-img" src="assets/img/{os.path.basename(f)}" alt=""></div>\n'
    return ''

CARD = ('<div class="se-component se-oglink"><div class="se-module se-module-oglink">'
        f'<a href="{CTA_URL}" class="se-oglink-card" target="_blank" rel="noopener" onclick="try{{fbq(\'track\',\'Lead\')}}catch(e){{}}">'
        '<div class="se-oglink-thumb" style="width:110px;min-height:110px;background:#f2f3f5 url(assets/img/linkcard.jpg) center/cover no-repeat"></div>'
        f'<div class="se-oglink-body"><div class="se-oglink-title">{html.escape(OG_TITLE)}</div>'
        f'<div class="se-oglink-desc">{html.escape(OG_DESC)}</div><div class="se-oglink-domain">{OG_DOMAIN}</div></div></a></div></div>\n')

body, buf, quote, check, comments = [], [], [], [], []
def flush():
    global buf
    if buf: body.append(text_comp(buf)); buf = []
def flush_quote():
    global quote
    if quote:
        body.append('<div class="se-component se-quotation uv-quote"><blockquote>' + '<br>'.join(html.escape(x) for x in quote) + '</blockquote></div>\n'); quote = []
def flush_check():
    global check
    if check:
        items = ''.join(f'<li>{html.escape(x)}</li>' for x in check)
        body.append(f'<div class="se-component bs-check"><ul>{items}</ul></div>\n'); check = []

in_cmt = False; refs = []
i = 0
while i < len(L):
    s = L[i].strip()
    if s.startswith('【인용】'):
        flush(); flush_check(); quote.append(s[4:].strip()); i += 1; continue
    flush_quote()
    if s.startswith('【체크】'):
        flush(); check.append(s[4:].strip()); i += 1; continue
    flush_check()
    if s.startswith('[참고문헌]'):
        flush(); refs = [x.strip()[2:] for x in L[i + 1:] if x.strip().startswith('- ')]; break
    if s == '[댓글]': flush(); in_cmt = True; i += 1; continue
    if in_cmt and s.startswith('>'):
        m = re.match(r'>\s*(└\s*)?\*\*(.+?)\*\*:\s*(.+)', s)
        if m: comments.append({'reply': bool(m.group(1)), 'author': m.group(2), 'text': m.group(3)})
        i += 1; continue
    in_cmt = False
    if s.startswith('【소제목】'):
        flush(); body.append(f'<div class="se-component bs-head"><h4>{html.escape(s[5:].strip())}</h4></div>\n')
    elif s.startswith('(인용구 아래 출처 칸)'):
        flush(); body.append(f'<div class="bs-cite">{html.escape(s.split(")", 1)[1].strip())}</div>\n')
    elif s == '———': flush(); body.append('<div class="se-component se-horizontalLine"><hr class="se-hr"></div>\n')
    elif s.startswith('[사진'):
        flush(); body.append(ph(s))
    elif s.startswith('[링크 카드'): flush(); body.append(CARD)
    elif s.startswith('[해당 링크는'): flush(); body.append(f'<p class="se-text-paragraph uv-p" style="color:#888;font-weight:400">{html.escape(s)}</p>\n')
    elif s == '' or s == '---': flush()
    else: buf.append(p(fmt(s)))
    i += 1
flush(); flush_quote(); flush_check()

cmt_html = '<div class="se-component bs-cmts"><div class="bs-cmts-h">댓글 ' + str(len(comments)) + '</div>' + ''.join(
    f'<div class="bs-c{" bs-reply" if c["reply"] else ""}"><b>{html.escape(c["author"])}</b><span>{html.escape(c["text"])}</span><em>방금 전 · 답글</em></div>' for c in comments) + '</div>\n'
joined = ''.join(body)
k = joined.rfind('<div class="se-component se-oglink">')
joined = joined[:k] + cmt_html + joined[k:]
ref_html = '<div class="bs-refs"><b>[참고문헌]</b><ol>' + ''.join(f'<li>{html.escape(r)}</li>' for r in refs) + '</ol></div>\n'
content = joined + ref_html

EXTRA_CSS = """<style>
.se-viewer .uv-p{font-weight:400 !important}
.bs-head h4{margin:34px 8px 6px;padding:14px 8px 12px;text-align:center;font-size:min(21px,5vw);font-weight:700;line-height:1.5;color:#111;border-bottom:3px solid #111}
.bs-cite{text-align:center;color:#777;font-size:min(15px,3.8vw);margin:0 0 22px}
.bs-check ul{list-style:none;margin:22px 10px;padding:16px 14px;background:#f4f6f8;border-left:5px solid #ff0010;border-radius:4px}
.bs-check li{margin:8px 0;font-size:min(16px,4vw);line-height:1.6;font-weight:700;text-align:left}
.bs-check li:before{content:'✔ ';color:#ff0010}
.bs-cmts{margin:30px 6px;padding:14px;border:1px solid #e3e5e8;border-radius:8px;text-align:left}
.bs-cmts-h{font-weight:700;font-size:15px;margin-bottom:10px}
.bs-c{padding:10px 0;border-top:1px solid #f0f1f3;font-size:14px;line-height:1.55}
.bs-c b{display:block;font-size:13px;color:#333;margin-bottom:2px}
.bs-c em{display:block;font-style:normal;color:#999;font-size:12px;margin-top:3px}
.bs-reply{margin-left:22px;background:#fafbfc;padding-left:10px}
.bs-refs{margin:26px 8px 10px;color:#777;font-size:12px;line-height:1.6;text-align:left}
.bs-refs ol{padding-left:18px;margin:6px 0}
.bs-img{display:block;width:100%;height:auto;margin:8px 0}
.se-oglink-card{display:flex;text-decoration:none;color:inherit;border:1px solid #e3e5e8;border-radius:8px;overflow:hidden;margin:12px 0}
.se-oglink-body{padding:12px;flex:1}
.se-oglink-title{font-weight:700;font-size:15px;line-height:1.4;color:#111}
.se-oglink-desc{font-size:13px;color:#666;margin-top:4px;line-height:1.4}
.se-oglink-domain{font-size:12px;color:#999;margin-top:6px}
</style>"""

tpl = open(os.path.join(UV, 'template.html'), encoding='utf-8').read()
page = (tpl.replace('__CONTENT__', content).replace('__PIXEL__', PIXEL_ID)
        .replace('__FL__', '당 관리 일기').replace('__TC__', 'BS1')
        .replace('</head>', EXTRA_CSS + '\n</head>'))

conf = {'blog': {'name': blog_name, 'title': blog_name, 'profile_image': '', 'profile_color': '#c9d2cc'},
        'post': {'title': title, 'category': blog_cat, 'date': '2026. 10. 20. 23:41'},
        'social': {'likes': 1647, 'shares': 288, 'views': 18930}, 'comments': [],
        'tracking': {'meta_pixel_id': PIXEL_ID, 'scroll_events': [], 'cta_event_name': 'Lead'}}

if os.path.exists(POST_DIR): shutil.rmtree(POST_DIR)
os.makedirs(POST_DIR)
shutil.copytree(os.path.join(UV, '_assets_src'), os.path.join(POST_DIR, 'assets'))
os.makedirs(os.path.join(POST_DIR, 'assets', 'img'), exist_ok=True)
for f in USED.values(): shutil.copy(f, os.path.join(POST_DIR, 'assets', 'img'))
shutil.copy(LINKCARD_IMG, os.path.join(POST_DIR, 'assets', 'img', 'linkcard.jpg'))
open(os.path.join(POST_DIR, 'index.html'), 'w', encoding='utf-8').write(page)
json.dump(conf, open(os.path.join(POST_DIR, 'config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print(f'built · 이미지 {sorted(USED)} · 생략된 사진 자리 {[n for n in range(1,30) if n not in USED]} · 댓글 {len(comments)}')
print(POST_DIR)
