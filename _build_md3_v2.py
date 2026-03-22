#!/usr/bin/env python3
"""MD3 v2 어드버토리얼 → SE HTML 변환 후 index.html 주입
페르소나: 32세 카페 자영업자 (자영업자_현우)
포스트 제목: 가글에 5년간 237만원 쓴 사람의 고백
"""

import re, json

CTA_URL = "https://soricare.com/product/sns-%EB%B9%84%EB%B0%80%EB%A7%81%ED%81%AC-%ED%8E%B8%EB%8F%84%EC%9E%A5%EB%B2%BD%EC%A0%9C-1%EC%9C%84/53/category/1/display/3/?icid=MAIN.product_listmain_2"

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

def image_block(src, alt=''):
    return f'''<div class="se-component se-image se-l-default">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a class="se-module-image-link">
        <img src="{esc(src)}" alt="{esc(alt)}" class="se-image-resource">
      </a>
    </div>
  </div>
</div>'''

# ===== MD3 v2 본문 구성 =====
blocks = []

# 참고논문
blocks.append(text_block([
    {'text': '<참고논문>', 'bold': True, 'fontSize': 'fs13'},
    {'text': '- Bezerra TF et al. "The Role of Tonsils in Halitosis." Braz J Otorhinolaryngol. 2013', 'fontSize': 'fs11'},
    {'text': '- Krespi YP et al. "The Relationship Between Oral Malodor and Volatile Sulfur Compound–Producing Bacteria." Otolaryngology. 2006', 'fontSize': 'fs11'},
    {'text': '- Stoodley P et al. "Biofilms as Complex Differentiated Communities." Annu Rev Microbiol. 2002', 'fontSize': 'fs11'},
    {'text': '- Miyake Y et al. "Inhibitory Effect of Propolis on Biofilm Formation." J Pharmacol Sci. 2021', 'fontSize': 'fs11'},
    {'text': '- Pruitt KM, Reiter B. "Biochemistry of Peroxidase System." Peroxidases in Chemistry and Biology. 1991', 'fontSize': 'fs11'},
]))

# 안티협찬 선언
blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '※주의※ 이 글은 가글에 5년간 237만원을 쓴 사람이 쓴 글이다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '리스테린, 가그린, 닥터세닥, 프로폴리스 가글까지 전부 써봤다', 'fontSize': 'fs15'},
    {'text': '제품 협찬은 받지 않았고 협찬 요청 업체는 댓글로 공개한다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 목차
blocks.append(text_block([
    {'text': '(목차)', 'bold': True, 'fontSize': 'fs15'},
    {'text': '1. 가글 정기배송 해지한 날', 'fontSize': 'fs15'},
    {'text': '2. 5년간 237만원의 명세서', 'fontSize': 'fs15'},
    {'text': '3. 가글이 편도 홈에 단 한 방울도 안 닿는 이유', 'fontSize': 'fs15'},
    {'text': '4. 알코올 가글의 배신 — 쓸수록 세균이 늘었다', 'fontSize': 'fs15'},
    {'text': '5. 재발의 진짜 원인은 세균막이었다', 'fontSize': 'fs15'},
    {'text': '6. 빼는 게 아니라 안 생기게 하는 것', 'fontSize': 'fs15'},
    {'text': '7. 편도장벽제 TOP 8 — 내가 세운 기준과 비교 결과', 'fontSize': 'fs15'},
    {'text': '8. 지금 시작해야 하는 이유', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 훅 섹션
blocks.append(text_block([
    {'text': '"가글에 5년간 237만원을 부었다', 'bold': True, 'fontSize': 'fs17'},
    {'text': '편도결석은 2주마다 정확히 돌아왔다"', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글이 편도에 닿지도 않는다는 걸', 'bold': True, 'fontSize': 'fs15'},
    {'text': '237만원 쓰고 나서야 알았다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(image_block('images/1773827354704_Group241.png', '편도결석 비포/애프터'))

blocks.append(hr_block())

# 1. 가글 정기배송 해지한 날
blocks.append(text_block([
    {'text': '1. 가글 정기배송 해지한 날', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 32살이고 가게를 운영한다', 'fontSize': 'fs15'},
    {'text': '카페 겸 디저트 가게라 손님이랑 가까이서 얘기할 일이 많다', 'fontSize': 'fs15'},
    {'text': '메뉴 추천도 하고 포장도 직접 하고', 'fontSize': 'fs15'},
    {'text': '하루에 40-50명은 마주 보고 말한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그런 사람한테 편도결석이 생겼다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '처음 나온 건 27살 때다', 'fontSize': 'fs15'},
    {'text': '가게 문 닫고 정리하는데 기침을 하다가', 'fontSize': 'fs15'},
    {'text': '목에서 뭔가 튀어나왔다', 'fontSize': 'fs15'},
    {'text': '노란색에 쌀알만한 알갱이', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '뭔지 몰라서 손가락으로 으깼다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그 순간 올라온 냄새', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이걸 아는 사람은 지금 이 글을 왜 클릭했는지', 'fontSize': 'fs15'},
    {'text': '설명이 필요 없다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 내 목 안에서 나왔다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(image_block('images/1773827499118_image30.png', '편도결석 실물'))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그 다음날부터 가게에서 달라진 게 있다', 'fontSize': 'fs15'},
    {'text': '손님한테 메뉴 설명할 때 자연스럽게 고개가 돌아갔다', 'fontSize': 'fs15'},
    {'text': '포장 건넬 때 입을 다물었다', 'fontSize': 'fs15'},
    {'text': '단골이 카운터 너머로 가까이 오면 한 발 뒤로 빠졌다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'혹시 냄새 나는 거 아닐까'", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '하루에 40번씩 이 생각을 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '네이버에 "편도결석 냄새" 치면', 'fontSize': 'fs15'},
    {'text': '나오는 글이란 글은 다 읽었다', 'fontSize': 'fs15'},
    {'text': '댓글마다 같은 말이었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"가글 해도 그 순간만 개운하고', 'fontSize': 'fs15'},
    {'text': '금방 다시 텁텁해져"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래도 안 하는 것보단 낫겠지 싶어서', 'fontSize': 'fs15'},
    {'text': '리스테린을 샀다', 'fontSize': 'fs15'},
]))

blocks.append(image_block('images/1773827460547_Group201.png', '시중 가글 제품들'))

blocks.append(text_block([
    {'text': '6개월 쓰고 가그린으로 바꿨다', 'fontSize': 'fs15'},
    {'text': '3개월 쓰고 닥터세닥으로 바꿨다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "바꿀 때마다 '이번엔 다르겠지' 했다", 'fontSize': 'fs15'},
    {'text': '2주 뒤면 똑같았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나중에 프로폴리스가 항균에 좋다는 글을 봤다', 'fontSize': 'fs15'},
    {'text': '프로폴리스 가글로 갈아탔다', 'fontSize': 'fs15'},
    {'text': '매달 3만 9천원 정기배송', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이건 좀 다를 줄 알았다', 'fontSize': 'fs15'},
    {'text': '14개월을 썼다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"2주만에 다시 생기네요"', 'fontSize': 'fs15'},
    {'text': '"이거 또 생겼어요... 목에 이물감 빡치네요"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '커뮤니티에 올라오는 글이 전부 내 얘기였다', 'fontSize': 'fs15'},
    {'text': '가글 이름만 다르고 결과는 다 똑같았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '14개월째 되던 날', 'fontSize': 'fs15'},
    {'text': '또 나왔다', 'fontSize': 'fs15'},
    {'text': '목 안쪽에서 그 익숙한 이물감', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '리스테린 6개월', 'fontSize': 'fs15'},
    {'text': '가그린 3개월', 'fontSize': 'fs15'},
    {'text': '닥터세닥 2개월', 'fontSize': 'fs15'},
    {'text': '프로폴리스 가글 14개월', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글 이름만 바뀌었지 결과는 한 번도 안 바뀌었다', 'fontSize': 'fs15'},
    {'text': '2주마다 돌아오는 게 정확히 똑같았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "이쯤 되니까 드는 생각이 있었다", 'fontSize': 'fs15'},
    {'text': "'가글이 문제가 아니라 가글로는 안 되는 건 아닌가'", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그날 정기배송을 끊고', 'fontSize': 'fs15'},
    {'text': '네이버에 검색을 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "근데 이번엔 '편도결석 가글 추천'이 아니었다", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'편도결석 자꾸 생김'", 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '왜 재발하는지를', 'fontSize': 'fs15'},
    {'text': '5년 동안 한 번도 검색해본 적이 없었다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 2. 5년간 237만원의 명세서
blocks.append(text_block([
    {'text': '2. 5년간 237만원의 명세서', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '질문을 바꾸고 나서 제일 먼저 한 건', 'fontSize': 'fs15'},
    {'text': '5년간 가글에 쓴 돈을 계산해본 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
]))

blocks.append(text_block([
    {'text': '항목 | 기간 | 금액', 'bold': True, 'fontSize': 'fs13'},
    {'text': '리스테린 대용량 3통 | 6개월 | 4만 5천원', 'fontSize': 'fs13'},
    {'text': '가그린 2통 | 3개월 | 2만원', 'fontSize': 'fs13'},
    {'text': '닥터세닥 1통 | 2개월 | 1만 8천원', 'fontSize': 'fs13'},
    {'text': '프로폴리스 가글 정기배송 | 14개월 | 54만 6천원', 'fontSize': 'fs13'},
    {'text': '워터픽 2대 (1대 고장) | — | 18만원', 'fontSize': 'fs13'},
    {'text': '이비인후과 12회 | 5년간 | 36만원', 'fontSize': 'fs13'},
    {'text': '구강세정 용품 기타 | 5년간 | 약 120만원', 'fontSize': 'fs13'},
    {'text': '합계 | 5년 | 약 237만원', 'bold': True, 'fontSize': 'fs13'},
]))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '237만원이었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 돈을 쓰는 동안', 'fontSize': 'fs15'},
    {'text': '편도결석은 2주 간격으로 한 번도 빠지지 않고 돌아왔다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"몇달째 가글이나 다른 방법들은', 'fontSize': 'fs15'},
    {'text': '도움이 안됐어요"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 사람도 나랑 같은 돈을 태우고 있었을 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '237만원이 아까운 게 아니다', 'fontSize': 'fs15'},
    {'text': '그 돈을 쓰면서도 한 번도 의심 안 한 5년이 아깝다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'가글을 하면 나아지겠지'", 'fontSize': 'fs15'},
    {'text': '이 한마디를 의심 없이 믿은 5년이었다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 3. 가글이 편도 홈에 단 한 방울도 안 닿는 이유
blocks.append(text_block([
    {'text': '3. 가글이 편도 홈에 단 한 방울도 안 닿는 이유', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'편도결석 자꾸 생김'으로 시작해서", 'fontSize': 'fs15'},
    {'text': '관련 글을 닥치는 대로 읽었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '블로그, 카페, 지식인, 유튜브 댓글', 'fontSize': 'fs15'},
    {'text': '읽으면 읽을수록 이상한 게 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글 쓰는 사람은 엄청 많은데', 'fontSize': 'fs15'},
    {'text': '가글로 재발이 멈췄다는 사람은 거의 없었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'나만 안 되는 건가' 싶었는데 아니었다", 'fontSize': 'fs15'},
    {'text': '다 안 되고 있었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그러다 이비인후과 의사가 올린 영상 하나를 봤다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도에는 홈이 있다', 'fontSize': 'fs15'},
]))

blocks.append(image_block('images/1773826204689_4.png', '편도 홈 구조'))

blocks.append(text_block([
    {'text': '2-3mm 깊이의 주름진 틈새다', 'fontSize': 'fs15'},
    {'text': '편도결석은 이 홈 안쪽에서 만들어진다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글은 입 안을 헹구는 거다', 'fontSize': 'fs15'},
    {'text': '이 홈 안쪽까지 들어가는 게 아니다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그 의사가 이렇게 말했다', 'fontSize': 'fs15'},
    {'text': '"가글은 구강 세정이지 편도 세정이 아닙니다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에는 물리적으로 닿지 않습니다"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 말을 듣는데 머리가 멍해졌다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "가글 광고에 '구강 세균 99.9% 제거'라고 써 있다", 'fontSize': 'fs15'},
    {'text': '맞다', 'fontSize': 'fs15'},
    {'text': '근데 그건 잇몸이나 혀 위에 있는 세균 얘기다', 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에 있는 세균은 해당이 안 된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세탁기를 떠올려보면 이해가 빠르다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세탁기 고무 패킹 안쪽에 낀 곰팡이', 'bold': True, 'fontSize': 'fs15'},
    {'text': '빨래를 돌린다고 곰팡이가 없어지나', 'fontSize': 'fs15'},
    {'text': '아무리 세제를 많이 넣어도', 'fontSize': 'fs15'},
    {'text': '물이 닿지 않는 틈새의 곰팡이는 그대로다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글이 그거다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(image_block('images/1773827434434_20220324162852735_WN6KGARM.png', '배수구 비유 — 직분사'))

blocks.append(text_block([
    {'text': '입 안을 아무리 헹궈도', 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에는 한 방울도 안 닿는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '커뮤니티에서 이런 후기를 본 적이 있다', 'fontSize': 'fs15'},
    {'text': '"입이 더 마르고 텁텁해짐', 'fontSize': 'fs15'},
    {'text': '가글 이런거 다 필요없다"', 'fontSize': 'fs15'},
    {'text': "그때는 '이 사람은 좀 극단적이네' 하고 넘겼다", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 아니었다', 'fontSize': 'fs15'},
    {'text': '가글이 나쁜 게 아니라', 'fontSize': 'fs15'},
    {'text': '편도까지 닿을 수 있는 형태가 아닌 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5년간 세탁기 돌리면서', 'fontSize': 'fs15'},
    {'text': '고무 패킹 곰팡이가 없어지길 기다린 꼴이었다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 4. 알코올 가글의 배신
blocks.append(text_block([
    {'text': '4. 알코올 가글의 배신 — 쓸수록 세균이 늘었다', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '안 닿는 것까지는 이해했다', 'fontSize': 'fs15'},
    {'text': "'그래도 입 안은 깨끗해지니까 안 하는 것보단 낫지 않나'", 'fontSize': 'fs15'},
    {'text': '나도 처음엔 그렇게 생각했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 가글이 왜 안 되는지를 찾다 보니', 'fontSize': 'fs15'},
    {'text': '자연스럽게 관련 논문도 읽게 됐다', 'fontSize': 'fs15'},
    {'text': '거기서 더 충격적인 걸 발견했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '안 닿는 것만 문제가 아니었다', 'fontSize': 'fs15'},
    {'text': '알코올 가글은 쓸수록 더 나빠지게 만들고 있었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '알코올이 입 안 점막을 말린다', 'fontSize': 'fs15'},
    {'text': '침이 줄어든다', 'fontSize': 'fs15'},
    {'text': '침은 원래 입 안에서 세균을 억제하는 역할을 한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '침이 줄면 산소를 싫어하는 세균이 폭발적으로 늘어난다', 'fontSize': 'fs15'},
    {'text': '이 세균들이 편도 홈 안에서 가스를 만든다', 'fontSize': 'fs15'},
    {'text': '황화수소, 메틸메르캅탄이라는 가스다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석을 으깼을 때 나는 그 냄새가', 'fontSize': 'fs15'},
    {'text': '바로 이 가스 냄새다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '리스테린을 쓰던 6개월이', 'fontSize': 'fs15'},
    {'text': '돌이켜보면 재발이 가장 잦았던 시기였다', 'fontSize': 'fs15'},
    {'text': '그때는 가글을 더 열심히 하면 나아질 줄 알았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '열심히 할수록 입이 더 말랐고', 'fontSize': 'fs15'},
    {'text': '입이 마를수록 세균은 더 빠르게 늘었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '커뮤니티에 이런 글이 있었다', 'fontSize': 'fs15'},
    {'text': '"피곤하거나 면역력이 떨어지면', 'fontSize': 'fs15'},
    {'text': '편도결석이 생기는 경향"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '피로만이 아니었다', 'fontSize': 'fs15'},
    {'text': '알코올 가글이 입을 말리면서', 'fontSize': 'fs15'},
    {'text': '재발을 부추기고 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
]))

blocks.append(text_block([
    {'text': '가글 유형 | 편도 도달 | 구강 건조 | 실제 효과', 'bold': True, 'fontSize': 'fs13'},
    {'text': '알코올 가글 | ✕ | 악화 ↑ | 역효과', 'fontSize': 'fs13'},
    {'text': '무알코올 가글 | ✕ | 중립 | 편도 무관', 'fontSize': 'fs13'},
    {'text': '프로폴리스 가글 | ✕ | 중립 | 편도 무관', 'fontSize': 'fs13'},
]))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '어떤 가글이든 편도에는 안 닿는다', 'fontSize': 'fs15'},
    {'text': '알코올 가글은 거기에 역효과까지 더한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '237만원 중 절반은', 'fontSize': 'fs15'},
    {'text': '오히려 재발을 재촉하는 데 쓴 셈이었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '여기까지 읽고 나서 한동안 아무것도 못 했다', 'fontSize': 'fs15'},
    {'text': '5년간 나는 치료를 한 게 아니었다', 'fontSize': 'fs15'},
    {'text': '편도결석이 더 잘 생기는 환경을 매달 돈 내고 만들고 있었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그때부터 방향을 완전히 바꿨다', 'fontSize': 'fs15'},
    {'text': '가글을 뭘로 바꿀까가 아니라', 'fontSize': 'fs15'},
    {'text': '편도결석이 왜 생기는지 원인부터 파기 시작했다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 5. 재발의 진짜 원인은 세균막이었다
blocks.append(text_block([
    {'text': '5. 재발의 진짜 원인은 세균막이었다', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글이 안 닿는다', 'fontSize': 'fs15'},
    {'text': '알코올 가글은 오히려 악화시킨다', 'fontSize': 'fs15'},
    {'text': '여기까지는 알았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그러면 편도 홈 안쪽에서는 대체 뭐가 일어나고 있길래', 'fontSize': 'fs15'},
    {'text': '2주마다 결석이 돌아오는 건가', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '블로그나 카페 글로는 답이 안 나왔다', 'fontSize': 'fs15'},
    {'text': "다들 '가글 해라' '면봉으로 빼라' '이비인후과 가라'", 'fontSize': 'fs15'},
    {'text': '원인을 설명하는 글이 없었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 영어 논문까지 찾아보기 시작했다', 'fontSize': 'fs15'},
    {'text': '편도결석 관련 논문이 생각보다 많았다', 'fontSize': 'fs15'},
    {'text': '읽다 보니까 빠져들었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '20편쯤 읽었을 때 하나의 단어가 계속 나왔다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '바이오필름', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '한국어로 세균막이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에 세균들이 모여서', 'fontSize': 'fs15'},
    {'text': '끈끈한 보호막을 만든다', 'fontSize': 'fs15'},
    {'text': '이 막 안에서 집단으로 살면서 음식물 찌꺼기를 분해한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 뭔지 감이 안 올 수 있다', 'fontSize': 'fs15'},
    {'text': '치석을 생각하면 된다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이빨에 끼는 치석', 'fontSize': 'fs15'},
    {'text': '양치질로 안 없어진다', 'fontSize': 'fs15'},
    {'text': '스케일링을 해야 벗겨진다', 'fontSize': 'fs15'},
    {'text': '왜? 세균이 단단한 막을 만들어서 이빨에 붙어있으니까', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에도 그게 생기는 거다', 'fontSize': 'fs15'},
    {'text': '가글로 헹겨지지 않는다', 'fontSize': 'fs15'},
    {'text': '막을 직접 건드려야 한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 세균막 안에서 세균들이 음식물을 분해하면서', 'fontSize': 'fs15'},
    {'text': '가스가 나온다', 'fontSize': 'fs15'},
    {'text': '아까 말한 황화수소, 메틸메르캅탄', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그리고 세균 잔해랑 칼슘이 뭉쳐서 굳으면', 'fontSize': 'fs15'},
    {'text': '그게 편도결석이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석 환자의 입 냄새 농도는', 'fontSize': 'fs15'},
    {'text': '비환자 대비 10.3배라는 연구 결과가 있다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '커뮤니티에 이런 글이 있었다', 'fontSize': 'fs15'},
    {'text': '"30년 묵은 결석이 워터픽으로', 'fontSize': 'fs15'},
    {'text': '터져나와 충격"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '30년이면 그 안에 세균막이 얼마나 두꺼웠을지', 'fontSize': 'fs15'},
    {'text': '생각하기도 싫다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '정리하면 이런 순서다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1. 편도 홈에 세균막이 생긴다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '2. 세균이 음식물을 분해하면서 냄새 가스가 나온다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '3. 세균 잔해 + 칼슘이 굳으면서 → 편도결석이 된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '4. 결석을 빼도 세균막이 남아 있으니까 → 또 생긴다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '결석은 결과물이었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '세균막이 원인이었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5년간 나는 결과물만 쫓고 있었다', 'fontSize': 'fs15'},
    {'text': '면봉으로 빼고, 가글로 헹구고', 'fontSize': 'fs15'},
    {'text': '근데 원인은 한 번도 안 건드렸다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 6. 빼는 게 아니라 안 생기게 하는 것
blocks.append(text_block([
    {'text': '6. 빼는 게 아니라 안 생기게 하는 것', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '여기서 생각이 완전히 뒤집어졌다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석을 빼는 건 이미 만들어진 걸 치우는 거다', 'fontSize': 'fs15'},
    {'text': '세균막을 없애는 건 아예 안 만들어지게 하는 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '고혈압 환자가 혈압 오를 때마다', 'fontSize': 'fs15'},
    {'text': '응급실 가서 주사 맞나', 'fontSize': 'fs15'},
    {'text': '아니다', 'fontSize': 'fs15'},
    {'text': '매일 약을 먹어서 혈압이 안 올라가게 관리한다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석도 같다', 'fontSize': 'fs15'},
    {'text': '생길 때마다 면봉으로 빼는 건 응급실 가는 거다', 'fontSize': 'fs15'},
    {'text': '세균막을 매일 억제하면', 'fontSize': 'fs15'},
    {'text': '결석이 만들어지는 속도 자체가 느려진다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '커뮤니티에 이런 글이 있었다', 'fontSize': 'fs15'},
    {'text': '"또 생기지요..."', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 말을 안 하려면', 'fontSize': 'fs15'},
    {'text': '빼는 루틴이 아니라 예방 루틴이 필요하다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그러면 세균막을 뭘로 억제하느냐', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '논문에서 반복적으로 나온 천연 성분이 있었다', 'fontSize': 'fs15'},
    {'text': '프로폴리스', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '벌이 벌집을 외부 세균으로부터 보호하려고 만드는 물질이다', 'fontSize': 'fs15'},
    {'text': '핵심 작용 성분은 플라보노이드', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
]))

blocks.append(text_block([
    {'text': '작용 | 내용 | 데이터', 'bold': True, 'fontSize': 'fs13'},
    {'text': '세균막 파괴 | 이미 생긴 세균막을 분해 | 파괴율 88.5%', 'fontSize': 'fs13'},
    {'text': '형성 억제 | 새로운 세균막이 생기는 걸 차단 | 억제율 71%', 'fontSize': 'fs13'},
    {'text': '점막 보호 | 편도 점막 염증 완화 | 활성산소 중화', 'fontSize': 'fs13'},
]))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세균을 죽이는 게 아니다', 'fontSize': 'fs15'},
    {'text': '세균이 막을 못 만들게 차단하는 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 프로폴리스가 아무리 좋아도', 'fontSize': 'fs15'},
    {'text': '편도까지 닿지 못하면 의미가 없다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '3번에서 말했다', 'fontSize': 'fs15'},
    {'text': '가글은 편도 홈에 안 닿는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스 가글도 마찬가지다', 'fontSize': 'fs15'},
    {'text': '프로폴리스가 들어있어도 가글 형태면', 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에는 닿을 수가 없다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 나는 가글이 아닌 형태를 찾기 시작했다', 'fontSize': 'fs15'},
    {'text': '편도에 직접 닿을 수 있는 형태', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '성분이 같아도 전달 방식이 다르면', 'bold': True, 'fontSize': 'fs15'},
    {'text': '결과가 완전히 달라진다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 7. 편도장벽제 TOP 8
blocks.append(text_block([
    {'text': '7. 편도장벽제 TOP 8 — 내가 세운 기준과 비교 결과', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도에 직접 닿을 수 있는 형태', 'fontSize': 'fs15'},
    {'text': '프로폴리스가 들어있는 것', 'fontSize': 'fs15'},
    {'text': '알코올이 안 들어있는 것', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 세 가지를 기준으로 제품을 찾기 시작했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '찾다 보니까 기준이 더 생겼다', 'fontSize': 'fs15'},
    {'text': '최종적으로 내가 세운 기준은 5가지다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1. 스프레이 형태 — 가글은 애초에 편도에 안 닿으니까 제외', 'bold': True, 'fontSize': 'fs15'},
    {'text': '2. 프로폴리스 함유 — 세균막 억제 데이터가 있는 성분', 'bold': True, 'fontSize': 'fs15'},
    {'text': '3. 알코올 프리 — 알코올 들어가면 입이 말라서 역효과', 'bold': True, 'fontSize': 'fs15'},
    {'text': '4. 올리고당 베이스 — 입 안 유익균까지 죽이면 안 되니까', 'bold': True, 'fontSize': 'fs15'},
    {'text': '5. 휴대 가능 — 가게에서 손님 사이사이에 바로 쓸 수 있어야 했다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 기준으로 시중에 나와있는 편도 관련 제품을 전부 찾아봤다', 'fontSize': 'fs15'},
    {'text': '편도장벽제라는 카테고리 자체가 아직 생소해서', 'fontSize': 'fs15'},
    {'text': '제품 수가 많지는 않았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래도 8개를 찾아서 비교해봤다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
]))

blocks.append(image_block('images/1773827275736_comparison_table_top8.png', '편도장벽제 TOP 8 비교표'))

blocks.append(text_block([
    {'text': '순위 | 제품 | 스프레이 | 프로폴리스 | 알코올프리 | 올리고당 | 휴대성 | 총점', 'bold': True, 'fontSize': 'fs13'},
    {'text': '1위 | H사 | ◎ | ◎ | ◎ | ◎ | ◎ | 5/5', 'fontSize': 'fs13'},
    {'text': '2위 | A사 | ◎ | ◎ | ◎ | ✕ | ◎ | 4/5', 'fontSize': 'fs13'},
    {'text': '3위 | B사 | ◎ | ✕ | ◎ | ✕ | ◎ | 3/5', 'fontSize': 'fs13'},
    {'text': '4위 | C사 | ✕(가글) | ◎ | ◎ | ✕ | ✕ | 2/5', 'fontSize': 'fs13'},
    {'text': '5-8위 | D-G사 | 혼재 | △ | 혼재 | ✕ | 혼재 | 1-2/5', 'fontSize': 'fs13'},
]))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5가지를 전부 충족하는 건 H사 제품 하나였다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 이걸 샀다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 7번 섹션 후반 — 사용 후기
blocks.append(text_block([
    {'text': '처음에는 솔직히 반신반의했다', 'fontSize': 'fs15'},
    {'text': '가글에 237만원 쓰고 낚인 사람이', 'fontSize': 'fs15'},
    {'text': '또 뭘 믿겠나', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 써보니까 확실히 달랐다', 'fontSize': 'fs15'},
    {'text': '가글이랑은 감각 자체가 다르다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '노즐을 목 안쪽으로 향하고 누르면', 'fontSize': 'fs15'},
    {'text': '미스트가 편도 쪽에 직접 닿는 게 느껴진다', 'fontSize': 'fs15'},
    {'text': '가글은 그 느낌이 없었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1주차', 'bold': True, 'fontSize': 'fs15'},
    {'text': '아직 결석이 나오긴 했다', 'fontSize': 'fs15'},
    {'text': '근데 양치 후에 뿌리는 게 습관이 되니까', 'fontSize': 'fs15'},
    {'text': '입 안이 마르는 느낌이 확실히 줄었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '2주차', 'bold': True, 'fontSize': 'fs15'},
    {'text': '원래 2주면 어김없이 나왔는데', 'fontSize': 'fs15'},
    {'text': '이번엔 안 나왔다', 'fontSize': 'fs15'},
    {'text': "'우연인가' 싶었다", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '4주차', 'bold': True, 'fontSize': 'fs15'},
    {'text': '한 달을 넘겼다', 'fontSize': 'fs15'},
    {'text': '5년 만에 처음이었다', 'fontSize': 'fs15'},
    {'text': '2주 간격으로 꼬박꼬박 나오던 게', 'fontSize': 'fs15'},
    {'text': '한 달 동안 안 나왔다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '지금은 쓴 지 3개월째다', 'fontSize': 'fs15'},
    {'text': '결석이 완전히 사라진 건 아니다', 'fontSize': 'fs15'},
    {'text': '근데 재발 간격이 확실히 늘었다', 'fontSize': 'fs15'},
    {'text': '2주 → 한 달 반 정도', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그리고 가게에서 달라진 게 있다', 'fontSize': 'fs15'},
    {'text': '손님한테 메뉴 설명할 때 고개를 안 돌린다', 'fontSize': 'fs15'},
    {'text': '그게 제일 크다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 다른 사람 후기
blocks.append(text_block([
    {'text': '나 혼자만 이런 건지 궁금해서', 'fontSize': 'fs15'},
    {'text': '같은 제품 쓰는 사람들 후기를 찾아봤다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

blocks.append(text_block([
    {'text': '첫 번째로 눈에 들어온 건 콜센터에서 일한다는 사람이었다', 'fontSize': 'fs15'},
    {'text': '나랑 비슷한 상황이었다', 'fontSize': 'fs15'},
    {'text': '하루 종일 전화로 말하는 직업인데 편도결석 때문에', 'fontSize': 'fs15'},
    {'text': '통화할 때마다 입 냄새가 신경 쓰였다고 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"가글을 하루에 3번씩 했는데 소용이 없었어요', 'fontSize': 'fs15'},
    {'text': '스프레이로 바꾸고 3주쯤 됐을 때', 'fontSize': 'fs15'},
    {'text': '결석 나오는 주기가 확실히 길어졌어요', 'fontSize': 'fs15'},
    {'text': '지금 2개월째인데 전화할 때 신경 안 씁니다"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '두 번째는 여자친구 때문에 시작했다는 20대 남자였다', 'fontSize': 'fs15'},
    {'text': '키스할 때 냄새가 신경 쓰여서 자꾸 피했다고 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"여친이 왜 요즘 키스 안 하냐고 물어봤는데', 'fontSize': 'fs15'},
    {'text': '차마 편도결석 얘기를 못 했어요', 'fontSize': 'fs15'},
    {'text': '쓴 지 한 달 반 됐는데 면봉을 꺼낸 적이 없어요', 'fontSize': 'fs15'},
    {'text': '솔직히 이게 제일 신기합니다"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세 번째는 중학생 아들 때문에 찾아본 엄마였다', 'fontSize': 'fs15'},
    {'text': '아이가 입 냄새 때문에 학교에서 놀림을 받는다고 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"아이한테 가글 시켰는데 계속 생기길래', 'fontSize': 'fs15'},
    {'text': '스프레이를 사줬어요', 'fontSize': 'fs15'},
    {'text': "한 달 지나니까 아이가 먼저 '요즘 안 나와' 하더라고요", 'fontSize': 'fs15'},
    {'text': '그 말 듣고 울 뻔 했습니다"', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

blocks.append(text_block([
    {'text': '후기를 읽으면 읽을수록 패턴이 보였다', 'fontSize': 'fs15'},
    {'text': '대부분 2-4주 사이에 변화를 느꼈다', 'fontSize': 'fs15'},
    {'text': '완전히 안 생긴다는 사람은 드물었고', 'fontSize': 'fs15'},
    {'text': '재발 간격이 늘어났다는 사람이 대부분이었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '제품 후기가 1,200개가 넘었다', 'fontSize': 'fs15'},
    {'text': '재구매율 43%', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 숫자가 말해주는 건 하나다', 'fontSize': 'fs15'},
    {'text': '한 번 쓰고 버리는 제품이 아니라', 'fontSize': 'fs15'},
    {'text': '계속 쓰고 있는 사람이 그만큼 많다는 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '내가 비교해서 고른 제품이 궁금하면', 'fontSize': 'fs15'},
    {'text': '여기 들어가서 직접 확인해보면 된다', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

blocks.append(hr_block())

# 8. 지금 시작해야 하는 이유
blocks.append(text_block([
    {'text': '8. 지금 시작해야 하는 이유', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '하나만 물어보겠다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '지금 편도결석이 나오는 간격이 얼마나 되나', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '2주? 한 달? 일주일?', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그 간격이 점점 짧아지고 있지 않나', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '커뮤니티에 이런 글이 있었다', 'fontSize': 'fs15'},
    {'text': '"처음엔 몇 달에 한 번이었는데', 'fontSize': 'fs15'},
    {'text': '요즘은 2주도 안 돼서 또 나와요', 'fontSize': 'fs15'},
    {'text': '구멍이 점점 커지는 느낌"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이건 느낌이 아니다', 'fontSize': 'fs15'},
    {'text': '진짜 커지고 있다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도 홈은 자극을 받을수록 넓어진다', 'fontSize': 'fs15'},
    {'text': '면봉으로 쑤실 때마다 물리적으로 벌어진다', 'fontSize': 'fs15'},
    {'text': '세균막이 오래 머물수록 염증으로 더 깊어진다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '구멍이 커지면 음식물이 더 잘 끼고', 'fontSize': 'fs15'},
    {'text': '세균막이 더 넓게 자리 잡고', 'fontSize': 'fs15'},
    {'text': '결석이 더 크게, 더 자주 생긴다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 무한 반복이다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '그리고 한번 넓어진 홈은 다시 좁아지지 않는다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 5년을 끌었다', 'fontSize': 'fs15'},
    {'text': '27살에 쌀알만했던 결석이', 'fontSize': 'fs15'},
    {'text': '32살에는 콩알만해졌다', 'fontSize': 'fs15'},
    {'text': '나오는 간격도 한 달에서 2주로 줄었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5년 동안 가글만 바꾸면서', 'fontSize': 'fs15'},
    {'text': '편도 홈이 넓어지는 걸 그냥 지켜본 거다', 'fontSize': 'fs15'},
    {'text': '그때 세균막이 뭔지 알았으면', 'fontSize': 'fs15'},
    {'text': '이렇게까지 안 됐을 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가게에서 손님 고개 돌리면서 말한 5년', 'fontSize': 'fs15'},
    {'text': '그 시간은 돌아오지 않는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 지금 이 글을 읽고 있는 사람은 다르다', 'fontSize': 'fs15'},
    {'text': '세균막이 뭔지 안다', 'fontSize': 'fs15'},
    {'text': '가글이 왜 안 되는지 안다', 'fontSize': 'fs15'},
    {'text': '뭘 해야 하는지 안다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '매일 양치 후에 편도 쪽으로 2-3번 뿌리면 된다', 'fontSize': 'fs15'},
    {'text': '3초다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도 홈이 지금보다 더 넓어지기 전에', 'fontSize': 'fs15'},
    {'text': '결석이 지금보다 더 커지기 전에', 'fontSize': 'fs15'},
    {'text': '시작하는 게 맞다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '내가 비교해서 고른 제품이 궁금하면', 'fontSize': 'fs15'},
    {'text': '여기 들어가서 직접 확인해보면 된다', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

blocks.append(hr_block())

# 긴급추가 1 — 2026.3.20
blocks.append(text_block([
    {'text': '✏️ 2026.3.20 추가', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '글 올리고 이틀 만에 메일이 200개 넘게 왔다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '제일 많은 질문이 "어떤 가글 쓰세요?"였다', 'fontSize': 'fs15'},
    {'text': '이 글을 끝까지 읽은 사람이라면 알겠지만', 'fontSize': 'fs15'},
    {'text': '가글이 아니다', 'fontSize': 'fs15'},
    {'text': '스프레이다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글은 편도에 안 닿는다', 'fontSize': 'fs15'},
    {'text': '이 글에서 제일 중요한 내용이 그거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그리고 두 번째로 많은 질문이', 'fontSize': 'fs15'},
    {'text': '"진짜 효과 있어요?"였다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나도 처음엔 반신반의했다', 'fontSize': 'fs15'},
    {'text': '237만원 날린 사람이 뭘 믿겠나', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 3개월째 쓰고 있고', 'fontSize': 'fs15'},
    {'text': '면봉을 꺼내는 횟수가 확실히 줄었다', 'fontSize': 'fs15'},
    {'text': '이건 내가 직접 겪은 거라서 다른 말이 필요 없다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '아직 안 본 사람들을 위해 링크 다시 남긴다', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

blocks.append(hr_block())

# 긴급추가 2 — 2026.3.23
blocks.append(text_block([
    {'text': '✏️ 2026.3.23 추가', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '초도 물량이 거의 소진됐다는 연락을 받았다', 'fontSize': 'fs15'},
    {'text': '재입고까지 2주 정도 걸린다고 한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '급한 사람은 지금 확인해보는 게 맞다', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))


# ===== 조립 =====
post_content = '\n\n'.join(blocks)

index_path = 'public/posts/tonsil-stone-md3/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- POST CONTENT START -->'
end_marker = '<!-- POST CONTENT END -->'
start_idx = html.index(start_marker) + len(start_marker)
end_idx = html.index(end_marker)

new_html = html[:start_idx] + '\n\n' + post_content + '\n\n' + html[end_idx:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

# config 업데이트 — 쿨티아 언급 제거, MD3 페르소나에 맞는 댓글
config_path = 'public/posts/tonsil-stone-md3/config.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

config['comments'] = [
    {
        "author": "가글5년차탈출",
        "profile_color": "#f8b4c8",
        "time": "1시간 전",
        "text": "세탁기 고무패킹 비유 소름... 가글이 왜 안 되는지 이제야 진짜로 이해됐어요",
        "likes": 38
    },
    {
        "author": "자영업자동병상련",
        "profile_color": "#b4d8f8",
        "time": "3시간 전",
        "text": "저도 음식점 운영하는데 손님한테 말할 때 고개 돌리는 거 공감 100%... 직업상 진짜 스트레스였어요",
        "likes": 52
    },
    {
        "author": "237만원_공감",
        "profile_color": "#d8f8b4",
        "time": "6시간 전",
        "text": "명세서 보니까 저도 비슷하게 쓴 것 같아서 충격ㅠㅠ 가글 종류만 바꾸면 되는 줄 알았는데",
        "likes": 29
    },
    {
        "author": "알코올가글배신자",
        "profile_color": "#f8d8b4",
        "time": "1일 전",
        "text": "알코올 가글이 오히려 역효과라는 거 몰랐다... 리스테린 제일 열심히 쓸 때 제일 자주 나왔던 이유가 그거였구나",
        "likes": 44
    },
    {
        "author": "세균막알게된후기",
        "profile_color": "#d8b4f8",
        "time": "2일 전",
        "text": "세균막이 원인이라는 거 논문 근거까지 있으니까 신뢰가 가네요. 스프레이로 바꾼 지 3주째인데 확실히 덜 나오는 느낌",
        "likes": 31
    }
]

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f'✅ MD3 v2 index.html 업데이트 완료 ({len(post_content)} chars)')
print(f'   블록 수: {len(blocks)}')
print(f'✅ config.json 업데이트 완료')
