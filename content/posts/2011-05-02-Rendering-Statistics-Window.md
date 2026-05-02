---
layout: post
title: "Rendering Statistics Window"
date: 2011-05-02 11:14:05
categories: [이글루스 백업, "2011-05"]
---

{% raw %}
# Rendering Statistics Window

The Game View has a Stats button top right. When this Stats button is pressed, an overlay window is displayed with realtime rendering statistics. This is very useful for helping to optimize your game. The statistics displayed vary depending on your build target.   
오른쪽 위 버튼 누르면 통계 나와요. 최적화할때 유용하지요. 이 통계표는 빌드 타겟에 영향받아요.

<!-- 로컬 경로 이미지 링크 제거됨 -->  
*Rendering Statistics Window.*

Statistics window contains the following information:

|  |  |
| --- | --- |
| Time per frame and FPS | How much time it takes to process and render one game frame (and resulting FPS). Note that this number only includes frame update and rendering of the game view; and does not include time taken in the editor to draw the scene view, inspector and other editor-only processing. |
| Draw Calls | How many objects are drawn in total. This accumulates objects that are drawn multiple times as well, for example some object that is affected by pixel lights will add several draw calls. |
| Batched (Draw Calls) | Number of draw calls that where batched together. Batching means that engine will be able to combine rendering of multiple objects into one draw-call which leads to lower CPU overhead. To ensure good batching you should share as many materials between different objects as possible. |
| Tris and Verts | Number of triangles and vertices drawn. This is mostly important when [optimizing for low-end hardware](Removed_Local_Path) |
| Used Textures | Count and memory size of textures used when drawing this frame. |
| Render Textures | Count and memory size of [Render Textures](Removed_Local_Path) that are created. Also displays how many times active Render Texture was switched during this frame. |
| Screen | Size, anti-aliasing level and memory taken by the screen itself. |
| VRAM usage | Approximate bounds of current video memory (VRAM) usage. Also shows how much video memory your graphics card has. |
| VBO total | Number of unique meshes (vertex buffers) that are uploaded to the graphics card. Each different model will cause new VBO to be created. In some cases scaled objects will cause additional VBOs to be created. In case of a static batching however number of objects can share same VBO.  그래픽 카드에 올라가는 독립된 메쉬의 수 (버텍스 버퍼). 각각의 다른 모델은 새로운 VBO가 생기는데 원인이 된다. 어떤 케이스에서는 스케일된 오브젝트가 VBO증가에 이유가 되기도 한다. 스테틱 배치의 케이스에서는 어쨌거나 오브젝트의 개수는 같은 VBO를 공유한다. |
| Visible Skinned Meshes | How many skinned meshes are rendered. |
| Animations | How many animations are playing. |
{% endraw %}