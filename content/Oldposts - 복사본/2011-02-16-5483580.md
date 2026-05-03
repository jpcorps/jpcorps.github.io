---
title: "Unity 내장 shader는 계속 변하는 중"
date: 2011-02-16T09:31:21Z
draft: false
---

Built-in shaders라고 해서, Unity 홈페이지 가면 내장된 쉐이더들의 코드를 받아볼 수 있지요.   
이걸 이용하면 평소에는 막혀져 있어서 볼 수 없는 내장 쉐이더들의 코드를 볼 수 있는데,   
그 동안 계속 보다 보니까... 이게 계속 변하더라고요. 다운로드 받을때마다 변해있다능.   
아무래도 한참 발전하는 엔진이다보니 그럴 수 있겠죠.   
  
근데 최근의 추세를 보니 내장된 스크립트를 이용한 쉐이더들이, 전부 CG를 이용한 surface 쉐이더로 바뀌는 중.   
  
예를 들어 Diffuse만 봐도 이렇습니다.   
  

=================================================================================  
  
// Upgrade NOTE: replaced 'PositionFog()' with multiply of UNITY\_MATRIX\_MVP by position  
// Upgrade NOTE: replaced 'V2F\_POS\_FOG' with 'float4 pos : SV\_POSITION'

Shader "Diffuse" {  
Properties {  
 \_Color ("Main Color", Color) = (1,1,1,1)  
 \_MainTex ("Base (RGB)", 2D) = "white" {}  
}

Category {  
 Tags { "RenderType"="Opaque" }  
 LOD 200  
 /\* Upgrade NOTE: commented out, possibly part of old style per-pixel lighting: Blend AppSrcAdd AppDstAdd \*/  
 Fog { Color [\_AddFog] }  
   
 // ------------------------------------------------------------------  
 // ARB fragment program  
   
 #warning Upgrade NOTE: SubShader commented out; uses Unity 2.x per-pixel lighting. You should rewrite shader into a Surface Shader.  
/\*SubShader {  
  // Ambient pass  
  Pass {  
   Name "BASE"  
   Tags {"LightMode" = "Always" /\* Upgrade NOTE: changed from PixelOrNone to Always \*/}  
   Color [\_PPLAmbient]  
   SetTexture [\_MainTex] {constantColor [\_Color] Combine texture \* primary DOUBLE, texture \* constant}  
  }  
  // Vertex lights  
  Pass {   
   Name "BASE"  
   Tags {"LightMode" = "Vertex"}  
   Lighting On  
   Material {  
    Diffuse [\_Color]  
    Emission [\_PPLAmbient]  
   }  
   SetTexture [\_MainTex] { constantColor [\_Color] Combine texture \* primary DOUBLE, texture \* constant}  
  }  
  // Pixel lights  
  Pass {  
   Name "PPL"  
   Tags { "LightMode" = "Pixel" }  
CGPROGRAM  
// Upgrade NOTE: excluded shader from Xbox360; has structs without semantics (struct v2f members uv,normal,lightDir)  
#pragma exclude\_renderers xbox360  
#pragma vertex vert  
#pragma fragment frag  
#pragma multi\_compile\_builtin  
#pragma fragmentoption ARB\_fog\_exp2  
#pragma fragmentoption ARB\_precision\_hint\_fastest  
#include "UnityCG.cginc"  
#include "AutoLight.cginc"

struct v2f {  
 float4 pos : SV\_POSITION;  
 LIGHTING\_COORDS  
 float2 uv;  
 float3 normal;  
 float3 lightDir;  
};

uniform float4 \_MainTex\_ST;

v2f vert (appdata\_base v)  
{  
 v2f o;  
 o.pos = mul (UNITY\_MATRIX\_MVP, v.vertex);  
 o.normal = v.normal;  
 o.uv = TRANSFORM\_TEX(v.texcoord, \_MainTex);  
 o.lightDir = ObjSpaceLightDir( v.vertex );  
 TRANSFER\_VERTEX\_TO\_FRAGMENT(o);  
 return o;  
}

uniform sampler2D \_MainTex;

float4 frag (v2f i) : COLOR  
{  
 // The eternal tradeoff: do we normalize the normal?  
 //float3 normal = normalize(i.normal);  
 float3 normal = i.normal;  
    
 half4 texcol = tex2D( \_MainTex, i.uv );  
   
 return DiffuseLight( i.lightDir, normal, texcol, LIGHT\_ATTENUATION(i) );  
}  
ENDCG  
  }  
 }\*/  
   
  // ------------------------------------------------------------------  
 // Radeon 9000

 #warning Upgrade NOTE: SubShader commented out because of manual shader assembly  
/\*SubShader {  
  // Ambient pass  
  Pass {  
   Name "BASE"  
   Tags {"LightMode" = "Always" /\* Upgrade NOTE: changed from PixelOrNone to Always \*/}  
   Color [\_PPLAmbient]  
   SetTexture [\_MainTex] {constantColor [\_Color] Combine texture \* primary DOUBLE, texture \* constant}  
  }  
  // Vertex lights  
  Pass {   
   Name "BASE"  
   Tags {"LightMode" = "Vertex"}  
   Lighting On  
   Material {  
    Diffuse [\_Color]  
    Emission [\_PPLAmbient]  
   }  
   SetTexture [\_MainTex] { constantColor [\_Color] Combine texture \* primary DOUBLE, texture \* constant}  
  }  
    
  // Pixel lights with 0 light textures  
  Pass {   
   Name "PPL"  
   Tags {   
    "LightMode" = "Pixel"   
    "LightTexCount" = "0"  
   }

CGPROGRAM  
// Upgrade NOTE: excluded shader from OpenGL ES 2.0 because it does not contain a surface program or both vertex and fragment programs.  
#pragma exclude\_renderers gles  
#pragma vertex vert  
#include "UnityCG.cginc"

struct v2f {  
 float4 pos : SV\_POSITION;  
 float2 uv  : TEXCOORD0;  
 float3 normal : TEXCOORD1;  
 float3 lightDir : TEXCOORD2;  
};

uniform float4 \_MainTex\_ST;

v2f vert(appdata\_base v)  
{  
 v2f o;  
 o.pos = mul (UNITY\_MATRIX\_MVP, v.vertex);  
 o.normal = v.normal;  
 o.uv = TRANSFORM\_TEX(v.texcoord, \_MainTex);  
 o.lightDir = ObjSpaceLightDir( v.vertex );  
 return o;   
}  
ENDCG  
   Program "" {  
    SubProgram {  
     Local 0, [\_ModelLightColor0]  
     Local 1, (0,0,0,0)

"!!ATIfs1.0  
StartConstants;  
 CONSTANT c0 = program.local[0];  
 CONSTANT c1 = program.local[1];  
EndConstants;

StartOutputPass;  
 SampleMap r0, t0.str;   # main texture  
 SampleMap r1, t2.str;   # normalized light dir  
 PassTexCoord r2, t1.str;  # normal  
   
 DOT3 r5.sat, r2, r1.2x.bias; # R5 = diffuse (N.L)  
   
 MUL r0, r0, r5;  
 MUL r0.rgb.2x, r0, c0;  
 MOV r0.a, c1;  
EndPass;   
"  
    }  
   }  
   SetTexture[\_MainTex] {combine texture}  
   SetTexture[\_CubeNormalize] {combine texture}  
  }  
    
  // Pixel lights with 1 light texture  
  Pass {  
   Name "PPL"  
   Tags {   
    "LightMode" = "Pixel"   
    "LightTexCount" = "1"  
   }

CGPROGRAM  
// Upgrade NOTE: excluded shader from OpenGL ES 2.0 because it does not contain a surface program or both vertex and fragment programs.  
#pragma exclude\_renderers gles  
#pragma vertex vert  
#include "UnityCG.cginc"

uniform float4 \_MainTex\_ST;  
uniform float4x4 \_SpotlightProjectionMatrix0;

struct v2f {  
 float4 pos : SV\_POSITION;  
 float2 uv  : TEXCOORD0;  
 float3 normal : TEXCOORD1;  
 float3 lightDir : TEXCOORD2;  
 float4 LightCoord0 : TEXCOORD3;  
};

v2f vert(appdata\_tan v)  
{  
 v2f o;  
 o.pos = mul (UNITY\_MATRIX\_MVP, v.vertex);  
 o.normal = v.normal;  
 o.uv = TRANSFORM\_TEX(v.texcoord, \_MainTex);  
 o.lightDir = ObjSpaceLightDir( v.vertex );  
   
 o.LightCoord0 = mul(\_SpotlightProjectionMatrix0, v.vertex);  
   
 return o;   
}  
ENDCG  
   Program "" {  
    SubProgram {  
     Local 0, [\_ModelLightColor0]  
     Local 1, (0,0,0,0)

"!!ATIfs1.0  
StartConstants;  
 CONSTANT c0 = program.local[0];  
 CONSTANT c1 = program.local[1];  
EndConstants;

StartOutputPass;  
 SampleMap r0, t0.str;   # main texture  
 SampleMap r1, t2.str;   # normalized light dir  
 PassTexCoord r4, t1.str;  # normal  
 SampleMap r2, t3.str;   # a = attenuation  
   
 DOT3 r5.sat, r4, r1.2x.bias; # R5 = diffuse (N.L)  
   
 MUL r0, r0, r5;  
 MUL r0.rgb.2x, r0, c0;  
 MUL r0.rgb, r0, r2.a;   # attenuate  
 MOV r0.a, c1;  
EndPass;   
"  
    }  
   }  
   SetTexture[\_MainTex] {combine texture}  
   SetTexture[\_CubeNormalize] {combine texture}  
   SetTexture[\_LightTexture0] {combine texture}  
  }  
    
  // Pixel lights with 2 light textures  
  Pass {  
   Name "PPL"  
   Tags {  
    "LightMode" = "Pixel"  
    "LightTexCount" = "2"  
   }  
CGPROGRAM  
// Upgrade NOTE: excluded shader from OpenGL ES 2.0 because it does not contain a surface program or both vertex and fragment programs.  
#pragma exclude\_renderers gles  
#pragma vertex vert  
#include "UnityCG.cginc"

uniform float4 \_MainTex\_ST;  
uniform float4x4 \_SpotlightProjectionMatrix0;  
uniform float4x4 \_SpotlightProjectionMatrixB0;

struct v2f {  
 float4 pos : SV\_POSITION;  
 float2 uv  : TEXCOORD0;  
 float3 normal : TEXCOORD1;  
 float3 lightDir : TEXCOORD2;  
 float4 LightCoord0 : TEXCOORD3;  
 float4 LightCoordB0 : TEXCOORD4;  
};

v2f vert(appdata\_tan v)  
{  
 v2f o;  
 o.pos = mul (UNITY\_MATRIX\_MVP, v.vertex);  
 o.normal = v.normal;  
 o.uv = TRANSFORM\_TEX(v.texcoord, \_MainTex);  
 o.lightDir = ObjSpaceLightDir( v.vertex );  
   
 o.LightCoord0 = mul(\_SpotlightProjectionMatrix0, v.vertex);  
 o.LightCoordB0 = mul(\_SpotlightProjectionMatrixB0, v.vertex);  
   
 return o;   
}  
ENDCG  
   Program "" {  
    SubProgram {  
     Local 0, [\_ModelLightColor0]  
     Local 1, (0,0,0,0)

"!!ATIfs1.0  
StartConstants;  
 CONSTANT c0 = program.local[0];  
 CONSTANT c1 = program.local[1];  
EndConstants;

StartOutputPass;  
 SampleMap r0, t0.str;   # main texture  
 SampleMap r1, t2.str;   # normalized light dir  
 PassTexCoord r4, t1.str;  # normal  
 SampleMap r2, t3.stq\_dq;  # a = attenuation 1  
 SampleMap r3, t4.stq\_dq;  # a = attenuation 2  
   
 DOT3 r5.sat, r4, r1.2x.bias; # R5 = diffuse (N.L)  
   
 MUL r0, r0, r5;  
 MUL r0.rgb.2x, r0, c0;  
 MUL r0.rgb, r0, r2.a;   # attenuate  
 MUL r0.rgb, r0, r3.a;  
 MOV r0.a, c1;  
EndPass;   
"  
    }  
   }  
   SetTexture[\_MainTex] {combine texture}  
   SetTexture[\_CubeNormalize] {combine texture}  
   SetTexture[\_LightTexture0] {combine texture}  
   SetTexture[\_LightTextureB0] {combine texture}  
  }  
 }\*/  
   
 // ------------------------------------------------------------------  
 // Radeon 7000  
   
 Category {  
  Material {  
   Diffuse [\_Color]  
   Emission [\_PPLAmbient]  
  }  
  Lighting On  
  #warning Upgrade NOTE: SubShader commented out; uses Unity 2.x style fixed function per-pixel lighting. Per-pixel lighting is not supported without shaders anymore.  
/\*SubShader {  
   // Ambient pass  
   Pass {  
    Name "BASE"  
    Tags {"LightMode" = "Always" /\* Upgrade NOTE: changed from PixelOrNone to Always \*/}  
    Color [\_PPLAmbient]  
    Lighting Off  
    SetTexture [\_MainTex] {Combine texture \* primary DOUBLE, primary \* texture}  
   }  
   // Vertex lights  
   Pass {   
    Name "BASE"  
    Tags {"LightMode" = "Vertex"}  
    Lighting On  
    Material {  
     Diffuse [\_Color]  
     Emission [\_PPLAmbient]  
    }  
    SetTexture [\_MainTex] {Combine texture \* primary DOUBLE, primary \* texture}  
   }  
   // Pixel lights with 2 light textures  
   Pass {  
    Name "PPL"  
    Tags {  
     "LightMode" = "Pixel"  
     "LightTexCount"  = "2"  
    }  
    ColorMask RGB  
    SetTexture [\_LightTexture0]  { combine previous \* texture alpha, previous }  
    SetTexture [\_LightTextureB0] { combine previous \* texture alpha, previous }  
    SetTexture [\_MainTex] { combine previous \* texture DOUBLE }  
   }  
   // Pixel lights with 1 light texture  
   Pass {  
    Name "PPL"  
    Tags {  
     "LightMode" = "Pixel"  
     "LightTexCount"  = "1"  
    }  
    ColorMask RGB  
    SetTexture [\_LightTexture0] { combine previous \* texture alpha, previous }  
    SetTexture [\_MainTex] { combine previous \* texture DOUBLE }  
   }  
   // Pixel lights with 0 light textures  
   Pass {  
    Name "PPL"  
    Tags {  
     "LightMode" = "Pixel"  
     "LightTexCount" = "0"  
    }  
    ColorMask RGB  
    SetTexture[\_MainTex] { combine previous \* texture DOUBLE }  
   }  
  }\*/  
 }  
}

Fallback "VertexLit", 2

}  
=================================================================================  
  
이게 옛날에 받은 Diffuse.  
  
  
이게 요즘에는 Surface 쉐이더로 바뀌었더군요.   
  
===============================================================================  
Shader "Diffuse" {  
Properties {  
 \_Color ("Main Color", Color) = (1,1,1,1)  
 \_MainTex ("Base (RGB)", 2D) = "white" {}  
}  
SubShader {  
 Tags { "RenderType"="Opaque" }  
 LOD 200

CGPROGRAM  
#pragma surface surf Lambert

sampler2D \_MainTex;  
float4 \_Color;

struct Input {  
 float2 uv\_MainTex;  
};

void surf (Input IN, inout SurfaceOutput o) {  
 half4 c = tex2D(\_MainTex, IN.uv\_MainTex) \* \_Color;  
 o.Albedo = c.rgb;  
 o.Alpha = c.a;  
}  
ENDCG  
}

Fallback "VertexLit"  
}  
========================================================================  
  
  
그리고 이게 아이폰에서 더 빠르더군요.   
여기서 생각할 수 있는 이전 게시물에 이은 망상 : Diffuse Fast 가 Diffuse 보다 빠르다는건 옛날 쉐이더 기준으로 써 놓은게 아니었을까. 서피스 쉐이더로 바뀌기 전에는 당근 더 무거웠을 듯. 그리고 지금은 오히려 서피스 쉐이더로 짜는게 최적화를 더 잘하게 되어 있어서 대부분의 쉐이더를 서피스 쉐이더로 바꾸는게 아닐까. 하긴 뭐 더 짜기도 쉽고.