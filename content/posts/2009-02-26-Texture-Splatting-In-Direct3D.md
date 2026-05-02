---
layout: post
title: "Texture Splatting In Direct3D"
date: 2009-02-26 21:00:56
categories: [이글루스 백업, "2009-02"]
---

{% raw %}
|  |
| --- |
| 역자: <https://blog.naver.com/lifeisforu/80023844066> |

역주 : 이 글에 대한 번역본은 없는 것 같아서 올려 봅니다. 예전에도 번역했던 것 같은 기억이 있는데... 홈페이지를 날려 먹어서 기억이 안 나네요. 일단 소개의 링크에 있는 글은 한 번씩 읽어보시기 바랍니다.

원문 : <https://www.gamedev.net/reference/articles/article2238.asp>

**Texture Splatting In Direct3D**

by Nate Glasser

**소개**

만약 지형 텍스처링 기법에 대해 공부해 왔다면, 아마도 텍스처 스플래팅에 대해서 들어 보았을 것이다. 이 개념은 Charles Bloom 에 의해서 만들어졌는데, 그는 <https://www.cbloom.com/3d/techdocs/splatting.txt> 에서 이에 대해 논의하고 있다 (번역본은 <https://blog.naver.com/dkdn111/8941198> 에 있음. 번역자에 대해서는 그 글의 상위에 있음). Charles Bloom 을 무시하려는 것은 아니지만, 그것은 더 이상 명확하거나 간결한 기사가 아니며, 혼란스러움을 남겨 왔다. 많이 사용되고 추천되는 반면, 일부는 그것을 충분히 설명하는데 시간을 할애해 왔다. 나는 그것을 둘러 싼 의혹들을 명확히 하고 당신의 지형 엔진에서 그것을 구현하는 방법에 대해서 설명하고자 한다.

**기초**

텍스처 스플래팅이란 무엇인가? 가장 간단한 형식으로 살펴 보자면 그것은 알파맵을 사용하여 서피스 상의 텍스처를 서로 블렌딩하는 방식이다.

나는 알파맵이라는 개념을 사용하여 단일 채널의 텍스처에 존재하는 그레이스케일 이미지를 참조할 것이다. 그것은 어떠한 채널이라도 될 수 있다. alpha, red, green, blue, luminance. 텍스처 스플래팅에서, 그것은 주어진 위치에서 텍스처가 얼마나 가시화될 것인지를 제어하는데 사용될 것이다. 그것은 단순한 곱셈( 알파맵 \* 텍스처 ) 에 의해서 수행될 것이다. 만약 알파맵의 텍셀 값이 1 이라면 그 텍스처는 그곳에서 전체 값으로 보일 것이다; 만약 알파맵의 텍셀 값이 0 이라면, 그 텍스처는 그곳에서 전혀 보이지 않게 될 것이다.

지형에 대해 그 텍스처는 잔디, 진흙, 암석, 눈, 또는 당신이 생각할 수 있는 여러 가지 유형의  지형일 수 있다. Bloom 은 텍스처 및 그것의 관련 알파맵을 스플랫(splat) 으로서 참조한다. 그것은 캔버스 위에 떨어진 페인트 방울(glob)로 비유될 수 있다. 스플랫은 당신이 그 페인트 방울을 볼 수 있는 모든 곳에 존재한다. 다중의 페인트 방울은 서로의 위에 겹쳐서 최종 그림을 만들어 낸다.

당신이 128 x 128 높이맵 지형을 가지고 잇으며, 32 x 32 의 크기를 가진 청크로 나누었다고 하자. 각 청크는 33 x 33 개의 정점으로 구성된다. 각 청크는 그 위에서 여러 번 반복되는 기저 텍스처를 가지고 있지만, 알파맵은 전체 영역에 대해서 펼쳐진다. 청크의 (0, 0) 좌표는 알파맵 좌표 (0, 0)을 가지며, 텍스처 좌표 (0, 0)을 가진다. 청크의 (33, 33) 좌표는 알파맵 좌표 (1, 1) 을 가지며, 텍스처 좌표 (x, x)를 가진다. 여기에서 x 는 텍스처가 반복되는 회수를 의미한다. x 는 텍스처 해상도에 달려 있다. 가까운 것은 충분히 반복할 필요가 있지만, 먼 것은 그렇게 많이 반복할 필요가 없다.

청크당 알파맵의 해상도는 당신 맘대로 하면 되지만, 2의 배승수를 추천한다. 32 x 32 청크에 대해 당신은 32 x 32 알파맵(유닛당 1텍셀), 64 x 64 알파맵(유닛당 2텍셀), 128 x 128 알파맵(유닛당 4 텍셀)을 가질 수 있다.(역주 : 여기에서 유닛(unit)이라고 하는 것은 타일을 의미한다.) 해상도를 결정할 때 주어진 청크 상에서 가시화되는 모든 텍스처에 대해서 알파맵을 필요로 한다는 것을 명심하기 바란다. 해상도가 높을 수록 블렌딩에 대한 제어는 더 많이 필요하고, 메모리를 더 필요로 하게 된다.

청크의 크기를 결정하는 것은 약간 미묘하다. 너무 작으면 상태 변경과 드로우 호출을 너무 많이 하게 되고, 너무 크면 알파맵의 대부분의 영역이 빈 공간이 된다. 예를 들어 유닛당 1텍셀을 가진 알파맵을 128 x 128 청크와 함께 생성하기로 했다고 할 때, 알파맵의 0 이 아닌 값이 4 x 4 영역이라면, 알파맵의 124 x 124 만큼의 메모리가 낭비된 것이다. 만약 청크 크기가 32 x 32 라면 단지 28 x 28 의 메모리만이 낭비될 것이다. 이것은 중요한 점을 상기시킨다 : 만약 주어진 텍스처가 주어진 청크에서 전혀 나타나지 않는다면, 그 청크에 그 텍스처를 위한 알파맵을 만들지 말라.

지형이 청크로 나뉘는 이유가 이제 나온다. 첫째 가장 중요한 부분으로 그것은 비디오 메모리를 절약할 수 있다. 둘째 그것은 필레이트(fillrate) 소비를 줄여줄 수 있다. 작은 텍스처를 사용함으로써 텍스처가 모든 청크에서 나타나지 않을 경우 비디오 카드가 수행해야 할 샘플링이 줄어든다. 셋째 그것은 지형이 어떤 식으로든 청크로 나뉘는 것을 요구하는 geomipmapping 과 같은 일반적인 LOD 기법에 들어 맞는다.

**블렌드 생성하기**

부드러운 블렌딩을 획득하는 핵심은 알파맵의 선형 보간이다. 0 다음에 바로 1이 온다고 가정하자. 알파맵이 전체 지형에 펼쳐질 때, Direct3D 는 두 값 사이의 블렌드를 생성한다. 그리고 나서 펼쳐진 알파맵은 지형 텍스처와 결합하여 텍스처 자체가 블렌딩되게 만든다.

Rendering then becomes the simple matter of going through each chunk and rendering the splats on it. 일반적으로 첫 번째 스플랫은 완전히 불투명할 것이며, 그 다음의 스플랫들은 알파맵에서 값이 변할 것이다. 특정한 상황에 대해 설명하도록 하겠다. 첫 번째 스플랫이 진흙이라고 하자. 그것은 먼저 청크상에 나타나기 때문에, 완전히 채워진(solid) 알파맵을 가지게 될 것이다.

![](https://blogfiles11.naver.net/data18/2006/4/26/250/splatting_01-lifeisforu.gif)

첫 번째 스플랫이 렌더링된 후, 이 청크는 진흙으로 뒤덮힌다. 그리고 나서 그 위에 잔디 레이어가 추가된다 :

![](https://blogfiles12.naver.net/data19/2006/4/26/59/splatting_02-lifeisforu.gif)

이 작업은 청크의 나머지 스플랫에 대해서 반복된다.

중요한 것은 각 청크에 대해서 같은 순서로 모든 것을 렌더링한다는 것이다. 스플랫 덧셈에는 교환법칙이 성립하지 않는다. 스플랫을 건너 뛰는 것은 어떠한 해도 끼치지 않지만, 순서를 변경하는 것은 다음과 같이 다른 모양으로 나타나게 만든다 :

![](https://blogfiles13.naver.net/data19/2006/4/26/284/splatting_03-lifeisforu.gif)

잔디 스플랫은 가려진다. 왜냐하면 진흙 스플랫이 완전히 불투명하고 두 번째로 렌더링되었기 때문이다.

당신은 왜 첫 번째 스플랫이 불투명해야만 하는지에 대해 궁금해 할 것이다. 그것이 불투명하지 않다고 하자. 그리고 대신에 잔디 스플랫이 존재하는 곳만 채워져 있다고 하자. 다음과 같은 일이 발생할 것이다 :

![](https://blogfiles1.naver.net/data20/2006/4/26/256/splatting_04-lifeisforu.gif)

이전에 블렌딩 했던 것과 비교했을 때 좋게 보이지 않는다는 것은 명확하다. 첫 번째 스플랫을 완전히 불투명하게 만듦으로써 당신은 위의 그림처럼 나타나는 것을 막을 수 있다.

**알파맵 생성하기**

이제 우리는 텍스처 스플래팅이 무엇인지 알게 되었다. 우리는 캔버스를 기술하기 위해서 알파맵을 생성할 필요가 있다. 그러나 알파맵에 어떤 값을 부여할 지를 어떻게 결정해야 하는가?

어떤 사람들은 지형 높이에 기반해서 그것을 결정하지만, 나는 알파맵을 당신이 원하는데로 만드는 기능을 부여하는 것을 추천한다. 이것은 제약 없이 원하는 곳에 텍스처를 배치하기 위한 유연성을 제공한다. 페인트 프로그램에서 채널을 그리기만 하면 된다. 더 좋은 방법은 아티스트가 알파맵을 확인하고 실제 월드에서 수정해 볼 수 있는 간단한 월드 에디터를 생성하는 것이다. (역주 : 차라리 자동으로 계산하는 것이 훨씬 나을 듯 합니다. 직접 알파맵 제작할 바에야 그냥 통맵 만들고 말지... 그렇지만 에디터에서 알파맵을 수정하는 기능을 추가해 준다면 더 낫겠죠.)

**구현**

단계를 다시 돌아보고, 우리가 가진 것들을 살펴 보자 :

- 높이맵과 같은 지형 표현의 정렬- 지형에 렌더링될 텍스처 집합- 각 텍스처를 위한 알파맵



세 번째를 살펴 보자. 우리는 각 알파맵이 텍스처로 존재해야 함을 알고 있다. 이것은 모든 알파맵이 자신만의 텍스처를 필요로 한다는 것을 의미하는가? 고맙게도 대답은 '그렇지 않다' 이다. 알파맵은 단지 텍스처의 단일 채널로서만 존재하기 때문에, 우리는 네 개의 알파맵을 단일 텍스처로 묶을 수 있다. 하나는 red, 하나는 green, 하나는 blue, 하나는 alpha 에 넣는다. 이들 개별 채널에 접근하기 위해, 우리는 픽셀 쉐이더를 사용할 필요가 있다. 그리고 다섯개의 텍스처를 필요로 하기 때문에(하나는 알파맵과 함께, 넷은 블렌딩을 위해), PS 1.4 가 요구된다. 안타깝게도 이것은 아직까지는 무리한 요구이다. 그래서 나는 픽셀 쉐이더 뿐만 아니라 고정함수 파이프라인을 사용해 텍스처 스플래팅을 사용하는 방법에 대해서도 보여줄 것이다.

**고정함수 파이프라인을 사용한 스플래팅**

고정 함수 파이프라인을 사용하는 것은 픽셀 쉐이더 기법을 사용하지 않는다는 이점을 가진다 : 그것은 비디오 카드에서 가상적으로 실행될 것이다. 그것이 요구하는 것은 알파맵당 하나의 텍스처 유닛, 텍스처당 하나의 텍스처 유닛, 올바른 블렌딩 상태이다.

나는 알파맵을 스테이지 0에 넣고, 텍스처를 스테이지 1에 넣기로 했다. 이것은 픽셀 쉐이더와의 일관성을 위한 것인데, 픽셀 쉐이더에서는 스테이지 0 에 알파맵을 설정한다. 텍스처 스테이지 스테이트는 그것보다는 상대적으로 직관적이다. 스테이지 0 은 그것은 알파값을 스테이지 1 로 전달한다. 스테이지 1 은 그 알파값을 자신의 것처럼 사용하며 자신의 색상 값과 그것을 한쌍으로 만든다.

// 알파맵 : 알파맵으로부터 알파를 취함. 색상은 신경쓰지 않음.  
g\_Direct3DDevice->SetTextureStageState(0, D3DTSS\_ALPHAOP, D3DTOP\_SELECTARG1);  
g\_Direct3DDevice->SetTextureStageState(0, D3DTSS\_ALPHAARG1, D3DTA\_TEXTURE);  
  
// 텍스처 : 텍스처로부터 색상을 취함. 이전 스테이지로부터 알파를 취함.  
g\_Direct3DDevice->SetTextureStageState(1, D3DTSS\_COLOROP, D3DTOP\_SELECTARG1);  
g\_Direct3DDevice->SetTextureStageState(1, D3DTSS\_COLORARG1, D3DTA\_TEXTURE);  
g\_Direct3DDevice->SetTextureStageState(1, D3DTSS\_ALPHAOP, D3DTOP\_SELECTARG1);  
g\_Direct3DDevice->SetTextureStageState(1, D3DTSS\_ALPHAARG1, D3DTA\_CURRENT);

다중 스플랫을 정확하게 결합하기 위해서 블렌딩 렌더링 스테이트도 설정해야만 한다. D3DRS\_SRCBLEND 는 렌더링되고 있는 스플랫으로부터 오는 알파이며, 우리는 그것을 D3DBLEND\_SRCALPHA 로 설정한다. 우리가 원하는 최종 방정식은 FinalColor = Alpha \* Texture + (1 - Alpha) \* PreviousColor 이다. 이것은 D3DRS\_DESTBLEND 를 D3DBLEN\_INVSRCALPHA 로 설정함으로써 수행된다.

g\_Direct3DDevice->SetRenderState(D3DRS\_ALPHABLENDENABLE, TRUE);  
g\_Direct3DDevice->SetRenderState(D3DRS\_SRCBLEND, D3DBLEND\_SRCALPHA);  
g\_Direct3DDevice->SetRenderState(D3DRS\_DESTBLEND, D3DBLEND\_INVSRCALPHA);

**픽셀쉐이더를 사용한 스플래팅**

왜 픽셀 쉐이더에 대해서 걱정하는가? 하나의 채널을 사용하는 것보다 텍스처 내의 이용 가능한 모든 채널을 사용하는 것이 메모리를 절약해 준다. 또한 단일 패스에서 네 개의 스플랫을 렌더링할 수 있도록 해 주기 때문에 변환에 필요한 정점 개수를 줄일 수 있다. 결합되는 모든 텍스처는 쉐이더 내에 배치되기 때문에, 고려해야 하는 텍스처 스테이지 스테이트가 존재하지 않는다. 우리는 단지 스테이지 0 에다가 각 채널 단위의 알파맵을 가진 텍스처를 로드하고, 스테이지 1 부터 4까지는 텍스처를 로드하고, 그리고 나서 렌더링하면 된다.

ps\_1\_4

////////////////////////////////  
// r0 : 알파맵  
// r1 - r4 : 텍스처  
////////////////////////////////

// 텍스처 샘플링  
texld r0, t0  
texld r1, t1  
texld r2, t1  
texld r3, t1  
texld r4, t1

// 텍스처들을 그것들의 알파맵에 기반해 결합한다  
mul r1, r1, r0.x  
lrp r2, r0.y, r2, r1  
lrp r3, r0.z, r3, r2  
lrp r0, r0.w, r4, r3

mul 명령어는 첫 번째 텍스처를 그것의 알파맵과 곱하는데, 이는 샘플러 0 의 텍스처의 red 채널에 저장되어 있는 알파값이다. lrp 명령어는 다음의 수학식을 수행한다 : dest = src0 \* src1 + (1 - src0) \* src2. r0.x 가 r1 에 저장된 진흙 텍스처의 알파맵이라고 하고, r0.y 는 r2 에 저장된 잔디 텍스처의 알파맵이라고 하자. r2 는 첫 번째 lrp 이후에 다음을 포함한다 : GrassAlpha \* GrassTexture + (1 - GrassAlpha) \* DirtBlended. 여기에서 DirtBlended 는 DirtAlpha \* DirtTexture 이다. 당신도 알겠지만 lrp 는 이전에 우리가 설정했던 렌더 스테이트와 텍스처 스테이지 스테이트와 같은 작업을 수행한다. 최종 lrp 는 r0 을 출력 레지스터로 사용하는데, 이는 최종 픽셀 색상으로서 사용되는 레지스터이다. 이것은 최종 mov 명령어에 대한 필요성을 없애 준다.

청크에 대해 두 개 혹은 세 개만의 스플랫을 렌더링할 필요가 있다면 어떻게 하는가? 만약 픽셀 쉐이더를 재사용하고자 한다면, 남은 채널들을 0 으로 채우기만 하면 된다. 그러한 방식을 사용하면 최종 결과에는 영향을 주지 않을 것이다. 아니면 두 개의 스플랫을 렌더링하거나 세 개의 스플랫을 렌더링하는 다른 픽셀 쉐이더를 생성할 수도 있다. 그러나 SetPixelShader 호출에 대한 부가적인 오버헤드는 명령어 두 개를 더 사용하는 것보다 더 안 좋을 수 있다.

당신이 청크에 대해서 네 개 이상의 스플랫을 렌더링하고자 한다면 다중 패스가 요구된다. 7개의 스플랫을 렌더링해야 한다고 가정하자. 첫 번째로 네 개를 렌더링하고, 나머지 세 개를 렌더링한다. 두 번째 알파맵 텍스처의 알파 채널은 0 으로 채워지며, 이는 네 번째 텍스처가 방정식에서 취소되는 결과를 낳는다. 당신은 알파맵 텍스처를 설정하고 세 개의 텍스처를 블렌딩하고 렌더링하게 된다. D3DRS\_BLEND 와 D3DRS\_SRCBLEND 스테이지는 픽셀 쉐이더의 lrp 와 같은 작업을 수행하는데, 이는 두 번째 패스가 첫 번째와 연속적으로 결합되도록 만든다.

**데모 프로그램**

The [demo application](https://downloads.gamedev.net/features/hardcore/splatting/TextureSplattingDemo.zip) uses the two techniques described here to render a texture splatted quad. I decided not to go for a full heightmap to make it as easy as possible to find the key parts in texture splatting. Because of this, the demo is completely fillrate limited. The initial overhead of the pixel shader may cause some video cards to perform worse with it than with its fixed function equivalent, so take the frame rates with a grain of salt. The pixel shader will almost always come out ahead in a more complex scene.

You can toggle between the fixed function pipeline and the pixel shader through the option in the View menu.

The textures used are property of nVidia® and are available in their full resolution at <https://developer.nvidia.com/object/IO_TTVol_01.html>.

**연결 부분의 문제점**

텍스처 스플래팅이 실망스러운게 있다면, 그것은 다음의 문제이다 : 두 개의 이웃하는 스플랫이 있을 때, 그것들 사이에 원하지 않는 단절 부분이 생성된다. 그 모양은 이전의 예제 스플랫을 네 번 타일링함으로써 생성될 수 있다.

![](https://blogfiles11.naver.net/data20/2006/4/26/58/seam-lifeisforu.gif)

왜 이런 일이 발생하는 것일까? 위의 두 영역(section)의 알파맵을 살펴 보자.

![](https://blogfiles5.naver.net/data19/2006/4/26/52/lineartexels-lifeisforu.gif)

둘 사이에 공백이 추가되었고 문제가 가시화되었다. 왼쪽에 존재하는 것은 오른쪽에 있는 것의 경계 값을 알지 못한다. 비디오 카드가 자신의 선형 블렌딩을 수행할 때, 그것은 흰색 텍셀 다음에 검은 색 텍셀이 존재하는지의 여부에 대해서 알 방법이 없다. 그것은 경계 부분과 같은 색상이라고 간주한다.

이것은 수정하기 쉬운 문제가 아니며, 많은 게임들이 그것을 방치해 둔다. 그것은 적절한 wrapping 텍스처 및 숙련된 레벨 디자이너에 의해서 감춰질 수 있다. 그러나 좋은 해결책이라 생각치는 않는다. 경험에 의하면 그것은 더 많은 문제를 가지고 있으며, 그것을 해결하는 것이 더 가치가 있다. 그리고 나는 텍스처 스플래팅의 이점이 그 이슈보다 중요하다고 믿는다.

**결론**

Hopefully this article has cleared up the mystery behind texture splatting. There are, of course, enhancements to be made, but texture splatting in its basic form is a powerful and flexible technique. It creates a smooth blend between different layers of terrain while giving detail at any distance and avoids the patterned look a detail map can give. Its main disadvantage is that it is very fillrate consuming, but with video cards becoming ever more powerful and the abilities of pixel shaders increasing, this is not an issue on modern and future hardware. Its ease of use and flexibility make it a perfect choice for texturing your terrain.

**소스**

Terrain Texture Compositing by Blending in the Frame-Buffer by Charles Bloom, <https://www.cbloom.com/3d/techdocs/splatting.txt>

And, of course, the helpful people at [https://www.gamedev.net](https://www.gamedev.net/)

Feel free to send any questions or comments to [nglasser@charter.net](mailto:nglasser@charter.net) or private message Raloth on the forums!

**[Discuss this article in the forums](https://www.gamedev.net/community/forums/topic.asp?key=featart&uid=2238&forum_id=35&Topic_Title=Texture+Splatting+in+Direct3D)**

Date this article was posted to GameDev.net: **4/23/2005**   
(Note that this date does not necessarily correspond to the date the article was written)

**See Also:**  
[Hardcore Game Programming](https://www.gamedev.net/reference/list.asp?categoryid=303)   

© 1999-2006 Gamedev.net. All rights reserved. [Terms of Use](https://www.gamedev.net/info/legal.htm#copyright) [Privacy Policy](https://www.gamedev.net/info/legal.htm#privacy)   
Comments? Questions? Feedback? [Click here!](https://www.gamedev.net/info/faq.asp)

![](https://blogimgs.naver.com/imgs/nblog/spc.gif)
{% endraw %}