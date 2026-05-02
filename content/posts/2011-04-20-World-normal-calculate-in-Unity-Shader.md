---
layout: post
title: "World normal calculate in Unity Shader"
date: 2011-04-20 11:19:57
categories: [이글루스 백업, "2011-04"]
---

{% raw %}
유니티에서 월드 노말 구하기  
정말 이 방법 뿐인가? 이녀석들은 노말맵을 자기들이 다 알아서 관리해서...   
  
  
struct v2f   
   {  
    float4 color : COLOR;  
    float4 vertex : POSITION;  
    float4 uvgrab : TEXCOORD0;  
    float2 uvmain : TEXCOORD1;  
    float3 TtoW0 : TEXCOORD2;  
    float3 TtoW1 : TEXCOORD3;  
    float3 TtoW2 : TEXCOORD4;  
    float3 viewDirWorld : TEXCOORD5;  
    float2 uvbump : TEXCOORD6;  
   }; //  어차피 appdata\_full 썼으니까 이건 필요 없지않남.   
  
  
  
v2f vert (appdata\_full v)  
   {  
    v2f o;  
    o.vertex = mul(UNITY\_MATRIX\_MVP, v.vertex);  
          
    TANGENT\_SPACE\_ROTATION;  
    o.TtoW0 = mul(rotation, \_Object2World[0].xyz \* unity\_Scale.w);  
    o.TtoW1 = mul(rotation, \_Object2World[1].xyz \* unity\_Scale.w);  
    o.TtoW2 = mul(rotation, \_Object2World[2].xyz \* unity\_Scale.w);   
      
    return o;  
   }  
  
  
float4 frag( v2f i ) : COLOR  
   {  
    // calculate world normal  
    float3 worldNormal;  
    worldNormal.x = dot(i.TtoW0, bump.xyz);  
    worldNormal.y = dot(i.TtoW1, bump.xyz);  
    worldNormal.z = dot(i.TtoW2, bump.xyz);  
    worldNormal = normalize(worldNormal);  
   
   }
{% endraw %}