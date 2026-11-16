# jpcorps.github.io

"대충 살아가는 게임개발자"(jpcorps.com) 블로그. Hugo + hugo-theme-stack, main 에 push 하면 GitHub Actions 가 GitHub Pages 로 배포한다.

- `content/posts/` 의 글 대부분(2천여 편)은 이글루스 백업이다. 수정하거나 지우지 않는다.
- 테크니컬 아트 소개글을 쓸 때는 `automation/WRITING_GUIDE.md` 를 먼저 읽고 그대로 따른다.
- 작업 전에 `automation/NOTES.md`(세션 간 공유 작업 노트: 지금까지 올린 글, 알게 된 함정과 요령)를 읽는다. 새로 알게 된 것은 거기에 덧붙인다.
- "티스토리에 글 올려 줘" 처럼 이 블로그 글을 티스토리(chulin28ho.tistory.com)에 올리라는 요청을 받으면, 먼저 `automation/TISTORY_CROSSPOST.md` 를 읽고 그 방법대로 한다. 컴퓨터가 바뀌어도 같은 방식이다.
  - 폰 등 어디서 명령하든 **JP-PC(항시 켜 두는 노트북)의 Chrome(Claude in Chrome 도구)** 으로 올린다. 클라우드 세션이라 Chrome 이 없다고 하지 말고, 이 PC 에 붙은 `mcp__claude-in-chrome__*` 도구를 불러(ToolSearch) 쓴다. 도구가 정말 없으면 오류 내용을 JP 에게 그대로 알린다.
  - JP 가 어떤 글인지 말하지 않았으면 문서의 "어떤 글을 올릴지 정하기" 대로 **아직 티스토리에 안 올린 글을 번호 목록으로 추천하고, JP 가 번호로 고른 글만** 올린다. 번호를 받기 전에는 발행하지 않는다.
- 테마는 서브모듈(`themes/hugo-theme-stack`)이다. 테마 파일을 직접 고치지 말고 `layouts/` 에서 덮어쓴다.
- 이글루스 백업 글은 이미지 수천 장을 포함하므로 clone 은 `--depth 1` 로 한다.
