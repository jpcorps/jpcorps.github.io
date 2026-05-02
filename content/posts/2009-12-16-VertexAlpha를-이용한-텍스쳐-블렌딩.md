---
layout: post
title: "VertexAlpha를 이용한 텍스쳐 블렌딩"
date: 2009-12-16 10:13:18
categories: [이글루스 백업, "2009-12"]
---

{% raw %}
..암것도 아닙니다. 말만 거창하지.   
해본게 처음이라 올린 것 뿐이빈다. (쿨럭)   
  
그래픽 작업하시는 분들에게 요청이 들어와서 알파채널로 합성하던걸 버텍스 알파를 이용하게 만들어 놓은 거지요.   
뭐 작업할땐 확실히 섬세하진 않아도 직관적이고 자유롭긴 하겠네요 :)   
  
![](/assets/images/posts/20091216_101318_c0055803_4b283453306c3.jpg)  
Vertex Alpha는 기본적이면서도 처음 써본거라..   
 PDP\_Color   6 PDT\_UByteColor 로 처리해야 한다는 것도 나름 신선하더군요.   
하긴 float이 아니라 255로 처리해야 하니까 UByteColor 를 사용해야겠지요:)   
(이런걸 처음보는 저는 초보)  
  
나머지는 걍   
float4 DTfinal = lerp(DT2, DT, In.VertexColors.a); // Blending by vertexalpha  
처리하면 끝...   
간단하긴 굉장히 간단했는데 오히려 시간내는게 더 힘들었어요 OTL   
{% endraw %}