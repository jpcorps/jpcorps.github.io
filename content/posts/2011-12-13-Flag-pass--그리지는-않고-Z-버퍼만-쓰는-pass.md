---
layout: post
title: "Flag pass : 그리지는 않고 Z 버퍼만 쓰는 pass"
date: 2011-12-13 09:35:55
categories: [이글루스 백업, "2011-12"]
---

{% raw %}
백업임.   
  
참고로   
Tags { "Queue"="Transparent+1" "IgnoreProjector"="True" "RenderType"="Transparent" }  
 Blend SrcAlpha OneMinusSrcAlpha  
였음.   
  
  
  
  
// flag pass  
     
 Pass   
 {  
 ColorMask A  
 Blend One Zero

 CGPROGRAM

 #pragma fragmentoption ARB\_precision\_hint\_fastest  
 #pragma vertex vert\_onlyAnimation  
 #pragma fragment frag\_alphaMask  
 #include "UnityCG.cginc"  
   
 struct v2f\_aniOnly {  
 float4 vertex : POSITION;  
 };  
   
   
   
 v2f\_aniOnly vert\_onlyAnimation(appdata\_full v)  
 {  
 v2f\_aniOnly o;  
       
 o.vertex = mul(UNITY\_MATRIX\_MVP, v.vertex);

 return o;  
 }  
   
   
   
 half4 frag\_alphaMask(v2f\_aniOnly i) : COLOR  
 {  
 return half4(0,0,0, 1);  
 }  
 

              
 ENDCG  
 }
{% endraw %}