---
layout: post
title: "Built-in state variables in shader programs"
date: 2011-04-20 11:09:57
categories: [이글루스 백업, "2011-04"]
---

{% raw %}
# Built-in state variables in shader programs

Often in [shader programs](https://unity3d.com/support/documentation/Components/SL-ShaderPrograms.html) you need to access some global state, for example, the current model\*view\*projection matrix, the current ambient color, and so on. There's no need to declare these variables for the built-in state, you can just use them in shader programs.

## Built-in matrices

Matrices (float4x4) supported:

UNITY\_MATRIX\_MVP
:   Current model\*view\*projection matrix

UNITY\_MATRIX\_MV
:   Current model\*view matrix

UNITY\_MATRIX\_P
:   Current projection matrix

UNITY\_MATRIX\_T\_MV
:   Transpose of model\*view matrix

UNITY\_MATRIX\_IT\_MV
:   Inverse transpose of model\*view matrix

UNITY\_MATRIX\_TEXTURE0 to UNITY\_MATRIX\_TEXTURE3
:   Texture transformation matrices

## Built-in vectors

Vectors (float4) supported:

UNITY\_LIGHTMODEL\_AMBIENT
:   Current ambient color.

:   으응... 월드 메트릭스로 변환하는건 없는건가...
{% endraw %}