---
title: "IOS performance in Unity"
date: 2011-06-28T11:05:35Z
draft: false
---

[iOS
===](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/Optimizing%20Graphics%20Performance.html)

If you want to optimize your content for iOS, then it is beneficial for you to [learn more about iOS hardware devices](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/iphone-Hardware.html).

Alpha-Testing
-------------

Contrary to the desktop, alpha-testing (or use of discard instruction in pixel shader) is very expensive on iOS. If you can replace your alpha-test shader with alpha-blend, do so. If you absolutely need to use alpha-testing, then you should keep areas of visible alpha-tested pixels to a minimum.

: 알파 테스트는 죄악이다! 라고 할 정도로 더럽게 비싸다고 써 놨는데... 실제 테스트해 봐도 - 나무를 빽빽히 심어서 비교해 봐도- 둘의 차이를 느끼기 힘듭니다. 아직까지 증명이 안된 관계로 정말? 이라고 믿을 수 없는 상황.

Vertex Performance
------------------

Generally you should aim at 40K or less vertices visible per frame when targeting iPhone 3GS or newer devices. You should aim at 10K or less vertices visible per frame when targeting older devices equipped with MBX GPU, such as: iPhone, iPhone 3G, iPod Touch 1st and 2nd Generation.

: 4만 폴리곤까지 쓸 수 있다라고 하는데... 구형 디바이스를 위해서는 만폴리곤으로 제한하라고 되어 있긴 한데... 실제로 테스트 해 보면 훨씬 더 쓸수 있단 말입니다.. 얼마였지...?

Lighting Performance
--------------------

Per-pixel dynamic lighting will add significant cost to every affected pixel and can lead to rendering object in multiple passes. Avoid having more than one Pixel Light affecting any single object, prefer it to be a directional light. Note that Pixel Light is a light which has a Render Mode setting set to Important.

라이트 선택하고 나오는 렌더 모드에서 important 선택하면 픽셀라이트로 가동됩니다. 픽셀 라이트 사용하지 말라고 하는 얘기지요. 이건 확실합니다. 느려져요. 라이트는 위의 두 가지 '버텍스 퍼포먼스와 알파' 보다 확실히 프레임에 밀접하게 영향을 끼칩니다.

Per-vertex dynamic lighting can add significant cost to vertex transformations. Avoid multiple lights affecting single objects. Bake lighting for static objects.

퍼 버텍스 라이트라 하더라도 어쨌건 IOS 에서는 여러 개 라이트는 금지. 버텍스 라이팅은 버텍스 트렌스포메이션에 코스트를 부여하지까요. 역시 언라이트 unlight 가 가장 빨라요.

Optimize Model Geometry
-----------------------

When optimizing the geometry of a model, there are two basic rules:

* Don't use excessive amount of faces if you don't have to
* Keep the number of UV mapping seams and hard edges as low as possible

Note that the actual number of vertices that graphics hardware has to process is usually not the same as what is displayed in a 3D application. Modeling applications usually display the geometric vertex count, i.e. number of points that make up a model.

For a graphics card however, some vertices have to be split into separate ones. If a vertex has multiple normals (it's on a "hard edge"), or has multiple UV coordinates, or has multiple vertex colors, it has to be split. So the vertex count you see in Unity is almost always different from the one displayed in 3D application.

하드 엣지가 뭐냐 했더니 멀티플 노말을 가진 버텍스로군요. 즉 폴리곤을 줄여라, 스무스 옵션을 꺼서 각진 오브젝트를 만들지 마라, uv 줄여라 하는 매우 고전적인 얘기.

Texture Compression
-------------------

Use iOS native [PVRT compression formats](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Components/class-Texture2D.html). They will not only decrease the size of your textures (resulting in faster load times and smaller memory footprint), but also can dramatically increase your rendering performance! Compressed texture requires only a fraction of memory bandwidth compared to full blown 32bit RGBA textures. For performance comparison check [iOS Hardware Guide](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/iphone-Hardware.html).

PVRT 포맷을 사용하란 말이군요. 단순히 사이즈만 줄이는게 아니라 메모리도 줄이고 로딩도 빠르고 킹왕짱이라는. 뭐 그래주죠. 알파 채널에서 압축되어서 깨지면 다른 툴로 극복해라...

Some images are prone to visual artifacts in alpha channels of PVRT compressed textures. In such case you might want to tweak PVRT compression parameters directly in your imaging software. You can do that by installing PVR export plugin or using [PVRTexTool](http://www.imgtec.com/powervr/insider/powervr-pvrtextool.asp) from Imagination Tech -- creators of PVRT format. Resulting compressed image with .pvr extension will be imported by Unity Editor as is and manually specified compression parameters will be preserved.

If PVRT compression formats do not deliver enough visual quality and you need extra crisp imaging (for example UI textures), then you should consider using 16bit texture over full 32bit RGBA texture. At least you will reduce memory bandwidth by half.

Tips for writing well performing shaders
----------------------------------------

Although GPUs fully support pixel and vertex shaders since iPhone 3GS, do not expect to grab a desktop shader with complex per-pixel functionality and run it on iOS device at 30 frames per second. Most often shaders will have to be hand optimized, calculations and texture reads kept to a minimum in order to achieve good frame rates.

쉐이더에서 그랩 grap 텍스쳐는 기대하지 말아라 ㅋㅋㅋ 안기대해 ㅋㅋㅋ

### Complex arithmetic operations

Arithmetic operations such as pow, exp, log, cos, sin, tan etc heavily tax GPU. Rule of thumb is to have not more than one such operation per fragment. Consider that sometimes lookup textures could be a better alternative.

Do NOT try to roll your own normalize, dot, inversesqrt operations however. Always use built-in ones -- this was driver will generate much better code for you.

Keep in mind that discard operation will make your fragments slower.

### Floating-point operations

Always specify precision of the floating-point variables while writing custom shaders. It is crucial to pick smallest possible format in order to achieve best performance.

If shader is written in GLSL ES, then precision is specified as following:

* highp - full 32bit floating-point format, well suitable for vertex transformations, slowest
* mediump - medium precision 16bit floating-point format, well suitable for texture UV coordinates, x2 faster than highp
* lowp - usually 12bit fixed-point format, well suitable for colors, lighting calculation and other high performant operations, x4 faster than highp

If shader is written in CG or it is a surface shader, then precision is specified as following:

* float - analogous to highp in GLSL ES, slowest
* half - analogous to mediump in GLSL ES, x2 faster than float
* fixed - analogous to lowp in GLSL ES, x4 faster than float

### Hardware documentation

Take your time to study Apple documentations on [hardware](http://developer.apple.com/library/ios/#documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/OpenGLESPlatforms/OpenGLESPlatforms.html%23//apple_ref/doc/uid/TP40008793-CH106-SW6) and [best practices for writing shaders](http://developer.apple.com/library/ios/#documentation/3DDrawing/Conceptual/OpenGLES_ProgrammingGuide/BestPracticesforShaders/BestPracticesforShaders.html). Note that we would suggest to be more aggressive with floating-point precision hints however.

Bake Lighting into Lightmaps
----------------------------

Bake your scene static lighting into textures using Unity built-in [Lightmapper](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/Lightmapping.html). The process of generating a lightmapped environment takes only a little longer than just placing a light in the scene in Unity, but:

* It is going to run a lot faster (2-3 times for eg. 2 pixel lights)
* And look a lot better since you can bake global illumination and the lightmapper can smooth the results

Share Materials
---------------

If a number of objects being rendered by the same camera uses the same material, then Unity iOS will be able to employ a large variety of internal optimizations such as:

* Avoiding setting various render states to OpenGL ES.
* Avoiding calculation of different parameters required to setup vertex and pixel processing
* Batching small moving objects to reduce draw calls
* Batching both big and small objects with enabled "static" property to reduce draw calls

All these optimizations will save you precious CPU cycles. Therefore, putting extra work to combine textures into single atlas and making number of objects to use the same material will always pay off. Do it!

Simple Checklist to make Your Game Faster
-----------------------------------------

* Keep vertex count below:
  + 40K per frame when targeting iPhone 3GS and newer devices (with SGX GPU) 4만 버텍스 아래로 !!!
  + 10K per frame when targeting older devices (with MBX GPU)
* Keep the number of different materials per scene low - share as many materials between different objects as possible.
* Set Static property on a non-moving objects to allow internal optimizations.
* Use PVRTC formats for textures when possible, otherwise choose 16bit textures over 32bit.
* Use combiners or pixel shaders to mix several textures per fragment instead of multi-pass approach.
* If writing custom shaders, always use smallest possible floating-point types:
  + fixed / lowp -- perfect for color, lighting information and normals,
  + half / mediump -- for texture UV coordinates,
  + float / highp -- avoid in pixel shaders, fine to use in vertex shader for vertex position calculations.
* Minimize use of complex mathematical operations such as pow, sin, cos etc in pixel shaders.
* Do not use Pixel Lights when it is not necessary -- choose to have only a single (preferably directional) pixel light affecting your geometry.
* Do not use dynamic lights when it is not necessary -- choose baking lighting instead.
* Choose to use less textures per fragment.
* Avoid alpha-testing, choose alpha-blending instead. : 이건 동의하기 힘듬. 결과를 보여줘!
* Do not use fog when it is not necessary.
* Learn benefits of Occlusion culling and use it to reduce amount of visible geometry and draw-calls in case of complex static scenes with lots of occlusion. Plan your levels to benefit from Occlusion culling.  어클루젼 컬링을 이용하라.. 뭐... 좋지..
* Use skyboxes to "fake" distant geometry.

See Also
--------

* [Optimizing iOS Performance](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/iphone-performance.html)
* [iOS Hardware Guide](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/iphone-Hardware.html)
* [iOS Automatic Draw Call Batching](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/iphone-DrawCall-Batching.html)
* [Modeling Optimized Characters](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/Modeling%20Optimized%20Characters.html)
* [Rendering Statistics](file:///Applications/Unity/UnityCrack.app/Contents/Documentation/Documentation/Manual/RenderingStatistics.html#RenderingStatisticsIPhone)