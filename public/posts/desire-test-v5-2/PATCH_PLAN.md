# v5 라이브 → v5.1 최소 외과 패치 플랜

> 목적: 라이브 v5의 유저 수정분(문장/이미지) 전부 보존 + RC/SM 깊이만 추가
> 방식: 삽입(INSERT)만, 수정/삭제 없음
> 대상 파일: `public/posts/desire-test-v5/index.html`

---

## 패치 요약

| Zone | 위치 | 삽입 내용 | 신규 이미지 |
|------|------|-----------|------------|
| **Zone 1** | line 1183 뒤 | 밀도 수치(18배) + 루프(B.oleronius) + 감시병(ILC2) | 3개 |
| **Zone 2** | line 1223 뒤 | Taieb 115일 재발 + 내 경험 연결 | 1개 |
| **Zone 3** | line 1479 뒤 (`<hr>` 앞) | SM 교육 블록 (2축+야행성+T4O혼합물+크림제형+매일성+시장부재) | 4개 |

**총 삽입:** 텍스트 ~1,600자 + 이미지 8개
**수정/삭제:** 0건
**유저 보존:** 기존 16개 이미지 + 모든 문장/수정분 그대로

---

## 신규 이미지 리스트 (제작 필요)

경로: `/posts/desire-test-v5/images/`

| 파일명 | 용도 | Zone |
|--------|------|------|
| `rc_density_compare.png` | 0.7 vs 12.8마리 대비 그래프 (18배) | 1 |
| `rc_loop_diagram.png` | 루프 순환 다이어그램 (번식→면역→독→환경→번식) | 1 |
| `rc_ilc2_paper.png` | Ricardo-Gonzalez 2022 Immunity 논문 캡처 | 1 |
| `rc_taieb_timeline.png` | Taieb 2016 115일 재발 타임라인 | 2 |
| `sm_2axis_diagram.png` | 진드기 억제 + 환경 변경 2축 | 3 |
| `sm_t4o_paper.png` | T4O 살충력 논문 캡처 | 3 |
| `sm_cream_vs_gel.png` | 크림 vs 겔 밤 시간축 | 3 |
| `sm_market_gap.png` | 처방약/화장품 2×2 매트릭스 | 3 |

---

## Zone 1: 밀도 수치 + 루프 + ILC2 (line 1183 뒤 삽입)

### 삽입 지점
기존 "그러면 면역이 반응해서 빨갛게 올라오는 거라고" (line 1182) 블록 **뒤**,
"모낭충이라는 건 알고 있었다 수란트라 발랐으니까" (line 1188) **앞**.

정확히는 line 1203의 `</div>` 닫히는 다음 줄(1204 빈 줄)에 새 블록들 삽입.

### 삽입 내용

**Block 1.1 (text)** — 정확한 숫자
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">나중에 정확한 숫자를 찾아봤는데</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">건강한 사람은 0.7마리</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">주사피부염 환자는 12.8마리</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>18배 차이였다</b></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
    </div>
  </div>
</div>
```

**Block 1.2 (image)** — 밀도 대비 그래프
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/rc_density_compare.png" alt="건강인 0.7마리 vs 환자 12.8마리 18배" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 1.3 (text)** — 루프 메커니즘
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그다음 줄에서 또 멈췄다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">진짜 무서운 건 여기였다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">모낭충이 죽을 때 B.oleronius라는 독이 나온대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">모낭충 안에 사는 세균인데</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">진드기가 죽으면 그 안에 있던 세균이 뿜어지는 거야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그 독이 면역을 더 자극해서 더 빨갛게 되고</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">빨갛게 된 피부는 모낭충이 살기 더 좋은 환경이 되고</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">살기 좋으면 더 번식하고</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>루프야 이게</b></span>
      </p>
    </div>
  </div>
</div>
```

**Block 1.4 (image)** — 루프 다이어그램
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/rc_loop_diagram.png" alt="루프 다이어그램 — 번식→면역→독→환경→번식" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 1.5 (text)** — ILC2 감시병 + 의사 용서
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그럼 왜 갑자기 시작되는 거냐</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">피부 안에 감시병 같은 면역세포가 있대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">ILC2라고</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">이게 모낭충 수를 매일 감시하면서 못 늘어나게 잡아주는 거였어</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">근데 스트레스든 호르몬이든 장벽이 무너지든</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">뭐든 이 감시병을 쓰러뜨리면</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그때부터 밀도가 올라가고 루프가 돌기 시작하는 거래</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">2022년에 논문에서 밝혀진 거라고</span>
      </p>
    </div>
  </div>
</div>
```

**Block 1.6 (image)** — ILC2 논문 캡처
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/rc_ilc2_paper.png" alt="Ricardo-Gonzalez 2022 Immunity 논문 — ILC2 감시병" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 1.7 (text)** — 의사 용서 재프레이밍
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">아 그래서였구나</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">피부과 10곳 돌았는데 아무도 이 얘기 안 한 거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">의사가 잘못한 게 아니라 2022년에 나온 연구였던 거야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">나온 지 얼마 안 된 거지</span>
      </p>
    </div>
  </div>
</div>
```

---

## Zone 2: Taieb 115일 재발 (line 1235 근처 삽입)

### 삽입 지점
기존 "시간 지나면 다시 번식한다고" (line 1222) 블록 **뒤**,
"바로 이해가 된 건 아니었다" (line 1241) **앞**.

정확히는 line 1235의 `</div>` 다음 빈 줄.

### 삽입 내용

**Block 2.1 (text)** — Taieb 설명
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">여기서 또 충격이었던 게</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">수란트라는 성충만 죽인대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">알 속 애벌레는 못 건드린대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">Taieb이라는 사람이 2016년에 추적한 연구가 있는데</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">수란트라 쓴 사람들이</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>115일 지나면 밀도가 다시 올라간다고</b></span>
      </p>
    </div>
  </div>
</div>
```

**Block 2.2 (image)** — Taieb 타임라인
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/rc_taieb_timeline.png" alt="Taieb 2016 — 수란트라 115일 재발 타임라인" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 2.3 (text)** — 내 경험 연결
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">내가 두 달 만에 돌아왔잖아</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">115일 안이야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">정확히 이 곡선 안이었던 거다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">수란트라가 원래 그런 약이었던 거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">내가 뭘 잘못해서가 아니라</span>
      </p>
    </div>
  </div>
</div>
```

---

## Zone 3: SM 교육 블록 전체 (line 1479 뒤, `<hr>` 1481 앞)

### 삽입 지점
기존 건이자 답글 블록 마지막 `</div>` (line 1479) **뒤**,
`<hr>` 수평선 (line 1481) **앞**.

### 삽입 내용

**Block 3.1 (text)** — 2축 선언
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">답글을 몇 번이고 다시 읽었다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">진드기를 잡는 거랑</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">진드기가 살기 좋은 상태를 바꿔주는 거랑</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>이 두 개를 한번에 해야 된다는 거였다</b></span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.2 (image)** — 2축 다이어그램
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/sm_2axis_diagram.png" alt="진드기 억제 + 환경 변경 2축 다이어그램" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 3.3 (text)** — 한쪽만 반복 + 루프 상기
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그동안 내가 한 건 전부 한쪽만이었다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">항생제는 진드기만 잡는 거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">수란트라도 진드기만 잡는 거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">장벽크림은 겉만 바꾸는 거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">둘이 만나는 지점이 없었던 거야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">감시병 쓰러지고 독 뿌려져서 루프 도는 거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">이걸 멈추려면 양쪽을 같이 해야 되는 거였어</span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.4 (text)** — 야행성
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그리고 한 가지 더 있었는데</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">모낭충은 밤에 나와서 활동한대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">낮에는 모공 속에 있다가</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">밤에 피부 위로 올라와서 번식하는 거지</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>자고 일어나면 항상 더 심했던 게 이거였어</b></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">자는 동안 모낭충이 일하고 있었던 거다</span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.5 (text)** — T4O 도입
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그럼 잡는 건 뭘로 하냐</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">티트리 오일 안에 T4O라는 성분이 있대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">이게 모낭충 신경근을 마비시키는 거야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">1% 농도만 돼도 충분히 잡는다고 논문에서 확인된 거래</span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.6 (image)** — T4O 논문 캡처
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/sm_t4o_paper.png" alt="T4O 살충력 논문 — Tighe/Yurekli" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 3.7 (text)** — T4O 혼합물 설명 (핵심 신규)
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">근데 여기서 한 가지 중요한 게 있다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">티트리 오일이 한 가지 성분이 아니다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">여러 성분이 섞인 오일인데</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그중에서 진드기를 잡는 건 T4O 이거 하나뿐이야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">일반 티트리 오일에 T4O는 30~40%밖에 안 들어있고</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">나머지 60%는 피부를 자극하는 성분이라고</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그러니까 티트리 오일을 그냥 얼굴에 바르면</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">진드기 잡으려던 30%가 들어가는 동시에</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">피부 자극하는 60%도 같이 들어가는 거지</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">자극 없이 매일 쓰려면</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">T4O만 충분히 들어있는 크림이어야 되는 거였다</span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.8 (text)** — 잡기만으로 부족 + 크림 제형 도입
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그리고 잡기만 해도 안 된다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그게 수란트라였으니까</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">115일 재발 그거</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그래서 크림 제형이어야 된대</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">겔은 흡수돼서 새벽쯤엔 거의 안 남거든</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">모낭충이 그때 나올 때 걸리는 게 없는 거다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">크림은 밤새 깔려있어서 활동 자체를 못 해</span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.9 (image)** — 크림 vs 겔 밤 타임라인
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/sm_cream_vs_gel.png" alt="크림 vs 겔 밤 시간축 — 모낭충 활동 시간 커버" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

**Block 3.10 (text)** — 매일성
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">그리고 매일 바를 수 있어야 된다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">수란트라가 안 된 이유가 정확히 여기야</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">처방 기간 끝나면 끊어야 하니까</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">끊는 순간 밀도가 다시 올라가</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">화장품 등급이면 매일 쓸 수 있어서 끊을 일이 없다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">밀도를 매일 한계선 아래로 눌러두는 게 핵심인 거였어</span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.11 (text)** — 시장 부재
```html
<div class="se-component se-text se-l-default">
  <div class="se-section se-section-text se-l-default">
    <div class="se-module se-module-text">
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">이 세 가지가 다 되는 게 시장에 있긴 한 건가 싶었다</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">처방약(수란트라) — 진드기는 잡는데 매일 못 써</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system">화장품(보습크림) — 매일 바르는데 진드기를 안 건드려</span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span class="se-fs-fs15 se-ff-system"><br></span>
      </p>
      <p class="se-text-paragraph se-text-paragraph-align- ">
        <span style="color:rgb(255, 0, 16);" class="se-fs-fs19 se-ff-system"><b>둘 다 되는 건 그동안 없었던 거야</b></span>
      </p>
    </div>
  </div>
</div>
```

**Block 3.12 (image)** — 시장 부재 매트릭스
```html
<div class="se-component se-image se-l-default __se-component">
  <div class="se-section se-section-image se-l-default">
    <div class="se-module se-module-image">
      <a>
        <img src="/posts/desire-test-v5/images/sm_market_gap.png" alt="시장 부재 2×2 매트릭스 — 처방약/화장품/동시" class="se-image-resource">
      </a>
    </div>
  </div>
</div>
```

---

## 적용 순서

1. **이미지 8개 제작** → `public/posts/desire-test-v5/images/` 에 업로드
   - AI 생성(Midjourney/DALL-E/Nano-banana) 또는 Figma/Canva 수작업
   - 논문 캡처 2개(ILC2, T4O)는 실제 PubMed 스크린샷 권장
2. **index.html에 Edit tool로 3개 Zone 삽입**
3. **Vercel 자동 배포 확인** (GitHub push 시)
4. **브라우저 검증** — `naver-blog-clone-ten.vercel.app/posts/desire-test-v5/`

---

## 롤백 플랜

각 Zone은 독립적으로 삽입되므로 각각 독립 롤백 가능.
이미지가 없으면 alt 텍스트만 보이고 레이아웃 깨지지 않음.
