---
title: "self shadow"
date: 2009-11-11T14:21:07Z
draft: false
---

[Game Dev./Shadows](http://www.egloos.com/category/Game%20Dev./Shadows) 2008/03/05 22:29 posted by sonee 

[![사용자 삽입 이미지](http://cfs5.tistory.com/upload_control/download.blog?fhandle=YmxvZzk4OTRAZnM1LnRpc3RvcnkuY29tOi9hdHRhY2gvMC82LkpQRw%3D%3D)](http://cfs5.tistory.com/upload_control/download.blog?fhandle=YmxvZzk4OTRAZnM1LnRpc3RvcnkuY29tOi9hdHRhY2gvMC82LkpQRw%3D%3D)

  
예전 D2 프로젝트를 진행하고, 지금 3D 야구게임 프로젝트를 하면서 저는 계속 라이팅과 그림자와 싸워왔습니다.-\_-  
  
그림자의 경우 간단한 프로젝션 쉐도우부터 쉐도우 볼륨, 스텐실 쉐도우, PSM, TSM, LISPM, CUBEMAP SHADOW 등 여러가지 방법을 테스트하고, 게임에 적용해봤습니다.  
Self Shadow 의 경우에는 Aliasing 때문에 정말 고생을 많이 했군요. 간단히 블러를 먹여도 보고, GRADIENT, VSM, SIMD, JITTER 등 여러가지를 시도해보았으나 OutDoor 를 하나의 텍스쳐를 사용하여 셀프 쉐도우로 표현하는 것은 결국 무리라고 최종 마무리를 지었습니다. 결국 CSM이나 PSSM 같은 방법이 그나마 OutDoor 에서 퀄리티 높은 그림자를 보여주네요. 그렇지만 지금 만들고 있는 야구게임같이 카메라의 줌인/아웃이 자유로운 상태에서는 CSM이나 PSSM 조차도 한계를 보입니다. double-precision 을 사용한다 해도 해결될 수 있는건 아니지요.  
  

|  |  |
| --- | --- |
| [사용자 삽입 이미지](http://cfs5.tistory.com/upload_control/download.blog?fhandle=YmxvZzk4OTRAZnM1LnRpc3RvcnkuY29tOi9hdHRhY2gvMC81LkpQRw%3D%3D) | [사용자 삽입 이미지](http://cfs5.tistory.com/upload_control/download.blog?fhandle=YmxvZzk4OTRAZnM1LnRpc3RvcnkuY29tOi9hdHRhY2gvMC83LkpQRw%3D%3D) |

  
  
이전에는 그림자기법을 개발하면서 이러한 OutDoor에 최적화된 최신 기술을 도입하면 좀 더 나은 퀄리티를 보여줄 것이다라는 기대를 하며 개발을 진행했는데, 이제와서 그림을 그려보면서 여러가지 쉐도우 기법 알고리즘을 표현해보니 역시나 지금 만드는 야구 게임에서는 위에 열거한 그림자 기법으로는 Aliasing 을 피할 수 없다라는 결론에 도달했습니다. 그럼 어떻게 해결할 수 있겠는가? 라는 질문을 하게 되는데 결국 각 장면에 최적화된 꽁수를 사용하는 방법밖엔 없겠다 라는 생각이 드는군요.  
  
Self Shadow의 경우 Light 에서 바라본 화면에서는 10pixel 을 차지하지만 실제 카메라로 바라본 화면에서는 10pixel 보다 훨씬 많은 부분을 차지하기 때문에 1:1 대응이 되지 않으므로 이러한 기법으로는 아무리 여러가지 방법(편차,보간,경사도)을 사용한다 해도 Aliasing 을 피할 수 없습니다.  
그나마 그림자 텍스쳐의 해상도가 클 수록 Aliasing 을  줄일 수 있고, 결국은 CSM, PSSM을 연동하면 되겠다 싶지만 카메라 줌인/줌아웃때문에 역시나 고민이 되는건 마찬가지군요.  
카메라 줌인을 하게 되면 화면에 보여지는 영역은 좁아지지만, 화면 안에 들어온 오브젝트는 멀리 있는 오브젝트도 크게 보이고, 가까이 있는 오브젝트도 크게 보이기 때문에 두 오브젝트의 그림자 퀄리티를 만족시키기에는 여간 힘든게 아니네요. 특히나 얼굴만 아주 크게 클로즈업 되는 경우에는 아주 죽을맛입니다. 클로즈업 한 캐릭터의 얼굴 옆 공간에 200미터 뒤에 수비수의 얼굴도 크게 나오거든요..-\_-  
  

[![사용자 삽입 이미지](http://cfs4.tistory.com/upload_control/download.blog?fhandle=YmxvZzk4OTRAZnM0LnRpc3RvcnkuY29tOi9hdHRhY2gvMC8zLkpQRw%3D%3D)](http://cfs4.tistory.com/upload_control/download.blog?fhandle=YmxvZzk4OTRAZnM0LnRpc3RvcnkuY29tOi9hdHRhY2gvMC8zLkpQRw%3D%3D)

  
  
여튼 realtime으로 SelfShadow 를 사용해야 한다면 다음과 같은 솔루션에 도달하게 됩니다.  
  
1. Diretional  
 - CSM + (VSM, GRADIENT)  
 - PSSM + (VSM, GRADIENT)  
 - TSM, LISPM + (VSM, GRADIENT)  
  
2. Spot  
 - (TSM, LISPM, PSM) + (VSM, GRADIENT, JITTER)  
  
3. Omni(Point Light)  
 - Cubemap Shadow  
  
(stencil을 사용하는 경우에는 칼같은 그림자가 보기에 그닥-\_- 이쁘지 않으므로 제외합니다)  
  
Cubemap shadow는 별다른건 없고, 걍 해당 라이트 기준에서 6방향으로 환경맵 만들듯이 찍어주면서 깊이를 텍스쳐에 기록합니다. 그리고 변환 matrix를 만들어서 uv 를 계산하여 처리합니다.  
  
위의 솔루션은 직접 테스트하면서 얻은 데이터와 여타 다른 게임들을 분석하면서 얻은 결과 입니다.  
  
realtime에서는 매 장면을 그릴때마다 그림자를 업데이트해줘야 하는 까닭에 퀄리티를 희생하고, 속도를 높이는 알고리즘으로 발전이 되어 왔습니다.   
그러나 하드웨어의 발전 속도와는 다르게 그림자 기법은 크게 발전하지 않았는데 어쩌면 지금까지 사용했던 텍스쳐에 라이트로 바라본 이미지 그리기를 버리고, 새로운 기법을 찾아보는 것이 맞을 지도 모르겠네요.