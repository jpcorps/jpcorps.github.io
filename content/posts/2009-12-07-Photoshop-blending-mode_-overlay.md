---
layout: post
title: "Photoshop blending mode_ overlay"
date: 2009-12-07 10:24:54
categories: [이글루스 백업, "2009-12"]
---

{% raw %}
<https://www.pegtop.net/delphi/articles/blendmodes/>  
  

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| |  |  |  |  |  |  |  |  |  |  |  | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |  |  |  |  |  |  |  |  | | --- | --- | --- | --- | --- | --- | --- | --- | | |  |  |  | | --- | --- | --- | |  | **overlay mode** |  |  |  |  |  |  | | --- | --- | --- | --- | | **Description:** A combination of screen and multiply mode, depending on the base color.  **Formula:**   |  |  | | --- | --- | | f(a,b) = | 2ab (for a < ½) | | 1 - 2 \* (1 - a) \* (1 - b) (else) |     **Disadvantage:** There is a separate formula for bright and for dark base colors, so there is a discontinuance for a = ½ (diagram 1 can be sparated into two parts).  **Code:** if a < 128 then result := (a\*b) SHR 7else result := 255 - ((255-a) \* (255-b) SHR 7); | | | |  | | --- | | [***index***](https://www.pegtop.net/delphi/articles/blendmodes/index.htm) | [***previous page***](https://www.pegtop.net/delphi/articles/blendmodes/difference.htm) | [***next page***](https://www.pegtop.net/delphi/articles/blendmodes/hardlight.htm) | | | |  |

  
그런데 정작 쉐이더 공식에 이미지 합성을 이렇게 했더니 원하는대로 안나온다. 뭔가 이유라도..?  
{% endraw %}