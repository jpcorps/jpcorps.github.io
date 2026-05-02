---
layout: post
title: "Shader Model 3.0 Fog"
date: 2010-05-28 11:24:07
categories: [이글루스 백업, "2010-05"]
---

{% raw %}
**Fog, Depth, and Shading Mode Changes**

When D3DRS\_SHADEMODE is set for flat shading during clipping and triangle rasterization, attributes with D3DDECLUSAGE\_COLOR are interpolated as flat shaded. If any components of a register are declared with a color semantic but other components of the same register are given different semantics, flat shading interpolation (linear vs. flat) will be undefined on the components in that register without a color semantic.

If fog rendering is desired, vs\_3\_0 and ps\_3\_0 shaders must implement fog. No fog calculations are done outside of the shaders. There is no fog register in vs\_3\_0 and additional semantics D3DDECLUSAGE\_FOG (for fog blend factor computed per vertex) and D3DDECLUSAGE\_DEPTH"/> (for passing in a depth value to the pixel shader to compute the fog blend factor) have been added.

Texture stage state D3DTSS\_TEXCOORDINDEX is ignored when using pixel shader 3.0.

간략하게 요약하자면

Shader 3.0 에서 Fog 연산은 Default 옵션은 아니고

D3DDECLUSAGE\_FOG 를 추가해서 사용하거나

PixelShader 에서 직접 연산 처리를 해줘야 한다.
{% endraw %}