---
title: "fragment shader 기본형"
date: 2012-09-05T17:54:35Z
draft: false
---

Shader "TestRedShader" {  
    Properties {  
//      \_MainTex ("Texture1", 2D) = "white" {}  
//      \_BumpMap ("Bumpmap", 2D) = "bump" {}  
//     \_Texture2 ("Texture2", 2D) = "gray" {}  
//      \_Amount ("Texture1->Texture2", Range(0,1)) = 0.5  
    }  
      
      
Category{

 SubShader {  
  Tags{ "Queue"="Geometry" "RenderType"="Opaque" }  
    
  pass{  
     
   CGPROGRAM  
   #pragma vertex vert  
   #pragma fragment frag  
   #pragma ARB\_precision\_hint\_fastest  
//   #pragma target 3.0  
   #include "UnityCG.cginc"  
     
   struct v2f  
   {  
   float4 vertex : POSITION;     
   };  
     
   v2f vert (appdata\_full v)  
   {  
   v2f o;  
   o.vertex = mul(UNITY\_MATRIX\_MVP, v.vertex);  
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