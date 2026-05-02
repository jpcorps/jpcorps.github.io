---
title: "Procedural Materials 에 대한 이야기. 섭스턴스 2부"
date: 2011-08-22T17:30:25Z
draft: false
---

뭐 섭스턴스가 어떤건지는 대충 알 것 같고, 사용하는 법도 알겠습니다만....  
그렇다면 이번엔 이걸 사용했을때 장단점도 알아봐야겠지요. 이놈이 이게 쓸 때 치명적인 문제가 있음 큰일나잖아요?   
안그래요 메튜? (섭스턴스 홍보담당 할아버지. 3번이나 날 만났는데도 여전히 못알아봄. 쳇.)  
  
그래서 긁어본 유니티 메뉴얼의 프로시져 메터리얼 내용중 옵티마이제이션 얘기입니다.   
  
===================================================================================

Performance and Optimization
----------------------------

Procedural Materials inherently tend to use less storage than bitmap images. However, the trade-off is that they are based around scripts and running those scripts to generate materials requires some CPU and GPU resources. The more complex your Procedural Materials are, the greater their runtime overhead.   
프로시져 텍스쳐는 근본적으로 비트맵 이미지보다 작습니다. 그럼에도 불구하고 거기에 상충해서, 이 이미지들은 스크립트로 제작되어 지고 돌아가는 메터리얼이기 때문에, 어쩔 수 없이 CPU와 GPU 자원을 소모합니다. (주: 메모리가 아니라 CPU 에서 만들어진다는 말이죠) 더 복잡한 프로시져 메터리얼들은, 더 큰 런타임 오버헤드를 유발시킵니다.

Procedural Materials support a form of caching whereby the material is only updated if its parameters have changed since it was last generated. Further to this, some materials may have many properties that could theoretically be changed and yet only a few will ever need to change at runtime. In such cases, you can inform Unity about the variables that will not change to help it cache as much data as possible from the previous generation of the material. This will often improve performance significantly.  
프로시져 메터리얼은 캐싱의 폼을 지원합니다. 그로써 메터리얼은 파라미터가 마지막 생성되었을 때 이후에 파라미터가 변경될때에나 업데이트 됩니다. 나아가서, 어떤 많은 설정값들을 가지고 있는 메터리얼은 이론적으로 변화가능하고 그리고 일부는 런타임에서 변화할 필요가 있을 겁니다. 그런 경우 유니티에게 변하지 않는 변수에 대해 알려주면 미리 생성된 재질로부터 가능한 많은 데이터들을 캐시에 담아놓을 수 있습니다.  
이것은 자주 의미있게 퍼포먼스를 향상시킵니다. 

Procedural Materials can refer to hidden, system-wide, variables, such as elapsed time or number of Procedural Material instances (this data can be useful for animations). Changes in the values of these variables can still force a Procedural Material to update even if none of the explicitly defined parameters change.

Procedural Materials can also be used purely as a convenience in the editor (ie, you can generate a standard Material by setting the parameters of a Procedural Material and then "baking" it). This will remove the runtime overhead of material generation but naturally, the baked materials can't be changed or animated during gameplay.   
프로시절 메터리얼은 맡길 수 있습니다. 히든에,  시스템-와이드, 변수들에, 이들의 시간이나 수의 프로시져 메터리얼 인스턴스와 같은 (이 데이터는 에니메이션에서 유용합니다) . 이런 변수들의 값의 변화는 심지어 이들의 파라미터가 극도로 변하더라도 프로시져 메터리얼의 업데이트에 영향을 끼칠 수 있습니다.   
프로시져 메터리얼은 또한 에디터에서 순수하게 편리하게 사용할 수 있습니다. (당신은 스텐다드 메터리얼을 생성할 수 있습니다. 프로시져 메터리얼을 셋팅하고 그걸 '베이킹' 하는 것으로) 이것은 런타임 오버헤드를 제거하지만 근본적으로, 베이킹한 메터리얼은 애니메이션이 안되지라우.

Using the Substance Player to Analyze Performance
-------------------------------------------------

Since the complexity of a Procedural Material can affect runtime performance, Allegorithmic incorporates profiling features in its Substance Player tool. This tool is available to download for free from [Allegorithmic뭩 website](http://www.allegorithmic.com/).

Substance Player uses the same optimized rendering engine as the one integrated into Unity 3.4, so its rendering measurement is more representative of performance in Unity than that of Substance Designer.   
프로시저 메터리얼의 복잡도는 런타임 퍼포먼스에 영향을 끼치는 관걔로, 알레고리드믹은 섭스턴스 플레이어 툴에다가 프로파일링 기능을 만들었지유. 이 툴은 알레고리드믹 웹사이트에서 받을 수 있구요.   
섭스턴스 플레이어는 유니티에 적용된 렌더엔진하고 같이 최적화 되었어요. 그래서 이 렌더링 측정기는 섭스턴스 디자이너보다 유니티에 더 대표적이라고 할 수 있지요.   
  
====================================================================================  
  
휘리릭 발번역이라 내용이 개판이지만 (...)   
대충 보기에도 원론적인 내용만 있다는 것을 알 수 있습니다. 그냥 '너무 복잡하게 쓰면 당근 느려지지' 라는 말 한 줄을 풀어쓴 것 밖에 안되는군요.   
  
뭐 일단 개념적으로, 텍스쳐의 메모리를 줄일 필요가 있거나 텍스쳐를 거대하게 사용하고 싶을 때에 주로 사용하는 것이 맞을겁니다. 또는 오버헤드 연산이 좀 남을 때 사용할 수 있겠지요. 우리 게임은 로직 연산량이 많은 편이라 가능할지 모르겠지만요...