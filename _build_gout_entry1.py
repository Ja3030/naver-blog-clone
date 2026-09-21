"""통풍 입구 1 「약 먹는데도 아프다」 v42 → 네이버 블로그 모바일 UI HTML
- 본문: 통풍/05_ADVERTORIAL/_draft/입구1_통합원고_v43_CTA확정_2026-09-21.md  (줄 = 문단, 빈 줄 = 간격, `> 📷 S##` = 이미지)
- 이미지: 통풍/05_ADVERTORIAL/_images/final/S##.jpg|gif  (GIF 우선 슬롯 = S04·S06·S56·S42·S49)
- 미확보 슬롯: HIDE_MISSING=True면 안 그림(운영) / False면 점선 플레이스홀더(검수)
- 픽셀: momsaju_new 1957044568277876 (스토어와 동일 · 2026-09-21 확정). 템플릿의 편도 픽셀을 이 값으로 교체

시각 위계 (2026-09-20 유저 피드백: 「스크롤 슥슥 내리다 눈에 걸릴 딱 한 문장이 단락마다 있어야 한다」)
- XL : 섹션 전환 큰 글씨 (22px 굵게)             — 「따로구나」·첫째/둘째/셋째·정리
- H  : 단락의 각인 문장 (노란 형광 + 굵게 + 19px)   — 단락당 1개, 앞부분(스크롤 구간)은 촘촘히
- B  : 보조 강조 (굵게)
- R  : 숫자·핵심 단어 빨강 (한 줄에 여러 개 허용)
- Q  : 혼잣말 한 줄 단락 → 인용구 블록 (크게, 가운데)
- 단락 간격 = 빈 줄 2개 (뭉침 해소)
"""
import os, re, json, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
SRC = '/Users/juan/Brand Manager/통풍/05_ADVERTORIAL/_draft/입구1_통합원고_v43_CTA확정_2026-09-21.md'
FINAL = '/Users/juan/Brand Manager/통풍/05_ADVERTORIAL/_images/final'
SLUG = 'gout-entry1'
POST_DIR = os.path.join(BASE, 'public', 'posts', SLUG)
IMG_REL = f'/posts/{SLUG}/images/'

# ── 스토어·픽셀 미정 (유저 확정 후 채움) ──
HIDE_MISSING = True      # 운영 배포용: 못 채운 사진 자리는 점선 박스 대신 '아예 안 그림'
                         # (False면 점선 플레이스홀더 — 내부 검수용)
PIXEL_ID = '1957044568277876'   # momsaju_new — 스토어(momsaju.com)가 쏘는 픽셀과 동일하게 맞춤
                               # (유저 결정 2026-09-21 「무조건 스토어 픽셀로」). 통풍 전용 579247025222647은 미사용
PRODUCT_URL = 'https://www.momsaju.com/product/%EB%89%B4%ED%8A%B8%EB%A6%AC%EB%9E%A9-%ED%83%80%ED%8A%B8%EA%B2%90-%EC%8A%A4%ED%8B%B1/19/category/43/display/1/'   # 뉴트리랩 타트겐 스틱 product_no=19 (2026-09-21 등록 확인)
CTA_URL = PRODUCT_URL + '?utm_source=naver&utm_medium=blog&utm_campaign=gout_entry1'
OG_TITLE = '뉴트리랩 타트겐 스틱 - NutriLab'                          # 2026-09-20 제품명 확정
OG_DESC = '타트체리농축액 93.2% · 콜라겐 · 뒷면 성분표로 확인하세요'
OG_DOMAIN = 'momsaju.com'

GIF_SLOTS = {'S04', 'S06', 'S56', 'S42', 'S49'}   # GIF 판이 있으면 GIF 사용
STANZA_GAP = 2                                    # 단락 사이 빈 줄 수
SENTENCE_GAP = 2                                  # 단락 안 문장 사이 빈 줄 수 (유저: 「문장 끝나면 엔터 두 번」)

# 문장 끝 판정 — 줄 끝이 이 패턴이면 문장 종료 (연결어미 데/서/고/면/니/래/까·게 는 제외)
_FINAL_RE = re.compile(r'(요|죠|다|냐|야|어|구나|\?|!|\.\.|…|\.)$')
# 다음 줄이 이걸로 시작하면 앞 문장에 붙은 것 (「아 발작 또 오려나? / 싶어서…」)
_CONT_START = ('싶', '이런', '이러', '이렇게', '하고', '하는', '그런', '라고', '라는', '이래', '이라')

def is_sentence_end(line, nxt):
    if nxt is None: return False
    if not _FINAL_RE.search(line.strip()): return False
    if nxt.strip().startswith(_CONT_START): return False
    if line.strip().endswith('?') and nxt.strip().endswith('?'): return False   # 연속 질문은 한 덩어리
    return True

# ===== 시각 위계 =====
XL_LINES = [
    "아, 검사지에 나오는 요산 수치랑", "관절에 껴 있는 요산 결정은 따로구나",
    "세 단계로 가요",
    "첫째, 더 쌓이지 않게 막기",
    "두 번째는", "이미 쌓인 결정들을 녹이는 거예요",
    "셋째, 긁힌 관절 챙기기",
    "마지막으로 정리해 볼게요",
    "마지막으로 딱 결론만 정리할게요",
]
H_LINES = [
    # PART 0
    "퉁퉁 부어 있는 거예요", "페브릭 하루도 안 빼먹었는데?", "발작이 오히려 더 자주 왔어요",
    "25년 뒤엔 나도 저렇게 되나 싶어서", "제대로 설명해주는 곳이 없어요", "바꾼 게 딱 하나 있었어요",
    "발작이 한 번도 없었어요", "발이 멀쩡해요", "그냥 넘기지 마세요",
    # PART 1
    "누가 망치로 막 내려찍는 것 같아서", "한 발짝을 못 떼겠는 거예요", "저는 술을 일절 안 먹거든요",
    "그냥 진료가 끝났어요", "진짜 괴상하게 옆으로 툭 튀어나와 있고", "나 이제 다시 자유구나",
    "두달에 막 세네 번씩", "발이 보라색처럼 퉁퉁 부은 거예요", "발가락을 잘라버리고 싶었어요",
    "그럴 수 있다고 하더라고요", "1년이 지나도 똑같은 거예요", "발작이 계속 와요", "화가 나더라고요",
    "발가락에 칼이 박히는 것 같은 거예요", "아예 한숨도 못 잤어요", "하루 종일 통풍 신경을 써야 된다는 거예요",
    "하.. 앞으로 평생 이렇게 살아야 되나?",
    # PART 2~3
    "발작이 또 오더라고요", "통풍약을 25년이나 드셨는데도요", "발은 왜 여전할까요?", "통풍약은 대체 뭘 하는 거지?",
    "허옇게 껴 있는 게", "따로 녹여야 한대요", "3년 만에 처음 알았어요",
    # PART 4
    "딱딱하게 굳은 요산이었던 거죠", "엔진 안에 눌어붙어 있는 찌꺼기는", "관절에 결정이 껴 있다고 보면 된대요",
    "통풍이 완치되는 게 아니었던 거죠", "따로 없애줘야 되는 거였어요", "오일만 열심히 갈아준 거예요",
    "시간 말고는 방법이 없다는 거예요", "발이 또 시뻘겋게 부어 있는 거예요", "눈물이 날 뻔했어요",
    # PART 5
    "왜 제 발은 그대로일까?", "그래서 페브릭은 끊으면 안 되고", "발작 가능성이 75%까지 낮아졌다는 거죠",
    "약이 아닌 타트체리로 대체하는 거예요", "제가 뭘 잘못 먹었는지 보이더라고요", "농축액으로 30ml, 60ml씩 먹인 거였어요",
    "0.5g도 안 되는 거예요", "하.. 나 진짜 뭐 한 거지?", "나중엔 뼈까지 파먹는대요", "저도 아버지처럼 되는 거죠",
    "수치는 낮아도 발작은 계속 오죠", "93.2%가 몽모랑시 타트체리 농축액이에요",
    # PART 6
    "솔직히 큰 기대는 안 했어요", "거의 두 달 정도 됐는데도 잠잠했어요", "그 뒤로는 발작이 한 번도 안 왔어요",
    "작년 11월이더라고요", "이 정도는 진짜 감개무량하죠", "관절에 쌓인 결정은 그대로예요",
    "의사 선생님도 챙겨주지 않아요", "딱 한 번만 물어보세요",
    # PART 7 CTA
    "댓글이랑 쪽지가 감당이 안 됩니다", "영양제 파는 사람이 아닙니다", 
    "뭐가 다른지 알 수가 없어요", "저는 석달치를 한 번에 사놓습니다",
]
B_LINES = [
    "발가락이 또 시뻘겋게", "끊으라는 말은 아니에요", "하나도 안 빼고 다 적었거든요",
    "3시간동안 달달 떨면서 버티는데", "이것만 먹으면 그래도 안 아프겠지", "오히려 4점대로 떨어지고 나서부터",
    "쌓여 있던 요산이 녹으면서", "낫느라고 아픈 거구나 하고요", "하, 내가 이렇게까지 일해야 되나?",
    "아 발작 또 오려나?", "진짜 숨이 턱 막히더라고요", "의미가 없는 것 같았어요", "네가 뭘 찾겠냐",
    "통풍약은 요산이 새로 쌓이는 걸 막아주는데", "손이 다 떨리더라고요",
    "요산 수치만 내려가면 괜찮다고 했거든요", "발에 있는 요산 결정 때문이었던 거죠", "따로 엔진 플러싱을 해줘야 되는 거고요",
    "이미 쌓인 요산 결정은 타트체리", "처음부터 다시 파보기로 했어요", "맨 아래 정리만 보셔도 돼요",
    "이건 페브릭이 하는 일이에요", "제가 3년 동안 놓치고 있었던 거죠", "그거면 된 거 아니냐?",
    "영양제가 무슨.. 다 돈낭비 아니야?", "품종은 어디에도 안 적혀 있고요", "여기서 필요한 게 콜라겐이에요",
    "콜라겐까지 같이 먹어줘야", "세 가지만 따져봤어요",
    "3일 만에 싹 빠지고", "고기 냄새만 맡아도 불안했거든요", "그때의 저에게 쓰는 글인 셈이죠",
    "그거 어디 거냐", "그리고 얼마나 먹어야 되냐", "제 돈 주고 삽니다", 
    "캡슐로 된 건 다 뺐습니다", "이 세 가지만 보고 고르세요", "제품 문의는 이제 그만 주세요",
]
R_PHRASES = [
    "두달에 세 번씩", "두달에 세 번", "두달에 막 세네 번씩", "4점대", "5점대", "7.9", "25년째", "25년", "3년째", "3년 동안",
    "네달", "633명", "53%", "75%", "63명", "30ml, 60ml", "0.5g", "93.2%", "10만 원", "1년", "1월 9일", "작년 11월",
    "2주씩", "3일 만에", "3주만", "보름치", "석달치", "몽모랑시", "타트체리", "콜라겐", "콜킨", "페브릭",
]
Q_STANZA_FIRST = [   # 이 줄로 시작하는 단락 = 인용구 블록
    "발 괜찮나?", "어? 진짜 뭐 삐었나?", "아 또야?", "대체 언제까지 요산이 녹고 있는 건데?",
    "어? 저게 뭐지?", "아 씨.. 이거 진짜 왜 이러는 거야", "마지막 발작이 언제였지?", "어? 뭐야 완전 말짱하네",
]

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def _n(x): return x.strip().strip('“”"\' ')
_XL = {_n(x) for x in XL_LINES}
_H = {_n(x) for x in H_LINES}
_B = {_n(x) for x in B_LINES}
_Q = {_n(x) for x in Q_STANZA_FIRST}
_RED = sorted(R_PHRASES, key=len, reverse=True)

def p_blank():
    return '      <p class="se-text-paragraph se-blank se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system"><br></span>\n      </p>'

def red_phrases(inner):
    """빨강 구절 — 긴 것부터, 이미 처리된 자리는 건너뜀"""
    out = inner
    for ph in _RED:
        e = esc(ph)
        if e in out and ('>' + e + '<') not in out:
            out = out.replace(e, '<span style="color:#ff0010;font-weight:700;">' + e + '</span>')
    return out

def styled_paragraph(s):
    n = _n(s)
    if s.startswith('(') and s.endswith(')'):
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-ff-system" style="color:#8a9098;font-size:15px;">' + esc(s) + '</span>\n      </p>')
    if n in _XL:
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-ff-system" style="font-size:22px;font-weight:800;line-height:1.5;">' + red_phrases(esc(s)) + '</span>\n      </p>')
    inner = red_phrases(esc(s))
    if n in _H:
        return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
                '        <span class="se-ff-system" style="font-size:19px;line-height:1.9;"><span style="background-color:#fff8b2;font-weight:700;">' + inner + '</span></span>\n      </p>')
    if n in _B:
        inner = '<b>' + inner + '</b>'
    return ('      <p class="se-text-paragraph se-text-paragraph-align- ">\n'
            '        <span class="se-ff-system" style="font-size:18px;line-height:1.9;">' + inner + '</span>\n      </p>')

def text_block(paras):
    return ('<div class="se-component se-text se-l-default">\n  <div class="se-section se-section-text se-l-default">\n'
            '    <div class="se-module se-module-text">\n' + '\n'.join(paras) + '\n    </div>\n  </div>\n</div>')

def quote_block(lines):
    inner = '\n'.join(
        '      <p class="se-text-paragraph se-text-paragraph-align-center">\n'
        '        <span class="se-ff-system" style="font-size:21px;font-weight:700;line-height:1.7;">' + esc(l) + '</span>\n      </p>'
        for l in lines)
    return ('<div class="se-component se-quotation se-l-quotation_line">\n'
            '  <div class="se-section se-section-quotation se-l-quotation_line">\n'
            '    <blockquote class="se-quotation-container" style="border-left:3px solid #222;padding:8px 0 8px 18px;margin:30px 0;">\n'
            '      <div class="se-module se-module-text se-quote">\n' + inner + '\n      </div>\n'
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
            '      <div style="font-size:11px;color:#b8bdc2;margin-top:8px;">이미지 자리 · 확보 후 교체</div>\n'
            '    </div>\n  </div>\n</div>')

def hr_block():
    return ('<div class="se-component se-horizontalLine se-l-default">\n  <div class="se-section se-section-horizontalLine se-l-default">\n'
            '    <div class="se-module se-module-horizontalLine">\n      <hr class="se-hr">\n    </div>\n  </div>\n</div>')

LINK_IMG = []

def link_text_block():
    """네이버 링크 카드 — og 썸네일(실물 상자 사진) + 제목 + 설명 + 도메인"""
    fn = 'og1.jpg'
    # ⛔ box_front.jpg 금지 — 참앤들 로고·제품명·중국산·HACCP가 다 읽힌다(은닉 위반)
    src = '/Users/juan/Brand Manager/통풍/05_ADVERTORIAL/_images/_references/product/og_link_card.jpg'
    thumb = ''
    if os.path.exists(src):
        LINK_IMG.append((fn, src)); thumb = f'        <img src="{IMG_REL}{fn}" alt="" class="se-oglink-thumb">\n'
    return ('<div class="se-component se-oglink se-l-default">\n'
            '  <div class="se-section se-section-oglink">\n'
            '    <div class="se-module se-module-oglink">\n'
            f'      <a href="{CTA_URL}" class="se-oglink-card __se_link" target="_blank" rel="noopener" '
            "onclick=\"if(typeof fbq==='function'){fbq('track','Lead');}\">\n" + thumb +
            '        <div class="se-oglink-body">\n'
            f'          <div class="se-oglink-title">{esc(OG_TITLE)}</div>\n'
            f'          <div class="se-oglink-desc">{esc(OG_DESC)}</div>\n'
            f'          <div class="se-oglink-domain">{esc(OG_DOMAIN)}</div>\n'
            '        </div>\n      </a>\n    </div>\n  </div>\n</div>')

def slot_file(slot):
    """S## → (파일명, 원본경로) · GIF 우선 슬롯은 gif, 그 외 jpg"""
    if slot in GIF_SLOTS and os.path.exists(f'{FINAL}/{slot}.gif'):
        return (slot.lower() + '.gif', f'{FINAL}/{slot}.gif')
    if os.path.exists(f'{FINAL}/{slot}.jpg'):
        return (slot.lower() + '.jpg', f'{FINAL}/{slot}.jpg')
    return None

def build():
    lines = open(SRC, encoding='utf-8').read().split('\n')
    blocks, paras = [], []
    used_img, missing = [], []
    title = ''
    stanza = []          # 현재 단락의 줄들 (인용구 판정용)
    def flush_paras():
        nonlocal paras
        if paras:
            blocks.append(text_block(paras)); paras = []
    def end_stanza():
        """단락 종료: 인용구면 별도 블록, 아니면 문단 + 간격"""
        nonlocal stanza, paras
        if not stanza: return
        if _n(stanza[0]) in _Q:
            flush_paras(); blocks.append(quote_block(stanza))
        else:
            for i, l in enumerate(stanza):
                paras.append(styled_paragraph(l))
                nxt = stanza[i + 1] if i + 1 < len(stanza) else None
                if is_sentence_end(l, nxt):
                    paras.extend(p_blank() for _ in range(SENTENCE_GAP))
            paras.extend(p_blank() for _ in range(STANZA_GAP))
        stanza = []
    for raw in lines:
        st = raw.rstrip().strip()
        if st.startswith('# ') or st.startswith('## '):
            continue
        if st.startswith('>') and not re.match(r'^>\s*📷\s*S\d{2}\b', st):
            continue   # 문서 메타 블록쿼트(표기 설명 등)는 본문 아님
        m = re.match(r'^\*\*제목\*\*:\s*(.+)$', st)
        if m:
            title = m.group(1).strip(); continue
        m = re.match(r'^>\s*📷\s*(S\d{2})\b(.*)$', st)
        if m:
            end_stanza(); flush_paras()
            slot, desc = m.group(1), m.group(2).strip()
            f = slot_file(slot)
            if f:
                used_img.append(f); blocks.append(img_block(IMG_REL + f[0], slot))
            else:
                missing.append(f'{slot} {desc[:40]}')
                if not HIDE_MISSING:
                    blocks.append(placeholder_block(f'{slot} · {desc[:38]}'))
            continue
        if st == '---':
            end_stanza(); flush_paras(); blocks.append(hr_block()); continue
        if st == '[제품 링크]':
            end_stanza(); flush_paras(); blocks.append(link_text_block()); continue
        if st == '':
            end_stanza(); continue
        stanza.append(st)
    end_stanza(); flush_paras()
    blocks.append(hr_block()); blocks.append(text_block([p_blank()]))
    print(f'🖼  이미지 {len(used_img)}장 · 플레이스홀더 {len(missing)}개')
    for lb in missing: print(f'   · {lb}')
    return '\n\n'.join(blocks), used_img + LINK_IMG, title

def audit(html):
    """강조 목록 중 본문에서 못 찾은 줄 보고 (오타·원고 변경 감지)"""
    body = open(SRC, encoding='utf-8').read()
    miss = [l for l in XL_LINES + H_LINES + B_LINES + Q_STANZA_FIRST if l not in body]
    if miss:
        print(f'⚠️  원고에 없는 강조 줄 {len(miss)}개:'); [print('   ·', m) for m in miss]
    n_h = html.count('background-color:#fff8b2'); n_xl = html.count('font-size:22px'); n_q = html.count('se-quotation-container'); n_r = html.count('color:#ff0010')
    print(f'🎨  형광 {n_h} · 큰글씨 {n_xl} · 인용구 {n_q} · 빨강 {n_r}')

def copy_images(used):
    d = os.path.join(POST_DIR, 'images'); os.makedirs(d, exist_ok=True)
    for fn, src in used: shutil.copy2(src, os.path.join(d, fn))

def secret_comments(n=127, seed=7):
    """댓글 전부 비밀 댓글 (흰머리 v7 규칙) · 남성 통풍 독자 느낌 닉네임"""
    import random
    rnd = random.Random(seed)
    ko_a = ['통풍', '요산', '페브릭', '새벽', '발가락', '트럭', '화물', '지게차', '야간', '퇴근', '출근', '아빠', '삼십대', '사십대', '오십대', '부산', '인천', '대구', '광주', '울산', '천안', '평택', '고기', '맥주', '치킨', '족발', '곱창', '삼겹', '막창', '야식', '운전', '기사', '현장', '공장', '배달', '택배', '주말', '월요일', '금요일', '새벽배송']
    ko_b = ['아빠', '남편', '형', '삼촌', '기사', '맨', '러', '씨', '님', '이', '군', '생각', '일기', '기록', '로그', '집', '방', '고민', '탈출', '3년차', '5년차', '10년차', '초보', '환자', '동지']
    en = ['jhkim', 'minsu', 'sungho', 'dw', 'jw', 'hs', 'ks', 'ys', 'truck', 'driver', 'gout', 'uric', 'daddy', 'papa', 'bro', 'mr', 'lee', 'park', 'choi', 'jung', 'kang', 'yoon', 'han', 'oh', 'shin']
    names, out = set(), []
    while len(out) < n:
        r = rnd.random()
        if r < 0.55: nm = rnd.choice(ko_a) + rnd.choice(ko_b) + (str(rnd.randint(1, 99)) if rnd.random() < 0.35 else '')
        elif r < 0.8: nm = rnd.choice(en) + rnd.choice(['', '_', '.']) + str(rnd.choice([rnd.randint(1, 99), rnd.randint(1975, 1992), rnd.randint(100, 9999)]))
        else: nm = rnd.choice(ko_a) + str(rnd.randint(75, 92)) + rnd.choice(['', '년생', 's'])
        if nm in names: continue
        names.add(nm); out.append(nm)
    times = []
    for i in range(n):
        if i < 3: times.append(rnd.choice(['방금 전', '1분 전', '3분 전']))
        elif i < 12: times.append(f'{rnd.randint(5, 58)}분 전')
        elif i < 30: times.append(f'{rnd.randint(1, 23)}시간 전')
        elif i < 100: times.append(f'{rnd.randint(1, 5)}일 전')
        else: times.append(f'{rnd.randint(6, 14)}일 전')
    def key(s):
        if s == '방금 전': return 0
        v = int(s.split()[0].rstrip('분시간일')) if s[0].isdigit() else 0
        u = s.split()[0]
        return v * (1 if '분' in u else 60 if '시간' in u else 1440)
    times.sort(key=key)
    lock = ('<span style="color:#888;display:inline-flex;align-items:center;gap:4px">'
            '<svg width="13" height="13" viewBox="0 0 14 14" fill="none"><rect x="2.5" y="6" width="9" height="6.5" rx="1.2" stroke="#999" stroke-width="1.2"/>'
            '<path d="M4.5 6V4.2a2.5 2.5 0 015 0V6" stroke="#999" stroke-width="1.2"/></svg>비밀 댓글입니다.</span>')
    return [{'author': out[i], 'time': times[i], 'text': lock, 'likes': (rnd.randint(1, 3) if rnd.random() < 0.08 else 0)} for i in range(n)]

def make_config(title):
    return {
        'blog': {'name': '페브릭3년차', 'title': '통풍 3년차 트럭 기사의 기록',
                 'profile_image': '', 'profile_color': '#b9c4cf'},
        'post': {'title': title, 'category': '건강', 'date': '2026. 7. 14. 22:38'},
        'social': {'likes': 1873, 'shares': 142, 'views': 16410},
        'comments': secret_comments(127),
        'tracking': {'meta_pixel_id': PIXEL_ID, 'ga_id': '',
                     'scroll_events': [25, 50, 75, 100], 'cta_event_name': 'Lead'},
        'cta': {'url': CTA_URL, 'text': '성분표 확인하기'},
    }

def save(se_html, title):
    os.makedirs(os.path.join(POST_DIR, 'images'), exist_ok=True)
    t = open(TEMPLATE, encoding='utf-8').read()
    if PIXEL_ID:
        t = t.replace('1727184084578989', PIXEL_ID)   # 공용 템플릿 = 편도 픽셀 하드코딩 → 이 포스트만 교체
    else:
        t = re.sub(r'<!-- Meta Pixel Code -->.*?<!-- End Meta Pixel Code -->', '<!-- Meta Pixel: 통풍 픽셀 미정 (PIXEL_ID 채우면 삽입) -->', t, flags=re.S)
    a, b = '<!-- POST CONTENT START -->', '<!-- POST CONTENT END -->'
    si, ei = t.index(a), t.index(b)
    html = t[:si + len(a)] + '\n\n' + se_html + '\n\n' + t[ei:]
    open(os.path.join(POST_DIR, 'index.html'), 'w', encoding='utf-8').write(html)
    json.dump(make_config(title), open(os.path.join(POST_DIR, 'config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print('🚀 통풍 입구1 빌드\n')
    se, used, title = build()
    copy_images(used)
    save(se, title)
    audit(se)
    print(f'\n✅ public/posts/{SLUG}/index.html · 제목: {title}')
