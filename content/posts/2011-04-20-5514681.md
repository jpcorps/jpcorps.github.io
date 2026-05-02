---
title: "Unity Shader Tag"
date: 2011-04-20T10:59:44Z
draft: false
---

Shader replacement tags in built-in Unity shaders
-------------------------------------------------

All built-in Unity shaders have a "RenderType" tag set that can be used when rendering with replaced shaders. Tag values are the following:

* Opaque: most of the shaders ([Normal](http://unity3d.com/support/documentation/Components/shader-NormalFamily.html), [Self Illuminated](http://unity3d.com/support/documentation/Components/shader-SelfIllumFamily.html), [Reflective](http://unity3d.com/support/documentation/Components/shader-ReflectiveFamily.html), terrain shaders).
* Transparent: most semitransparent shaders ([Transparent](http://unity3d.com/support/documentation/Components/shader-TransparentFamily.html), Particle, Font, terrain additive pass shaders).
* TransparentCutout: masked transparency shaders ([Transparent Cutout](http://unity3d.com/support/documentation/Components/shader-TransparentCutoutFamily.html), two pass vegetation shaders).
* Background: Skybox shaders.
* Overlay: GUITexture, Halo, Flare shaders.
* TreeOpaque: terrain engine tree bark.
* TreeTransparentCutout: terrain engine tree leaves.
* TreeBillboard: terrain engine billboarded trees.
* Grass: terrain engine grass.
* GrassBillboard: terrain engine billboarded grass.