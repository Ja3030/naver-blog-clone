#!/usr/bin/env python3
"""SA 어드버토리얼 v2 — 가독성 개선 + 이미지 삽입
기존 demodex-rosacea 포스트 이미지를 상대경로로 참조"""

import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, 'templates', 'post-template.html')
POSTS_DIR = os.path.join(BASE, 'public', 'posts')

# 이미지 경로 (demodex-rosacea 포스트에서 참조)
IMG = '/posts/demodex-rosacea/images/'
IMAGES = {
    'before_after': IMG + '1775151355225_Group31.png',
    'skin_clinic': IMG + '1775151468371_image1.png',
    'cream_shelf': IMG + '1775151535266_Group4.png',
    'flareup': IMG + '1775151566587_image2.png',
    'cream_bottles': IMG + '1775151631403_image4.png',
    'paper': IMG + '1775151674129__2024-07-03__5.18.57.png',
    'vicious_cycle': IMG + '1775151686894_image5.png',
    'demodex_micro1': IMG + '1775154179435_hf_20260402_181847_94d95c10-9ba2-4e84-95c3-04a8fb4d0431.png',
    'demodex_micro2': IMG + '1775153955951_hf_20260402_181605_8aee6e37-ce9a-430d-b6d9-a9cc59a6f10e.png',
    'demodex_compare': IMG + '1775153934074_hf_20260402_181634_e14ef78b-2c3a-4366-a0b3-8e38bd988937.png',
    'cycle_info': IMG + '1775153583449_Group7.png',
    'product': IMG + '1775154473754_hf_20260402_182401_d837551c-7bbd-45e3-bc4d-dd2216eacb01.png',
    'result_timeline': IMG + '1775152007060_Group5.png',
    'product_spec': IMG + '1775152022378_Group6.png',
}

CTA_URL = "https://soricare.com/product/detail.html?product_no=64&utm_source=google&utm_medium=cpc&utm_campaign=sa_{slug}"

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def p_tag(text, fs='fs15', bold=False, color=None):
    if not text.strip():
        return '      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span class="se-fs-fs15 se-ff-system"><br></span>\n      </p>'
    inner = esc(text)
    if bold:
        inner = f'<b>{inner}</b>'
    style = f' style="color:{color};"' if color else ''
    return f'      <p class="se-text-paragraph se-text-paragraph-align- ">\n        <span{style} class="se-fs-{fs} se-ff-system">{inner}</span>\n      </p>'

def text_block(paras):
    return f'''<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
{chr(10).join(paras)}
    </div>
  </div>
</div>'''

def img_block(src, alt=''):
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


# ===== 각 포스트별 수동 구성 (가독성 + 이미지 최적 배치) =====

def build_c1():
    """C1 모낭충 직접"""
    blocks = []

    # 오프닝
    blocks.append(text_block([
        p_tag('모낭충 검색하다가 여기까지 오신 거죠..', fs='fs19'),
        p_tag(''),
        p_tag('저도 그랬어요.', fs='fs19'),
        p_tag(''),
        p_tag(''),
        p_tag('저는 올해 32살이고 평범한 직장인인데요.'),
        p_tag('2년 전부터 얼굴이 이상해지더니 지금까지도 안 낫고 있어요.'),
        p_tag('매일 아침 일어나면 볼이 뜨거워요. 이게 2년째예요.'),
    ]))

    # 피부과
    blocks.append(text_block([
        p_tag(''),
        p_tag('처음엔 그냥 트러블인 줄 알고 동네 피부과 갔거든요.'),
        p_tag('거기서 주사피부염이라고 하시더라고요.'),
        p_tag('수란트라 처방받고 집에 왔는데 바른 지 5일 만에 얼굴이 완전 뒤집어져서 회사도 못 나갔어요.'),
    ]))
    blocks.append(img_block(IMAGES['flareup'], '뒤집어진 피부'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('선생님한테 전화했더니'),
        p_tag('"명현반응일 수 있으니 좀 더 써보세요"'),
        p_tag('하시는데'),
        p_tag('솔직히 그 상태로 출근할 수가 없었거든요.'),
        p_tag('결국 끊었어요.', fs='fs19'),
    ]))

    # 크림 실패
    blocks.append(text_block([
        p_tag(''),
        p_tag('끊고 나니까 뭘 발라야 하는지 모르겠는 거예요.'),
        p_tag('그래서 장벽크림이 좋다길래 에스트라 아토베리어 샀거든요 올리브영에서.'),
        p_tag('근데 안 맞는 것 같아서 바꾸고.. 또 바꾸고..'),
        p_tag('올리브영 세일할 때마다 하나씩 사게 되더라고요.'),
        p_tag('세면대에 크림만 늘어나고..'),
    ]))
    blocks.append(img_block(IMAGES['cream_bottles'], '세면대 크림들'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('남자친구가 어느 날 "너 또 크림 샀어?" 하는데'),
        p_tag('별 뜻 없이 한 건데 왜 그렇게 속상하던지..'),
    ]))

    # 잃어버린 것들
    blocks.append(text_block([
        p_tag(''),
        p_tag('그게 속상했던 게 크림만의 문제가 아니었거든요.'),
        p_tag('제가 원래 매운 거 엄청 좋아했는데 마라탕 짬뽕 이런 거요.'),
        p_tag('근데 매운 거 먹으면 얼굴이 빨개지니까 안 먹게 됐어요.'),
        p_tag('2년째 한번도 못 먹었어요.'),
        p_tag('회사 점심에 국물 나와도 얼굴이 달아올라서 고개 숙이고 빨리 먹고 먼저 나오는 게 습관이 됐고요.'),
        p_tag(''),
        p_tag('주말에 친구가 보자고 하면 그날 아침에 거울부터 보게 되더라고요.'),
        p_tag('빨가면 안 나가요. 핑계 대고 취소하고..'),
        p_tag('한번은 한 달에 약속 3개 잡았는데 2개를 취소한 적 있어요.'),
        p_tag('그때 집에 와서 사진 보다가 2년 전 사진이 뜨더라고요.'),
        p_tag('친구들이랑 고기집에서 찍은 건데 그때는 아무 데나 가고 아무거나 먹고 아무나 만났거든요.'),
        p_tag('지금은 전부 거울부터 보고 결정해요.'),
    ]))

    blocks.append(hr_block())

    # 모낭충 발견
    blocks.append(text_block([
        p_tag(''),
        p_tag('그래서 새벽에 또 검색을 하게 되더라고요.'),
        p_tag('뭐라도 찾아보자 싶어서 이것저것 찾다가 모낭충이라는 걸 알게 됐는데요.', fs='fs19'),
        p_tag(''),
        p_tag('솔직히 처음엔 소름 돋았어요.'),
        p_tag('내 모공에 벌레가 산다고..?'),
    ]))
    blocks.append(img_block(IMAGES['demodex_micro1'], '모낭충 현미경'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('엄마한테 전화했더니'),
        p_tag('"무슨 벌레가 얼굴에 살아 말도 안 돼" 이러시는데'),
        p_tag('진짜였어요.'),
    ]))

    # 비누 실패 → RC 교육
    blocks.append(text_block([
        p_tag(''),
        p_tag('그래서 모낭충 비누 찾아봤는데 티트리 비누 유황 비누 이런 거 나오길래'),
        p_tag('한 달 넘게 열심히 세안했거든요.'),
        p_tag('근데 안 나아요.'),
        p_tag('아침에 일어나면 볼이 뜨거운 건 똑같고..'),
        p_tag('또 실패인가 싶어서 진짜 포기하려다가'),
        p_tag('왜 안 되는 건지 한번만 더 찾아보자 싶었어요.'),
        p_tag(''),
        p_tag('그때 알게 된 건데요.'),
        p_tag('모낭충이 밤에만 활동한다고 하더라고요.', fs='fs19'),
    ]))
    blocks.append(img_block(IMAGES['demodex_micro2'], '모낭충 야행성 활동'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('낮에는 모공 안에 숨어있다가 밤에 모공 밖으로 나와서'),
        p_tag('세균을 묻히고 다시 들어가고.'),
        p_tag('그 세균이 염증을 만들고 그게 장벽을 부수는 거래요.'),
        p_tag(''),
        p_tag('그러니까 아침에 비누로 아무리 열심히 씻어도 30초 씻고 끝이잖아요.'),
        p_tag('모공 안에 있는 놈한테는 아무것도 안 한 거더라고요..'),
    ]))
    blocks.append(img_block(IMAGES['vicious_cycle'], '악순환 사이클'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('그걸 알고 나니까 수란트라도 이해가 되는 거예요.'),
        p_tag('죽이긴 하는데 환경 자체를 안 바꾸니까 끊으면 다시 번식한대요.'),
        p_tag('그래서 끊으면 돌아오는 거였어요..'),
        p_tag(''),
        p_tag('2년 동안 왜 뭘 해도 안 됐던 이유가 그제서야 이해가 됐어요.', fs='fs19'),
        p_tag('결국 핵심은 모공 안에서 모낭충이 못 사는 환경을 만드는 거더라고요.', fs='fs19'),
        p_tag('죽이는 게 아니라 환경을 바꾸는 거.'),
    ]))

    blocks.append(hr_block())

    # 제품 발견
    blocks.append(text_block([
        p_tag(''),
        p_tag('그래서 밤에 바르는 크림을 찾기 시작했어요.'),
        p_tag('비누는 씻고 끝이니까 의미가 없고 밤새 모공 안에 남아있으면서 환경을 바꿔야 하니까요.'),
        p_tag('찾다 보니까 티트리 성분이 모낭충한테 잘 듣는다는 게 나오더라고요.'),
        p_tag('근데 보통 화장품에는 티트리가 0.1~0.5%밖에 안 들어간대요.'),
        p_tag('그 정도로는 모공 안까지 안 된다고..'),
        p_tag(''),
        p_tag('그러다가 1% 넘게 들어간 크림을 하나 찾았는데요.'),
        p_tag('1.07%라고 하더라고요.', fs='fs19'),
        p_tag('그리고 크림이니까 밤에 바르면 안 씻겨나가고 8시간 동안 모공 안에 남아있는 거요.', fs='fs19'),
        p_tag('비누 30초 vs 크림 8시간이면 접촉 시간 자체가 비교가 안 되는 거였어요.'),
        p_tag('거기다 유익균을 복원하는 성분도 있어서 모낭충 환경을 바꾸면서 다시 안 돌아오게 만드는 구조라고..'),
    ]))
    blocks.append(img_block(IMAGES['product'], '티트리셀 제품'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('솔직히 또 속는 건 아닌가 싶었어요.'),
        p_tag('세면대에 크림만 쌓여가는 거 또 반복하기 싫었거든요.'),
        p_tag('근데 지금까지 해본 건 전부 겉에서 바르거나 씻어내는 거였고'),
        p_tag('이건 밤새 모공 안에서 환경을 바꾼다는 게 달랐어요.'),
        p_tag('한번만 더 해보자 싶었어요.'),
    ]))

    # 결과
    blocks.append(text_block([
        p_tag(''),
        p_tag('1주차에는 솔직히 모르겠더라고요. 뭐가 달라진 건지..'),
        p_tag(''),
        p_tag('근데 2주차 어느 아침에 눈 뜨고 볼에 손을 댔는데'),
        p_tag('안 뜨거운 거예요.', fs='fs19'),
        p_tag(''),
        p_tag('거울을 봤는데'),
        p_tag('빨갛긴 한데.. 평소보다 확실히 덜했어요.'),
    ]))
    blocks.append(img_block(IMAGES['result_timeline'], '변화 타임라인'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('남자친구한테 따로 말 안 했는데 한 달쯤 됐을 때 알아서 그러더라고요.'),
        p_tag(''),
        p_tag('"너 요즘 피부 좀 괜찮아진 거 아니야?"', fs='fs19'),
        p_tag(''),
        p_tag('그 말 듣고 좀 울었어요 ㅠ..'),
        p_tag('마라탕 못 먹고 약속 취소하고 고개 숙이고 밥 먹던 게 한꺼번에 올라와서..'),
    ]))

    blocks.append(hr_block())

    # 마무리
    blocks.append(text_block([
        p_tag(''),
        p_tag('아직 완치는 아니에요.'),
        p_tag('확신도 없어요 솔직히.'),
        p_tag('근데 2년 동안 뭘 해도 안 달라지던 아침이 달라지긴 했어요.'),
        p_tag(''),
        p_tag('혹시 모낭충 때문에 같은 고민이신 분 있으면'),
        p_tag('비누 말고 밤에 바르는 크림 쪽으로 찾아보세요.'),
        p_tag('저는 그게 전환점이었어요.'),
    ]))

    blocks.append(hr_block())

    # 추가/수정
    blocks.append(text_block([
        p_tag('추가) 제품 뭐냐고 물어보시는 분이 많아서..', bold=True, fs='fs13', color='#666'),
        p_tag('티트리셀이라는 크림이에요.'),
        p_tag('자세한 건 여기서 보실 수 있어요.'),
    ]))
    blocks.append(oglink_block('c1_demodex'))
    blocks.append(img_block(IMAGES['product_spec'], '제품 스펙'))
    blocks.append(text_block([
        p_tag(''),
        p_tag('올리브영에는 없고 여기서만 살 수 있더라고요.'),
        p_tag(''),
        p_tag('수정) 가격 물어보시는 분들 있어서 추가하면', bold=True, fs='fs13', color='#666'),
        p_tag('49,900원인데 피부과 한 달 다니는 것보다는 싸요..'),
        p_tag('저는 피부과만 2년 동안 얼마를 쓴 건지..'),
        p_tag(''),
        p_tag('혹시 써보신 분 있으면 댓글로 알려주세요.'),
        p_tag('저만 이런 건지 궁금해서요..'),
    ]))

    return '\n\n'.join(blocks)


def inject_and_save(slug, se_html, config_data):
    post_dir = os.path.join(POSTS_DIR, slug)
    os.makedirs(os.path.join(post_dir, 'images'), exist_ok=True)

    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    start = '<!-- POST CONTENT START -->'
    end = '<!-- POST CONTENT END -->'
    si = template.index(start)
    ei = template.index(end)
    before = template[:si + len(start)]
    after = template[ei:]
    html = before + '\n\n' + se_html + '\n\n' + after

    with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(post_dir, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print(f'  ✅ {slug}/')


# ===== 실행 =====
print('🚀 SA v2 빌드 시작 (가독성 + 이미지)\n')

# C1만 먼저 빌드 — 확인 후 나머지 추가
inject_and_save('sa-demodex-direct', build_c1(), {
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
})

print('\n✅ C1 빌드 완료 — 확인 후 나머지 4개 추가')
print('URL: /posts/sa-demodex-direct/')
