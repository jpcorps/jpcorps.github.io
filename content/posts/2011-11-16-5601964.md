---
title: "Oren-Nayar Lighting Model"
date: 2011-11-16T11:47:02Z
draft: false
---

출처: 렐릭의 포프님!!  
공개하셨다길래 무의식중에 일단 퍼왔...  
  
  
Oren-Nayar Lighting Model

We used a lookup texture for optimization for a while  
( <http://content.gpwiki.org/index.php/D3DBook:(Lighting)_Oren-Nayar> )

●

half computeOrenNayarLighting\_TextureLookup( half3 N, half3 L, half3 V, half roughness )  
{  
half LdotN = dot( L, N );  
half result = saturate(LdotN);  
if ( roughness > 0 )  
{  
// compute the other aliases  
half VdotN = dot( V, N );  
half gamma = dot( V - N \* VdotN, L - N \* LdotN );  
half rough\_sq = roughness \* roughness;  
half A = 1.0 - 0.5 \* (rough\_sq / (rough\_sq + 0.33));  
half B = 0.45 \* (rough\_sq / (rough\_sq + 0.09));  
// The two dot-products will be in the range of  
// 0.0 to 1.0 which is perfect for a texture lookup:  
half2 tex\_coord = half2( VdotN, LdotN ) \* 0.5 + 0.5;  
half C = tex2D(gOrenNayarSampler, tex\_coord).x;  
result \*= (A + B \* max(0.0, gamma) \* C);  
}  
return result;  
}  
  
  
Oren-Nayar Lighting Model

But we made it even faster with an approximation

●

Practically, we didn't notice any badness from this

●

half ComputeOrenNayarLighting\_Fakey( half3 N, half3 L, half3 V, half roughness )

{

// Through brute force iteration I found this approximation. Time to test it out.

half LdotN = dot( L, N );

half VdotN = dot( V, N );

half result = saturate(LdotN);

half soft\_rim = saturate(1-VdotN/2); //soft view dependant rim

half fakey = pow(1-result\*soft\_rim,2);//modulate lambertian by rim lighting

half fakey\_magic = 0.62;

//(1-fakey)\*fakey\_magic to invert and scale down the lighting

fakey = fakey\_magic - fakey\*fakey\_magic;

return lerp( result, fakey, roughness );

}