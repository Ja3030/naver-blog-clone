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


# 약어 헬퍼
BR = p_tag('')  # 빈 줄
def RED(text, fs='fs19'): return p_tag(text, fs=fs, bold=True, color='rgb(255, 0, 16)')
def BLUE(text, fs='fs19'): return p_tag(text, fs=fs, bold=True, color='rgb(0, 0, 255)')
def BIG(text): return p_tag(text, fs='fs19')
def BOLD(text): return p_tag(text, bold=True)
def NORM(text): return p_tag(text)
def GRAY(text): return p_tag(text, fs='fs13', color='#666', bold=True)


def build_c1():
    """C1 모낭충 직접"""
    blocks = []

    # 오프닝
    blocks.append(text_block([
        BIG('모낭충 검색하다가 여기까지 오신 거죠..'),
        BR,
        BIG('저도 그랬어요.'),
        BR, BR, BR,
        NORM('저는 올해 32살이고 평범한 직장인인데요.'),
        NORM('2년 전부터 얼굴이 이상해지더니 지금까지도 안 낫고 있어요.'),
        BR,
        RED('매일 아침 일어나면 볼이 뜨거워요'),
        RED('이게 2년째예요'),
        BR, BR,
    ]))

    # 피부과
    blocks.append(text_block([
        NORM('처음엔 그냥 트러블인 줄 알고 동네 피부과 갔거든요.'),
        NORM('거기서 주사피부염이라고 하시더라고요.'),
        NORM('수란트라 처방받고 집에 왔는데'),
        BR,
        RED('바른 지 5일 만에 얼굴이 완전 뒤집어져서 회사도 못 나갔어요'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['flareup'], '뒤집어진 피부'))
    blocks.append(text_block([
        BR,
        NORM('선생님한테 전화했더니'),
        BOLD('"명현반응일 수 있으니 좀 더 써보세요"'),
        NORM('하시는데'),
        NORM('솔직히 그 상태로 출근할 수가 없었거든요.'),
        BR,
        RED('결국 끊었어요'),
        BR, BR, BR,
    ]))

    # 크림 실패
    blocks.append(text_block([
        NORM('끊고 나니까 뭘 발라야 하는지 모르겠는 거예요.'),
        NORM('그래서 장벽크림이 좋다길래 에스트라 아토베리어 샀거든요 올리브영에서.'),
        NORM('근데 안 맞는 것 같아서 바꾸고.. 또 바꾸고..'),
        NORM('올리브영 세일할 때마다 하나씩 사게 되더라고요.'),
        BR,
        BOLD('세면대에 크림만 늘어나고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['cream_bottles'], '세면대 크림들'))
    blocks.append(text_block([
        BR,
        NORM('남자친구가 어느 날 "너 또 크림 샀어?" 하는데'),
        NORM('별 뜻 없이 한 건데 왜 그렇게 속상하던지..'),
        BR, BR,
    ]))

    # 잃어버린 것들
    blocks.append(text_block([
        NORM('그게 속상했던 게 크림만의 문제가 아니었거든요.'),
        BR,
        NORM('제가 원래 매운 거 엄청 좋아했는데 마라탕 짬뽕 이런 거요.'),
        NORM('근데 매운 거 먹으면 얼굴이 빨개지니까 안 먹게 됐어요.'),
        BOLD('2년째 한번도 못 먹었어요.'),
        BR,
        NORM('회사 점심에 국물 나와도 얼굴이 달아올라서'),
        NORM('고개 숙이고 빨리 먹고 먼저 나오는 게 습관이 됐고요.'),
        BR,
        NORM('주말에 친구가 보자고 하면 그날 아침에 거울부터 보게 되더라고요.'),
        NORM('빨가면 안 나가요. 핑계 대고 취소하고..'),
        BR,
        NORM('한번은 한 달에 약속 3개 잡았는데 2개를 취소한 적 있어요.'),
        NORM('그때 집에 와서 사진 보다가 2년 전 사진이 뜨더라고요.'),
        NORM('친구들이랑 고기집에서 찍은 건데'),
        BOLD('그때는 아무 데나 가고 아무거나 먹고 아무나 만났거든요.'),
        BR,
        RED('지금은 전부 거울부터 보고 결정해요'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 모낭충 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그래서 새벽에 또 검색을 하게 되더라고요.'),
        NORM('뭐라도 찾아보자 싶어서 이것저것 찾다가'),
        BR,
        RED('모낭충이라는 걸 알게 됐는데요'),
        BR,
        NORM('솔직히 처음엔 소름 돋았어요.'),
        BOLD('내 모공에 벌레가 산다고..?'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro1'], '모낭충 현미경'))
    blocks.append(text_block([
        BR,
        NORM('엄마한테 전화했더니'),
        BOLD('"무슨 벌레가 얼굴에 살아 말도 안 돼"'),
        NORM('이러시는데'),
        BR,
        BOLD('진짜였어요.'),
        BR, BR,
    ]))

    # 비누 실패 → RC 교육
    blocks.append(text_block([
        NORM('그래서 모낭충 비누 찾아봤는데 티트리 비누 유황 비누 이런 거 나오길래'),
        NORM('한 달 넘게 열심히 세안했거든요.'),
        BR,
        BOLD('근데 안 나아요.'),
        BR,
        NORM('아침에 일어나면 볼이 뜨거운 건 똑같고..'),
        NORM('또 실패인가 싶어서 진짜 포기하려다가'),
        NORM('왜 안 되는 건지 한번만 더 찾아보자 싶었어요.'),
        BR, BR,
        NORM('그때 알게 된 건데요.'),
        BR,
        RED('모낭충이 밤에만 활동한다고 하더라고요'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro2'], '모낭충 야행성 활동'))
    blocks.append(text_block([
        BR,
        NORM('낮에는 모공 안에 숨어있다가'),
        BOLD('밤에 모공 밖으로 나와서'),
        NORM('세균을 묻히고 다시 들어가고.'),
        NORM('그 세균이 염증을 만들고 그게 장벽을 부수는 거래요.'),
        BR,
        NORM('그러니까 아침에 비누로 아무리 열심히 씻어도'),
        BOLD('30초 씻고 끝이잖아요.'),
        RED('모공 안에 있는 놈한테는 아무것도 안 한 거더라고요..', fs='fs15'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['vicious_cycle'], '악순환 사이클'))
    blocks.append(text_block([
        BR,
        NORM('그걸 알고 나니까 수란트라도 이해가 되는 거예요.'),
        NORM('죽이긴 하는데 환경 자체를 안 바꾸니까'),
        BOLD('끊으면 다시 번식한대요.'),
        NORM('그래서 끊으면 돌아오는 거였어요..'),
        BR, BR,
        RED('2년 동안 왜 뭘 해도 안 됐던 이유가 그제서야 이해가 됐어요'),
        BR,
        BLUE('결국 핵심은'),
        BLUE('모공 안에서 모낭충이 못 사는 환경을 만드는 거더라고요'),
        BLUE('죽이는 게 아니라 환경을 바꾸는 거'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 제품 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그래서 밤에 바르는 크림을 찾기 시작했어요.'),
        NORM('비누는 씻고 끝이니까 의미가 없고'),
        NORM('밤새 모공 안에 남아있으면서 환경을 바꿔야 하니까요.'),
        BR,
        NORM('찾다 보니까 티트리 성분이 모낭충한테 잘 듣는다는 게 나오더라고요.'),
        NORM('근데 보통 화장품에는 티트리가 0.1~0.5%밖에 안 들어간대요.'),
        NORM('그 정도로는 모공 안까지 안 된다고..'),
        BR,
        NORM('그러다가 1% 넘게 들어간 크림을 하나 찾았는데요.'),
        RED('1.07%라고 하더라고요'),
        BR,
        BOLD('그리고 크림이니까 밤에 바르면 안 씻겨나가고'),
        RED('8시간 동안 모공 안에 남아있는 거요'),
        BR,
        NORM('비누 30초 vs 크림 8시간이면'),
        BOLD('접촉 시간 자체가 비교가 안 되는 거였어요.'),
        BR,
        NORM('거기다 유익균을 복원하는 성분도 있어서'),
        NORM('모낭충 환경을 바꾸면서 다시 안 돌아오게 만드는 구조라고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['product'], '티트리셀 제품'))
    blocks.append(text_block([
        BR,
        NORM('솔직히 또 속는 건 아닌가 싶었어요.'),
        NORM('세면대에 크림만 쌓여가는 거 또 반복하기 싫었거든요.'),
        BR,
        NORM('근데 지금까지 해본 건 전부 겉에서 바르거나 씻어내는 거였고'),
        BOLD('이건 밤새 모공 안에서 환경을 바꾼다는 게 달랐어요.'),
        NORM('한번만 더 해보자 싶었어요.'),
        BR, BR, BR,
    ]))

    # 결과
    blocks.append(text_block([
        NORM('1주차에는 솔직히 모르겠더라고요.'),
        NORM('뭐가 달라진 건지..'),
        BR, BR,
        NORM('근데 2주차 어느 아침에'),
        NORM('눈 뜨고 볼에 손을 댔는데'),
        BR,
        RED('안 뜨거운 거예요'),
        BR,
        NORM('거울을 봤는데'),
        NORM('빨갛긴 한데.. 평소보다 확실히 덜했어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['result_timeline'], '변화 타임라인'))
    blocks.append(text_block([
        BR,
        NORM('남자친구한테 따로 말 안 했는데'),
        NORM('한 달쯤 됐을 때 알아서 그러더라고요.'),
        BR,
        BLUE('"너 요즘 피부 좀 괜찮아진 거 아니야?"'),
        BR,
        NORM('그 말 듣고 좀 울었어요 ㅠ..'),
        NORM('마라탕 못 먹고 약속 취소하고 고개 숙이고 밥 먹던 게 한꺼번에 올라와서..'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 마무리
    blocks.append(text_block([
        BR,
        NORM('아직 완치는 아니에요.'),
        NORM('확신도 없어요 솔직히.'),
        BR,
        BOLD('근데 2년 동안 뭘 해도 안 달라지던 아침이 달라지긴 했어요.'),
        BR, BR,
        NORM('혹시 모낭충 때문에 같은 고민이신 분 있으면'),
        BOLD('비누 말고 밤에 바르는 크림 쪽으로 찾아보세요.'),
        NORM('저는 그게 전환점이었어요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 추가/수정
    blocks.append(text_block([
        BR,
        GRAY('추가) 제품 뭐냐고 물어보시는 분이 많아서..'),
        NORM('티트리셀이라는 크림이에요.'),
        NORM('자세한 건 여기서 보실 수 있어요.'),
        BR,
    ]))
    blocks.append(oglink_block('c1_demodex'))
    blocks.append(img_block(IMAGES['product_spec'], '제품 스펙'))
    blocks.append(text_block([
        BR,
        NORM('올리브영에는 없고 여기서만 살 수 있더라고요.'),
        BR, BR,
        GRAY('수정) 가격 물어보시는 분들 있어서 추가하면'),
        NORM('49,900원인데 피부과 한 달 다니는 것보다는 싸요..'),
        NORM('저는 피부과만 2년 동안 얼마를 쓴 건지..'),
        BR, BR,
        NORM('혹시 써보신 분 있으면 댓글로 알려주세요.'),
        NORM('저만 이런 건지 궁금해서요..'),
        BR,
    ]))

    return '\n\n'.join(blocks)


def build_c5():
    """C5 수란트라 대안"""
    blocks = []

    # 오프닝
    blocks.append(text_block([
        BIG('수란트라 부작용 검색하다가 여기까지 오신 거죠..'),
        BR,
        BIG('저도 그랬어요.'),
        BR, BR, BR,
        NORM('저는 올해 32살 직장인이고요.'),
        NORM('주사피부염 진단받은 지 2년 됐어요.'),
        NORM('매일 아침 일어나면 볼이 뜨거운데 이게 안 낫고 있거든요.'),
        BR, BR,
    ]))

    # 수란트라 시작 → 뒤집어짐
    blocks.append(text_block([
        NORM('처음에 피부과에서 수란트라 처방받고 진짜 마지막이라 생각하고 시작했어요.'),
        NORM('카페에서 수란트라 후기 찾아보면 5일차에 뒤집어진다는 글이 많았는데'),
        NORM('설마 나도 그러겠어 싶었거든요.'),
        BR,
        RED('근데 진짜 5일차에 뒤집어졌어요'),
        BR,
        NORM('아침에 거울 봤는데 얼굴이 평소보다 두 배는 빨갛고'),
        NORM('좁쌀 같은 게 볼에 올라와 있는 거예요.'),
        RED('회사도 못 나갔어요'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['flareup'], '뒤집어진 피부'))
    blocks.append(text_block([
        BR,
        NORM('선생님한테 전화했더니 "명현반응이니까 2주만 버텨보세요" 하시는데'),
        NORM('솔직히 그 얼굴로 출근은 못 하거든요.'),
        NORM('남자친구가 보더니 "병원 잘못 간 거 아니야?" 하는데 그 말이 너무 서럽더라고요..'),
        BR, BR,
    ]))

    # 3개월 → 끊으면 재발
    blocks.append(text_block([
        NORM('2주를 버텼어요 진짜.'),
        NORM('좀 가라앉긴 했어요.'),
        BOLD('근데 그다음이 문제였거든요.'),
        BR,
        NORM('3개월 쓰고 피부과 선생님이 "이제 끊어도 될 것 같아요" 하셔서 끊었는데'),
        RED('2주 만에 다시 올라왔어요'),
        NORM('열감이랑 붉은기가 거의 원래대로 돌아온 거예요.'),
        BR, BR,
        NORM('그때 진짜 멘탈이 나갔어요.'),
        BOLD('3개월을 뒤집어지면서 버텼는데 끊으니까 다시 원점이라니.'),
        NORM('카페에 "수란트라 끊으면 돌아오나요" 검색했는데'),
        NORM('저 같은 사람이 엄청 많더라고요.'),
        BR, BR,
    ]))

    # 크림 실패 + 잃어버린 것들
    blocks.append(text_block([
        NORM('그러면서 장벽크림을 바꾸기 시작했어요.'),
        NORM('에스트라 아토베리어 사고 안 맞는 것 같으면 바꾸고..'),
        BOLD('세면대에 크림만 늘어나는데 아침마다 볼은 뜨겁고..'),
        BR, BR,
        NORM('그때쯤 제가 좋아하던 것들이 하나씩 사라지고 있었어요.'),
        BOLD('마라탕을 2년째 못 먹었어요 얼굴 빨개지니까.'),
        NORM('주말에 친구가 보자고 하면 그날 아침 거울부터 보게 되고.'),
        NORM('빨가면 핑계 대고 안 나가거든요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # RC 교육 — 수란트라가 왜 돌아오는지
    blocks.append(text_block([
        BR, BR,
        NORM('그러다가 새벽에 또 검색하다가'),
        NORM('수란트라가 왜 끊으면 돌아오는지를 찾아보게 됐어요.'),
        NORM('수란트라 성분이 이버멕틴인데 이게 모낭충을 죽이는 약이거든요.'),
        BR,
        NORM('근데 찾아보니까요.'),
        RED('수란트라가 모낭충을 죽이긴 하는데 모공 안 환경 자체를 안 바꾼대요'),
        NORM('죽여놔도 환경이 그대로니까 끊으면 다시 번식하는 거래요.'),
        NORM('그래서 끊으면 돌아오는 거였어요..'),
        BR, BR,
    ]))
    blocks.append(img_block(IMAGES['vicious_cycle'], '모낭충 환경 악순환'))
    blocks.append(text_block([
        BR,
        NORM('그걸 알고 나니까 3개월이 이해가 되는 거예요.'),
        NORM('바르는 동안은 죽이니까 괜찮다가'),
        BOLD('끊으면 모공 안 환경이 그대로니까 다시 사는 거였어요.'),
        BR, BR,
        BLUE('결국 핵심은 죽이는 게 아니라 환경을 바꾸는 거더라고요'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 제품 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그래서 모공 안 환경을 바꿀 수 있는 걸 찾기 시작했어요.'),
        NORM('수란트라는 처방약이라 매일 쓰기도 부담스럽고 끊으면 돌아오니까'),
        NORM('처방 없이 매일 쓸 수 있으면서 밤새 모공 안에서 환경을 바꾸는 게 필요했거든요.'),
        BR,
        NORM('찾다 보니까 티트리 성분이 모낭충한테 잘 듣는다는 게 나오더라고요.'),
        NORM('근데 보통 화장품에는 0.1~0.5%밖에 안 들어간대요.'),
        NORM('그 정도로는 모공 안까지 안 된다고..'),
        BR,
        NORM('그러다가 1% 넘게 들어간 크림을 찾았는데'),
        RED('1.07%라고 하더라고요'),
        BR,
        BOLD('그리고 크림이니까 밤에 바르면 안 씻겨나가고'),
        RED('8시간 동안 모공 안에 남아있는 거요'),
        BR,
        NORM('수란트라는 환경을 안 바꾸니까 끊으면 돌아오는데'),
        BOLD('이건 유익균을 복원하면서 환경 자체를 바꾸는 구조라고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['product'], '티트리셀 제품'))
    blocks.append(text_block([
        BR,
        NORM('솔직히 수란트라 3개월 쓰고 재발한 사람이'),
        NORM('크림 하나로 달라지겠어? 싶었어요.'),
        NORM('근데 수란트라랑 근본적으로 다른 게'),
        BOLD('죽이기가 아니라 환경을 바꾼다는 거였거든요.'),
        NORM('한번만 더 해보자 싶었어요.'),
        BR, BR, BR,
    ]))

    # 결과
    blocks.append(text_block([
        NORM('1주차에는 모르겠더라고요.'),
        BR,
        NORM('근데 2주차에 아침에 볼이 안 뜨거운 거예요.'),
        RED('수란트라 쓸 때 3개월 걸렸던 게 2주 만에..?'),
        NORM('솔직히 믿기지 않았어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['result_timeline'], '변화 타임라인'))
    blocks.append(text_block([
        BR,
        NORM('한 달쯤 됐을 때 남자친구가 알아서 그러더라고요.'),
        BR,
        BLUE('"너 요즘 피부 좀 괜찮아진 거 아니야?"'),
        BR,
        NORM('그 말 듣고 좀 울었어요 ㅠ..'),
        NORM('수란트라 뒤집어지면서 버텼던 거랑 끊고 돌아왔던 거랑 한꺼번에 올라와서..'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 마무리
    blocks.append(text_block([
        BR,
        NORM('아직 완치는 아니에요.'),
        NORM('확신도 없어요 솔직히.'),
        BR,
        BOLD('근데 수란트라 끊고 돌아왔을 때의 그 절망감은 지금은 없어요.'),
        NORM('환경을 바꾸는 거니까 끊어도 돌아올 이유가 없다는 게 다르더라고요.'),
        BR, BR,
        NORM('혹시 수란트라 쓰면서 같은 고민이신 분 있으면'),
        BOLD('죽이기가 아니라 환경 바꾸기 쪽으로 찾아보세요.'),
        NORM('저는 그게 전환점이었어요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 추가/수정
    blocks.append(text_block([
        BR,
        GRAY('추가) 제품 뭐냐고 물어보시는 분이 많아서..'),
        NORM('티트리셀이라는 크림이에요.'),
        NORM('자세한 건 여기서 보실 수 있어요.'),
        BR,
    ]))
    blocks.append(oglink_block('c5_soolantra'))
    blocks.append(img_block(IMAGES['product_spec'], '제품 스펙'))
    blocks.append(text_block([
        BR,
        NORM('수란트라처럼 처방 필요 없고 매일 밤 바르면 되더라고요.'),
        BR, BR,
        GRAY('수정) 가격 물어보시는 분들 있어서 추가하면'),
        NORM('49,900원인데 수란트라 처방받으러 피부과 다니는 것보다는 싸요..'),
        BR, BR,
        NORM('혹시 써보신 분 있으면 댓글로 알려주세요.'),
        NORM('수란트라에서 넘어온 분 경험이 궁금해서요..'),
        BR,
    ]))

    return '\n\n'.join(blocks)


def build_c2():
    """C2 주사피부염"""
    blocks = []

    # 오프닝
    blocks.append(text_block([
        BIG('주사피부염 치료 검색하다가 여기까지 오신 거죠..'),
        BR,
        BIG('저도 그랬어요.'),
        BR, BR, BR,
        NORM('저는 올해 32살 직장인이고요.'),
        NORM('주사피부염 진단받은 지 2년 됐는데 아직도 안 낫고 있어요.'),
        RED('매일 아침 일어나면 볼이 뜨거워요. 이게 2년째예요.'),
        BR, BR,
    ]))

    # 피부과 진단 + 스테로이드
    blocks.append(text_block([
        NORM('처음에 얼굴이 빨개지길래 그냥 트러블인 줄 알았거든요.'),
        NORM('동네 피부과 갔더니 "주사피부염이에요" 하시는데 그게 뭔지도 몰랐어요.'),
        NORM('선생님이 설명해주시긴 했는데 솔직히 와닿는 건 "평생 관리해야 해요"밖에 없었어요.'),
        BR, BR,
        NORM('처음에 스테로이드 연고 처방받았거든요.'),
        BOLD('바르면 진짜 좋아져요. 하루 만에 붉은기가 확 빠지더라고요.'),
        NORM('근데 끊으면 이틀 만에 원래대로 돌아오고..'),
        NORM('그래서 계속 바르게 되는데 선생님이 "오래 쓰면 안 돼요" 하시거든요.'),
        RED('오래 쓰면 안 되는 걸 왜 처방해주시는 건지..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['skin_clinic'], '피부과 치료'))
    blocks.append(text_block([
        BR, BR,
    ]))

    # 수란트라 + 뒤집어짐
    blocks.append(text_block([
        NORM('그다음에 수란트라 처방받았어요.'),
        RED('바른 지 5일 만에 얼굴이 완전 뒤집어져서 회사도 못 나갔어요'),
        NORM('2주 버텨보라고 해서 버텼는데 좀 가라앉긴 했거든요.'),
        BOLD('근데 3개월 쓰고 끊었더니 2주 만에 다시 돌아왔어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['flareup'], '수란트라 뒤집어짐'))
    blocks.append(text_block([
        BR, BR,
    ]))

    # 레이저 + 한의원
    blocks.append(text_block([
        NORM('레이저도 해봤어요.'),
        NORM('브이빔 3회 맞았는데 맞을 때만 좀 괜찮고 한 달 지나면 다시 올라오더라고요.'),
        BOLD('1회에 15만원이었는데 3회면 45만원이거든요..'),
        BR,
        NORM('엄마한테 전화했더니 "한의원 가봐" 하셔서 한의원도 갔어요.'),
        NORM('약침이랑 한약 2개월 했는데 솔직히 달라진 게 모르겠더라고요.'),
        NORM('돈은 돈대로 시간도 많이 쓰고..'),
        BR, BR,
    ]))

    # 잃어버린 것들
    blocks.append(text_block([
        NORM('그 사이에 제 생활이 바뀌고 있었거든요.'),
        BOLD('마라탕을 2년째 못 먹었어요. 매운 거 먹으면 얼굴이 난리가 나니까.'),
        NORM('회사 점심에 국물 나와도 고개 숙이고 빨리 먹고 나오는 게 습관이 됐고요.'),
        NORM('주말에 친구가 보자고 하면 그날 아침 거울부터 보게 되더라고요.'),
        NORM('빨가면 안 나가요.'),
        BR,
        NORM('한번은 한 달에 약속 3개 잡았는데 2개를 취소한 적 있어요.'),
        NORM('그때 사진 보다가 2년 전 사진이 뜨더라고요.'),
        RED('그때는 아무 데나 가고 아무거나 먹었거든요.'),
        BR, BR,
        BOLD('스테로이드도 수란트라도 레이저도 한의원도 해봤는데 다 일시적이었어요.'),
        RED('뭘 해도 돌아오거든요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 모낭충 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그러다가 새벽에 또 검색하다가 왜 다 일시적인 건지를 찾아보게 됐어요.'),
        BR,
        NORM('그때 알게 된 건데요.'),
        RED('주사피부염의 원인 중 하나가 모낭충이라고 하더라고요'),
        NORM('모공 안에 사는 기생충인데 밤에만 활동한대요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro1'], '모낭충 현미경'))
    blocks.append(text_block([
        BR,
        NORM('낮에는 모공 안에 숨어있다가 밤에 모공 밖으로 나와서'),
        BOLD('세균을 묻히고 다시 들어가고.'),
        NORM('그 세균이 염증을 만들고 그게 장벽을 부수는 거래요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro2'], '모낭충 야행성 활동'))
    blocks.append(text_block([
        BR, BR,
        NORM('그걸 알고 나니까 다 이해가 되는 거예요.'),
        NORM('스테로이드는 염증을 눌러서 잠깐 좋아지는 건데 원인은 그대로니까 끊으면 돌아오고.'),
        NORM('수란트라는 모낭충을 죽이긴 하는데 환경을 안 바꾸니까 끊으면 다시 번식하고.'),
        NORM('레이저는 혈관을 줄이는 건데 혈관이 왜 확장됐는지는 안 건드리는 거고.'),
        NORM('한의원은.. 모낭충이랑 관계가 없었던 거고.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['cycle_info'], '악순환 구조'))
    blocks.append(text_block([
        BR,
        RED('2년 동안 뭘 해도 돌아왔던 이유가 전부 같았어요'),
        BOLD('겉만 건드리고 모공 안에 있는 원인은 안 건드린 거.'),
        BR, BR,
        BLUE('결국 핵심은 모공 안에서 모낭충이 못 사는 환경을 만드는 거더라고요'),
        BLUE('죽이는 게 아니라 환경을 바꾸는 거'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 제품 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그래서 밤에 바르는 크림을 찾기 시작했어요.'),
        NORM('비누는 씻고 끝이니까 의미가 없고 밤새 모공 안에 남아있으면서 환경을 바꿔야 하니까요.'),
        BR,
        NORM('찾다 보니까 티트리 성분이 모낭충한테 잘 듣는다는 게 나오더라고요.'),
        NORM('근데 보통 화장품에는 0.1~0.5%밖에 안 들어간대요.'),
        NORM('그러다가 1.07% 들어간 크림을 찾았는데요.'),
        BR,
        BOLD('크림이니까 밤에 바르면 8시간 동안 모공 안에 남아있고'),
        NORM('유익균 복원 성분도 있어서 환경 자체를 바꾸는 구조라고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['product'], '티트리셀 제품'))
    blocks.append(text_block([
        BR,
        NORM('솔직히 스테로이드 수란트라 레이저 한의원까지 해보고'),
        NORM('크림 하나로 달라지겠어? 싶었어요.'),
        NORM('근데 지금까지 한 건 전부 겉을 건드린 거였고'),
        BOLD('이건 모공 안에서 환경을 바꾼다는 게 달랐어요.'),
        BR, BR, BR,
    ]))

    # 결과
    blocks.append(text_block([
        NORM('2주차에 아침에 볼이 안 뜨거운 거예요.'),
        RED('2년 만에 처음이었어요.'),
        BR,
        NORM('스테로이드 바르면 하루 만에 좋아지긴 했는데 끊으면 바로 돌아왔거든요.'),
        BOLD('이건 끊어도 돌아오지 않더라고요..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['result_timeline'], '변화 타임라인'))
    blocks.append(text_block([
        BR,
        NORM('남자친구가 한 달쯤 됐을 때 "너 요즘 피부 좀 괜찮아진 거 아니야?" 하는데'),
        BR,
        BLUE('"너 요즘 피부 좀 괜찮아진 거 아니야?"'),
        BR,
        NORM('그 말 듣고 좀 울었어요 ㅠ..'),
        NORM('피부과 한의원 레이저 다니면서 얼마를 쓴 건지..'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 마무리
    blocks.append(text_block([
        BR,
        NORM('아직 완치는 아니에요.'),
        NORM('확신도 없어요 솔직히.'),
        BR,
        BOLD('근데 뭘 해도 돌아오던 게 안 돌아오고 있어요.'),
        NORM('저한테는 그게 가장 큰 차이였어요.'),
        BR, BR,
        NORM('혹시 주사피부염 때문에 같은 고민이신 분 있으면'),
        BOLD('겉을 건드리는 게 아니라 모공 안 환경을 바꾸는 쪽으로 찾아보세요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 추가/수정
    blocks.append(text_block([
        BR,
        GRAY('추가) 제품 뭐냐고 물어보시는 분이 많아서..'),
        NORM('티트리셀이라는 크림이에요.'),
        NORM('자세한 건 여기서 보실 수 있어요.'),
        BR,
    ]))
    blocks.append(oglink_block('c2_rosacea'))
    blocks.append(img_block(IMAGES['product_spec'], '제품 스펙'))
    blocks.append(text_block([
        BR,
        NORM('처방 필요 없고 매일 밤 바르면 되더라고요.'),
        BR, BR,
        GRAY('수정) 가격 물어보시는 분들 있어서 추가하면'),
        NORM('49,900원인데 피부과 레이저 1회보다 싸요..'),
        NORM('저는 피부과+한의원+레이저에 얼마를 쓴 건지 모르겠어요.'),
        BR, BR,
        NORM('혹시 써보신 분 있으면 댓글로 알려주세요.'),
        NORM('주사피부염이신 분 경험이 궁금해서요..'),
        BR,
    ]))

    return '\n\n'.join(blocks)


def build_c3():
    """C3 안면홍조"""
    blocks = []

    # 오프닝
    blocks.append(text_block([
        BIG('얼굴 빨개지는 이유 검색하다가 여기까지 오신 거죠..'),
        BR,
        BIG('저도 그랬어요.'),
        BR, BR, BR,
        NORM('저는 올해 32살 직장인이고요.'),
        NORM('2년 전부터 얼굴이 빨개지기 시작했는데 아직도 안 낫고 있어요.'),
        RED('매일 아침 일어나면 볼이 뜨거워요. 이게 2년째예요.'),
        BR, BR,
    ]))

    # 진정크림 실패
    blocks.append(text_block([
        NORM('처음엔 그냥 피부가 예민해진 줄 알았거든요.'),
        NORM('환절기라 그런가 싶어서 진정 크림 바르고 넘어갔는데 안 나아요.'),
        NORM('한 달이 지나도 아침마다 볼이 빨갛고 열감이 올라오는 거예요.'),
        BR, BR,
        NORM('그래서 피부과를 갔거든요.'),
        NORM('선생님이 "주사피부염 초기인 것 같아요" 하시는데'),
        NORM('그게 뭔지도 몰랐고 솔직히 좀 무서웠어요.'),
        BR,
        NORM('스테로이드 연고 처방받고 집에 왔는데'),
        BOLD('바르면 하루 만에 좋아지거든요. 근데 끊으면 이틀 만에 원래대로예요.'),
        NORM('선생님한테 전화했더니 "오래 쓰면 안 돼요" 하시고..'),
        RED('그럼 어떡하라는 건지..'),
        BR, BR,
    ]))

    # 크림 실패
    blocks.append(text_block([
        NORM('그다음부터 장벽크림을 바꾸기 시작했어요.'),
        NORM('에스트라 아토베리어 샀는데 안 맞는 것 같아서 바꾸고.. 또 바꾸고..'),
        NORM('올리브영 세일할 때마다 하나씩 사게 되더라고요.'),
        BOLD('세면대에 크림만 늘어나고..'),
        BR,
        NORM('엄마한테 전화했더니 "알로에 발라봐" 이러시고'),
        NORM('친구는 "시카크림 좋다던데" 하고'),
        RED('다 발라봤는데 아침에 거울 보면 똑같아요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['cream_shelf'], '크림 실패'))
    blocks.append(text_block([
        BR, BR,
    ]))

    # 잃어버린 것들
    blocks.append(text_block([
        NORM('그게 크림만의 문제가 아니었거든요.'),
        NORM('제가 원래 매운 거 엄청 좋아했는데 마라탕 짬뽕 이런 거요.'),
        NORM('근데 매운 거 먹으면 얼굴이 빨개지니까 안 먹게 됐어요. 2년째요.'),
        NORM('회사 점심에 국물 나와도 얼굴이 달아올라서 고개 숙이고 먹게 되고.'),
        NORM('주말에 친구가 보자고 하면 그날 아침 거울부터 보게 되더라고요.'),
        NORM('빨가면 핑계 대고 안 나가요.'),
        BR,
        NORM('한번은 한 달에 약속 3개 중 2개를 취소한 적 있어요.'),
        NORM('그때 사진 보다가 2년 전 사진이 뜨더라고요.'),
        RED('그때는 아무 데나 가고 아무거나 먹었거든요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 모낭충 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그러다가 새벽에 또 검색하게 되더라고요.'),
        NORM('안면홍조 원인이 뭔지 진짜 제대로 찾아보자 싶었어요.'),
        BR,
        NORM('혈관이 확장돼서 그렇다는 글도 있고'),
        NORM('스트레스라는 글도 있고'),
        NORM('체질이라는 글도 있는데'),
        NORM('다 읽어봐도 결국 "관리하세요"밖에 없더라고요.'),
        BR, BR,
        NORM('그러다가 하나 알게 된 게 있는데요.'),
        RED('모낭충이라는 거요'),
        NORM('모공 안에 사는 기생충인데 밤에만 활동한대요.'),
        BR,
        NORM('솔직히 처음엔 소름 돋았어요.'),
        BOLD('내 모공에 벌레가 산다고..?'),
        NORM('엄마한테 전화했더니 "무슨 벌레가 얼굴에 살아 말도 안 돼" 이러시는데'),
        BOLD('진짜였어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro1'], '모낭충 현미경'))
    blocks.append(text_block([
        BR,
        NORM('모낭충이 밤에 모공 밖으로 나와서 세균을 묻히고 다시 들어가는데'),
        BOLD('그 세균이 염증을 만들고 장벽을 부수는 거래요.'),
        RED('그러니까 아침마다 볼이 뜨거운 게 밤새 모낭충이 활동해서 그런 거였어요'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro2'], '모낭충 야행성 활동'))
    blocks.append(text_block([
        BR, BR,
        NORM('그걸 알고 나니까 다 이해가 되더라고요.'),
        NORM('장벽크림은 겉을 세우는 건데 안에서 부수는 놈이 있으니까 매일 원점이고.'),
        NORM('스테로이드는 염증을 눌러서 잠깐 좋아지는 건데 원인은 그대로고.'),
        BOLD('진정 크림 시카 크림 다 겉에서 바르는 건데 모공 안은 안 건드리는 거였어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['vicious_cycle'], '악순환 사이클'))
    blocks.append(text_block([
        BR,
        RED('2년 동안 왜 뭘 발라도 아침에 똑같았는지 그제서야 이해가 됐어요'),
        BR, BR,
        BLUE('결국 핵심은 모공 안에서 모낭충이 못 사는 환경을 만드는 거더라고요'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 제품 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그래서 밤에 바르는 크림을 찾기 시작했어요.'),
        NORM('비누는 30초 씻고 끝이니까 의미가 없고 밤새 모공 안에 남아있어야 하니까요.'),
        BR,
        NORM('찾다 보니까 티트리 성분이 모낭충한테 잘 듣는다는 게 나오더라고요.'),
        NORM('근데 보통 화장품에는 0.1~0.5%밖에 안 들어간대요.'),
        NORM('그러다가 1.07% 들어간 크림을 찾았는데요.'),
        BR,
        BOLD('크림이라 밤에 바르면 8시간 동안 모공 안에 남아있고'),
        NORM('유익균 복원 성분도 있어서 환경 자체를 바꾸는 구조라고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['product'], '티트리셀 제품'))
    blocks.append(text_block([
        BR,
        NORM('솔직히 장벽크림을 몇 개를 바꿔봤는데 또 크림이라고? 싶었어요.'),
        NORM('근데 지금까지 바른 건 전부 겉에서 바르는 거였고'),
        BOLD('이건 모공 안에서 환경을 바꾼다는 게 달랐거든요.'),
        BR, BR, BR,
    ]))

    # 결과
    blocks.append(text_block([
        NORM('2주차에 아침에 볼이 안 뜨거운 거예요.'),
        RED('2년 만에 처음이었어요.'),
        NORM('거울 봤는데 빨갛긴 한데.. 확실히 덜했어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['result_timeline'], '변화 타임라인'))
    blocks.append(text_block([
        BR,
        NORM('남자친구가 한 달쯤 됐을 때 알아서 그러더라고요.'),
        BR,
        BLUE('"너 요즘 피부 좀 괜찮아진 거 아니야?"'),
        BR,
        NORM('그 말 듣고 좀 울었어요 ㅠ..'),
        NORM('마라탕 못 먹고 약속 취소하고 고개 숙이고 밥 먹던 게 한꺼번에 올라와서..'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 마무리
    blocks.append(text_block([
        BR,
        NORM('아직 완치는 아니에요.'),
        NORM('확신도 없어요 솔직히.'),
        BR,
        BOLD('근데 2년 동안 안면홍조 원인을 몰라서 뭘 해도 안 됐던 게'),
        NORM('원인을 알고 나니까 달라지더라고요.'),
        BR, BR,
        NORM('혹시 얼굴 빨개지는 이유를 모르겠어서 여기까지 오신 분 있으면'),
        BOLD('모낭충이라는 거 한번 찾아보세요.'),
        NORM('저는 그게 시작이었어요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 추가/수정
    blocks.append(text_block([
        BR,
        GRAY('추가) 제품 뭐냐고 물어보시는 분이 많아서..'),
        NORM('티트리셀이라는 크림이에요.'),
        NORM('자세한 건 여기서 보실 수 있어요.'),
        BR,
    ]))
    blocks.append(oglink_block('c3_redness'))
    blocks.append(img_block(IMAGES['product_spec'], '제품 스펙'))
    blocks.append(text_block([
        BR,
        NORM('처방 필요 없고 매일 밤 바르면 되더라고요.'),
        BR, BR,
        GRAY('수정) 가격 물어보시는 분들 있어서 추가하면'),
        NORM('49,900원이에요. 피부과 한 번 가는 것보다 싸요..'),
        BR, BR,
        NORM('혹시 안면홍조인데 써보신 분 있으면 댓글로 알려주세요.'),
        NORM('저만 이런 건지 궁금해서요..'),
        BR,
    ]))

    return '\n\n'.join(blocks)


def build_c4():
    """C4 모낭염"""
    blocks = []

    # 오프닝
    blocks.append(text_block([
        BIG('모낭염 치료 검색하다가 여기까지 오신 거죠..'),
        BR,
        BIG('저도 그랬어요.'),
        BIG('근데 결론부터 말하면 제 건 모낭염이 아니었어요.'),
        BR, BR, BR,
        NORM('저는 올해 32살 직장인이고요.'),
        NORM('2년 전부터 얼굴에 좁쌀 같은 게 올라오고 빨개지기 시작했거든요.'),
        NORM('동네 피부과 갔더니 "모낭염이에요" 하시면서 항생제 연고 처방해주셨어요.'),
        NORM('에스로반이었는데 발랐더니 좀 가라앉더라고요.'),
        BR, BR,
    ]))

    # 항생제 반복 실패
    blocks.append(text_block([
        NORM('근데 2주쯤 지나니까 또 올라왔어요.'),
        NORM('다시 피부과 갔더니 같은 연고 또 처방해주시고.'),
        RED('바르면 가라앉고 끊으면 올라오고..'),
        NORM('이걸 반복하다가 3개월째 됐을 때'),
        NORM('선생님한테 "왜 계속 재발하는 거예요?" 했거든요.'),
        BOLD('"모낭염은 원래 재발 잘 하는 거예요. 관리 잘 하셔야 해요"'),
        NORM('하시더라고요.'),
        BR,
        RED('관리를 잘 하라는데 뭘 어떻게 관리하라는 건지..'),
        BR, BR,
        NORM('그래서 약국에서 후시딘도 사서 발라보고'),
        NORM('올리브영에서 여드름 패치도 사서 붙여보고'),
        NORM('세안도 하루에 두 번 꼼꼼히 했거든요.'),
        BR,
        BOLD('근데 안 나아요.'),
        NORM('아침에 일어나면 볼에 좁쌀 같은 게 또 올라와 있고 빨갛고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['skin_clinic'], '항생제 연고 반복'))
    blocks.append(text_block([
        BR, BR,
    ]))

    # 잃어버린 것들
    blocks.append(text_block([
        NORM('그 사이에 생활도 바뀌더라고요.'),
        BOLD('매운 거 먹으면 더 심해지길래 마라탕을 끊었어요. 2년째예요.'),
        NORM('회사 점심에 국물 나와도 얼굴이 달아올라서 고개 숙이고 먹게 되고.'),
        NORM('주말에 약속 잡으면 그날 아침 거울부터 보게 되거든요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 모낭충 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그러다가 새벽에 또 검색하다가'),
        NORM('모낭염이 왜 재발하는지를 찾아보게 됐어요.'),
        NORM('항생제 연고를 발라도 왜 계속 돌아오는 건지.'),
        BR, BR,
        NORM('그때 알게 된 건데요.'),
        RED('모낭염이랑 비슷하게 생긴 건데 원인이 다른 게 있더라고요'),
        RED('모낭충이라는 거요'),
        NORM('모공 안에 사는 기생충인데 이게 염증을 만든대요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_compare'], '모낭염 vs 모낭충 비교'))
    blocks.append(text_block([
        BR,
        NORM('모낭염은 세균이 원인이라 항생제 연고로 가라앉거든요.'),
        BOLD('근데 모낭충이 원인이면 항생제를 발라봤자 소용이 없는 거래요.'),
        NORM('세균을 죽여도 모낭충이 또 세균을 만들어내니까.'),
        RED('그래서 가라앉았다가 또 올라오는 거였어요..'),
        BR, BR,
        NORM('그걸 알고 나니까 3개월이 이해가 되는 거예요.'),
        NORM('항생제 연고 바르면 세균이 죽어서 가라앉는데'),
        NORM('모공 안에 모낭충이 그대로 있으니까'),
        BOLD('끊으면 또 세균 만들어서 다시 올라오는 거였어요.'),
        RED('모낭염이 재발하는 게 아니라 원인이 다른 거였거든요.'),
        BR, BR,
    ]))

    # 밤에 활동
    blocks.append(text_block([
        NORM('그러면서 모낭충에 대해 더 찾아봤는데요.'),
        RED('밤에만 활동한대요'),
        NORM('낮에는 모공 안에 숨어있다가 밤에 나와서 세균을 묻히고 다시 들어가는 거래요.'),
        BR,
        NORM('그러니까 아침에 세안을 아무리 열심히 해도 모공 안에 있는 놈은 안 건드리는 거고'),
        BOLD('항생제 연고 발라도 세균만 죽이지 모낭충은 그대로인 거였어요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['demodex_micro2'], '모낭충 야행성 활동'))
    blocks.append(text_block([
        BR,
        BLUE('결국 핵심은 모공 안에서 모낭충이 못 사는 환경을 만드는 거더라고요'),
        BLUE('세균을 죽이는 게 아니라 세균을 만드는 놈의 환경을 바꾸는 거'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 제품 발견
    blocks.append(text_block([
        BR, BR,
        NORM('그래서 밤에 바르는 크림을 찾기 시작했어요.'),
        NORM('연고는 세균만 죽이는 거고 비누는 30초 씻고 끝이니까'),
        NORM('밤새 모공 안에 남아있으면서 모낭충 환경을 바꿔야 하니까요.'),
        BR,
        NORM('찾다 보니까 티트리 성분이 모낭충한테 잘 듣는다는 게 나오더라고요.'),
        NORM('근데 보통 화장품에는 0.1~0.5%밖에 안 들어간대요.'),
        NORM('그러다가 1.07% 들어간 크림을 찾았는데요.'),
        BR,
        BOLD('크림이라 밤에 바르면 8시간 동안 모공 안에 남아있고'),
        NORM('유익균 복원 성분도 있어서 환경 자체를 바꾸는 구조라고..'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['product'], '티트리셀 제품'))
    blocks.append(text_block([
        BR,
        NORM('솔직히 또 연고 바꾸는 거 아닌가 싶었어요.'),
        NORM('근데 연고는 세균을 죽이는 거고 이건 모낭충 환경을 바꾸는 거라'),
        BOLD('근본적으로 다르더라고요.'),
        BR, BR, BR,
    ]))

    # 결과
    blocks.append(text_block([
        NORM('2주차에 아침에 좁쌀이 안 올라온 거예요.'),
        RED('3개월 동안 항생제 바르면서 안 됐던 게..'),
        BOLD('제가 모낭염이 아니라 모낭충이었던 거예요.'),
        BR,
    ]))
    blocks.append(img_block(IMAGES['result_timeline'], '변화 타임라인'))
    blocks.append(text_block([
        BR,
        NORM('남자친구가 한 달쯤 됐을 때 "너 요즘 피부 좀 괜찮아진 거 아니야?" 하는데'),
        BR,
        BLUE('"너 요즘 피부 좀 괜찮아진 거 아니야?"'),
        BR,
        NORM('그 말 듣고 좀 울었어요 ㅠ..'),
        NORM('항생제만 계속 바르면서 왜 안 되지 했던 시간이 올라와서..'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 마무리
    blocks.append(text_block([
        BR,
        NORM('아직 완치는 아니에요.'),
        NORM('확신도 없어요 솔직히.'),
        BR,
        BOLD('근데 항생제 연고 바르면서 가라앉았다 올라왔다를 반복하시는 분 있으면'),
        NORM('혹시 모낭충은 아닌지 한번 찾아보세요.'),
        NORM('저는 그걸 알게 된 게 전환점이었어요.'),
        BR, BR, BR,
    ]))

    blocks.append(hr_block())

    # 추가/수정
    blocks.append(text_block([
        BR,
        GRAY('추가) 제품 뭐냐고 물어보시는 분이 많아서..'),
        NORM('티트리셀이라는 크림이에요.'),
        NORM('자세한 건 여기서 보실 수 있어요.'),
        BR,
    ]))
    blocks.append(oglink_block('c4_folliculitis'))
    blocks.append(img_block(IMAGES['product_spec'], '제품 스펙'))
    blocks.append(text_block([
        BR,
        NORM('항생제 연고랑 다르게 처방 없이 매일 밤 바르면 되더라고요.'),
        BR, BR,
        GRAY('수정) 가격 물어보시는 분들 있어서 추가하면'),
        NORM('49,900원이에요.'),
        BR, BR,
        NORM('혹시 저처럼 모낭염인 줄 알았는데 모낭충이었던 분 있으면'),
        NORM('댓글로 알려주세요. 저만 이런 건지 궁금해서요..'),
        BR,
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


# ===== 공통 설정 =====
SHARED_BLOG = {'name': '피부고민 수진', 'title': '수진이의 피부 이야기', 'profile_image': '', 'profile_color': '#a8d8ea'}
SHARED_TRACKING = {'meta_pixel_id': '1727184084578989', 'ga_id': '', 'scroll_events': [25, 50, 75, 100], 'cta_event_name': 'Lead'}


# ===== 실행 =====
print('🚀 SA v2 빌드 시작 (가독성 + 이미지)\n')

# C1
inject_and_save('sa-demodex-direct', build_c1(), {
    'blog': SHARED_BLOG,
    'post': {'title': '모낭충 3년째 달고 사는 사람이 알게 된 것', 'category': '건강·의학', 'date': '2026. 4. 5. 23:14'},
    'social': {'likes': 632, 'shares': 38, 'views': 4821},
    'comments': [
        {'author': '피부맘일기', 'profile_color': '#f0d6e8', 'time': '3시간 전', 'text': '저도 모낭충 비누 한 달 넘게 써봤는데 안 됐거든요.. 밤에만 활동한다는 거 처음 알았어요', 'likes': 23},
        {'author': '주사3년차극복중', 'profile_color': '#d6e8f0', 'time': '8시간 전', 'text': '수란트라 끊으면 돌아오는 이유가 이거였구나.. 환경이 안 바뀌니까', 'likes': 41},
        {'author': '올리브영탐험가', 'profile_color': '#e8f0d6', 'time': '1일 전', 'text': '에스트라 제로이드 닥터지 저도 다 써봤어요 ㅠㅠ 세면대에 크림만 쌓이는 거 완전 공감', 'likes': 35},
    ],
    'tracking': SHARED_TRACKING,
    'cta': {'url': CTA_URL.format(slug='c1_demodex'), 'text': '티트리셀 카밍 크림 자세히 보기'},
})

# C5
inject_and_save('sa-soolantra-alt', build_c5(), {
    'blog': SHARED_BLOG,
    'post': {'title': '수란트라 3개월 쓰고 끊었더니 다시 돌아온 사람', 'category': '건강·의학', 'date': '2026. 4. 3. 21:38'},
    'social': {'likes': 891, 'shares': 52, 'views': 7234},
    'comments': [
        {'author': '수란트라졸업반', 'profile_color': '#f0e0d6', 'time': '2시간 전', 'text': '저도 수란트라 3개월 쓰고 끊었는데 2주 만에 원래대로 돌아왔어요.. 진짜 멘탈 나감', 'likes': 56},
        {'author': '새벽검색러', 'profile_color': '#d6f0e0', 'time': '5시간 전', 'text': '죽이기가 아니라 환경을 바꾸는 거라는 말이 진짜 와닿네요', 'likes': 38},
        {'author': '직장인피부고민', 'profile_color': '#e0d6f0', 'time': '1일 전', 'text': '수란트라 뒤집어지면서 회사 못 간 거 저도요 ㅠㅠ 그 상태로 출근을 어떻게 해요', 'likes': 44},
    ],
    'tracking': SHARED_TRACKING,
    'cta': {'url': CTA_URL.format(slug='c5_soolantra'), 'text': '티트리셀 카밍 크림 자세히 보기'},
})

# C2
inject_and_save('sa-rosacea', build_c2(), {
    'blog': SHARED_BLOG,
    'post': {'title': '주사피부염 2년차가 치료 다 해보고 알게 된 것', 'category': '건강·의학', 'date': '2026. 4. 1. 22:51'},
    'social': {'likes': 1247, 'shares': 89, 'views': 12450},
    'comments': [
        {'author': '홍조탈출일기', 'profile_color': '#f0d6d6', 'time': '4시간 전', 'text': '스테로이드 수란트라 레이저 한의원 저도 순서 똑같아요.. 다 일시적이었어요', 'likes': 67},
        {'author': '모낭충알게됨', 'profile_color': '#d6d6f0', 'time': '7시간 전', 'text': '겉만 건드리고 모공 안은 안 건드린 거라는 말에 소름 돋았어요', 'likes': 53},
        {'author': '엄마가알로에발라', 'profile_color': '#f0f0d6', 'time': '2일 전', 'text': '엄마한테 한의원 가봐 듣고 간 거 저도요 ㅋㅋ 돈만 날림', 'likes': 42},
    ],
    'tracking': SHARED_TRACKING,
    'cta': {'url': CTA_URL.format(slug='c2_rosacea'), 'text': '티트리셀 카밍 크림 자세히 보기'},
})

# C3
inject_and_save('sa-facial-redness', build_c3(), {
    'blog': SHARED_BLOG,
    'post': {'title': '얼굴 빨개지는 이유 2년째 찾다가 알게 된 것', 'category': '건강·의학', 'date': '2026. 3. 28. 20:15'},
    'social': {'likes': 758, 'shares': 41, 'views': 5832},
    'comments': [
        {'author': '장벽크림5개째', 'profile_color': '#d6f0f0', 'time': '6시간 전', 'text': '진정 크림 시카 크림 다 발라봤는데 아침에 똑같은 거 진짜 공감.. 겉에서만 바르는 거였구나', 'likes': 29},
        {'author': '안면홍조10년', 'profile_color': '#f0d6f0', 'time': '12시간 전', 'text': '모낭충이라는 거 처음 알았어요 혈관 문제인 줄만 알았는데', 'likes': 47},
        {'author': '마라탕2년째못먹음', 'profile_color': '#f0e8d6', 'time': '1일 전', 'text': '매운 거 못 먹는 거 너무 공감 ㅠㅠ 친구들이랑 밥 먹을 때 제일 서러워요', 'likes': 31},
    ],
    'tracking': SHARED_TRACKING,
    'cta': {'url': CTA_URL.format(slug='c3_redness'), 'text': '티트리셀 카밍 크림 자세히 보기'},
})

# C4
inject_and_save('sa-folliculitis', build_c4(), {
    'blog': SHARED_BLOG,
    'post': {'title': '모낭염 연고 3개월 발라도 재발하는 진짜 이유', 'category': '건강·의학', 'date': '2026. 3. 25. 19:42'},
    'social': {'likes': 543, 'shares': 29, 'views': 3941},
    'comments': [
        {'author': '에스로반3통째', 'profile_color': '#e0f0d6', 'time': '4시간 전', 'text': '항생제 연고 바르면 가라앉는데 끊으면 또 올라오는 거 3개월째 반복 중이에요..', 'likes': 28},
        {'author': '모낭염인줄알았음', 'profile_color': '#d6e0f0', 'time': '9시간 전', 'text': '저도 모낭염인 줄 알았는데 모낭충이었어요.. 항생제가 소용없었던 이유가 이거였구나', 'likes': 39},
        {'author': '얼굴좁쌀파티', 'profile_color': '#f0d6e0', 'time': '1일 전', 'text': '아침마다 좁쌀 올라오는 거 진짜 미치겠어요 이게 모낭충 때문이었을 수도 있다니', 'likes': 22},
    ],
    'tracking': SHARED_TRACKING,
    'cta': {'url': CTA_URL.format(slug='c4_folliculitis'), 'text': '티트리셀 카밍 크림 자세히 보기'},
})

print('\n✅ 전체 5개 빌드 완료 (C1 + C5 + C2 + C3 + C4)')
print('URLs:')
print('  /posts/sa-demodex-direct/')
print('  /posts/sa-soolantra-alt/')
print('  /posts/sa-rosacea/')
print('  /posts/sa-facial-redness/')
print('  /posts/sa-folliculitis/')
