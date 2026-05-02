---
layout: post
title: "겜브리오 엔진지원 Position, Rotation,Scale"
date: 2008-05-07 15:58:31
categories: [이글루스 백업, "2008-05"]
---

{% raw %}
Position  
  
xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /

·         Linear Position

·         Bezier Position

·         TCB Position

·         Path constraint  
  
1대1 컨버전. 커브 에디터에서 가로 방향 수정은 컨버전 안됨. 세로는 됨.   
  
나머지는 30프레임 샘플링됨.

·         Position XYZ

·         Attachment

·         AudioPosition

·         Motion Clip SlavePos

·         Noise Position

·         Position Expression

·         Position Motion Capture

·         Position Reaction

·         Position Script

·         SlavePos

·         Spring

·         Surface

·         [Biped](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Animation/Position__Rotation__And_Scale.htm#Biped)

Max의 디폴트 position animation controller는 Position XYZ라는 점에 주의하세요. 이것은 지원되지 않으며 샘플링 될 것입니다.

  

Rotation

·         Euler XYZ

·         Linear Rotation

·         Smooth Rotation

·         TCB Rotation  
  
1대 1 컨버전됨.  
가장 빠르고 정확한 결과를 얻으려면 Linear Rotation Controller를 사용하세요  
엔진에서 보간(interpolating) 할 때는 Linear key가 계산하기에 가장 빠르고,   
Euler XYZ key(Max의 디폴트)가 계산하기에 가장 느립니다.  
  
모두 다 100% 완벽한 것은 아님.  
  
나머지는 모두 30프레임 샘플링.

·         AudioRotation

·         LookAt Contstraint

·         MotionClip SlaveRotation

·         Noise Rotation

·         Orientation Constraint

·         Rotation List

·         Rotation Motion Capture

·         Rotation Reaction

·         Rotation Script

·         SlaveRotation

·         [Biped](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Animation/Position__Rotation__And_Scale.htm#Biped)

·         [IK](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Animation/Position__Rotation__And_Scale.htm#Bones)

Scale  
non-uniform scale 애니메이션은 지원되지 않습니다. 스케일, 이동, 회전은 오브젝트 레벨에서 처리할 수 있습니다. non-uniform scaling이나 squashing은 버텍스 레벨에서 처리해야 합니다. 어떤 것을 non-uniform 식으로 스케일 하거나 찌그러뜨려야(squash) 한다면 morph target을 사용하십시오. 몰프 타깃은 3ds max에서 오브젝트를 찌그러뜨리고 Tools / Snapshot으로 원하는 몰프 타깃을 구해서 생성할 수 있습니다.

Supported Scale

Gamebryo는 아래 컨트롤러들을 직접 지원하며, 이들은 1대1 key conversion이 됩니다:

·         Bezier Scale

·         Linear Scale

·         TCB Scale

Sampled Scale

Gamebryo는 아래 컨트롤러들을 직접 지원하지 않으며, 여기선 키프레임이 30 FPS로 샘플링 됩니다:

(자세한 사항은 [Supported Controllers vs Sampling](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Animation/Position__Rotation__And_Scale.htm#Supported_Controllers_vs_Sampling) 섹션을 참조하세요.)

·         AudioScale

·         Motion Clip SlaveScale

·         Noise Scale

·         Scale Expression

·         Scale List

·         Scale Motion Capture

·         Scale Reaction

·         Scale Script

·         ScaleXYZ

·         SlaveScale

오브젝트 모양(shape)의 애니메이션

Gamebryo 3ds max Plug-in에선 melt, noise, twist, taper와 같이 좀 더 복잡한 modifier들도 애니메이트 되지 않습니다. 여기서도 이런 오브젝트를 생성하는 올바른 방법은, 원래의 modifier를 사용하고 애니메이트 되고 있는 메쉬의 스냅샷을 찍어서 Morph-target key-frame을 생성하는 것입니다.

Biped

Character Studio는 Biped 애니메이션에 TCB 키를 사용하나, 불행하게도 TCB 파라미터 중 어떤 것도 익스포트 하지 못합니다. 이런 사실로 인해, Gamebryo 3ds max Plug-in은 컨트롤러를 샘플링 합니다. 자세한 사항은 [Exporting](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Exporting/Gamebryo_3ds_max_Export_Options1.htm) 섹션의 [Animation Options Sub-panel](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Exporting/Gamebryo_3ds_max_Export_Options1.htm)을 참조하세요.

Bones

bone의 모든 Inverse Kinematics 세트는 프레임 당 샘플링 되고, 남아도는 키프레임들은 익스포트 동안 최적화 과정에서 줄어듭니다. 표준 키프레임은 원래대로 익스포트 됩니다.

Supported Controllers vs. Sampling

Max Plug-in은 지원되지 않는 애니메이션 컨트롤러를 가진 오브젝트를 발견하면 애니메이션을 샘플링 합니다. 지원되는 컨트롤러에 있어선, 각 Max 키프레임 마다 Gamebryo 키프레임 하나가 생성됩니다.

샘플링이 일어나면, Gamebryo Max plug-in은 씬 그래프에서 가장 높은 키프레임과 가장 낮은 키프레임을 사용해서 애니메이션을 샘플링 합니다. 플러그인은 Max 컨트롤러가 초당 30 프레임의 속도로 Gamebryo 키프레임에 모두 적용된 후 위치와 회전을 기록할 것입니다. 그러나 이는 Character Studio biped와 같은 경우엔 키프레임을 제대로 샘플링 하기에 충분하지 않을 수 있습니다. 이런 경우엔 샘플링 시간 범위의 처음과 끝에 최상위 레벨의 note track entry를 추가해야 합니다. [animation sequences](mk:@MSITStore:C:\Documents%20and%20Settings\정종필\바탕%20화면\Gamebryo2.2.2_kor027.chm::/Artist_s_Guides/Gamebryo_3ds_max_Plug_in/Tutorials/Simple_Animation_Sequences/Simple_Animation_Sequences.htm)를 사용하면 이 작업이 저절로 이루어집니다
{% endraw %}