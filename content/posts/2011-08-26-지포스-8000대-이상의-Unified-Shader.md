---
title: "지포스 8000대 이상의 Unified Shader"
date: 2011-08-26T17:15:18Z
draft: false
---

지포스 8000대의 하드웨어 성능표를 보니 버텍스 필레이트가 없네요??? 뭐지???  
그래서 조사하다가 알게 된 것. Unified Shader.  
  
다이렉트 X 10에서부터 요구하는 기본 사양인 "통합쉐이더 아키텍쳐 (Unified Shader)" 는   
지포스라면 8000 대 이상부터, AMD 는 HD2000 대 급 이상부터 적용되었으며,   
이 아키텍쳐의 특징은 다음과 같습니다.   
  
지금까지는 그래픽 카드에 버텍스 쉐이더 프로세서와 픽셀 쉐이더 프로세서가 독립되어 있었습니다. 다이렉트 X 9 지원하는 그래픽 카드까지는 말이죠. 이런 경우 단점은... 버텍스 연산이 심하고 픽셀 연산이 적을때는, 픽셀 쉐이더 프로세서가 놀고 있음에도 불구하고 버텍스 쉐이더 프로세서가 병목현상이 걸려서 게임이 느려집니다.   
반대로 말해서 픽셀 처리가 많아지면, 버텍스가 작더라도 느려진다는 거지요.   
  
![](/images/c0055803_4e5b5053820cf.png)

버텍스 쉐이더와 픽셀 쉐이더는 서로 절대 도와주지 않습니다

  
  
  
이런 단점을 극복하기 위해 만든것이 통합 쉐이더 아키텍쳐입니다. 이것은 즉 기존처럼 픽셀 쉐이더와 버텍스 쉐이더 프로세서가 독립되어 있는 것이 아닌, 그냥 통합된 하나의 쉐이더 프로세서가 존재하고, 이것이 픽셀이 무거우면 픽셀쪽으로, 버텍스가 무거우면 버텍스 쪽으로 유동적으로 이동하면서 처리해 준다는 말이지요.   
  
![](/images/c0055803_4e5b512e81e46.png)

통합 쉐이더 아키텍쳐에서는 서로 도와줍니다.

  
  
  
   
호오... 훌륭한 개념이네요. 정말 좋...   
근데...   
덕분에 그래픽 디자이너한테 '이정도로 만드세요' 하고 제한하기는 더더욱 힘들어 졌네요 OTL 유동적이 되었으니 제한이 없다는 거잖아요 ...   
형규는 '버텍스 버퍼' 로 계산해서 제한 때리라는데... 그래픽 디자이너들한테 그거 계산시키기가 쉽나... OTL   
  
최저사양은 그래도 아직 지포스 6000 ~ 7000대에서 머물테니까, 버텍스는 거기에 맞춰야 겠습니다만, 근데 거긴 또 디스턴스 컬링 옵션이 다를테니까 귀찮네요 ..   
  
일단 7000 대중에서 최고 성능의 그래픽 카드를 끼워다가 그걸 권장이라 생각하고 맞춰보는 작업부터 진행중입니다.   
7600만 봐도 <http://www.passmark.com/> 에서 비교해 봤을 때 8000 대보다 다소 떨어지긴 하지만 어렴풋이 힌트가 될 수 있을 것 같아서요.   
  
어쨌거나 이래서 다른 게임에서도 권장사양으로 8000 대 이상으로 하는 거였군요. 우리도 테스트는 해 보겠지만, 권장에서 훌륭한 그래픽을 나타내려면 8000 대 이상을 권장으로 하는 것이 맞아 보이긴 합니다.   
  
그래도 테스트는 일단 7600에 맞추는 이유는, 저사양때의 버텍스 / 픽셀 비례를 위해서이기도 하고 나중에 각종 기능과 캐릭터, 로직, 효과, UI 등이 추가되었을 때를 예상하기 위한 패널티랄까요.   
  
  
아래 글은 자료글입니다.   
  
======================================================================================  
  
  
  
출처 : <http://sadiles.blog.me/10088627648>  
  
  
  
  
\* embedded graphics hardware는 아직 unified shader core 기술이 적용되어 있지 않은 하드웨어가 많은 것 같다. 안타까운 일이다. 성능과 general computing 적합도를 고려해보면 언젠가는 unified shader core로 옮겨 가기는 하겠지만 말이다.

Q: What does unified shader core mean?

A: Historically, GPUs have had dedicated units for different types of operations in the rendering pipeline, such as vertex processing and pixel shading. With the unified architecture of the GeForce 8 Series, NVIDIA designed a single floating point shader core with multiple independent processors. Each of these independent processors can handle any type of shading operation, including pixel shading, vertex shading, geometry shading, and physics shading. GeForce 8 Series GPUs dynamically allocate processing power depending on the workload of the application, providing unprecedented performance and efficiency.

( Unified Shader Core를 설명하기 위하여 살짝 설명을 보태서 의역하면 아래와 같다. )

Q: unified shader core가 무엇인가요?

A: 역사적으로, GPU는 렌더링 파이프 라인에서 수행되는 각각의 단계별 작업에 특화된 여러개의 processing unit의 집합체였다. 예를 들어서, 그동안의 GPU는 vertex processing을 처리하는 vertex processor와 pixel shading을 처리하는 pixel processor의 집합체였다고 할 수 있다. (embedded 쪽의 GPU는 아직도 그렇다.)

GeForce 8 시리즈는 통합 구조의 GPU를 가지고 있다. 하나의 floating point shader core가 여러 개의 다른 일을 수행할 수 있다. 즉, 하나의 unified shader core가 pixel shading, vertex shading, geometry shading 그리고 physics shading과 같은 어느 타입의 작업이라도 처리할 수 있다는 것이다. 이 말은 작업량을 분할하여 처리하는데 효율성이 높아졌다는 것과 같다. 이전의 GPU구조에서는 vertex proessor와 pixel processor의 작업 부하를 사용자가 직접 조정하여 어느 한 쪽에 병목이 생기지 않도록 조정하여야 했다. 하지만, GeForce 8 시리즈의 unified shader core를 사용한 GPU는 응용 프로그램의 작업 부하에 따라서 동적으로 각각의 core에 처리량을 할당할 수 있다.

< Reference >

1. Site:<http://www.nvidia.com/object/geforce_8600_8500_faq.html>