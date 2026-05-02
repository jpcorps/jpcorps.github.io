---
title: "AT2/Char/Main"
date: 2011-04-22T16:58:35Z
draft: false
---

구시대 쉐이더. 버린것. 백업.

Shader "AT2/Char/Main" {

    Properties {  
 \_Color ("Main Color", Color) = (1,1,1,1)  
 \_SpecColor ("Main Specular Color", Color) = (0.5, 0.5, 0.5, 1)  
 \_Shininess ("Main Shininess (Normal.b)", Range (0.01, 1)) = 0.078125  
 \_SpecColor1 ("View Direct SpecColor (Only Forward)", Color) = (0.5, 0.5, 0.5, 1)  
 \_Shininess1 ("View Direct Shininess (Normal.b)", Range (0.01, 1)) = 0.078125  
 \_RimColor ("Rim Color", Color) = (0.26,0.19,0.16,0.0)  
 \_RimPower ("Rim Power", Range(0.5,8.0)) = 3.0  
    \_MainTex ("Texture", 2D) = "white" {}  
 \_BumpMap2 ("Normal Texture(RG)", 2D) = "grey" {}  
 \_Cutoff ("Alpha cutoff", Range (0,1)) = 0.0  
 \_GiLight\_Top ("GiLight Top", Color) = (0.5,0.5,0.5,0.0)  
 \_GiLight\_Bottom ("GiLight Bottom", Color) = (0.5,0.5,0.5,0.0)  
 \_WorldLightDir("WorldLightDir", Vector) = (0,-1,0,1)  
 \_DyeColor ("DyeColor (Normal.a)", Color) = (0.5,0.5,0.5,0.0)  
    
 \_RimColor2 ("Rim Color2", Color) = (0.26,0.19,0.16,0.0)  
 \_RimPower2 ("Rim Power2", Range(0.5,8.0)) = 3.0  
    }

    SubShader {  
     
    Tags {    
  //~ "RenderType" = "Opaque"  
  "RenderType"="TransparentCutout"  
  //~ "Queue"="Geometry"   
  //~ "Queue"="Transparent" //활성시 디퍼드  라이팅  동작 꺼짐  
  "IgnoreProjector"="True"  
  }  
 LOD 600

    Cull Back  
 ZWrite On  
     
     
     
 // Start CGPROGRAM /////////////////////////////////////////////////////////////////////////////////////////    
    CGPROGRAM  
   
 uniform float4 \_Color;  
 //~ uniform float4 \_SpecColor; //이미 정의되어 있어서 굳이 할 필요 없단다.   
 uniform float4 \_SpecColor1;  
 uniform float \_Shininess;  
 uniform float \_Shininess1;   
 uniform float4 \_RimColor;  
 uniform float \_RimPower;  
 uniform float \_Cutoff;  
   
 uniform sampler2D \_MainTex;  
 uniform sampler2D \_BumpMap2;

 uniform float4 \_GiLight\_Top;  
 uniform float4 \_GiLight\_Bottom;  
 uniform float4 \_WorldLightDir;  
 uniform float4 \_DyeColor;  
   
 uniform float4 \_RimColor2;  
 uniform float \_RimPower2;  
     
     
 #pragma surface surf SimpleLambertJP  
 #include "UnityCG.cginc"  
 #pragma target 3.0 // it's for prevent "arithmetic instruction limit" -JP-

 //Forward rendering light term ------------------------------------------------------------------  
 inline half4 LightingSimpleLambertJP (SurfaceOutput s, half3 lightDir, half3 viewDir, half atten)  
   {  
  half4 c;  
      
  // rim factor-----------------------------------------------------------------------------------------------  
  //~ float rim = pow(1- dot(s.Normal, viewDir),\_RimPower);  
  //~ half3 rimlight = rim\* \_RimColor.rgb;  
      
  // Rambert factor------------------------------------------------------------------------------------------  
  half NdotL = saturate(dot (s.Normal, lightDir));  
      
  // Specular factor------------------------------------------------------------------------------------------  
  half3 h = normalize( lightDir + viewDir );      
  float nh = saturate( dot( h, s.Normal ) );  
  float spec = pow( nh, s.Specular ) \* s.Gloss;  
      
  // View Direction Specular factor------------------------------------------------------------------------------------------  
  float nh1 = saturate( dot( viewDir, s.Normal ) );  
  float spec1 = pow( nh1, \_Shininess1\*128 ) \* s.Gloss;  
      
  //fake light-----------------------------------------------------------------------------------------------  
  //~ half3 GlTerm = saturate(CalculateGiLight(L1, s.Normal, \_GiLight\_Top))  ;  
  half GlTerm =dot(s.Normal, \_WorldLightDir.xyz)\*5+1;// It's for negative light. Don't use saturate  
  half3 GIColor = lerp (\_GiLight\_Bottom,\_GiLight\_Top,GlTerm)- half3(0.5,0.5,0.5);   
              
  // Final Calculation ------------------------------------------------------------------------------------------    
  c.rgb = s.Albedo \*\_Color\* \_LightColor0.rgb \* ((NdotL \* atten \* 2) + GIColor) ;  
  c.rgb += \_SpecColor.rgb \* spec;   
  c.rgb += \_SpecColor1.rgb \* spec1;   
  //~ c.rgb += rimlight;   
        c.a = s.Alpha;  
        return c;  
      }  
     
     
  //Deferred rendering light term ------------------------------------------------------------------  
/-  inline half4 LightingSimpleLambertJP\_PrePass (SurfaceOutput s, half4 light)  
 {  
  half4 c;  
    
  half3 spec = pow( light.a ,\_Shininess + 0.4) \*\_SpecColor.rgb \* s.Gloss ;  
  //fake light-----------------------------------------------------------------------------------------------  
  //~ half3 GlTerm = saturate(CalculateGiLight(L1, s.Normal, \_GiLight\_Top))  ;  
  half GlTerm =dot(s.Normal, \_WorldLightDir.xyz)\*2+1;// It's for negative light. Don't use saturate  
  half3 GIColor = lerp (\_GiLight\_Bottom,\_GiLight\_Top,GlTerm)- half3(0.5,0.5,0.5);   
     
  c.rgb = (s.Albedo\*\_Color \* light.rgb )+ GIColor;  
  c.rgb += spec;  
  c.a = s.Alpha + Luminance(spec);  
  return c;  
 }    
  \*-  
   
   
     
      struct Input {  
        float2 uv\_MainTex;  
        float2 uv\_BumpMap2;  
  float3 viewDir;  
      };

     
     
      void surf (Input IN, inout SurfaceOutput o) {  
      
  half4 MainTex = tex2D (\_MainTex, IN.uv\_MainTex);  
  clip(MainTex.a - \_Cutoff);  
  //----------------------------------------------------------------  
  //Normal1 method : NormalMap, Traditional method  
  //----------------------------------------------------------------  
  //~ half4 NormalTex = tex2D (\_BumpMap, IN.uv\_BumpMap);  
  //~ half3 UPNormal =UnpackNormal(NormalTex);  
   //~ o.Normal =  UPNormal;  
      
  //----------------------------------------------------------------  
  //Normal2 method : Texture , Old (Gamebryo) method  
  //----------------------------------------------------------------  
  half4 NormalTex2 = tex2D (\_BumpMap2, IN.uv\_BumpMap2);  
       
  /- if ( 1.0 == sign(IN.uv\_BumpMap2.x-1.0f) )  
 {    
  o.Normal =  (half3(NormalTex2.r,NormalTex2.g,1)\*2.0f-1.0f);  
  o.Normal = normalize(half3(-o.Normal.r,o.Normal.g,o.Normal.b));  
    
 }  
 else  
 { \*-  
  o.Normal =  normalize(half3(NormalTex2.r,NormalTex2.g,1)\*2.0f-1.0f);  
 //~ }  
  //----------------------------------------------------------------    
      
  // Rim ------------------------------------------------  
  float Fresnel= 1.0 - dot( normalize( float4(IN.viewDir, 1.0).xyz), o.Normal ) ;  
  float rim = pow(Fresnel,\_RimPower);  
  half3 rimlight = rim\* \_RimColor.rgb;  
    
  // Rim2------------------------------------------------------------------  
  float rim2 = pow(Fresnel+0.1,\_RimPower2);  
  half3 rimlight2 = rim2\* \_RimColor2.rgb;  
      
  //DyeColor -----------------------------------------------------  
  half3 Albedo;  
  half3 Dye = (1.0f - ((1.0f - \_DyeColor) \* (1.0f - MainTex.rgb)))\*2-1;  
  Albedo = lerp (Dye,MainTex.rgb,NormalTex2.a);

      
  o.Gloss = NormalTex2.b;  
  o.Specular = \_Shininess \* 128;  
        o.Albedo = Albedo ;  
  //~ o.Emission  = rimlight;  
  //~ o.Emission  = lerp (rimlight,rimlight2,rim2);  
        //~ o.Albedo = half3(1,0,0);  
  //~ o.Alpha = MainTex.a;  
  o.Alpha =1;

      }  
    
      ENDCG  
  // End CGPROGRAM /////////////////////////////////////////////////////////////////////////////////////////  
   
    }

    Fallback "Diffuse"  
  }