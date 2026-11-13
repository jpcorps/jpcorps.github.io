# jpcorps.github.io

"대충 살아가는 게임개발자"(jpcorps.com) 블로그. Hugo + hugo-theme-stack, main 에 push 하면 GitHub Actions 가 GitHub Pages 로 배포한다.

- `content/posts/` 의 글 대부분(2천여 편)은 이글루스 백업이다. 수정하거나 지우지 않는다.
- 테크니컬 아트 소개글을 쓸 때는 `automation/WRITING_GUIDE.md` 를 먼저 읽고 그대로 따른다.
- 테마는 서브모듈(`themes/hugo-theme-stack`)이다. 테마 파일을 직접 고치지 말고 `layouts/` 에서 덮어쓴다.
- 이글루스 백업 글은 이미지 수천 장을 포함하므로 clone 은 `--depth 1` 로 한다.
