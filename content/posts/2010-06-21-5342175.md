---
title: "Texture sampling"
date: 2010-06-21T17:57:19Z
draft: false
---

아놔 알겠는데 왜 안되냐고.....  
  
========================================================================  
  
출처: 겜브리오 메뉴얼   
  
  
텍스처의 필터링  
  
xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /세 번째 텍스처링 문제는 (Gamebryo에서 "mipmapping"이나 "trilinear interpolation"이라고도 하는) pyramidal filtering은 텍스처의 VRAM 크기를 원래 크기의 1.3 배까지 증가시킨다는 점입니다. (summed area나 none과는 반대로) pyramidal filtering이 작동됐을 때는 텍스처를 필터 레벨(이 필터 레벨에서 각 레벨은 전 레벨의 1/4 크기가 됨)과 함께 저장해야 합니다. pyramidal filtering에선 텍스처의 앨리어싱(aliasing)이 개선되겠지만 VRAM에서 공간의 대가를 치르게 됩니다. 다시 말해서 pyramidal filtering은 씬의 시각적 품질을 향상시키며 거의 모든 경우에서 쓰이긴 하지만 pyramidal filter가 적용된 텍스처는 필요한 메모리를 1.3배까지 증가시킨다는 것입니다.

거의 수직으로 보이는 표면에 쓰이는 텍스처에 좋은 또 다른 필터링 모드가 있습니다. 이 모드는 anisotropic filtering으로서 추가적인 샘플을 최대 이방성의 방향으로 최대 개수까지 취합니다. 이 최대치는 조정이 가능하며 자동으로 런타임 하드웨어의 최대치가 되는 곳으로 고정됩니다. 하드웨어가 anisotropic filtering을 지원하지 않으면 대신 trilinear filtering으로 취급됩니다.

trilinear filtering과 anisotropic filtering의 차이는 텍스처들이 좀 더 날카로워지면서 커집니다.

주의: anisotropic filtering은 trilinear filtering보다 최대 N 배만큼 비용이 더 들 수 있습니다(여기서 N은 퀄리티와 최대 샘플 수). anisotropic filtering은 그것의 시각적인 효과가 나타날 곳에서만 써야 하며 N은 좋은 결과가 나오는 가장 작은 숫자로 설정해야 합니다.  
  
  
(정확한 텍스처 좌표가 구성된 후) 텍스처 맵의 색 기여도를 계산하는 두 번째 단계는 어떤 방식, 즉 어떤 "필터링"을 사용해서 텍스처 맵으로부터 색을 뽑아낼지를 결정하는 것입니다. Gamebryo 어플리케이션과 NIF 파일은 주어진 텍스처에 쓰이는 필터링 모드를 설정할 수 있습니다. Gamebryo는 6가지 필터 모드를 제공하는데, 이 여섯 모드를 두 개의 독립적인 카테고리로 나누어 생각할 수 있습니다. 즉, 한 밉맵(mipmap) 레벨에 걸쳐 두 가지 필터링 방식이 있으며, 밉맵 레벨들 간에 세 가지 필터링 방식이 있습니다.

한 밉맵 레벨 안의 두 가지 필터링 방식은 "nearest neighbor"와 "bilinear interpolation"입니다.

·         Nearest neighbor - 가장 가까운 텍스처 픽셀(텍셀)을 골라 그것을 사용합니다.

·         Bilinear interpolation - 텍스처 좌표를 에워싸는 네 개의 텍셀을 선형으로 보간합니다.

현재의 모든 하드웨어는 이 두 가지 방식을 모두 지원하는데, "bilinear interpolation"과 비교하여 "nearest neighbor"를 선택하는 이유는 단 하나, "뭉툭한(blocky)" 효과를 만들기 위해서입니다. "bilinear interpolation" 방식에선 텍스처가 뿌옇게 나오는데, 이는 디자이너가 주어진 텍스처에서 원하는 게 아닐 수도 있습니다.

보간을 처리할 정확할 밉맵 레벨을 고르는 세 가지 방식이 있습니다. 이들을 렌더링 비용과 품질이 높은 순으로 나열하면 다음과 같습니다:

·         None - 가장 간단한 방식은 밉맵핑을 아예 피하고, 매우 세밀한 형태의 텍스처를 보간에 사용하는 것입니다. 이것은 밉맵핑을 끄는 것과 같습니다.

·         Nearest - 다음 레벨은 가장 단순한 형태의 밉맵핑으로, 이 방식에서 밉맵 레벨은 픽셀의 상세 레벨을 맞추는 것과 가장 가깝습니다.

·         Linear - 원하는 상세 레벨을 에워싸는 두 개의 밉맵 레벨 즉, 굉장히 상세한 레벨과 별로 상세하지 않은 레벨을 선택한 뒤 이 두 레벨을 선형으로 보간합니다.

이 3x2 옵션에선 다음과 같은 여섯 가지 모드와 한 가지 추가 모드가 나옵니다:

|  |  |
| --- | --- |
| 필터 모드의 이름 | 필터 연산 |
| FILTER\_NEAREST | 밉맵핑 없이 "nearest neighbor"을 사용합니다. |
| FILTER\_BILERP | 밉맵핑 없이 "bilinear interpolation"을 사용합니다. |
| FILTER\_NEAREST\_MIPNEAREST | "nearest level mipmapping"을 사용한 뒤, 그 결과 위에 "nearest neighbor"을 사용합니다. |
| FILTER\_BILERP\_MIPNEAREST | "nearest level mipmapping"을 사용한 뒤, 그 결과 위에 "bilinear interpolation"을 사용합니다. |
| FILTER\_NEAREST\_MIPLERP | 가장 인접한 두 밉맵 레벨 각각에 "nearest neighbor"를 사용한 뒤, 그 결과들 사이에서 "linear mipmap interpolation"을 수행합니다. |
| FILTERP\_TRILERP | trilinear filtering이라 불림. 가장 인접한 두 밉맵 레벨 각각에 "bilinear interpolation"을 사용한 뒤, 그 결과들 사이에 "linear mipmap interpolation"을 수행합니다. |
| FILTER\_ANISOTROPIC | 이 필터링 모드는 trilinear와 비슷한 동작을 수행하나 최대 이방성 방향으로 (탭이라 불리는) 두 개 이상의 텍스처 샘플을 취함. |