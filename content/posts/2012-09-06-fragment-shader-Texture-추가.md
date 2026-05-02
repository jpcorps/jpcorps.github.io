---
layout: post
title: "fragment shader Texture 추가"
date: 2012-09-06 09:59:39
categories: [이글루스 백업, "2012-09"]
---

{% raw %}
Shader "TestRedShader" {  
Properties {  
**\_MainTex ("Texture1", 2D) = "white" {}**  
// \_BumpMap ("Bumpmap", 2D) = "bump" {}  
// \_Texture2 ("Texture2", 2D) = "gray" {}  
// \_Amount ("Texture1->Texture2", Range(0,1)) = 0.5  
}  
  
  
Category{

SubShader {  
Tags{ "Queue"="Geometry" "RenderType"="Opaque" }  
  
pass{  
  
CGPROGRAM  
#pragma vertex vert  
#pragma fragment frag  
#pragma ARB\_precision\_hint\_fastest  
// #pragma target 3.0  
#include "UnityCG.cginc"  
  
struct v2f  
{  
float4 vertex : POSITION;   
};  
  
**float4 \_MainTex\_ST;**  
  
v2f vert (appdata\_full v)  
{  
v2f o;  
o.vertex = mul(UNITY\_MATRIX\_MVP, v.vertex);  
**o.texcoord = TRANSFORM\_TEX (v.texcoord, \_MainTex);  
//o.texcoord = v.texcoord ; //해도 상관 없지만, shader option의 tiling 이나  offset 등을 적용하기 위해서는 위와 같이 해야 함**  
return o;  
}  
  
float4 frag(v2f i) : COLOR  
{  
float4 finalcolor = float4(1,0,0,1);  
return finalcolor;   
}  
ENDCG  
  
}//pass  
}//subshader  
}//Category   
  
  
}
{% endraw %}