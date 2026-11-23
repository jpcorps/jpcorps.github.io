# jpcorps.com 글을 티스토리에 올리는 방법

JP 가 "티스토리에도 올려 줘"라고 하면 이 문서대로 한다. 컴퓨터가 바뀌거나 포맷돼도 이 문서만 읽으면 같은 방식으로 할 수 있다.
(2026-11-15 에 실제로 두 편을 올려 확인한 절차. 올린 글: https://chulin28ho.tistory.com/1007, /1008)

## 대상

- 티스토리 블로그: `chulin28ho.tistory.com` ("대충 살아가는 게임개발자"). JP 가 이 블로그가 맞다고 확인했다.
- JP 는 `gamedevforever.tistory.com` 도 갖고 있지만 거기에는 올리지 않는다.
- 글쓰기 주소: `https://chulin28ho.tistory.com/manage/newpost`

## 새 컴퓨터에서 처음 준비할 것 (사람이 해야 하는 것)

1. Chrome 에 **Claude in Chrome** 확장 프로그램을 설치한다. (Chrome 웹 스토어 → "Claude in Chrome")
2. 확장 프로그램 사이드 패널에 이 앱과 **같은 계정**으로 로그인한다.
3. 같은 Chrome 프로필에서 **티스토리에 로그인**한다. (카카오 로그인, 비밀번호 입력은 사람이 직접. Claude 는 비밀번호를 넣지 않는다.)
4. Claude 세션에서 `list_connected_browsers` 가 브라우저를 한 개 이상 돌려주는지 확인한다. 빈 목록이면 연결이 안 된 것이다.
   - 확장 프로그램을 껐다 켜고 사이드 패널을 다시 연다. 그래도 안 되면 데스크톱 앱을 새 세션으로 다시 연다. (연결이 중간에 끊겼다가 새 세션에서 다시 붙은 적이 있다.)

로그인 정보, 쿠키, 토큰은 이 저장소(public)에 절대 올리지 않는다.

## 어떤 글을 올릴지 정하기

JP 가 "티스토리에 글 올려 줘" 처럼 글을 지정하지 않고 말하면, 아래 순서로 **추천하고 번호로 받는다.** 번호를 받기 전에는 아무것도 발행하지 않는다.

1. **후보 찾기.** `content/posts/` 에서 front matter 에 `categories: ["테크니컬 아트"]` 가 있는 글만 후보다. (2천여 편의 이글루스 백업 글은 후보가 아니다.)
2. **이미 올린 글 빼기.** 이 저장소 `automation/NOTES.md` 의 "티스토리에 올린 글" 목록을 본다. JP 가 직접 올렸을 수도 있으니, 티스토리 글 목록(`https://chulin28ho.tistory.com/manage/posts/`)의 제목과도 비교해서 같은 제목이 있으면 뺀다.
3. **번호 목록으로 보여 주기.** 최신 글부터 번호를 붙인다. 형식 예:
   ```
   티스토리에 아직 안 올린 글이에요.
   1. (2026-11-16) 카프콤 VORTEXEL 쉽게 읽기 (2) 미리 굽지 않는 바람 — Turbulence  ← 추천
      - 한 줄 요약(front matter 의 summary)
   2. ...
   올릴 글 번호를 알려 주세요. (여러 개면 "1,2", 전부면 "전부")
   ```
   추천은 가장 오래된 미게시 글을 권하되(연재라면 순서대로 올려야 하므로), 이유를 한 줄로 적는다. 후보가 하나도 없으면 "안 올린 글이 없어요"라고 말한다.
4. **번호를 받으면** 아래 "올리는 절차"대로 한다. 여러 개면 오래된 것부터 하나씩 올리고 확인한다.
5. **올린 뒤에** 이 저장소 `automation/NOTES.md` 의 "티스토리에 올린 글" 목록에 날짜, 제목, 티스토리 번호를 덧붙이고 commit, push 한다.

## 올리는 절차

글 하나씩, **오래된 것부터** 올린다. 하나 올려서 문제없는지 확인한 뒤 다음 글로 간다.

1. **본문 가져오기.** 티스토리 글쓰기 탭에서 원본 페이지를 `fetch` 한다. (jpcorps.com 은 CORS 를 허용해서 된다.)
   - 제목: 원본 페이지 `<title>` 그대로.
   - 본문: `.article-content` 의 `innerHTML` 만.
   - `src`, `href` 의 상대 주소(`/images/...`, `/posts/...`)는 앞에 `https://jpcorps.com` 을 붙여 절대 주소로 바꾼다. `srcset` 은 지운다.
   - 그림은 티스토리에 따로 올리지 않는다. jpcorps.com 주소 그대로 불러온다.
   - 본문 맨 위에 "이 글은 jpcorps.com 에 먼저 올린 글입니다." 같은 안내 문구를 **넣지 않는다.** (JP 가 2026-11-16 에 빼 달라고 했다. 이미 올린 1007~1009 에서도 지웠다.) 본문은 `.article-content` 를 그대로 쓴다.
   - 원문 출처(슬라이드 등) 표기와 그림 캡션의 출처는 지우지 않는다.
2. **태그.** JP 가 준 태그를 쓴다. 안 줬으면 원본 글의 태그를 쓴다.
3. **카테고리.** 티스토리에 '테크니컬 아트' 카테고리가 있으면 그걸로, 없으면 비워 둔다. (2026-11-15 에는 없었다.)
4. **HTML 모드로 넣기.** 아래 "함정" 을 먼저 읽는다.
5. **미리보기로 확인.** 그림이 전부 뜨는지, 코드 블록이 깨지지 않는지 본다. 하나라도 이상하면 발행하지 않고 JP 에게 말한다.
6. **발행.** 완료 → 발행 창에서 **공개**를 고르고 "공개 발행". (기본값이 '비공개'다.)
7. 끝나면 티스토리 글 주소(`https://chulin28ho.tistory.com/<번호>`)를 JP 에게 알려 준다. 글 목록(`/manage/posts/`)에서 새 글 링크를 읽으면 된다.

## 함정과 요령

- **HTML 모드 전환 확인 창.** 편집 모드를 HTML 로 바꿀 때 브라우저 확인 창이 떠서 Claude in Chrome 이 멈춘다(클릭이 30초 뒤 시간 초과). 모드 전환 **전에** 페이지에서 `window.confirm = () => true; window.alert = () => {}` 를 실행해 둔다. 모드 전환은 `기본모드` 드롭다운 → `HTML` 을 클릭한다.
- **본문 입력은 TinyMCE 로.** HTML 모드의 입력창은 CodeMirror 인데, 거기에만 `setValue` 하면 미리보기의 본문이 비어 있다. `tinymce.get('editor-tistory').setContent(html)` 로 넣으면 CodeMirror 에도 같이 반영되고 미리보기도 나온다. 이때 코드 하이라이트용 `span`/`class` 는 정리되지만 글자와 줄바꿈은 그대로다. (넣은 뒤 글자 수와 `<pre>` 글자 수가 원본과 같은지 확인했다.) **`setContent` 뒤에 반드시 `editor.save()` 를 호출해야** 폼 필드에 동기화된다. 빠뜨리면 발행 후 본문이 비어 있다. (2026-11-16 에 겪음.)
- **제목 입력.** `#post-title-inp` 는 textarea 다. 네이티브 `value` setter 로 값을 넣고 `input`, `change` 이벤트를 보낸다.
- **태그 입력.** 화면 아래쪽 `태그입력` 칸을 `scroll_to` 로 찾아 클릭하고, 태그마다 **쉼표**를 붙여 입력한다. (`뉴럴 셰이더,신경망,...`)
- **JS 도구는 await 를 기다려 주지 않는다.** 비동기 `fetch` 는 결과를 `window.__x` 같은 전역 변수에 저장하고, 다음 호출에서 읽는다.
- **병렬 호출 주의.** 페이지 이동(`navigate`)과 같은 메시지에서 JS 를 실행하면 이동이 끝나기 전에 실행돼 실패한다. 이동 뒤 따로 실행한다.
- **작은 창.** Chrome 창이 좁으면 버튼 좌표가 달라진다. 스크린샷으로 확인하고 클릭한다. (미리보기, 완료, 모드 드롭다운은 화면 아래·위 고정 막대에 있다.)
- **미리보기 확인 방법.** 미리보기는 같은 페이지 안의 iframe 이다. 그 안의 `img.naturalWidth > 0` 과 `pre` 개수로 그림과 코드 블록을 확인할 수 있다.
- **임시저장 알림.** 글쓰기 화면에서 임시저장된 글 복구 팝업이 뜨면 새 글을 쓰는 거니까 "취소"를 눌러야 한다. 이 팝업은 브라우저 확인 창이라 Claude 가 못 누르고, 떠 있는 동안 화면 캡처와 클릭이 시간 초과로 막힌다. JP 에게 눌러 달라고 한다. (2026-11-16 에 겪음.)
- **로그인이 풀려 있을 때.** 글쓰기 주소가 `tistory.com/auth/login` 으로 넘어가면 로그인이 풀린 것이다. 티스토리 로그인 쿠키는 세션 쿠키라 Chrome 을 완전히 닫거나 재부팅하면 사라질 수 있다. 로그인은 JP 가 직접 한다. Claude 는 로그인 화면이 열린 Chrome 창을 띄워 주기만 한다. (Chrome 이 백그라운드에서만 돌면 창이 없으니 `Start-Process chrome <글쓰기 주소>` 로 연다.)
- Chrome 설정을 "중단한 위치에서 계속하기"(`chrome://settings/onStartup`)로 바꾸면 로그인이 덜 풀린다. `chrome://` 화면은 Claude 가 못 열어서 JP 가 직접 바꿔야 한다.

## 2026-11-23 에 /1016 을 올리며 확인한 보강 (처음부터 끝까지 그대로 된 순서)

JP 가 글 경로·제목·태그를 다 줬을 때의 흐름이다. 다른 컴퓨터에서도 이대로 하면 된다.

0. **글 파일이 없으면 `git pull`.** 글은 스케줄 작업이 원격에만 push 했을 수 있다. `git fetch` 후 `git status` 로 뒤처졌는지 보고 `git pull --ff-only`. 원본 주소가 열리는지(`curl -s -o /dev/null -w "%{http_code}" <원본주소>` → 200)도 본다. 안 열리면 배포 전이니 JP 에게 말한다.
1. **도구 불러오기.** ToolSearch 로 `mcp__claude-in-chrome__*` (tabs_context_mcp, navigate, computer, javascript_tool, find, list_connected_browsers) 를 한 번에 불러온다. `list_connected_browsers` 에 브라우저가 둘 나올 수 있는데 `onThisComputer: true` / `inUse: true` 인 쪽이 이 PC 다. 따로 고르지 않아도 된다.
2. **글쓰기 페이지 열기.** `tabs_context_mcp(createIfEmpty)` 로 탭을 얻고 `navigate` 로 `.../manage/newpost`. 주소가 `tistory.com/auth/login` 으로 넘어가면 로그인이 풀린 것이다. Claude 는 로그인하지 않고, `Start-Process chrome "<글쓰기 주소>"` 로 로그인 창을 띄운 뒤 JP 에게 부탁한다. "로그인 완료"를 받으면 같은 탭을 다시 `navigate` 한다.
3. **페이지 이동 뒤 따로** JS 를 실행해 confirm 을 막고 원본을 가져온다. 아래 코드를 한 번에 넣고, 결과는 다음 호출에서 읽는다.
   ```js
   window.confirm = () => true; window.alert = () => {}; window.__x = null;
   fetch('<원본 주소>').then(r=>r.text()).then(t=>{
     const d = new DOMParser().parseFromString(t,'text/html');
     const a = d.querySelector('.article-content');
     a.querySelectorAll('[src],[href]').forEach(e=>['src','href'].forEach(k=>{
       const v=e.getAttribute(k);
       if(v && v.startsWith('/') && !v.startsWith('//')) e.setAttribute(k,'https://jpcorps.com'+v)}));
     a.querySelectorAll('[srcset]').forEach(e=>e.removeAttribute('srcset'));
     window.__x = {title:d.title, html:a.innerHTML, imgs:a.querySelectorAll('img').length, pre:a.querySelectorAll('pre').length};
   });
   ```
   다음 호출에서 `__x.title`, `__x.imgs` 가 JP 가 말한 제목·그림 수와 맞는지 본다.
4. **HTML 모드.** 스크린샷(1037x583 기준) 으로 `기본모드` 드롭다운(우상단, 약 865,34) → `HTML`(약 848,145) 을 클릭한다. 위치는 창 크기에 따라 다르니 스크린샷으로 확인한다.
5. **제목·본문 넣기.** 한 번의 JS 로:
   ```js
   const t=document.querySelector('#post-title-inp');
   Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(t,__x.title);
   t.dispatchEvent(new Event('input',{bubbles:true})); t.dispatchEvent(new Event('change',{bubbles:true}));
   const ed=tinymce.get('editor-tistory'); ed.setContent(__x.html); ed.save();
   ```
   `ed.getBody().querySelectorAll('img').length` 가 원본 그림 수와 같은지 본다.
6. **태그.** `find` 로 `태그입력` 칸의 ref 를 얻어 `scroll_to` → `left_click` → `type` 으로 `태그1,태그2,...,` 를 **마지막에도 쉼표를 붙여** 입력한다. JS 로 `.tag` 요소 텍스트를 읽어 태그가 다 들어갔는지 확인한다.
7. **미리보기 확인.** `미리보기` 버튼(find 로 ref) 클릭 → 4초 기다림 → 페이지 안 iframe 중 **`id` 가 없는 것**이 미리보기다. 그 안의 `img` 를 `naturalWidth>0` 으로 센다. 목록에는 블로그 테마 아이콘(`daumcdn`, `new_ico_3.gif`)도 섞여 있으니, 주소로 본문 그림(`jpcorps.com`, 원문 출처 이미지)만 따져서 JP 가 말한 장수와 맞는지 본다. 확인 뒤 오른쪽 위 `X`(약 971,35)로 닫는다. 그림이 하나라도 안 뜨면 발행하지 않고 JP 에게 말한다.
8. **발행.** 닫은 직후 JS 로 `tinymce.get('editor-tistory').save()` 를 한 번 더 호출하고, `완료` 버튼(find 로 ref) 클릭 → 발행 창에서 `공개`(약 167,243) 선택 → `공개 발행`(약 566,521). 기본값이 `비공개` 라 반드시 바꾼다.
9. **발행 확인.** 발행되면 `/manage/posts/` 로 넘어간다. 거기서 `a[href*="chulin28ho.tistory.com/"]` 중 새 제목의 링크를 읽으면 번호가 나온다. 그리고 `fetch('/<번호>')` 로 받아 그림 수(`jpcorps`·원문 출처 이미지 `img`)와 `og:title` 을 확인하면 본문이 비지 않았다는 증거가 된다.
10. **기록.** `automation/NOTES.md` 의 "티스토리에 올린 글" 목록에 `- 날짜 제목 → /번호` 줄을 **"이후 글은 JP 가 요청할 때만…" 줄 바로 위에** 덧붙이고 commit, push 한다. (`git pull --ff-only` 를 먼저 한다.)

올린 기록: 2026-11-23 엔드필드 한 프레임 글 → /1016 (그림 8장, 위 순서 그대로 성공).

## 하지 않는 것

- 매일 자동으로 올리는 예약 작업은 만들지 않았다. 필요하면 JP 가 따로 요청한다. 공개 글이 자동으로 나가는 설정이니 반드시 JP 의 확인을 받는다.
- 로그인, 비밀번호, 캡차는 Claude 가 대신 하지 않는다.

## 참고: 예전에 JP 가 만들어 둔 도구

Google Drive 의 `youtube_to_gdocs` 폴더에 유튜브·논문 요약을 티스토리에 올리는 Playwright 도구(`tistory_publisher.py`)가 있다. 블로그 아이디(`chulin28ho`)와 "제목·본문을 채운 뒤 사람이 확인하고 발행" 흐름이 같다. 이 문서의 방식은 그 도구 대신 Claude in Chrome 으로 같은 일을 하는 것이다.
