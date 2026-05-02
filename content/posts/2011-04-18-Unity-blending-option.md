---
layout: post
title: "Unity blending option"
date: 2011-04-18 16:28:55
categories: [이글루스 백업, "2011-04"]
---

{% raw %}
AlphaTest GEqual [\_Cutoff]  
Blend SrcAlpha OneMinusSrcAlpha     // Alpha blending  
Blend One One                       // Additive  
Blend One OneMinusDstColor          // Soft Additive  
Blend DstColor Zero                 // Multiplicative  
Blend DstColor SrcColor             // 2x Multiplicative
{% endraw %}