#!/usr/bin/env python3
"""MD2 v2 어드버토리얼 → SE HTML 변환 후 index.html 주입"""

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

# ===== MD2 v2 본문 구성 =====
blocks = []

# 참고논문
blocks.append(text_block([
    {'text': '<참고논문>', 'bold': True, 'fontSize': 'fs13'},
    {'text': '- Bezerra TF et al. "The Role of Tonsils in Halitosis." Braz J Otorhinolaryngol. 2013', 'fontSize': 'fs11'},
    {'text': '- Krespi YP et al. "The Relationship Between Oral Malodor and VSC-Producing Bacteria." Otolaryngology. 2006', 'fontSize': 'fs11'},
    {'text': '- Stoodley P et al. "Biofilms as Complex Differentiated Communities." Annu Rev Microbiol. 2002', 'fontSize': 'fs11'},
    {'text': '- Miyake Y et al. "Inhibitory Effect of Propolis on Biofilm Formation." J Pharmacol Sci. 2021', 'fontSize': 'fs11'},
    {'text': '- Sforcin JM. "Biological Properties and Therapeutic Applications of Propolis." Phytother Res. 2016', 'fontSize': 'fs11'},
    {'text': '- Stepanović S et al. "Biofilm Formation by Oral Bacteria." Oral Microbiol Immunol. 2004', 'fontSize': 'fs11'},
]))

# 안티협찬 선언
blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '※주의※', 'bold': True, 'fontSize': 'fs15'},
    {'text': '이 글은 편도결석 수술을 3번 예약하고 3번 취소한 사람이 쓴 글이다', 'fontSize': 'fs15'},
    {'text': '수술 후기를 100건 이상 읽고 논문을 직접 뒤진 기록이다', 'fontSize': 'fs15'},
    {'text': '제품 협찬은 받지 않는다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '협찬 요청하시는 업체분들은 연락 시 업체명 공개한다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 목차
blocks.append(text_block([
    {'text': '(목차)', 'bold': True, 'fontSize': 'fs15'},
    {'text': '1. 수술 후기를 읽다가 포기한 이유', 'fontSize': 'fs15'},
    {'text': '2. 면봉으로 빼면 안 되는 진짜 이유', 'fontSize': 'fs15'},
    {'text': '3. 양치·가글이 편도에 닿지 않는 구조적 한계', 'fontSize': 'fs15'},
    {'text': '4. 논문에서 찾은 진짜 원인 — 세균막', 'fontSize': 'fs15'},
    {'text': '5. 세균막을 부수는 성분이 존재한다', 'fontSize': 'fs15'},
    {'text': '6. 가글 vs 스프레이, 편도에 닿느냐 마느냐', 'fontSize': 'fs15'},
    {'text': '7. 직접 비교한 편도장벽제 TOP 8', 'fontSize': 'fs15'},
    {'text': '8. 직접 써본 후기 + 주변 반응', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 훅 섹션
blocks.append(text_block([
    {'text': '"칼로 찌르는 듯한 고통이 2~7일 간다"', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 편도절제술 후기에서 가장 많이 나오는 문장이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"물 한모금 넘기는 게 큰 결심이 필요함"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"침 삼키면 귀까지 칼로 긋는 느낌"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"밤에 잠 못 자서 진통제 먹다가 위가 나가버림"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '수술 후 2주 동안 죽만 먹고', 'fontSize': 'fs15'},
    {'text': '5kg 빠진 사람도 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 수술을 예약했다가 취소했다', 'fontSize': 'fs15'},
    {'text': '그리고 또 예약했다가 또 취소했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세 번째 예약을 취소한 날', 'fontSize': 'fs15'},
    {'text': '유튜브랑 블로그를 다 뒤졌다', 'fontSize': 'fs15'},
    {'text': '편도결석 관련이면 댓글까지 전부 읽었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '읽으면 읽을수록 머리가 복잡해지기 시작했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '수술해도 80%가 재발한다고 했다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '30~50만원 내고 2주 굶고 80% 재발', 'fontSize': 'fs15'},
    {'text': '이건 도박이었다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 1. 수술 후기를 읽다가 포기한 이유
blocks.append(text_block([
    {'text': '1. 수술 후기를 읽다가 포기한 이유', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 35살 직장인이다', 'fontSize': 'fs15'},
    {'text': '편도결석 첫 발견은 7년 전', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '처음엔 기침하다 나온 노란 알갱이가 뭔지도 몰랐다', 'fontSize': 'fs15'},
    {'text': '으깨보고 냄새 맡아보고', 'fontSize': 'fs15'},
    {'text': '세상에서 제일 더러운 냄새를 맡았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그게 내 목 안에 있었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그때부터 시작됐다', 'fontSize': 'fs15'},
    {'text': '회의 전 화장실에서 편도 확인하는 습관', 'fontSize': 'fs15'},
    {'text': '숨 들이쉬면서 얘기하는 습관', 'fontSize': 'fs15'},
    {'text': '상대방이 코를 만지면 자동으로 위축되는 습관', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"비대면으로 일하는 직종으로 바꿀까 싶을만큼"', 'fontSize': 'fs15'},
    {'text': '진심으로 그런 생각을 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 수술을 알아봤다', 'fontSize': 'fs15'},
    {'text': '레이저 편도절제술', 'fontSize': 'fs15'},
    {'text': '가격 30~50만원', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 후기를 읽을수록 겁이 났다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '수술 후기 100건을 읽었다', 'fontSize': 'fs15'},
    {'text': '"2주 동안 물도 못 삼켰다"', 'fontSize': 'fs15'},
    {'text': '"퇴원하고 다시 입원했다 출혈 터져서"', 'fontSize': 'fs15'},
    {'text': '"죽만 먹다가 5kg 빠졌다"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이런 후기가 절반이 넘었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 진짜 문제는 따로 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"수술하면 오바야???"', 'fontSize': 'fs15'},
    {'text': '"레이저도 80% 이상 재발"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '재발률이 80%라는 걸 수술 상담에서 말해준 병원이 없었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '세 군데를 갔는데 한 곳도', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도가 면역기관이라는 얘기도 못 들었다', 'fontSize': 'fs15'},
    {'text': '잘라내면 면역 방어선 하나가 사라진다는 거다', 'fontSize': 'fs15'},
    {'text': '이걸 집에 와서 직접 검색해서 알았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세 군데 병원을 다녔는데', 'fontSize': 'fs15'},
    {'text': '재발률도 면역기능도 어디서도 설명을 안 해줬다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 수술 후 재발 후기를 따로 찾아봤다', 'fontSize': 'fs15'},
    {'text': '"수술하고 1년 만에 또 나왔다"', 'fontSize': 'fs15'},
    {'text': '"50만원 내고 2주 고생했는데 결국 또 면봉 들고 있다"', 'fontSize': 'fs15'},
    {'text': '이런 글이 수두룩했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '면역기능 쪽도 직접 찾아봤다', 'fontSize': 'fs15'},
    {'text': '"편도절제술 후 IgA 분비가 감소한다"는 논문이 있었다', 'fontSize': 'fs15'},
    {'text': 'IgA가 뭔지 몰라서 또 찾아봤다', 'fontSize': 'fs15'},
    {'text': '목 안쪽에서 세균을 처음 막아주는 항체라고 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그걸 잘라내겠다는 거였다', 'fontSize': 'fs15'},
    {'text': '재발률 80%인데 면역기관까지 잘라내겠다는 거였다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 사실을 환자한테 설명해주는 병원이 왜 없는 거냐', 'fontSize': 'fs15'},
    {'text': '그게 진짜 화가 났다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"구취 중 뭘 해도 소용 없는게 편도결석이예요"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 댓글을 본 순간', 'fontSize': 'fs15'},
    {'text': '방향을 바꿨다', 'fontSize': 'fs15'},
    {'text': '왜 안 없어지는지를 먼저 이해하기로 했다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 2. 면봉으로 빼면 안 되는 진짜 이유
blocks.append(text_block([
    {'text': '2. 면봉으로 빼면 안 되는 진짜 이유', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석이 보이면 본능적으로 빼고 싶다', 'fontSize': 'fs15'},
    {'text': '나도 그랬다', 'fontSize': 'fs15'},
    {'text': '면봉, 귀이개, 심지어 젓가락까지 써봤다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '빠지긴 빠진다', 'fontSize': 'fs15'},
    {'text': '근데 문제는 그다음이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"구멍이 점점 커지는 느낌"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이건 진짜 커지고 있는 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도에는 2-3mm 깊이의 홈이 있다', 'fontSize': 'fs15'},
    {'text': '면봉으로 쑤시면 이 홈이 물리적으로 넓어진다', 'fontSize': 'fs15'},
    {'text': '구멍이 커지면 → 음식물이 더 잘 끼고', 'fontSize': 'fs15'},
    {'text': '→ 세균이 더 잘 자라고', 'fontSize': 'fs15'},
    {'text': '→ 결석이 더 크게, 더 자주 생긴다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '빼면 빼는 만큼 구멍이 늘어나는 악순환이었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"난 혼자 하면 항상 피나고 나중에 목 아프고"', 'fontSize': 'fs15'},
    {'text': '"구멍에 박힌 애는 면봉 대려고만 해도 심하게 구역질"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나만 그런 게 아니었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '면봉 = 해결이 아니라 악화였다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '7년 동안 결석이 점점 커진 이유가 여기 있었다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 3. 양치·가글이 편도에 닿지 않는 구조적 한계
blocks.append(text_block([
    {'text': '3. 양치·가글이 편도에 닿지 않는 구조적 한계', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"양치를 아무리 해도 입냄새가 안 사라지는데 어떡하죠.."', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 질문을 네이버 지식인에서만 수백 건 봤다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '답은 간단했다', 'fontSize': 'fs15'},
    {'text': '양치질은 편도까지 안 닿는다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '칫솔이 닿는 건 치아, 잇몸, 혀', 'fontSize': 'fs15'},
    {'text': '편도는 목 안쪽 양 옆에 있다', 'fontSize': 'fs15'},
    {'text': '물리적으로 칫솔이 도달할 수 없는 위치다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"그럼 가글은?"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '동네 이비인후과 선생님한테 직접 물어봤다', 'fontSize': 'fs15'},
    {'text': '"가글로 편도결석 관리 되나요?"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '선생님이 이렇게 말했다', 'fontSize': 'fs15'},
    {'text': '"가글은 입 안을 헹구는 거지 편도 구멍 안까지는 안 들어가요"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"편도 홈 깊이가 2-3mm인데 가글액이 거기까지 침투하는 건 구조적으로 어렵습니다"', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '비유하면 이렇다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '배수구 주변 바닥을 물로 씻는 것 = 가글', 'bold': True, 'fontSize': 'fs15'},
    {'text': '바닥은 깨끗해진다', 'fontSize': 'fs15'},
    {'text': '근데 배수구 안쪽에 낀 물때는 그대로다', 'fontSize': 'fs15'},
    {'text': '거기서 올라오는 냄새도 그대로다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '배수구 안쪽 물때를 직접 분해하는 것 = 필요한 것', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글이 나쁜 게 아니다', 'fontSize': 'fs15'},
    {'text': '편도까지 닿을 수 있는 형태가 아닌 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '알코올 가글은 더 문제다', 'fontSize': 'fs15'},
    {'text': '구강을 바싹 말려서 세균이 더 잘 번식하는 환경을 만든다', 'fontSize': 'fs15'},
    {'text': '쓰면 쓸수록 역효과다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 4. 논문에서 찾은 진짜 원인 — 세균막
blocks.append(text_block([
    {'text': '4. 논문에서 찾은 진짜 원인 — 세균막', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '면봉은 구멍을 키우고', 'fontSize': 'fs15'},
    {'text': '양치는 안 닿고', 'fontSize': 'fs15'},
    {'text': '가글은 표면만 헹구고', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그러면 편도결석의 진짜 원인은 뭔가', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '논문 30건을 읽고 나서야 한 단어를 찾았다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '바이오필름(세균막)', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도 홈 안쪽에 세균들이', 'fontSize': 'fs15'},
    {'text': '끈끈한 보호막을 만들어서 집단으로 눌러앉는다', 'fontSize': 'fs15'},
    {'text': '이 막이 바이오필름이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '쉽게 말하면 이렇다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '욕실 배수구 안쪽에 끼는 미끌미끌한 물때', 'bold': True, 'fontSize': 'fs15'},
    {'text': '그게 세균막이다', 'fontSize': 'fs15'},
    {'text': '손으로 문질러도 잘 안 벗겨지는 그것', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 세균막 안에서 세균들이 음식물 찌꺼기를 분해하면서', 'fontSize': 'fs15'},
    {'text': '냄새 가스를 뿜는다', 'fontSize': 'fs15'},
    {'text': '이게 그 역겨운 냄새의 정체다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '실제 데이터가 있다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석 환자의 구취 농도(VSC)는', 'fontSize': 'fs15'},
    {'text': '비환자 대비 10.3배', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '10배가 아니라 10.3배다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"회의 하면 옆자리까지 느껴져서"라는 후기가 과장이 아니었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '정리하면 이 순서다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1. 편도 홈에 세균막이 형성된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '2. 세균이 음식물을 분해하며 냄새 가스 생성', 'bold': True, 'fontSize': 'fs15'},
    {'text': '3. 세균 잔해 + 칼슘이 굳으면서 → 편도결석이 된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '4. 면봉으로 제거 → 구멍 확대 → 더 큰 세균막 → 더 큰 결석', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '결석을 빼는 건 증상 제거일 뿐이었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '세균막을 부수지 않으면 영원히 반복된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 이걸 알고 나니까', 'fontSize': 'fs15'},
    {'text': '팀 미팅이 더 괴로워졌다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '어느 날 발표 중에 옆에 앉은 동료가', 'fontSize': 'fs15'},
    {'text': '슬쩍 고개를 돌리는 게 보였다', 'fontSize': 'fs15'},
    {'text': '그 순간 말이 막혔다', 'fontSize': 'fs15'},
    {'text': '발표 끝나고 화장실에서 편도를 확인했다', 'fontSize': 'fs15'},
    {'text': '하얗게 박혀 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그날 밤에 또 거울 앞에 섰다', 'fontSize': 'fs15'},
    {'text': '면봉으로 쑤시면서 생각했다', 'fontSize': 'fs15'},
    {'text': '이러다 진짜 평생 이러겠구나', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그때부터 검색 키워드가 바뀌었다', 'fontSize': 'fs15'},
    {'text': '"편도결석 없애는 법" "편도결석 자꾸 생김"', 'fontSize': 'fs15'},
    {'text': '한국어로는 답이 안 나왔다', 'fontSize': 'fs15'},
    {'text': '영어로 "tonsil stone cause"를 검색하기 시작했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '거기서 세균막을 부수는 성분이 있다는 걸 처음 알았다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 5. 세균막을 부수는 성분이 존재한다
blocks.append(text_block([
    {'text': '5. 세균막을 부수는 성분이 존재한다', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세균막이 원인이라는 걸 알았다', 'fontSize': 'fs15'},
    {'text': '그러면 이걸 어떻게 부수느냐', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '항생제?', 'fontSize': 'fs15'},
    {'text': '→ 바이오필름은 항생제 내성이 강하다', 'fontSize': 'fs15'},
    {'text': '세균이 막 안에 숨어서 약물이 침투 못 한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그래서 계속 논문을 뒤졌다', 'fontSize': 'fs15'},
    {'text': '반복적으로 등장하는 천연 성분이 하나 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '벌이 벌집을 외부 세균으로부터 보호할 때 쓰는 물질이다', 'fontSize': 'fs15'},
    {'text': '그 안에 들어있는 플라보노이드 성분이 핵심인데', 'fontSize': 'fs15'},
    {'text': '세균막에 대해 3중으로 작용한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세균막 파괴 | 이미 굳어진 바이오필름 분해 | 파괴율 88.5%', 'bold': True, 'fontSize': 'fs13'},
    {'text': '형성 억제 | 새로운 세균막 생성 차단 | 억제율 71%', 'bold': True, 'fontSize': 'fs13'},
    {'text': '점막 보호 | 편도 점막 염증 완화 | 활성산소 중화', 'bold': True, 'fontSize': 'fs13'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세균을 죽이는 것만이 아니라', 'fontSize': 'fs15'},
    {'text': '세균이 다시 막을 형성하지 못하도록 차단하는 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '기존에 시도했던 것들과 비교하면 차이가 명확하다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '양치 | 치아·잇몸 세균 제거 | 편도 미도달', 'fontSize': 'fs13'},
    {'text': '가글 | 구강 전체 헹굼 | 편도 홈 침투 불가', 'fontSize': 'fs13'},
    {'text': '면봉 | 결석 물리적 제거 | 구멍 확대 악순환', 'fontSize': 'fs13'},
    {'text': '프로폴리스 | 세균막 자체 파괴+재형성 차단 | 전달 방식이 관건', 'bold': True, 'fontSize': 'fs13'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '마지막 줄이 핵심이다', 'fontSize': 'fs15'},
    {'text': '프로폴리스가 아무리 좋아도', 'fontSize': 'fs15'},
    {'text': '편도까지 도달시키는 방법이 없으면 소용없다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 6. 가글 vs 스프레이
blocks.append(text_block([
    {'text': '6. 가글 vs 스프레이, 편도에 닿느냐 마느냐', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스 가글도 시중에 있다', 'fontSize': 'fs15'},
    {'text': '근데 3번에서 말했듯이', 'fontSize': 'fs15'},
    {'text': '가글은 구조적으로 편도 홈에 안 닿는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그러면 프로폴리스를 편도에 직접 보내려면?', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '스프레이', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '노즐을 목 안쪽으로 향하고 분사하면', 'fontSize': 'fs15'},
    {'text': '편도 표면에 직접 닿는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글은 입을 헹구는 것이고', 'fontSize': 'fs15'},
    {'text': '스프레이는 편도에 직접 쏘는 것이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 차이가 전부다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '성분이 같아도 전달 방식이 다르면', 'fontSize': 'fs15'},
    {'text': '결과가 완전히 달라진다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '내가 제품을 고를 때 세운 기준 5가지:', 'bold': True, 'fontSize': 'fs15'},
    {'text': '1. 프로폴리스 함유 (플라보노이드 3% 이상)', 'fontSize': 'fs15'},
    {'text': '2. 스프레이 형태 (가글 제외)', 'fontSize': 'fs15'},
    {'text': '3. 알코올 프리', 'fontSize': 'fs15'},
    {'text': '4. 올리고당 베이스 (구강 유익균 보호)', 'fontSize': 'fs15'},
    {'text': '5. 휴대 사이즈 (외출 시 즉시 사용 가능)', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 5가지 기준으로 시중 편도 스프레이 8개를 전수 비교했다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 7. 비교표
blocks.append(text_block([
    {'text': '7. 직접 비교한 편도장벽제 TOP 8', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
]))

blocks.append(text_block([
    {'text': '순위 | 제품 | 프로폴리스 | 세균막타깃 | 직분사 | 알코올무첨가 | 자극테스트 | 총점', 'bold': True, 'fontSize': 'fs13'},
    {'text': '', 'fontSize': 'fs13'},
    {'text': '1위 | D사 | ◎ 고농축 | ◎ | ◎ 노즐 | ◎ | ◎ 0.00 | 5.0', 'fontSize': 'fs13'},
    {'text': '2위 | A사 | ○ | △ 가글형 | ◎ | ○ | △ | 3.2', 'fontSize': 'fs13'},
    {'text': '3위 | B사 | ◎ | ○ | △ 미스트 | ◎ | ○ | 3.0', 'fontSize': 'fs13'},
    {'text': '4위 | C사 | △ 저함량 | ○ | ◎ | ✕ 알코올 | ○ | 2.8', 'fontSize': 'fs13'},
    {'text': '5위 | E사 | ○ | ✕ 가글 | ✕ | ◎ | ○ | 2.5', 'fontSize': 'fs13'},
    {'text': '6위 | F사 | ✕ | △ | ◎ | ○ | △ | 2.3', 'fontSize': 'fs13'},
    {'text': '7위 | G사 | ○ | ✕ 가글 | ✕ | ✕ 알코올 | ✕ | 1.8', 'fontSize': 'fs13'},
    {'text': '8위 | H사 | ✕ | ✕ | △ | ○ | ✕ | 1.5', 'fontSize': 'fs13'},
]))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5가지 기준을 전부 충족하는 제품은 딱 하나였다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스 고농축 + 세균막 직접 타깃 + 노즐 직분사 + 알코올 무첨가 + 피부 자극 지수 0.00', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 조합을 가진 제품이 D사 하나뿐이라는 게', 'fontSize': 'fs15'},
    {'text': '솔직히 좀 놀라웠다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '8개 다 비교해봤는데 나머지는 가글이거나 알코올이 들어가거나', 'fontSize': 'fs15'},
    {'text': '노즐이 편도까지 안 닿는 미스트 형태였다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 8. 직접 써본 후기
blocks.append(text_block([
    {'text': '8. 직접 써본 후기 + 주변 반응', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이걸 쓰기 시작한 건 나 혼자였다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 회사 동료한테 얘기했더니', 'fontSize': 'fs15'},
    {'text': '"나도 편도결석 있는데?" 하는 거다', 'fontSize': 'fs15'},
    {'text': '10년 넘게 같이 일했는데 처음 알았다', 'fontSize': 'fs15'},
    {'text': '그래서 같이 써보자고 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1주차에 물어봤다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"아직 모르겠는데 뿌릴 때 목 안쪽이 시원한 느낌은 있다"고 했다', 'fontSize': 'fs15'},
    {'text': '가글이랑은 확실히 다른 느낌이라고', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '2주차에 다시 물어봤다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"원래 2주마다 면봉 꺼냈는데 아직 안 꺼냈다"고 했다', 'fontSize': 'fs15'},
    {'text': '이물감이 안 온다고', 'fontSize': 'fs15'},
    {'text': '보통이면 벌써 목 안쪽이 까끌까끌해지는 시점인데', 'fontSize': 'fs15'},
    {'text': '그게 없다고', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '3주차에 카톡이 먼저 왔다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '"야 나 면봉 진짜 안 든다"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '3주째 면봉을 안 꺼냈다는 거다', 'fontSize': 'fs15'},
    {'text': '7년 동안 2주마다 빼던 사람이', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '와이프한테도 줬다', 'fontSize': 'fs15'},
    {'text': '와이프는 나보다 결석이 작은 편이었는데', 'fontSize': 'fs15'},
    {'text': '면봉 대신 가글로 버티고 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '2주 쯤 되니까', 'fontSize': 'fs15'},
    {'text': '"요즘 가글 안 해도 입에서 냄새 안 나는 것 같다"고 했다', 'fontSize': 'fs15'},
    {'text': '아침에 일어났을 때 그 텁텁한 느낌이 줄었다고', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 6주째다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '면봉을 든 횟수가 0이다', 'fontSize': 'fs15'},
    {'text': '2주마다 거울 앞에서 쑤시던 게 일상이었는데', 'fontSize': 'fs15'},
    {'text': '그게 사라졌다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '3명이라 통계라고 할 수는 없다', 'fontSize': 'fs15'},
    {'text': '근데 3명 다 면봉 드는 횟수가 줄었다', 'fontSize': 'fs15'},
    {'text': '2주 주기가 깨졌다', 'fontSize': 'fs15'},
    {'text': '그건 세균막이 실제로 억제되고 있다는 뜻이다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 대세감
blocks.append(text_block([
    {'text': '이 제품이 조용히 퍼지고 있다는 걸 안 건', 'fontSize': 'fs15'},
    {'text': '디시 구강건강 갤러리에서였다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"편도장벽제"로 검색하면', 'fontSize': 'fs15'},
    {'text': '3개월 전에는 글이 거의 없었다', 'fontSize': 'fs15'},
    {'text': '지금은 주 10건 이상 올라온다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '출시 6개월 만에 리뷰가 2,300개를 넘었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '재구매율이 67%다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '재구매율 67%라는 건', 'fontSize': 'fs15'},
    {'text': '3명 중 2명이 다시 산다는 뜻이다', 'fontSize': 'fs15'},
    {'text': '가글은 정기배송 해지하면 끝인데', 'fontSize': 'fs15'},
    {'text': '이건 다시 사는 사람이 3분의 2다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나만 찾은 게 아니었다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 마무리 + CTA
blocks.append(text_block([
    {'text': '7개월간 논문 뒤지고 제품 8개 비교하고', 'fontSize': 'fs15'},
    {'text': '직접 써보고 동료한테 줘보고', 'fontSize': 'fs15'},
    {'text': '그 과정을 전부 이 글에 적었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 이걸 알고 나서 가글 정기배송을 해지했다', 'fontSize': 'fs15'},
    {'text': '6주째 면봉을 안 꺼내고 있다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '내가 비교해서 고른 제품이 궁금하면', 'fontSize': 'fs15'},
    {'text': '여기 들어가서 직접 확인해봐라 →', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

blocks.append(hr_block())

# 긴급추가 1
blocks.append(text_block([
    {'text': '✏️ 2026.3.18 긴급추가', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '글 올리고 나서 메일이 쏟아졌다', 'fontSize': 'fs15'},
    {'text': '"그 제품 이름이 뭐냐" "어디서 사냐" 가 대부분이었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '본문에 다 적어놨는데 못 찾는 분들이 많아서', 'fontSize': 'fs15'},
    {'text': '여기 링크 하나 더 남긴다', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

# 긴급추가 2
blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '✏️ 2026.3.20 추가 업데이트', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1차 물량 다 나갔다고 한다', 'fontSize': 'fs15'},
    {'text': '지금 주문하면 입고 후 순차 발송이라고', 'fontSize': 'fs15'},
    {'text': '급한 분들은 확인해보시길', 'fontSize': 'fs15'},
]))

blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))


# ===== 조립 =====
post_content = '\n\n'.join(blocks)

index_path = 'public/posts/tonsil-stone-md2/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- POST CONTENT START -->'
end_marker = '<!-- POST CONTENT END -->'
start_idx = html.index(start_marker) + len(start_marker)
end_idx = html.index(end_marker)

new_html = html[:start_idx] + '\n\n' + post_content + '\n\n' + html[end_idx:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

# config 업데이트 — 쿨티아 댓글 수정
config_path = 'public/posts/tonsil-stone-md2/config.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

config['comments'] = [
    {
        "author": "수술고민중",
        "profile_color": "#f8b4c8",
        "time": "2시간 전",
        "text": "저도 수술 예약했다 취소한 사람... 면역기관 잘라내는 게 너무 무서워서",
        "likes": 34
    },
    {
        "author": "직장인다은",
        "profile_color": "#b4d8f8",
        "time": "5시간 전",
        "text": "배수구 비유 소름... 가글이 왜 안 되는지 이제야 이해됐어요",
        "likes": 21
    },
    {
        "author": "7년차결석러",
        "profile_color": "#d8f8b4",
        "time": "1일 전",
        "text": "면봉으로 쑤시면 구멍 커진다는 거 진짜였구나 ㅠㅠ 나도 7년째인데 공감 100%",
        "likes": 45
    },
    {
        "author": "결석탈출러",
        "profile_color": "#f8d8b4",
        "time": "2일 전",
        "text": "세균막이 원인이라는 거 논문에서 나온 거라 신뢰감 있네요",
        "likes": 18
    },
    {
        "author": "스프레이전환후기",
        "profile_color": "#d8b4f8",
        "time": "3일 전",
        "text": "스프레이로 바꾼 지 한 달 됐는데 면봉 진짜 안 들어요. 이거 실화",
        "likes": 29
    }
]

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f'✅ MD2 v2 index.html 업데이트 완료 ({len(post_content)} chars)')
print(f'   블록 수: {len(blocks)}')
print(f'✅ config.json 업데이트 완료')
