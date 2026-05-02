---
layout: post
title: "Performance Tips when Writing Shaders in Unity"
date: 2011-02-11 14:44:04
categories: [이글루스 백업, "2011-02"]
---

{% raw %}
# Performance Tips when Writing Shaders

## Use Common sense ;)

Compute only things that you need; anything that is not actually needed can be eliminated. For example, supporting per-material color is nice to make a shader more flexible, but if you always leave that color set to white then it's useless computations performed for each vertex or pixel rendered on screen.

Another thing to keep in mind is frequency of computations. Usually there are many more pixels rendered (hence their pixel shaders executed) than there are vertices (vertex shader executions); and more vertices than objects being rendered. So generally if you can, move computations out of pixel shader into the vertex shader; or out of shaders completely and set the values once from a script.   
  
당신이 원하는 것만 계산하세요 ; 원하지 않는것은 제거될 수 있습니다. 예를 들어서 per 메터리얼 칼라는 쉐이더를 유연하게 만들어 줄때 좋습니다. 그렇지만 당신이 그걸 그냥 언제나 흰색으로 놔둔다면 그것은 렌더링 될때 쓸데없는 계산을 낭비하게 되는 것입니다.   
마음에 둘 또하나의 내용은, 계산의 반복여부입니다. 보통 많은 픽셀들이 버텍스(버텍스 쉐이더가 돌고)보다도 많게 렌더링되고 (그래서 픽셀쉐이더들도 따라서 돌고) ; 그리고 오브젝트보다 많은 개수의 버텍스들이 렌더링됩니다. 그러므로 가능하다면 계산을 픽셀 쉐이더보다 버텍스로 이동시키세요 (주: 버텍스 쉐이더를 많이 쓰세요) ; 혹은 쉐이더의 복잡도를 줄이고 스크립트에서 값을 한 번만 셋팅하세요.

## Less Generic Surface Shaders

[Surface Shaders](https://unity3d.com/support/documentation/Components/SL-SurfaceShaders.html) are great for writing shaders that interact with lighting. However, their default options are tuned for "general case". In many cases, you can tweak them to make shaders run faster or at least be smaller:  
   
가벼운 서피스 쉐이더   
  
서피스 쉐이더는 라이팅과 연산하는데 무척 훌륭합니다.(주: 멋진 결과물을 냅니다) 그럼에도 불구하고, 그들의 기본적인 옵션들은 '일반적인 케이스'에 맞게 튜닝되어 있습니다. 많은 경우에서, 당신은 쉐이더를 더 빠르거나 적어도 비슷하게 조정할 수 있습니다.  

* `approxview` directive for shaders that use view direction (i.e. Specular) will make view direction be normalized per-vertex instead of per-pixel. This is approximate, but often good enough.* approxview 뷰 디렉션을 직접 사용하는 쉐이더는 (스페큘러 같이 말이죠) 뷰 디렉션을 픽셀보다 버텍스에서 노말라이즈 하세요.  이건 뭐 대충인건 사실이지만 충분히 괜찮은 결과가 나옵니다.* `halfasview` for Specular shader types is even faster. Half-vector (halfway between lighting direction and view vector) will be computed and normalized per vertex, and [lighting function](https://unity3d.com/support/documentation/Components/SL-SurfaceShaderLighting.html) will already receive half-vector as a parameter instead of view vector.* halfasview  이 방식은 스페큘러쉐이더 타입 계산에서 빠릅니다. 하프벡터(라이트 디렉션과 뷰 벡터 사이의 중간값) 는 버텍스별로 계산하고 노말라이즈 합니다. 그리고 라이트 펑션은 언제나 하프 벡터를 뷰 벡터 대신에 받습니다. 그리고 라이팅 펑션을 사용하면 이미 뷰 벡터 대신에 하프 벡터를 받아오게 됩니다.

* `noforwardadd` will make a shader fully support only one directional light in Forward rendering. The rest of the lights can still have an effect as per-vertex lights or spherical harmonics. This is great to make shader smaller and make sure it always renders in one pass, even with multiple lights present.* noforwardadd  이것은 포워드 렌더링에서 다이렉트 라이트를 풀버전으로 서포트 합니다. 결과값은 라이트가 여전히 버텍스 단위의 효과를 나타내거나 공 모양의 하모닉스를 씁니다. 이것은 쉐이더를 작게 하거나 언제나 한 패스만 돌게 합니다. 심지어 여러 라이트가 있는 상황에서도 말입니다.* `noambient` will disable ambient lighting and spherical harmonics lights on a shader. This can be slightly faster.
    * noambient  는 엠비언트 라이트를 끄고 공 모양의 하모닉스라이트를 쓰는 쉐이더입니다. 이것은 쬐끔 빠릅니다.

## Precision of computations

When writing shaders in Cg/HLSL, there are three basic number types: `float`, `half` and `fixed` (as well as vector & matrix variants of them, e.g. half3 and float4x4):   
  
계산 정밀도   
CG나 HLSL 쉐이더를 쓸 때에는 3개의 넘버 타입이 있습니다. : float과 half와 fixed (벡터와 메트릭스 등에서도 말입니다. 예를들어 half3나 float4\*4 같은)

* `float`: high precision floating point. Generally 32 bits, just like float type in regular programming languages.* float : 높은 정밀도의 플로팅 포인트입니다. 보통 32비트입니다. 이것은 일반적 프로그래밍 언어의 플로트 타입 같은겁니다.* `half`: medium precision floating point. Generally 16 bits, with a range of -60000 to +60000 and 3.3 decimal digits of precision.* half : 중간 정도의 정밀도의 플로팅 포인트로, 보통 16비트입니다. 이것은 -60000 에서 +60000 의 범위를 가지고 있고 3.3 소수의 정밀도를 가지고 있습니다.* `fixed`: low precision fixed point. Generally 11 bits, with a range of -2.0 to +2.0 and 1/256th precision.
        * fixed : 낮은 정밀도의 고정된 포인트입니다. 보통 11비트죠. -2 에서 +2 의 범위를 가지고 있고 1/256th 정밀도를 가지고 있습니다.

Use lowest precision that is possible; this is especially important on mobile platforms like iOS and Android. Good rules of thumb are:  
 낮은 정밀도를 사용하는 것은 가능합니다 ; 이것은 특별히 모바일이나 안드로이드 플렛폼에서 말입니다. 열라 좋은 최고의 규칙은 ;

* For colors and unit length vectors, use `fixed`.* 칼라나 유닛의 길이 벡터는 fixed를 사용하세요.* For others, use `half` if range and precision is fine; otherwise use `float`.
    * 다른것은, 범위가 괜찮으면 half를 사용하세요 ; 아님 float 쓰시덩가.

On mobile platforms, the key is to ensure as much as possible stays in low precision in the fragment shader. On most mobile GPUs, applying swizzles to low precision (fixed/lowp) types is costly; converting between fixed/lowp and higher precision types is quite costly as well.   
모바일 플렛폼에서 열쇠는 프레그먼트 쉐이더에서 가능한한 낮은 정밀도를 유지시키는 것입니다. 많은 모바일 플렛폼의 GPU에서, 낮은 정밀도의 타입(fixed / lowp)을 섞는 것은 비쌉니다;  fixed/lowp 타입을 높은 정밀도 타입으로 컨버팅하는건 열라 비쌉니다.

## Alpha Testing

Fixed function [AlphaTest](https://unity3d.com/support/documentation/Components/SL-AlphaTest.html) or it's programmable equivalent, `clip()`, has different performance characteristics on different platforms:   
  
알파 테스팅   
고정함수인 알파 테스트나 그에 상응하는 계산인 clip() 은 플렛폼에 따라 다른 퍼포먼스를 내놓습니다.

* Generally it's a small advantage to use it to cull out totally transparent pixels on most platforms.* 보통 이것은 일반적 플렛폼에서 투명도로 물체를 잘라낼때 약간의 장점을 가집니다.* However, on PowerVR GPUs found in iOS and some Android devices, alpha testing is expensive. Do not try to use it as "performance optimization" there, it will be slower.
    * 그럼에도 불구하고,  PowerVR GPUs 를 사용하는 IOS나 안드로이드 디바이스에서는 알파 테스팅이 비쌉니다. '퍼포먼스의 절감' 을 위해서 사용하지 마세요. 이것들은 더 느리게 될겁니다.

## Color Mask

칼라 마스크  
  
On some platforms (mostly mobile GPUs found in iOS and Android devices), using [ColorMask](https://unity3d.com/support/documentation/Components/SL-Pass.html) to leave out some channels (e.g. `ColorMask RGB`) can be expensive, so only use it if really necessary.   
  
어떤 플렛폼에서 (iOS나 안드로이드 디바이스에서 찾을 수 있는 대부분의 모바일 GPU에서는) 는 칼라 마스크를 써서 몇몇 채널을 남겨 놓는 것이 더 비쌉니다. 그러므로 이건 꼭 필요할때만 사용하세요.
{% endraw %}