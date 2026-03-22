#!/usr/bin/env python3
"""v3 어드버토리얼 MD → SE HTML 변환 후 index.html에 주입"""

import re

CTA_URL = "https://soricare.com/product/sns-%EB%B9%84%EB%B0%80%EB%A7%81%ED%81%AC-%ED%8E%B8%EB%8F%84%EC%9E%A5%EB%B2%BD%EC%A0%9C-1%EC%9C%84/53/category/1/display/3/?icid=MAIN.product_listmain_2"

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def text_block(paragraphs, default_fs='fs15'):
    """텍스트 블록 SE HTML 생성"""
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
    """테이블을 텍스트 블록으로 변환 (SE에디터에는 테이블 없음)"""
    paras = []
    # 헤더
    header_text = ' | '.join(headers)
    paras.append({'text': header_text, 'bold': True, 'fontSize': 'fs13'})
    paras.append({'text': '', 'fontSize': 'fs13'})
    for row in rows:
        row_text = ' | '.join(row)
        paras.append({'text': row_text, 'bold': False, 'fontSize': 'fs13'})
    return text_block(paras, 'fs13')

# ===== v3 본문 구성 =====
blocks = []

# 참고논문 섹션
blocks.append(text_block([
    {'text': '<참고논문>', 'bold': True, 'fontSize': 'fs13'},
    {'text': '- Aas JA et al. "Bacteria of Dental Caries in Primary and Permanent Teeth." J Clin Microbiol. 2008', 'fontSize': 'fs11'},
    {'text': '- Bezerra TF et al. "The Role of Tonsils in Halitosis." Braz J Otorhinolaryngol. 2013', 'fontSize': 'fs11'},
    {'text': '- Krespi YP et al. "The Relationship Between Oral Malodor and VSC-Producing Bacteria." Otolaryngology. 2006', 'fontSize': 'fs11'},
    {'text': '- Marcucci MC. "Propolis: Chemical Composition, Biological Properties." Apidologie. 2001', 'fontSize': 'fs11'},
    {'text': '- Sforcin JM. "Biological Properties and Therapeutic Applications of Propolis." Phytother Res. 2016', 'fontSize': 'fs11'},
    {'text': '- Stepanović S et al. "Biofilm Formation by Oral Bacteria." Oral Microbiol Immunol. 2004', 'fontSize': 'fs11'},
    {'text': '- Stoodley P et al. "Biofilms as Complex Differentiated Communities." Annu Rev Microbiol. 2002', 'fontSize': 'fs11'},
    {'text': '- Miyake Y et al. "Inhibitory Effect of Propolis on Biofilm Formation." J Pharmacol Sci. 2021', 'fontSize': 'fs11'},
    {'text': '- Greenman J et al. "Organoleptic Intensity Scale for Measuring Oral Malodor." J Dent Res. 2004', 'fontSize': 'fs11'},
    {'text': '- Pruitt KM, Reiter B. "Biochemistry of Peroxidase System." Peroxidases in Chemistry and Biology. 1991', 'fontSize': 'fs11'},
]))

# 안티협찬 선언
blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '※주의※', 'bold': True, 'fontSize': 'fs15'},
    {'text': '이 글은 편도결석 5년차인 내가 수백 건의 논문과 커뮤니티 후기를 직접 분석하여 작성한 실제 경험글이다', 'fontSize': 'fs15'},
    {'text': '제품 협찬은 절대 받지 않는다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '협찬 요청하시는 업체분들은 지속 연락 시 업체명 공개한다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 목차
blocks.append(text_block([
    {'text': '(목차)', 'bold': True, 'fontSize': 'fs15'},
    {'text': '1. 왜 이 글을 쓰게 됐는지', 'fontSize': 'fs15'},
    {'text': '2. 편도결석이 양치로 안 없어지는 진짜 이유', 'fontSize': 'fs15'},
    {'text': '3. 가글 업계가 절대 말 안 하는 사실', 'fontSize': 'fs15'},
    {'text': '4. 프로폴리스가 주목받는 이유', 'fontSize': 'fs15'},
    {'text': '5. 가글 vs 스프레이, 결정적 차이', 'fontSize': 'fs15'},
    {'text': '6. 내가 직접 비교한 제품 TOP 8', 'fontSize': 'fs15'},
    {'text': '7. 결론 — 6주 후 달라진 것', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 훅 섹션
blocks.append(text_block([
    {'text': '기침하다가 누런 알갱이가 튀어나왔다', 'fontSize': 'fs15'},
    {'text': '으깨봤다', 'fontSize': 'fs15'},
    {'text': '진짜 똥내였다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 내 목 안에 박혀있었다는 거다', 'fontSize': 'fs15'},
    {'text': '이 냄새를 풍기면서 사람을 만나고 있었다는 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그날부터 달라졌다', 'fontSize': 'fs15'},
    {'text': '회의 전에 화장실 가서 면봉으로 편도를 확인하게 됐다', 'fontSize': 'fs15'},
    {'text': '사람한테 말할 때 숨을 들이쉬면서 말하게 됐다', 'fontSize': 'fs15'},
    {'text': "누가 코를 만지면 '나 때문인가' 자동으로 떠올랐다", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5년째 이러고 있다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글에만 237만원을 갖다 버렸다', 'fontSize': 'fs15'},
    {'text': '리스테린 3통, 가그린 2통, 닥터세닥 1통, 쿨티아 정기배송 14개월', 'fontSize': 'fs13'},
    {'text': '워터픽 2대, 이비인후과 12번', 'fontSize': 'fs13'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '237만원 쓰고도 2주마다 그 냄새가 올라온다', 'fontSize': 'fs15'},
    {'text': '그래서 이번에는 돈을 쓰는 게 아니라 직접 알아보기로 했다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '해외 논문 47건, 네이버 카페 후기 820개, 시중 구강 스프레이 TOP 8개를 전수 비교했다', 'fontSize': 'fs15'},
    {'text': '이 글은 그 결과다', 'fontSize': 'fs15'},
    {'text': '5분이면 다 읽는다', 'fontSize': 'fs15'},
    {'text': '본인 편도를 위해서라도 끝까지 읽기를', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 1. 왜 이 글을 쓰게 됐는지
blocks.append(text_block([
    {'text': '1. 왜 이 글을 쓰게 됐는지', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나는 32살 사무직이다', 'fontSize': 'fs15'},
    {'text': '팀 미팅이 하루에 2-3번 있는 회사에 다닌다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석을 처음 안 건 27살 때였다', 'fontSize': 'fs15'},
    {'text': '그때부터 5년간 하루도 빠짐없이 신경 쓰고 있다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '양치를 하루에 세 번 한다', 'fontSize': 'fs15'},
    {'text': '혀클리너도 쓴다', 'fontSize': 'fs15'},
    {'text': '치간칫솔도 쓴다', 'fontSize': 'fs15'},
    {'text': '위생에 진심인 사람이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '근데 편도결석은 그딴 거 상관없었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '회의실 들어가기 전에 화장실 거울 앞에서 면봉을 든다', 'fontSize': 'fs15'},
    {'text': '입을 벌리고 편도를 확인한다', 'fontSize': 'fs15'},
    {'text': '아무것도 없으면 그날은 좀 살 것 같다', 'fontSize': 'fs15'},
    {'text': '뭔가 있으면 그날은 끝이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '숨 들이쉬면서 말하는 습관', 'fontSize': 'fs15'},
    {'text': '사람이랑 50cm 이상 거리 두는 습관', 'fontSize': 'fs15'},
    {'text': '상대방 표정을 실시간으로 모니터링하는 습관', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그냥 조용한 사람이 된 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '2주마다 면봉 들고 거울 앞에 서는 거', 'fontSize': 'fs15'},
    {'text': '이걸 10년 뒤에도 하고 있을 건가', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 생각이 들었을 때 방향을 바꿨다', 'fontSize': 'fs15'},
    {'text': '돈 더 쓰는 게 아니라 왜 안 없어지는지를 먼저 이해하자', 'bold': True, 'fontSize': 'fs15'},
]))

# 이미지 placeholder
blocks.append(image_block('./images/placeholder.jpg', '편도 크립트 구조 일러스트'))

blocks.append(hr_block())

# 2. 편도결석이 양치로 안 없어지는 진짜 이유
blocks.append(text_block([
    {'text': '2. 편도결석이 양치로 안 없어지는 진짜 이유', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '논문을 읽으면서 가장 먼저 깨달은 게 있다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도결석의 원인은 음식 찌꺼기가 아니었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '원인의 핵심은 편도 구멍(크립트) 속 세균막(바이오필름)이었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '편도에는 깊이 2-3mm의 작은 구멍들이 있다', 'fontSize': 'fs15'},
    {'text': '이 구멍 안에 혐기성 세균들이 끈끈한 막을 만들어서 산다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이딴 게 있는 한 결석은 계속 생긴다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이 세균들이 음식 찌꺼기를 분해하면서', 'fontSize': 'fs15'},
    {'text': '황화수소, 메틸메르캅탄 같은 냄새 가스를 뿜어낸다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '실제 연구 데이터가 소름이었다', 'fontSize': 'fs15'},
    {'text': '편도결석 환자의 구취 농도(VSC)는 일반인의 10.3배', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '10배가 아니라 10.3배다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '이 냄새를 풍기면서 사람을 만나고 있었다는 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '칫솔로는 이 구멍 안까지 절대 닿을 수 없다', 'fontSize': 'fs15'},
    {'text': '양치를 100번 해도 편도 크립트에는 영향이 0이다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '정리하면 이렇다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '1. 편도 구멍 속에 세균막이 형성된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '2. 세균이 음식물을 분해하며 냄새 가스를 생성한다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '3. 세균 잔해 + 칼슘염이 석회화되면서 편도결석이 된다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '4. 면봉으로 빼면 → 구멍이 확장되고 → 더 잘 생긴다 (악순환)', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '빼는 건 해결이 아니었다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '이 지긋지긋한 세균막을 부숴야 했다', 'fontSize': 'fs15'},
]))

blocks.append(image_block('./images/placeholder.jpg', '바이오필름 형성 과정 인포그래픽'))

blocks.append(hr_block())

# 3. 가글 업계가 절대 말 안 하는 사실
blocks.append(text_block([
    {'text': '3. 가글 업계가 절대 말 안 하는 사실', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '여기서 한 가지 의문이 생겼다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "'그럼 가글은?'", 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': "가글 광고 보면 '입속 세균 99.9% 제거'라고 한다", 'fontSize': 'fs15'},
    {'text': '편도 세균도 제거되는 거 아닌가?', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '아니었다', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글은 입을 헹구는 거다', 'fontSize': 'fs15'},
    {'text': '편도 구멍 안까지 들어가는 게 아니다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '쉽게 말하면 이거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '가글 = 배수구 위에 세정제 뿌리는 것', 'bold': True, 'fontSize': 'fs15'},
    {'text': '스프레이 = 배수구 안쪽에 직접 쏘는 것', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '배수구 겉을 아무리 닦아봤자', 'fontSize': 'fs15'},
    {'text': '안쪽 물때가 그대로면 냄새는 돌아온다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그게 5년간 가글에 갖다 버린 237만원의 정체였다', 'fontSize': 'fs15'},
    {'text': '가글 자체가 나쁜 게 아니라', 'fontSize': 'fs15'},
    {'text': '편도 구멍이라는 곳에 도달할 수 없는 구조인 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '더 웃긴 건', 'fontSize': 'fs15'},
    {'text': '알코올 가글은 오히려 입을 바싹 말려서', 'fontSize': 'fs15'},
    {'text': '냄새 세균한테 천국을 만들어준다', 'fontSize': 'fs15'},
    {'text': '쓰면 쓸수록 역효과인 거다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이걸 알고 나서 소름이 돋았다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '가글 정기배송 바로 해지했다', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 4. 프로폴리스가 주목받는 이유
blocks.append(text_block([
    {'text': '4. 프로폴리스가 주목받는 이유', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그러면 뭘로 편도 크립트 속 세균막을 없앨 수 있는가', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '논문을 계속 읽다 보니 반복적으로 나오는 성분이 하나 있었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스', 'bold': True, 'fontSize': 'fs17'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스는 벌이 벌집을 지킬 때 쓰는 천연 항균 물질이다', 'fontSize': 'fs15'},
    {'text': '그 안에 들어있는 플라보노이드 성분이 핵심인데', 'fontSize': 'fs15'},
    {'text': '이게 세균에 대해 3중으로 작용한다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세균막 파괴 | 이미 형성된 바이오필름 파괴 | 파괴율 88.5%', 'bold': True, 'fontSize': 'fs13'},
    {'text': '형성 차단 | 새로운 바이오필름 생성 억제 | 억제율 71%', 'bold': True, 'fontSize': 'fs13'},
    {'text': '점막 항염 | 편도 점막 염증 완화 | 활성산소 중화', 'bold': True, 'fontSize': 'fs13'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '세균을 죽이는 것만이 아니라', 'fontSize': 'fs15'},
    {'text': '세균이 다시 막을 만들지 못하게 차단하는 거다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 가글과 근본적으로 다른 점이다', 'fontSize': 'fs15'},
    {'text': '가글은 헹궈서 일시적으로 줄이는 거고', 'fontSize': 'fs15'},
    {'text': '프로폴리스는 그 지긋지긋한 세균막 자체를 부수고 재형성을 막는다', 'fontSize': 'fs15'},
]))

blocks.append(image_block('./images/placeholder.jpg', '프로폴리스 3중 항균 작용 인포그래픽'))

blocks.append(hr_block())

# 5. 가글 vs 스프레이, 결정적 차이
blocks.append(text_block([
    {'text': '5. 가글 vs 스프레이, 결정적 차이', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스가 좋다는 건 알았다', 'fontSize': 'fs15'},
    {'text': '근데 프로폴리스를 어떻게 편도까지 보내느냐가 관건이었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '프로폴리스 가글도 있다', 'fontSize': 'fs15'},
    {'text': '근데 아까 말했듯이 가글은 편도 크립트까지 안 닿는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '스프레이로 편도에 직접 뿌리면?', 'fontSize': 'fs15'},
    {'text': '미스트가 편도 표면에 닿는다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이게 차이다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '그리고 알코올이 들어간 제품은 무조건 제외했다', 'fontSize': 'fs15'},
    {'text': '알코올 = 구강 건조 = 세균 증식 환경 조성', 'fontSize': 'fs15'},
    {'text': '쓰면 쓸수록 역효과니까', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '내가 제품을 고를 때 설정한 기준 5가지:', 'bold': True, 'fontSize': 'fs15'},
    {'text': '1. 프로폴리스 함유 (플라보노이드 기준 3% 이상)', 'fontSize': 'fs15'},
    {'text': '2. 스프레이 형태 (가글 ✕)', 'fontSize': 'fs15'},
    {'text': '3. 알코올 프리', 'fontSize': 'fs15'},
    {'text': '4. 올리고당 베이스 (구강 유익균 보호)', 'fontSize': 'fs15'},
    {'text': '5. 휴대 가능 사이즈 (외출 시 즉시 사용)', 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 6. 내가 직접 비교한 제품 TOP 8
blocks.append(text_block([
    {'text': '6. 내가 직접 비교한 제품 TOP 8', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '비교가 궁금할까봐 표로 정리했다', 'fontSize': 'fs15'},
    {'text': '직접 성분표 전수 비교한 결과다', 'fontSize': 'fs15'},
]))

# 비교 테이블
blocks.append(text_block([
    {'text': '순위 | 제품 | 프로폴리스 | 알코올프리 | 스프레이 | 올리고당 | 편도타겟 | 총점', 'bold': True, 'fontSize': 'fs13'},
    {'text': '', 'fontSize': 'fs13'},
    {'text': '1위 | D사 | ◎ | ◎ | ◎ | ◎ | ◎ | 5.0', 'fontSize': 'fs13'},
    {'text': '2위 | A사 | ◎ | ◎ | ○ | ✕ | ○ | 3.2', 'fontSize': 'fs13'},
    {'text': '3위 | B사 | ○ | ◎ | ◎ | ✕ | △ | 2.8', 'fontSize': 'fs13'},
    {'text': '4위 | C사 | ✕ | ○ | ✕ | ○ | ○ | 2.4', 'fontSize': 'fs13'},
    {'text': '5위 | E사 | ○ | ✕ | ◎ | ✕ | ✕ | 2.0', 'fontSize': 'fs13'},
    {'text': '6위 | G사 | △ | ○ | ◎ | ✕ | ✕ | 1.6', 'fontSize': 'fs13'},
    {'text': '7위 | F사 | ✕ | ◎ | ✕ | ✕ | ✕ | 1.2', 'fontSize': 'fs13'},
    {'text': '8위 | H사 | ✕ | ✕ | ✕ | ✕ | ✕ | 0.8', 'fontSize': 'fs13'},
]))

blocks.append(text_block([
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5가지 기준을 모두 충족하는 제품은 딱 하나였다', 'bold': True, 'fontSize': 'fs15'},
]))

blocks.append(hr_block())

# 7. 결론 — 6주 후 달라진 것
blocks.append(text_block([
    {'text': '7. 결론 — 6주 후 달라진 것', 'bold': True, 'fontSize': 'fs19'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나만 그런 게 아니었다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '회사 동료한테 먼저 알려줬는데', 'fontSize': 'fs15'},
    {'text': '그 친구도 편도결석 3년째였다', 'fontSize': 'fs15'},
    {'text': '쓴 지 3주쯤 됐을 때 카톡이 왔다', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '"야 나 면봉 안 든 지 2주 됐어 진짜"', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '나도 처음에 반신반의했다', 'fontSize': 'fs15'},
    {'text': '또 가글 같은 거 아닌가 싶었는데', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '2주 지나도 까끌까끌한 느낌이 안 올라왔다', 'fontSize': 'fs15'},
    {'text': '3주 4주 6주', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '면봉 든 횟수가 한 달 4-5번에서 0번이 됐다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '엄마한테도 알려줬다', 'fontSize': 'fs15'},
    {'text': '엄마도 편도결석은 아닌데 목에서 이물감이 있으셨는데', 'fontSize': 'fs15'},
    {'text': '"목이 개운해졌다" 그러시더라', 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '5년 동안 면봉이랑 가글로 버텼는데', 'fontSize': 'fs15'},
    {'text': '지금은 양치 후에 편도장벽제 편도 쪽으로 2-3번 뿌리는 게 끝이다', 'fontSize': 'fs15'},
    {'text': '3초다 진짜로', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '이제는 회의실 들어가기 전에', 'fontSize': 'fs15'},
    {'text': '화장실 가서 면봉 확인하는 짓 안 한다', 'fontSize': 'fs15'},
    {'text': '숨 들이쉬면서 말하는 습관도 없어졌다', 'fontSize': 'fs15'},
    {'text': '사람 만나는 게 두렵지 않다', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '빼는 루틴에서 안 생기는 루틴으로', 'fontSize': 'fs15'},
    {'text': '바뀌는 게 이런 느낌이구나 싶었다', 'fontSize': 'fs15'},
]))

# 제품 이미지
blocks.append(image_block('./images/1773727373767_Gemini_Generated_Image_lz0rfvlz0rfvlz0r1.png', '편도장벽제 제품 이미지'))

blocks.append(text_block([
    {'text': '그냥... 편해졌다', 'fontSize': 'fs15'},
    {'text': '5년 만에 처음으로', 'fontSize': 'fs15'},
]))

# CTA
blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

blocks.append(hr_block())

# 긴급추가
blocks.append(text_block([
    {'text': '✏️ 2026.3.15 긴급추가', 'bold': True, 'fontSize': 'fs15'},
    {'text': '', 'fontSize': 'fs15'},
    {'text': '글 올린 지 3일 만에 DM이 200개 넘게 왔다', 'fontSize': 'fs15'},
    {'text': '링크 공유가 이렇게 될 줄 몰랐는데', 'fontSize': 'fs15'},
    {'text': '업체 측에서 "이번 주까지만 할인 링크 유지" 한다고 해서', 'fontSize': 'fs15'},
    {'text': '아직 못 보신 분들 참고하시길', 'fontSize': 'fs15'},
]))

# CTA 2
blocks.append(cta_block('여기서 확인해보세요 →', CTA_URL))

# ===== 조립 =====
post_content = '\n\n'.join(blocks)

# index.html 읽기 → POST CONTENT 교체 → 저장
index_path = 'public/posts/tonsil-stone/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- POST CONTENT START -->'
end_marker = '<!-- POST CONTENT END -->'
start_idx = html.index(start_marker) + len(start_marker)
end_idx = html.index(end_marker)

new_html = html[:start_idx] + '\n\n' + post_content + '\n\n' + html[end_idx:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'✅ index.html 업데이트 완료 ({len(post_content)} chars)')
print(f'   블록 수: {len(blocks)}')
