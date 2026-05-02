---
title: "Unity Shader 기본 CG 쉐이더"
date: 2010-12-31T11:52:29Z
draft: false
---

유니티에서의 쉐이더 처리는 크게 3가지로 나눌 수 있다 (라고 지금까지는 보인다)   
  
1. 내장 스크립트로 처리하는 방법 : 가장 효율이 좋고 범용적이지만 할 수 있는게 별로 없다.   
2. CG 사용법 : 버텍스 쉐이더와 픽셀 쉐이더를 정해서 처리하는 법.   
3. 서페이스 라이팅 구조 : 라이팅 구조를 따로 작성해서 깊이 파고드는 법이다. inline등으로 직접 라이트 계산이 가능하다.  
  
아래는 라이팅 연산을 하지 않는, 이펙트를 위한 CG 기본구조를 CG와 서페이스 라이팅으로 만들어 본것.   
아직 연구중이라 틀린게 많을 수도 있다.  
  
  
밝혀낸것. (밝혀낸것 같은것 : 의문점들)   
  
- 애석하게도 CG 상태로 하면 내장된 텍스쳐의 타일링이나 옵셋 변화가 작동되지 않는다.   
- 서페이스 라이팅 구조를 사용하면 라이트 세트의 선택이 가능하지만, 조정에 한계가 있다.   
- CG 상태에서는 Pass 를 필수로 사용해야 하지만, 서페이스 라이팅 구조로 사용하면 Pass 를 사용하면 에러가 난다.

==============================================================  
그중 CG 사용의 기본구조. 단순 칼라 출력  
  
  
Shader "Color" {

Properties {  
   
\_Color ("Color Tint", Color) = (1,1,1,1)

}

SubShader {  
      
    ZWrite On  
    Tags { "Queue" = "Transparent" }  
    Blend SrcAlpha OneMinusSrcAlpha

    Pass {

CGPROGRAM

#pragma vertex vert  
#pragma fragment frag  
#include "UnityCG.cginc"

float4 \_Color;  
struct v2f {  
    V2F\_POS\_FOG;  
};

v2f vert (appdata\_base v)  
{  
    v2f o;  
    PositionFog( v.vertex, o.pos, o.fog );  
    return o;  
}

half4 frag (v2f i) : COLOR  
{  
    return \_Color;  
}  
ENDCG

    }  
}  
Fallback "Diffuse"

}  
  
==============================================================  
  
  
이번엔 거기다 텍스쳐추가 \* 아까 그 칼라에 곱셈

Shader "Color\_Texture" {

Properties{  
  \_Color ("Color Tint", Color) = (1,1,1,1)  
  \_MainTex ("MainTex", 2D) = "white" {}  
   }

SubShader   
 {  
  ZWrite On  
  Tags { "Queue" = "Transparent" }  
  Blend SrcAlpha OneMinusSrcAlpha  
   
 Pass   
  {  
   CGPROGRAM  
    
   #pragma vertex vert  
   #pragma fragment frag  
   //~ #pragma fragmentoption ARB\_fog\_exp2  
   #include "UnityCG.cginc"

   sampler2D \_MainTex;  
   float4 \_Color;  
    
  struct v2f   
   {  
    V2F\_POS\_FOG;  
    float4 texcoord : TEXCOORD0;  
   };  
     
  v2f vert (appdata\_base v)  
   {  
    v2f o;  
    PositionFog( v.vertex, o.pos, o.fog );  
    o.texcoord = v.texcoord;  
    return o;  
   }  
     
  half4 frag (v2f i) : COLOR  
   {  
    float4 Final = tex2D (\_MainTex, i.texcoord.xy) \* \_Color;  
    return Final;  
   }  
     
  ENDCG  
  }  
   
 }  
Fallback "Transparent/Diffuse"

}  
  
==============================================================  
  
서페이스 라이팅 구조로 붉은색만 나오게 만든 것.

Shader "Color\_Texture" {

Properties{  
  \_Color ("Color Tint", Color) = (1,1,1,1)  
  \_MainTex ("MainTex", 2D) = "white" {}  
   }

SubShader   
 {  
  ZWrite On  
  Tags { "Queue" = "Transparent" }  
  Blend SrcAlpha OneMinusSrcAlpha  
   
 //~ Pass   
  //~ {  
   CGPROGRAM  
    
   //~ #pragma vertex vert  
   //~ #pragma fragment frag  
   //~ #pragma fragmentoption ARB\_fog\_exp2  
   //~ #include "UnityCG.cginc"  
   #pragma surface surf Lambert

   sampler2D \_MainTex;  
   float4 \_Color;  
    
  /\* struct v2f   
   {  
    V2F\_POS\_FOG;  
    float4 texcoord : TEXCOORD0;  
   };  
     
    
     
  v2f vert (appdata\_base v)  
   {  
    v2f o;  
    PositionFog( v.vertex, o.pos, o.fog );  
    o.texcoord = v.texcoord;  
    return o;  
   }  
     
  half4 frag (v2f i) : COLOR  
   {  
    float4 Final = tex2D (\_MainTex, i.texcoord.xy)\* \_Color;  
    return Final;  
   }  
 \*/  
  struct Input   
   {  
    float2 uv\_MainTex;  
   };  
     
     
  void surf (Input IN, inout SurfaceOutput o)   
  {  
   o.Albedo = float4(1.0,0.0,0.0,1.0);  
   o.Normal = float3(0.0,0.0,1.0);  
   o.Emission = 0.0;  
   o.Gloss = 0.0;  
   o.Specular = 0.0;  
   o.Alpha = 1.0;  
  }  
     
  ENDCG  
  //~ }  
   
 }  
Fallback "Transparent/Diffuse"

}