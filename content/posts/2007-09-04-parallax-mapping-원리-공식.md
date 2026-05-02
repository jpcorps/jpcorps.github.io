---
layout: post
title: "parallax mapping 원리 공식"
date: 2007-09-04 17:06:12
categories: [이글루스 백업, "2007-09"]
---

{% raw %}
[parallax\_mapping.pdf](https://pds5.egloos.com/pds/200709/04/03//parallax_mapping.pdf)  
  
![](/assets/images/posts/20070904_170612_c0055803_46dd02b340737.jpg)좌측이 일반 범프 맵핑. 오른쪽이 시차보정한 페럴렉스 맵핑.  
  
페럴렉스 맵핑 공식의 핵심은   
임의의 h 값을 정해서 그 값에 해당되는 뷰 벡터의 위치값에 해당하는 텍셀값을 계산한 다음에   
그 텍셀값을 찍어주는 공식.   
  
![](/assets/images/posts/20070904_170612_c0055803_46dd027a69ddd.jpg)  
여기서 즉. T(actual) 값은 틀린것이고,   
T (corrected)가 맞은 것이다.   
그래서 A에서 B 점으로 이동시켜야 하는데...  
  
![](/assets/images/posts/20070904_170612_c0055803_46dd031ec084a.jpg)그래서 강제로 eye vector 방향으로 Offset 값을 넣어서 이동시킨 좌표를 구한다음,   
그 좌표의 텍셀값을 넣음으로써 적당히 시차를 보정해 주는 것이다.   
  
여기서 핵심 공식은 Offset을 어떻게 이동시켜 주느냐는 것인데....  
아니 얼마나 이동시켜 주냐는 것인데,   
일단 기준치는 T0 점에서의 A 좌표의 높이값인 P 를 기준으로 해서 그 값을 이동시켜 준다.   
물론 오차율 \* 를 추가시켜주고...  
  
그럼 계산법은...   
우선 eye 벡터가 단위 벡터라고 쳐도, z 값은 1이 아니기 때문에 강제로 1로 만들어주는 공식을 쓴다.   
  
**EYE/EYE.z**  
=  ( EYE.x / EYE.z  ,  EYE.y / EYE.z ,  EYE.z / EYE.z )  
=  ( EYE.x / EYE.z  ,  EYE.y / EYE.z ,  1 )  
  
z값이 1이 되었다.   
그러면 이제 높이값인 P를 곱해주면, z값이 P 인 EYE 벡터의 xy값을 구할 수 있다.   
  
P\* ( EYE.x / EYE.z  ,  EYE.y / EYE.z ,  1 )  
=   ( P \* EYE.x / EYE.z  ,  P \* EYE.y / EYE.z ,  P \* 1 )  
  
**= P \*  EYE.xy / EYE.z**  
  
가 패럴렉스 맵의 공식이 된다.   
  
;This shader normal maps the walls with two lights.  The base map and normal  
;map are sampled using an offset texture coordinate computed via a parallax  
;mapping algorithm.  
;  
;H  = Height from height map  
;V  = View vector  
;To = The orginal texture coordinate in t0  
;Tn = The new texture coordinate used to sample the base and normal map.  
;Off= The texture offset scale.  
;  
;Tn = To + (V \* (H \* Off + (-0.5 \* Off))  
  
{% endraw %}