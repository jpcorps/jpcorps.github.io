---
title: "Unity Direction : UnityCG.cginc"
date: 2011-04-20T11:22:26Z
draft: false
---

이것뿐?   
  
  
// Computes world space light direction  
inline float3 WorldSpaceLightDir( in float4 v )  
{  
 float3 worldPos = mul(\_Object2World, v).xyz;  
 #ifndef USING\_LIGHT\_MULTI\_COMPILE  
  return \_WorldSpaceLightPos0.xyz - worldPos \* \_WorldSpaceLightPos0.w;  
 #else  
  #ifndef USING\_DIRECTIONAL\_LIGHT  
  return \_WorldSpaceLightPos0.xyz - worldPos;  
  #else  
  return \_WorldSpaceLightPos0.xyz;  
  #endif  
 #endif  
}

// Computes object space light direction  
inline float3 ObjSpaceLightDir( in float4 v )  
{  
 float3 objSpaceLightPos = mul(\_World2Object, \_WorldSpaceLightPos0).xyz;  
 #ifndef USING\_LIGHT\_MULTI\_COMPILE  
  return objSpaceLightPos.xyz - v.xyz \* \_WorldSpaceLightPos0.w;  
 #else  
  #ifndef USING\_DIRECTIONAL\_LIGHT  
  return objSpaceLightPos.xyz \* unity\_Scale.w - v.xyz;  
  #else  
  return objSpaceLightPos.xyz;  
  #endif  
 #endif  
}

// Computes world space view direction  
inline float3 WorldSpaceViewDir( in float4 v )  
{  
 return \_WorldSpaceCameraPos.xyz - mul(\_Object2World, v).xyz;  
}

// Computes object space view direction  
inline float3 ObjSpaceViewDir( in float4 v )  
{  
 float3 objSpaceCameraPos = mul(\_World2Object, float4(\_WorldSpaceCameraPos.xyz, 1)).xyz \* unity\_Scale.w;  
 return objSpaceCameraPos - v.xyz;  
}