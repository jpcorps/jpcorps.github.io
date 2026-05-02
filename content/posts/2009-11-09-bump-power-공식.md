---
layout: post
title: "bump power 공식"
date: 2009-11-09 10:33:17
categories: [이글루스 백업, "2009-11"]
---

{% raw %}
    float3 bumps;  
  bumps.y = (Bumpy\* (tex2D(normalSampler,Tex.xy).xyz-0.5)).x;  
    bumps.x = (Bumpy\* (tex2D(normalSampler,Tex.xy).xyz-(0.5).xxx)).y;  
    bumps.z = (Bumpy\* (tex2D(normalSampler,Tex.xy).xyz-(0.5).xxx)).z;  
  
노말맵의 강도를 결정해 주는 듯.   
그것보다는 power에 가까운 것 같은데?   
공부해 볼 필요가 있을듯  
{% endraw %}