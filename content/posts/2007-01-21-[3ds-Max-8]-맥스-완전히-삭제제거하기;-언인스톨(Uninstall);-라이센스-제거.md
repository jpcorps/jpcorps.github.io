---
layout: post
title: "[3ds Max 8] 맥스 완전히 삭제/제거하기; 언인스톨(Uninstall); 라이센스 제거"
date: 2007-01-21 00:36:49
categories: [이글루스 백업, "2007-01"]
---

{% raw %}
(3ds Max 버전 8 을 기준으로 설명)  
  
3ds Max를 다시 설치하거나 버전업을 하기 위해서는, 기존의 버전을 하드에서 깨끗이 삭제하는 것이 좋습니다. 그런데 3ds Max 는 여러가지 프로그램들로 구성되어 있는 방대한 소프트웨어이기에, 제거하는 것도 그리 간단하지 않더군요.  
  
  
윈도우 제어판의 "프로그램 추가/제거"에서  
  
\* Backburner (네트워크 렌더링 툴)  
\* Autodesk 3ds Max 8 Reference Files (도움말 파일)  
\* Autodesk 3ds Max 8 Architectural Materials (건축용 재질)  
\* Autodesk 3ds Max 8 Additional Maps and Materials (추가 맵과 재질)  
\* Autodesk 3ds Max 8 (맥스 본체)  
  
이상과 같은 것을 제거(언인스톨)합니다. 되도록 덜 중요한 것부터 제거하는 것이 안전하겠더군요.  
  
  
  
(맥스를 C: 드라이브에 설치했다고 가정)  
그런 후, 하드에서  
  
C:\Program Files\**Autodesk**  
C:\Program Files\Common Files\**Autodesk Shared**  
  
Autodesk... 라는 폴더가 남아 있다면 지웁니다. 물론 C:\Program Files\Common Files\ 이런 상위 폴더는 절대 지우면 안됩니다!!! 윈도우의 기본 폴더입니다.  
  
그리고 맥스 외에, 오토캐드 같은 Autodesk 사의 제품을 사용중이라면 "Autodesk..." 라는 이름의 폴더는 지우지 말아야 합니다. 아래도 마찬가지입니다:  
  
C:\Documents and Settings\All Users\Application Data\**Autodesk**  
이 폴더 안에는 라이센스 파일이 있는데, 만약 이 폴더를 지우면 맥스 판매처에 전화를 걸어서 맥스의 인증을 다시 받아야 합니다. 그래도 상관 없다면 지워도 됩니다.  
  
  
(C:\Documents and Settings\All Users\Application Data 폴더는 히든(Hidden) 폴더이기에, 잘 찾아지지 않을 수도 있습니다.)
{% endraw %}