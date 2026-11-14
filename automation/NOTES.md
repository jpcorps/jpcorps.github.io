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

## 알게 된 것

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
