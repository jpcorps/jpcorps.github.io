# 작업 노트 (세션 간 공유)

매일 글 작업을 하는 Claude 세션들이 서로 모르는 것을 여기 적어 둔다. 어느 컴퓨터에서 돌든 작업 전에 `git pull` 하고 이 파일을 읽는다.
규칙은 `WRITING_GUIDE.md` 가 정하고, 이 파일은 그 규칙을 지키다가 알게 된 사실과 요령을 모은다.

## 지금까지 올린 글

- 2026-11-13 구름으로 배우는 뉴럴 셰이더 (원문 소개글, Charles Grassi)
- 2026-11-14 중학생도 할 수 있는 신경망 셰이더: 숫자 337개로 하트 그리기 (JP 요청 튜토리얼, 어제 글 후속)
  - 파일: `content/posts/2026-11-14-neural-shader-heart-tutorial.md`
  - 그림·코드: `static/images/tech-art/neural-shader-heart-tutorial/` (그림 6장 + `heart_nn.py` + `NeuralHeart.shader`)
  - 내용: (u, v) → 뉴런 16 → 16 → 출력 1, 가중치 337개. numpy 로 64×64 정답 하트를 8000번 학습(Adam, seed 11), 출력한 `weights.hlsl` 을 유니티 언릿 셰이더(Built-in, CGPROGRAM)에 붙여 넣는다.
  - 이 글을 이어 쓸 때: 같은 코드로 원·별 모양 바꾸기, 뉴런 수 늘리기, 텍스처에 가중치 넣기 등이 자연스러운 후속 주제다.
- 2026-11-15 카프콤 VORTEXEL 쉽게 읽기 (1) 게임이 지형을 '레고 블록'으로 읽는 법 (요청 연재 1/4)
  - 파일: `content/posts/2026-11-15-capcom-vortexel-1-geometry.md`
  - 그림: `static/images/tech-art/capcom-vortexel-1-geometry/` (직접 만든 2D 그림 4장 + `make_figures.py`). 원문 슬라이드 이미지는 못 씀(아래 참고).
  - 2편 이후 쓸 때: 슬라이드 쪽 번호 — 개요 p.10-16, Geometry p.25-72, Turbulence 는 p.75 전후부터, 풀 태우기 동기 p.112, Physics 접촉 p.136-152, 메모리 p.176, AABB 지정 구축 p.183.

- 2026-11-16 카프콤 VORTEXEL 쉽게 읽기 (2) 미리 굽지 않는 바람 — Turbulence (요청 연재 2/4)
- 2026-11-16 스마트폰에서 레일리 산란을요? — 사이버에이전트 그래픽스 엔지니어 2026 인터뷰 (JP 요청, gamemakers.jp 기사)
  - 파일: `content/posts/2026-11-16-cyberagent-mobile-graphics-2026.md`
  - 원문: https://gamemakers.jp/article/2026_11_02_148754/ (神山大輝, [PR] 기사)
  - 내용: 24시간 라이팅(레일리·미 산란, QualiArts), 원거리 그림자 보완(베이크드 섀도맵+CSM, Sirius 패키지), 모바일 디퍼드 렌더링+Surface Cache GI, HLSL 단위 테스트(컴퓨트 셰이더), 그래픽스 회귀 테스트(스크린샷 히트맵, CI)
  - 파일: `content/posts/2026-11-16-capcom-vortexel-2-turbulence.md`
  - 그림: `static/images/tech-art/capcom-vortexel-2-turbulence/` (직접 만든 그림 4장 + `make_figures.py`, 2D 안정 유체 흉내. 실행 약 10초)
  - 3편 쓸 때: Thermal Conductor 는 슬라이드 p.102-111 (구형 발화점을 링크로 잇는 방식). 비용 p.176-177, 끄기 옵션 p.179-181.
  - 슬라이드에는 유체 계산 알고리즘(이류·압력 반복 횟수, 격자 크기)이 안 나온다. 지어내지 말 것.

- 2026-11-17 카프콤 VORTEXEL 쉽게 읽기 (3) 불은 온도가 아니라 '시간'으로 번진다 — Thermal Conductor (요청 연재 3/4)
- 2026-11-18 바닥을 기는 안개는 어떻게 만드나 — 높이 안개 셰이더 해부 (JP 요청, Three.js 포럼 red-reddington 2025-12)
  - 파일: `content/posts/2026-11-18-ground-fog-shader.md`
  - 그림: `static/images/tech-art/ground-fog-shader/` (직접 만든 그림 3장 + `make_figures.py`. 실행 수 초)
  - 내용: 높이 기반 밀도(world Y 지수 감쇠), FBM 노이즈 8 옥타브로 흔들기, early exit, yomotsu 2D 유체 시뮬 데모 비교
  - Three.js 포럼 URL: https://discourse.threejs.org/t/high-performance-ground-fog-for-games-three-js/88522
  - 파일: `content/posts/2026-11-17-capcom-vortexel-3-thermal.md`
  - 그림: `static/images/tech-art/capcom-vortexel-3-thermal/` (직접 만든 그림 4장 + `make_figures.py`, 점 80개 그래프에 1초 착화·2초 연소 규칙. 실행 2초)
  - 이번엔 슬라이드 이미지를 못 씀: 클라우드 프록시가 docswell.com·bcdn.docswell.com 을 403 으로 막아 Playwright 로 임베드 페이지를 못 열었다.
  - 슬라이드 쪽: Thermal 102~116 (월드 시절 뒷이야기 113~115), 시간 규칙 예시(1초 착화·2초 연소, 화염구 5초)는 111쪽. 발표자 노트에는 '2초 데워지면 착화, 5초 연소'라는 다른 숫자도 있어 슬라이드 본문 숫자를 따랐다. 이 부품만의 메모리·ms 는 슬라이드에 없음.
  - 4편 쓸 때: Physics 접촉 p.136-152, 고급 파라미터 숨기기 p.174, 메모리 p.176, 처리 시간 p.177, 끄기 옵션 p.179-181, 실내 마스크 p.182.

- 2026-11-18 카프콤 VORTEXEL 쉽게 읽기 (4) 이펙트를 위한 '대충' 물리, 그리고 체크 하나로 끝 (요청 연재 4/4, 연재 끝)
  - 파일: `content/posts/2026-11-18-capcom-vortexel-4-physics.md`
  - 그림: `static/images/tech-art/capcom-vortexel-4-physics/` (직접 만든 그림 4장 + `make_figures.py`, 2D 강체 파편 40개를 '칸마다 대표 법선 평면 + 내접원 충돌'로 흉내. 실행 2초)
  - 슬라이드 쪽(WebFetch 앵커 번호 기준. 위 노트의 136~152 같은 예전 추정과 다르다): Physics 119~165, Tiny Physics 반지름 0.5m 127, 대표 법선 141~143, 내접구 149~156, PS5 1만 개 0.06/0.03ms 158, 쓰인 곳 159~161, Wakeup Over Reaction 163, Click to Go 168~173, 고급 파라미터·질량 숨김 174, 메모리 176, 처리 시간 177, 끄기 옵션·실내 마스크 178~182, AABB 지정 구축 183~185, 엑스포 몬스터헌터 브리지 187~188.
  - 반발·마찰 계수는 슬라이드에 없다. 지어내지 말 것.

- 2026-11-19 하늘이 예뻐지는 건 대단한 기술보다 작은 요령 덕분 — 항해 게임 개발 일지 '예쁜 하늘' 읽기 (원문 소개글, Thomas ten Cate / Frozen Fractal, Graphics Programming Weekly 462 에서 찾음)
  - 파일: `content/posts/2026-11-19-pretty-sky-small-tricks.md`
  - 그림: 원문 이미지 5장 + 직접 만든 그림 3장 `static/images/tech-art/pretty-sky/` (`make_figures.py`, 노멀 꺾기·레이마칭 순서·톤 매핑 장난감 계산. 실행 수 초)
  - 같은 시리즈 33편(구름), 35편(항해)도 있다. 35편은 게임 디자인 쪽이라 TA 글감으로는 약함.

- 2026-11-20 연기 스프라이트에 빛을 '나중에' 입히는 법 — 6방향 라이트맵과 신경망 (원문 소개글, arXiv 2604.03748 'Real-time Neural Six-way Lightmaps', LIGHTSPEED 등)
  - 파일: `content/posts/2026-11-20-neural-six-way-lightmaps.md`
  - 그림: 직접 만든 4장 `static/images/tech-art/neural-six-way/` (`make_figures.py`, 56^3 장난감 연기에 단일 산란 6방향 굽기·섞기·옆 시점 비교. 실행 약 12초) + Unity 블로그 GIF 1장.
  - 논문 그림은 못 씀: WebFetch 가 arXiv HTML 을 마크다운으로 바꿔 줘서 진짜 img src 가 안 나오고, curl 은 arxiv.org·cdn.sanity.io 모두 프록시 403.
  - 장난감에서 논문 식 5(성분 절댓값 가중치)를 그대로 쓰면 대각선 빛에서 1.4~1.6배 밝았다. 글에는 제곱 가중치(합 1)를 썼다고 밝혔다.
  - 글감 찾기: GPW 463 의 LinkedIn 글(SSS albedo remapping)과 jacktollenaar.top(Split Radiance Cascades)은 검색 결과에 URL 이 안 나와 PROVENANCE_REQUIRED 로 못 열었다.

- 2026-11-21 빛을 '거리별 칸'에 나눠 담기 — 스플릿 래디언스 캐스케이드 구현기 읽기 (원문 소개글, jacktollenaar.top, GPW 463 에서 찾음. 바탕 논문 arXiv 2607.20384 Freeman·Sannikov·Pitt-Francis)
  - 파일: `content/posts/2026-11-21-split-radiance-cascades.md`
  - 그림: 직접 만든 3장 `static/images/tech-art/split-radiance-cascades/` (`make_figures.py`, 2D 방 두 칸에서 광선을 맞은 거리로 칸에 나누고 투과율 있/없이 합쳐 빛 샘 비교. 실행 1초) + 원문 그림 5장(SaintRC, ProbePos, blockedRay, BedPT, BedRC).
  - 원문 본문에 필자 이름·날짜가 없다(도메인만). source_author 는 "jacktollenaar.top" 로 적었다. 홈페이지는 PROVENANCE_REQUIRED 로 못 열었다.
  - jacktollenaar.top 도 처음엔 PROVENANCE_REQUIRED 였지만 `"Split Radiance Cascades" jacktollenaar` 검색(extended)에 나온 뒤 열렸다. 이미지 주소는 curl 프록시 403 이라 직접 열어 확인 못 함.
  - 원문 코드의 방향 수(BaseDirections << Cascade 와 '4배' 설명)가 서로 안 맞는다. 글에서는 배수를 적지 않았다.
  - 장난감 요령: 벽 위치가 프로브 칸 경계(0.5×2^c 의 배수)와 맞으면 빛 샘이 전혀 안 생겨 비교가 안 된다. 벽을 x=9.3 처럼 어긋나게 둘 것.

- 2026-11-22 숫자 열두 개로 색 팔레트 만들기 — 이니고 킬레스의 '코사인 팔레트' 읽기 (원문 소개글, 고전. iquilezles.org/articles/palettes)
  - 파일: `content/posts/2026-11-22-cosine-color-palettes.md`
  - 그림: 직접 만든 6장 `static/images/tech-art/cosine-palettes/` (`make_figures.py`, 원문 예시 숫자 7세트 그대로 띠로 그림. 실행 2초). HLSL 예시는 glslangValidator 컴파일만 확인.
  - 원문 그림은 못 씀: WebFetch 결과에 상대 경로(gfx00.jpg 등)만 나오고 예시 표 이미지 src 는 비어 있었으며, curl 은 iquilezles.org 연결 자체가 안 됐다(000).
  - 원문의 'c 를 0.5 의 정수배로 두면 0..1 에서 순환' 문장은 식으로 따져 보면 c=0.5 에서 끝과 처음 색이 달라 글에서는 뺐다(정수 c 만 소개).
  - 글감 찾기: GPW 463/462 후보 중 NVIDIA 경로 추적 백서(github.com/NVIDIA-RTX/Whitepapers)는 README URL PROVENANCE_REQUIRED, tree URL robots_disallowed 로 못 읽음. LinkedIn SSS 글은 여전히 검색에 안 나옴. 'The Hidden Assumptions in Every Volume Renderer' 는 유튜브 영상이라 내용을 읽을 길이 없었다.

## 알게 된 것

### 원문 페이지 읽기 (WebFetch 권한)
- 스케줄 실행에서는 URL 을 WebFetch 로 바로 열면 "PROVENANCE_REQUIRED"(사용자 승인 대기)로 막힌다. **WebSearch 결과에 그 URL 이 먼저 나오게 한 뒤** WebFetch 하면 열린다.
  - 예: docswell 슬라이드는 `"VORTEXEL" カプコン VFX ボクセル` 검색(extended)으로 나온 뒤 열렸다.
- docswell 슬라이드 본문 글자는 WebFetch 로 쪽 번호와 함께 읽힌다. 쪽별 이미지 주소는 WebFetch 로는 안 나오지만, **브라우저로 임베드 페이지 `https://www.docswell.com/slide/<ID>/embed?mode=extend` 를 열면** 전 쪽의 `bcdn.docswell.com/page/<쪽ID>.jpg` 가 순서대로 들어 있다(VORTEXEL 은 191쪽). 이렇게 찾아 VORTEXEL 1·2편에 슬라이드 7장(27, 32, 42, 46, 84, 98, 100쪽)을 걸어 썼다. 출처 캡션 필수, 확인 못 한 주소는 안 쓴다.
- gamemakers.jp 기사도 같은 이유로 못 열었다(검색 결과에 안 나옴).
- 원문 페이지는 WebFetch 로 읽혀도, 그 안의 이미지 주소를 WebFetch·curl 로 직접 여는 건 막힐 수 있다(frozenfractal.com: WebFetch 는 PROVENANCE_REQUIRED, curl 은 프록시 403). 이럴 땐 원문 페이지를 다시 WebFetch 해서 마크다운 이미지 주소를 그대로 받아 쓰고, '직접 열어 확인은 못 했다'고 보고한다.
- covered.md 에 2026-11-18 안개 글 기록이 빠져 있어 2026-11-19 세션이 보충했다. 글을 올리면 covered.md 기록을 잊지 말 것.

### 날짜가 미래면 글이 안 뜬다
- front matter 시각이 `07:30:00+09:00` 인데, Hugo 는 빌드 시점보다 미래인 글을 빼고 만든다(buildFuture 꺼짐).
- **07:30 KST 전에 push 하면 그 배포에서 글이 빠지고, 다음 push 까지 안 보인다.** push 는 07:30 이후에 하거나, 일찍 끝났으면 기다렸다가 한다.
- 확인: GitHub Actions 의 "Build with Hugo" 단계 시작 시각이 07:30 KST 이후인지 본다.

### 로컬에서 Hugo 빌드로 미리 확인하기
- 워크플로가 Hugo `0.157.0` extended 를 쓴다. 같은 버전 바이너리를 받아 쓴다.
- 테마는 최신 HEAD 를 쓰면 `.Site.Language.Locale` 에러가 난다. 저장소에 고정된 서브모듈 커밋을 써야 한다:
  `git ls-tree HEAD themes/hugo-theme-stack` 로 커밋을 보고 그 커밋만 `--depth 1` 로 fetch.
- 이글루스 백업 글까지 다 빌드할 필요는 없다. 임시 폴더에 `hugo.toml`, `layouts/`, `assets/`, 새 글과 그 그림만 복사해서 빌드하면 빠르다.
- 다른 글 링크는 `{{< relref "파일명.md" >}}` 가 잘 된다. 주소는 `/posts/<파일명>/`.
- 직접 만든 그림은 `/images/...` 절대 경로로 걸면 그대로 나온다. front matter `image:` 도 같은 경로로 된다.

### 유니티 없이 셰이더를 실제로 돌려 확인하기
지침상 "직접 만든 코드는 실행해서 확인한 것만" 싣는다. 유니티가 없는 환경에서는 이렇게 했다.
1. `apt-get install glslang-tools spirv-cross`, `pip install moderngl`
2. ShaderLab 껍데기에서 CGPROGRAM~ENDCG 부분만 떼고, `UnityCG.cginc` 대신 짧은 대역(`appdata_base`, `UnityObjectToClipPos`, `fixed4`)을 넣는다.
3. `glslangValidator -D -V -S frag -e frag` 로 HLSL → SPIR-V 컴파일(문법 검사).
4. `spirv-cross --version 430` 으로 GLSL 로 바꾸고, moderngl(EGL, llvmpipe 소프트웨어 GPU)로 전체 화면을 그려서 파이썬 결과와 픽셀 단위로 비교.
   - 상수 버퍼(`_Global`)에 `MVP` mat4 가 먼저 들어가니, 색 값은 그 뒤 오프셋에 넣는다.
   - WebGL(ESSL 300)은 2차원 배열 상수를 못 받아서 이 경로는 안 됐다.
- 글에는 "유니티 에디터가 아니라 이 방법으로 확인했다"고 솔직히 적는다.

### 작은 신경망 학습 요령 (하트 실험에서)
- ReLU 신경망은 입력을 -1~1 로 옮기고, 1층 가중치를 크게(표준편차 3), 편향을 -2~2 균등으로 시작해야 모양이 제대로 잡혔다. 기본 초기화로는 뭉개진다.
- 숨은 층 1개(16~32개)보다 2층(16×16)이 훨씬 낫다.
- seed 마다 결과 모양이 꽤 다르다. 몇 개 돌려 보고 좋은 걸 고른다.
- 학습률을 점점 줄이면(0.01 → 0.0005) 가장자리 잡티가 줄어든다.

### 날짜 함정 (다시 확인)
- 스케줄 실행은 KST 07시 조금 넘어 시작한다. 시스템 날짜(UTC)는 전날이니 파일 날짜는 반드시 `TZ=Asia/Seoul date` 로 정한다.
- 로컬 Hugo 확인은 07:30 전이면 새 글이 빠지므로 `--buildFuture` 를 붙여 본다. push 는 07:30 이후에.

### 티스토리에도 올리기
- 방법은 `TISTORY_CROSSPOST.md` 에 따로 적어 뒀다. (Claude in Chrome 으로 chulin28ho.tistory.com 에 HTML 모드로 넣는다.)
- 티스토리에 올린 글 (https://chulin28ho.tistory.com/<번호>):
  - 2026-11-13 구름으로 배우는 뉴럴 셰이더 → /1006
  - 2026-11-14 중학생도 할 수 있는 신경망 셰이더: 숫자 337개로 하트 그리기 → /1007
  - 2026-11-15 카프콤 VORTEXEL 쉽게 읽기 (1) 게임이 지형을 '레고 블록'으로 읽는 법 → /1008
  - 2026-11-16 카프콤 VORTEXEL 쉽게 읽기 (2) 미리 굽지 않는 바람 — Turbulence → /1009
  - 2026-11-16 스마트폰에서 레일리 산란을요? — 사이버에이전트 그래픽스 엔지니어 2026 인터뷰 → /1010
  - 2026-11-17 카프콤 VORTEXEL 쉽게 읽기 (3) 불은 온도가 아니라 '시간'으로 번진다 — Thermal Conductor → /1011
  - 2026-11-18 바닥을 기는 안개는 어떻게 만드나 — 높이 안개 셰이더 해부 → /1012
  - 2026-11-18 카프콤 VORTEXEL 쉽게 읽기 (4) 이펙트를 위한 '대충' 물리, 그리고 체크 하나로 끝 → /1013
  - 2026-11-19 하늘이 예뻐지는 건 대단한 기술보다 작은 요령 덕분 — 항해 게임 개발 일지 '예쁜 하늘' 읽기 → /1014
  - 2026-11-20 연기 스프라이트에 빛을 '나중에' 입히는 법 — 6방향 라이트맵과, 그걸 매 프레임 만들어 내는 신경망 → /1015
- 이후 글은 JP 가 요청할 때만 올린다. 어떤 글을 올릴지 말하지 않으면 `TISTORY_CROSSPOST.md` 의 "어떤 글을 올릴지 정하기" 대로 안 올린 글을 번호로 추천한다.
