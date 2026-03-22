#!/usr/bin/env python3
"""펩타이드 크림 어드버토리얼 v2 → 네이버 블로그 클론 SE HTML 변환 후 index.html 주입"""

import re
import os
import json
import shutil

CTA_URL = "https://perfusync.com"  # TODO: 실제 상세페이지 URL로 교체

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def text_block(paragraphs, default_fs='fs15'):
    paras_html = []
    for p in paragraphs:
        text = p.get('text', '')
        bold = p.get('bold', False)
        fs = p.get('fontSize', default_fs)
        if not text.strip():
            paras_html.append(f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span class="se-fs-{fs} se-ff-system"><br></span>\n      </p>')
        else:
            inner = f'<b>{esc(text)}</b>' if bold else esc(text)
            paras_html.append(f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span class="se-fs-{fs} se-ff-system">{inner}</span>\n      </p>')
    return f'''<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
{chr(10).join(paras_html)}
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

def cta_block(text, url):
    return f'''<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><a href="{esc(url)}" target="_blank" rel="noopener" onclick="if(typeof fbq==='function'){{fbq('track','Lead');}}">{esc(text)}</a></span>
      </p>
    </div>
  </div>
</div>'''

def table_block(headers, rows):
    paras = []
    header_text = ' | '.join(headers)
    paras.append({'text': header_text, 'bold': True, 'fontSize': 'fs13'})
    paras.append({'text': '', 'fontSize': 'fs13'})
    for row in rows:
        row_text = ' | '.join(row)
        paras.append({'text': row_text, 'bold': False, 'fontSize': 'fs13'})
    return text_block(paras, 'fs13')

# ===== 본문 구성 =====
blocks = []

# ── 블록 A: 서론 ──

blocks.append(text_block([
    {'text': '45세 이후 피부 콜라겐은 1년에 6%씩 사라진다', 'bold': True, 'fontSize': 'fs19'},
    {'text': '일반 노화의 12배 속도다', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '지금 바르고 있는 크림으로는 이 속도를 못 따라잡는다', 'fontSize': 'fs15'},
    {'text': '크림의 문제가 아니다', 'fontSize': 'fs15'},
    {'text': '피부 세포가 그 크림에 반응할 수 없는 상태다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '왜 그런지, 그리고 어떻게 해야 하는지를 3년간 437만원을 쓰고 나서야 알았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이건 논문에서 읽은 남의 이야기가 아니다', 'fontSize': 'fs15'},
    {'text': '3년간 내 얼굴에서 일어난 일이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '돈 받고 쓰는 글이 아니다. 논문 읽고, 직접 발라보고, 비교한 기록이다.', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 A: 페르소나 ──

blocks.append(text_block([
    {'text': '나는 47세, 서울에서 마케팅 회사를 다니고 있다', 'fontSize': 'fs15'},
    {'text': '하루 10시간을 모니터 앞에서 보내고, 형광등 아래에서 김밥으로 점심을 때우고, 퇴근하면 아이 둘 숙제를 봐주다가 자정에 쓰러지는 게 일상이었다', 'fontSize': 'fs15'},
    {'text': '그런 일상이 3년째.', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '주름을 신경 쓸 여유가 없었다', 'fontSize': 'fs15'},
    {'text': '정확히 말하면, 신경 쓰지 않으려고 했던 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그런데 44세 겨울, 회의 중에 동료와 나란히 프레젠테이션 화면을 보고 있었는데', 'fontSize': 'fs15'},
    {'text': '유리벽에 내 옆모습이 비쳤다', 'fontSize': 'fs15'},
    {'text': '팔자주름이 그림자처럼 턱 아래까지 내려와 있었고, 입꼬리 옆으로 깊은 골이 파여 있더라', 'fontSize': 'fs15'},
    {'text': '에어컨 바람이 목덜미를 스치는데 갑자기 등이 서늘해졌다', 'fontSize': 'fs15'},
    {'text': "'저 사람이 나야?'", 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그날 이후로 아침이 달라졌다', 'fontSize': 'fs15'},
    {'text': '세안하고 거울 앞에 서면 베개 자국이 볼에 찍혀 있었다', 'fontSize': 'fs15'},
    {'text': '예전엔 세수하면 바로 사라지던 자국인데, 30분이 지나도 그대로였다', 'fontSize': 'fs15'},
    {'text': '손가락으로 볼을 눌러보면 피부가 천천히 돌아왔다', 'fontSize': 'fs15'},
    {'text': '예전의 그 탱탱한 반발력 — 사라져 있었구나', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '남편은 아무 말을 하지 않더라', 'fontSize': 'fs15'},
    {'text': '그게 더 무서운 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': "'보이는 거겠지, 나한테도 보이는데'", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '거울 앞에 설 때마다 가슴이 답답해지기 시작했다', 'fontSize': 'fs15'},
    {'text': '뭐라도 하지 않으면 이대로 더 나빠질 것 같았다', 'fontSize': 'fs15'},
    {'text': '크림을 바꿨다', 'fontSize': 'fs15'},
    {'text': '비싼 걸로, 더 비싼 걸로', 'fontSize': 'fs15'},
    {'text': '437만원.', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '돈이 아깝다기보다, 의심이 들었다', 'fontSize': 'fs15'},
    {'text': "'내가 지금 뭘 바르고 있는 건지 나 자신도 모르고 있었구나'", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그 의심이 방향을 바꿔놨다', 'fontSize': 'fs15'},
    {'text': '바르는 걸 멈추고, 읽기 시작했다', 'bold': True, 'fontSize': 'fs15'},
]))

# 테이블
blocks.append(table_block(
    ['시도', '비용', '기간', '결과'],
    [
        ['백화점 크림 3종', '89만원', '8개월', '촉촉해지지만 주름은 그대로'],
        ['올리브영 펩타이드 크림 4종', '23만원', '6개월', '비슷비슷'],
        ['레티놀 세럼 2종', '14만원', '4개월', '각질·홍조에 중단'],
        ['피부과 보톡스 2회', '110만원', '—', '3개월마다 원점'],
        ['리쥬란 1회', '55만원', '—', '한 달 반짝'],
        ['기타 앰플·마스크팩', '146만원', '3년', '기분 탓'],
        ['합계', '437만원', '3년', '팔자주름 깊이 변화 없음'],
    ]
))

blocks.append(hr_block())

# ── 블록 B: 고군분투 ──

blocks.append(text_block([
    {'text': '네이버에 \'주름크림 추천\'을 검색했다', 'fontSize': 'fs15'},
    {'text': '블로그마다 다른 말, 전부 협찬 글이었다', 'fontSize': 'fs15'},
    {'text': '뭘 믿어야 하는지 모르겠더라', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 제일 비싼 걸로 바꿨다', 'fontSize': 'fs15'},
    {'text': '백화점 1층 카운터에서 89만원짜리를 샀다', 'fontSize': 'fs15'},
    {'text': '하루 이틀은 촉촉한 것 같았다', 'fontSize': 'fs15'},
    {'text': '한 달이 지나도 주름은 그대로였다', 'fontSize': 'fs15'},
    {'text': '촉촉해지는 것과 주름이 줄어드는 건 다른 문제였구나', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그 다음은 레티놀이었다', 'fontSize': 'fs15'},
    {'text': '유튜브에서 피부과 전문의가 추천하길래 기대를 했다', 'fontSize': 'fs15'},
    {'text': '하루 이틀은 괜찮았다', 'fontSize': 'fs15'},
    {'text': '2주차에 볼이 벌겋게 달아올랐다', 'fontSize': 'fs15'},
    {'text': '각질이 일어나서 화장이 떠버렸다', 'fontSize': 'fs15'},
    {'text': '화가 나기 시작했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '보톡스도 맞아봤다', 'fontSize': 'fs15'},
    {'text': '확실히 달라지긴 하더라', 'fontSize': 'fs15'},
    {'text': '근데 3개월 지나니까 원점이었다', 'fontSize': 'fs15'},
    {'text': '또 맞고, 또 원점', 'fontSize': 'fs15'},
    {'text': '돈도 돈인데 끝이 안 보이는 게 더 힘들었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '정말 그냥 다 내려놓고 포기하고 싶었다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 B: 전환점 ──

blocks.append(text_block([
    {'text': '유튜브에서 피부과 전문의 영상을 보다가', 'fontSize': 'fs15'},
    {'text': '댓글에 누가 논문 링크를 달아놨는데', 'fontSize': 'fs15'},
    {'text': "거기서 처음으로 '에스트로겐 절벽'이라는 단어를 봤다", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '구글 번역기 돌려가며 읽었다', 'fontSize': 'fs15'},
    {'text': '처음엔 하나도 이해 못했다', 'fontSize': 'fs15'},
    {'text': '용어 하나 검색하면 또 모르는 용어가 나왔다', 'fontSize': 'fs15'},
    {'text': '그렇게 논문 47건을 읽었다', 'fontSize': 'fs15'},
    {'text': '국내 커뮤니티 후기 890개를 봤다', 'fontSize': 'fs15'},
    {'text': 'TOP 20 제품 성분표를 전수 비교했다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 B: 해결책 단서 (v5) ──

blocks.append(text_block([
    {'text': '그날 밤, 잠이 안 와서 또 논문을 읽고 있었는데', 'fontSize': 'fs15'},
    {'text': '한 문장에서 멈췄다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '내가 3년간 바른 크림은, 애초에 효과가 날 수 있는 구조가 아니었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '437만원이 왜 날아갔는지', 'fontSize': 'fs15'},
    {'text': '보톡스가 왜 3개월이면 원점이었는지', 'fontSize': 'fs15'},
    {'text': '비싼 크림이나 싼 크림이나 왜 결과가 똑같았는지', 'fontSize': 'fs15'},
    {'text': '그 논문 한 문장으로 전부 설명이 됐다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '45세 이후, 피부 안에서 3가지가 동시에 무너지고 있었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '일반 노화의 12배 속도로', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그리고 그 3가지 중 하나는, 솔직히 소름이 돋았다', 'fontSize': 'fs15'},
    {'text': '피부 세포가 늙은 게 아니었다', 'fontSize': 'fs15'},
    {'text': '세포는 살아 있는데, 신호를 못 받고 있었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '그러니까 아무리 좋은 재료를 발라도 세포가 반응을 안 하는 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '65개 브랜드를 전부 봤는데', 'fontSize': 'fs15'},
    {'text': '이걸 설명하는 곳이 한 곳도 없더라', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '아래에 내가 정리한 내용을 다 적어놨다', 'fontSize': 'fs15'},
    {'text': '이걸 읽고 나면 크림 고르는 기준이 완전히 바뀐다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 C: 메커니즘 교육 ──

blocks.append(text_block([
    {'text': '45세가 넘으면 에스트로겐이 급격히 줄어든다', 'fontSize': 'fs15'},
    {'text': '그러면 피부에서 세 가지가 동시에 일어난다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '첫째, 콜라겐을 만드는 명령이 끊긴다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '에스트로겐이 그 명령을 보내고 있었는데, 보내는 쪽이 멈춘 거다', 'fontSize': 'fs15'},
    {'text': '그래서 아침에 베개 자국이 안 펴지는 거다', 'fontSize': 'fs15'},
    {'text': '새 콜라겐이 만들어지지 않으니까 눌리면 눌린 채로 있는 거다', 'fontSize': 'fs15'},
    {'text': '이 속도면 5년 뒤에는 지금보다 30% 더 얇아진다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '둘째, 콜라겐을 부수는 효소가 폭주한다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '원래 에스트로겐이 잠재우고 있었는데, 잠금장치가 풀린 거다', 'fontSize': 'fs15'},
    {'text': '만드는 건 멈추고, 부수는 건 빨라지고', 'fontSize': 'fs15'},
    {'text': '그래서 작년보다 올해 주름이 깊어진 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '셋째, 이게 진짜 중요한데', 'bold': True, 'fontSize': 'fs15'},
    {'text': "피부 세포 자체가 '다시 만들어'라는 신호를 못 받는 상태가 된다", 'fontSize': 'fs15'},
    {'text': '세포가 죽은 게 아니다', 'fontSize': 'fs15'},
    {'text': '살아 있는데 귀가 먹은 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '그러니까 아무리 비싼 재료를 발라도 세포가 움직이지 않는 거다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 C: 왜 안 됐나 (역매칭) ──

blocks.append(text_block([
    {'text': '그렇다면 그때 바른 크림들은 왜 안 됐던 건가', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '백화점 크림(89만원)은 히알루론산과 콜라겐이 주성분이었다', 'fontSize': 'fs15'},
    {'text': '이건 피부 위에 보습막을 올려놓는 거다', 'fontSize': 'fs15'},
    {'text': '촉촉해진 건 보습막 덕분이고, 주름과는 관계없는 거다', 'fontSize': 'fs15'},
    {'text': '촉촉해지니까 효과 있다고 착각했던 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '레티놀은 세포 회전율을 높여주는 성분이다', 'fontSize': 'fs15'},
    {'text': '근데 신호가 끊긴 세포에게 회전율을 높여봤자', 'fontSize': 'fs15'},
    {'text': '콜라겐 합성으로 이어지지 않는다', 'fontSize': 'fs15'},
    {'text': '피부만 예민해지고 홍조가 올라온 건 그래서다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '보톡스는 근육을 일시적으로 마비시키는 거다', 'fontSize': 'fs15'},
    {'text': '표정근이 안 움직이니까 주름이 펴 보이는 건 맞는데', 'fontSize': 'fs15'},
    {'text': '진피층 콜라겐은 계속 줄어들고 있다', 'fontSize': 'fs15'},
    {'text': '3개월 뒤 원점인 이유가 이거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '겉은 매끈해 보이지만 안쪽은 계속 무너지고 있었던 거다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 C: 해결 방향 + 제품 공개 ──

blocks.append(text_block([
    {'text': '그러면 뭘 해야 하는가', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "재료를 가져다주는 게 아니라", 'fontSize': 'fs15'},
    {'text': "세포한테 '다시 만들어'라고 신호를 보내야 한다", 'fontSize': 'fs15'},
    {'text': '동시에 폭주하는 분해효소를 다시 잠재워야 한다', 'fontSize': 'fs15'},
    {'text': '무너진 장벽을 복원해서 좋은 성분이 안쪽까지 도달하게 해야 한다', 'fontSize': 'fs15'},
    {'text': '그리고 표정근을 완화해서 새 주름이 더 생기지 않게 보호해야 한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '만들기 + 지키기 + 전달하기 + 보호하기', 'bold': True, 'fontSize': 'fs15'},
    {'text': '이 4가지가 동시에 돼야 한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이걸 하는 성분이 펩타이드다', 'fontSize': 'fs15'},
    {'text': '펩타이드는 재료가 아니라 명령이다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '여기까지 읽고 나서 펩타이드 크림을 찾기 시작했다', 'fontSize': 'fs15'},
    {'text': '65개 브랜드의 성분표를 전부 비교했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '대부분은 펩타이드가 1-2종만 들어가 있었다', 'fontSize': 'fs15'},
    {'text': '신호를 보내는 건 되는데, 분해를 막거나 장벽을 복원하는 건 빠져 있었다', 'fontSize': 'fs15'},
    {'text': '4가지가 동시에 되는 제품은 극소수였다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "그중 하나가 '펩타이드 시그널 크림'이었다", 'bold': True, 'fontSize': 'fs15'},
    {'text': '8종 펩타이드가 4가지 역할을 동시에 한다', 'fontSize': 'fs15'},
    {'text': '식약처 이중기능성 인증(주름개선 + 미백)까지 받았다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 D: 후기 ──

blocks.append(text_block([
    {'text': '솔직히 또 기대했다가 실망할까봐 무서웠다', 'fontSize': 'fs15'},
    {'text': '437만원을 날린 뒤라 반신반의로 시작했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "첫 주에는 딱히 모르겠었다", 'fontSize': 'fs15'},
    {'text': "'이것도 그냥 그런 건가' 싶었다", 'fontSize': 'fs15'},
    {'text': '2주차까지도 확신이 없었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 3주차 아침, 세수하고 거울 앞에 섰는데', 'fontSize': 'fs15'},
    {'text': '베개 자국이 없었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '정확히 말하면, 예전처럼 세수하면 바로 사라져 있었다', 'fontSize': 'fs15'},
    {'text': '손가락으로 볼을 눌러봤다', 'fontSize': 'fs15'},
    {'text': '돌아오는 느낌이 달랐다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '아직 모르겠지만, 이건 확실히 달라진 것 같다', 'fontSize': 'fs15'},
    {'text': '그래서 계속 발랐다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '한 달째 되던 날, 남편이 뭐라고 했는지 아는가', 'fontSize': 'fs15'},
    {'text': '아무 말도 안 했다', 'fontSize': 'fs15'},
    {'text': '근데 내 얼굴을 쳐다보는 시간이 길어졌다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '그게 더 확실한 증거였다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 D: 동료 후기 ──

blocks.append(text_block([
    {'text': '동료한테 알려줬다', 'fontSize': 'fs15'},
    {'text': '50세, 나보다 상태가 심했다', 'fontSize': 'fs15'},
    {'text': '보톡스를 5번이나 맞았는데 계속 원점이라고 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'또 크림이야?' 하면서 반신반의로 시작했는데", 'fontSize': 'fs15'},
    {'text': '한 달 뒤에 카톡이 왔다', 'fontSize': 'fs15'},
    {'text': "'아침에 거울 보는 게 덜 무섭다'", 'bold': True, 'fontSize': 'fs15'},
    {'text': '그 한마디에 다 들어 있었다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 D: 대세감 ──

blocks.append(text_block([
    {'text': '그래서 다른 사람들은 어떤지 직접 찾아봤다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '리뷰 2,847개 — 내가 3년 동안 본 후기보다 많다', 'fontSize': 'fs15'},
    {'text': '3명 중 2명이 다시 산다는 건, 기분 탓이 아니라는 뜻이다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '런칭한 지 3개월인데 두 번이나 품절됐다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이미 이렇게 많은 사람이 쓰고 있었는데', 'fontSize': 'fs15'},
    {'text': '나만 아직 437만원을 헤매고 있었던 거다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# ── 블록 D: CTA ──

blocks.append(text_block([
    {'text': '이 글을 여기까지 읽었다면', 'fontSize': 'fs15'},
    {'text': '이미 크림을 고르는 기준이 바뀌어 있을 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '펩타이드 시그널 크림 — 8종 펩타이드 × 이중기능성 인증', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

# ===== HTML 주입 =====
body_html = '\n'.join(blocks)

# 템플릿 읽기
template_path = '/Users/juan/Brand Manager/naver-blog-clone/templates/post-template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# SE 본문 영역의 더미 콘텐츠를 교체
import re
output_html = re.sub(
    r'<!-- POST CONTENT START -->.*?<!-- POST CONTENT END -->',
    f'<!-- POST CONTENT START -->\n{body_html}\n<!-- POST CONTENT END -->',
    template,
    flags=re.DOTALL
)

# 포스트 디렉토리 생성
post_dir = '/Users/juan/Brand Manager/naver-blog-clone/public/posts/peptide-cream-v2'
os.makedirs(post_dir, exist_ok=True)

# index.html 저장
with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(output_html)

# config.json 생성
config = {
    "blog": {
        "name": "탄력연구소_수현",
        "title": "수현이의 스킨케어 노트",
        "profile_image": "",
        "profile_color": "#f8b4c8"
    },
    "post": {
        "title": "주름크림 15개, 시술 2회, 총 437만원을 쓰고 나서야 알게 된 것",
        "category": "뷰티·미용",
        "date": "2026. 3. 20. 09:15"
    },
    "social": {
        "likes": 1247,
        "shares": 634,
        "views": 34820
    },
    "comments": [
        {
            "author": "직장인소이",
            "profile_color": "#a8d8ea",
            "time": "2시간 전",
            "text": "44세인데 공감 미칠 것 같아요... 베개자국 안 펴지는 거 진짜ㅠ",
            "likes": 18
        },
        {
            "author": "뷰티초보맘",
            "profile_color": "#d8f8b4",
            "time": "5시간 전",
            "text": "437만원 쓴 거 보고 소름... 저도 비슷하게 쓴 것 같아요 크림만 10개 넘게 바꿨는데",
            "likes": 24
        },
        {
            "author": "갱년기스터디",
            "profile_color": "#f8d8b4",
            "time": "1일 전",
            "text": "에스트로겐 절벽 처음 알았어요 왜 아무데서도 안 알려주는 건지",
            "likes": 31
        },
        {
            "author": "미니멈스킨",
            "profile_color": "#d8b4f8",
            "time": "2일 전",
            "text": "펩타이드 시그널 크림 저도 쓰고 있어요! 3주차부터 확실히 달라지더라고요",
            "likes": 15
        },
        {
            "author": "코코아라떼",
            "profile_color": "#b4d8f8",
            "time": "3일 전",
            "text": "보톡스 3개월마다 원점인 이유가 이거였구나... 시술비 아깝다",
            "likes": 9
        }
    ],
    "tracking": {
        "meta_pixel_id": "1727184084578989",
        "ga_id": "",
        "scroll_events": [25, 50, 75, 100],
        "cta_event_name": "Lead"
    },
    "cta": {
        "url": CTA_URL,
        "text": "여기서 확인해보세요"
    }
}

with open(os.path.join(post_dir, 'config.json'), 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f'✅ HTML saved: {post_dir}/index.html')
print(f'✅ Config saved: {post_dir}/config.json')
print(f'🔗 Local: http://localhost:8080/posts/peptide-cream-v2/')

# ===== 자동 배포 =====
from _deploy import auto_deploy
auto_deploy("peptide-cream-v2", "펩타이드 크림 어드버토리얼 v2 업데이트")
