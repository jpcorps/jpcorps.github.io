---
title: "Max Exporter 만들기 #3 - Animation Exporter"
date: 2008-02-14T16:15:05Z
draft: false
---

===================================================================================  
게임 강좌 - 게임개발 문턱 넘기기  
by 조무영  
===================================================================================  
제 4 편 : Max Exporter #3 - Animation Exporter  
-----------------------------------------------------------------------------------  
지난번에는 본을 익스포트 해보았습니다.  
이번에는 그 본의 애니메이션을 익스포트 하겠습니다.  
기본적인 골격은 같으니 그리 어렵지 않을 듯 합니다.  
  
-----------------------------------------------------------------------------------  
0. 들어가며  
  
1) 몇가지 알아둘 점  
  
별로 없어요... -.-;  
  
2) 강좌의 내용  
  
본 애니메이션을 뽑아내는 Exporter 를 살펴보겠습니다.  
지난번과 마찬가지로 스크립트 소스를 풀로 올리고 주석을 다는 방식으로 진행하겠습니다.  
설명하는 내용은 // 로 처리하겠습니다. (이건 스크립트 실제 주석처리는 아닙니다)  
  
  
-----------------------------------------------------------------------------------  
1. DelDX\_Anim\_Export.ms 소스 분석  
  
macroScript AnimationExport category: "DelDX"  
(  
--==============================================================상수 (어차피 변수로 처리되지만)  
local DelDXAnimVersion = 0010  
local Dir\_Output = "D:\Work\델마당\세미나 강의\예제\Dat\Anim"  
global StrLen\_Comment = 64  
// 위의 상수 선언부는 지난시간 강좌내용과 비슷합니다.  
  
--==============================================================변수  
global ExportNow = False  
global Comment = ""  
global SamplingGap  
global TickToMS  
// 변수 선언부도 비슷...  
  
--==============================================================라이브러리 파일을 포함하는 부분  
Include "Lib\_Fnc.ms"  
Include "DelDX\_Fnc.ms"  
// 라이브러리 불러오는 부분도 비슷...  
// 근데 이번에는 딱히 라이브러리 함수를 쓰지 않았다는 생각이 문득 드는군요... -.-;  
  
--==============================================================뭔가 입력받기 위한 창 (이벤트 핸들러도 있다 !!!)  
// 여기서부터 롤아웃입니다.  
// 역시 지난번 시간에 다루었던 내용인데요, 이번에는 샘플링 간격도 입력받습니다.  
// Default 값은 1 인데요, 이렇게 하면 샘플링을 촘촘하게 하기 때문에 정확도가 높아지는 대신 파일 용량이 늘어납니다.  
rollout InputInfoBox "DelDX Animation Exporter" width:291 height:240  
(  
label TitleLable "DelDX Animation Exporter v" pos:[16,10] width:264 height:17  
label lbl10 "간단한 설명을 적어보셔요..." pos:[17,46] width:272 height:17  
edittext CommentEdit "" pos:[12,67] width:261 height:20 enabled:true  
label lbl9 "프레임의 샘플링 간격을 정해주셔요..." pos:[13,117] width:263 height:19  
spinner SamplingGapSpin "" pos:[14,143] width:259 height:16 enabled:true range:[0,1000,1] type:#integer scale:1   
button OKBtn "OK" pos:[84,179] width:118 height:24  
on InputInfoBox open do  
(  
TitleLable.Caption = ("DelDX Animation Exporter v"+(DelDXAnimVersion as String))  
)  
on OKBtn pressed do  
(  
Comment = CommentEdit.Text  
SamplingGap = SamplingGapSpin.Range.z -- Value 프로퍼티가 없다고 우기니 원...   
DestroyDialog InputInfoBox  
ExportNow = True  
)  
)  
  
////////////////////////////////////////////////////////////////////////////////// 여기서부터 본격적인 프로그램 시작입니다.  
// 지난시간에 다루었던 중복되는 내용은 따로 설명하지 않고 넘어가겠습니다.  
// 혹시 제가 헷갈려서 새로운 내용인데 빼먹었거나... 그런 경우에는 리플 달아주셔요...  
//////////////////////////////////////////////////////////////////////////////////  
  
BoneObjList = GetBoneObjList()  
// 본 목록을 구합니다.  
// 요기서 익스포트할 애니메이션이라는게 결국 본 애니메이션인데요...  
// 예를 들어, 0.1 초 단위로 애니메이션을 하면서 본의 현재상태를 계속 저장한다면...  
// 게임 엔진에서 그걸 시간 단위로 적용해나가면 일종의 애니메이션이 재현되는 셈이겠지요 ?  
// 그런 방식입니다...  
  
if (BoneObjList != Undefined) and (BoneObjList.Count > 0) then -- 본이 없으면 애니도 엄따 !!!  
(  
--파일 이름 선택  
local AnimFileName = getSaveFileName caption:"DelDX Anim Export" types: "Anim Files (\*.dan)|\*.dan|All Files (\*.\*)|\*.\*|" filename: (Dir\_Output+"\\*.dan")  
if AnimFileName != Undefined then  
(  
CreateDialog InputInfoBox Modal:True  
if ExportNow then  
(  
--Max 시간을 ms 단위로 환산하기 위한 상수를 구하고...  
TickToMS = ticksPerFrame \* 1000 / 4800  
// 맥스에서의 프레임당 Tick 이라는 것이 우리가 프로그래밍에서 흔히 쓰는 1/1000초 (=ms) 와는  
// 다른 단위입니다.  
// 그래서 시간을 저장할때 환산하기 위해서 이렇게 변수를 하나 만들어서 값을 넣어두었습니다.  
  
--파일 열기  
AnimFile = fOpen AnimFileName "wb"  
  
if AnimFile != Undefined then  
(  
--FileHeader  
WriteLong AnimFile DelDXAnimVersion  
if Comment == Undefined then Comment = ""  
WriteStringByLen AnimFile Comment StrLen\_Comment --이 애니메이션에 대한 간단한 설명  
WriteLong AnimFile BoneObjList.Count  
WriteFloat AnimFile (AnimationRange.Start \* TickToMS)  
WriteFloat AnimFile (AnimationRange.End \* TickToMS)  
// 애니메이션 파일의 헤더를 쓰는 부분입니다.  
// 디자이너의 코멘트 뒤로 본의 갯수와 애니메이션 시작/끝 시각을 ms 단위로 넣어주고 있지요.  
  
undo off  
// 여기서부터 일어나는 일에 대해서는 언두 버퍼에 저장하지 않겠다는 뜻입니다.  
// 속도증가와 사용메모리 감소 효과가 있다고 스크립트 레퍼런스에 나오는데 체감효과는 없더군요.  
  
--Make Clone  
local CloneObjList = #()  
// 쌍동이 오브젝트 목록입니다.  
// 본 오브젝트의 쌍동이들을 만들어서 여기다가 넣을겁니다.  
// 본이 오브젝트가 아닌 다른 것으로 만들어지는 경우에도 Transform 행렬 등을 사용해야 하므로  
// 이렇게 쌍동이 "오브젝트" 로 만들어 쓰면 편리합니다.  
  
for iObj in BoneObjList do  
(  
// 본 오브젝트 목록의 모든 오브젝트에 대해 다음 과정을 통해 쌍동이를 만들어줍니다.  
CloneObj = Snapshot iObj Name:(iObj.Name as String + "\_Clone")  
CloneObj.Parent = Undefined  
CloneObj.Transform = iObj.Transform  
CloneObj.Position.Track = Bezier\_Position()  
CloneObj.Rotation.Track = Tcb\_Rotation()  
CloneObj.Scale.Track = Tcb\_Scale()  
Append CloneObjList CloneObj  
// 요렇게 만들어진 쌍동이 오브젝트를 오브젝트 목록(CloneObj) 에 추가(Append)합니다.  
)  
  
for i=1 to BoneObjList.Count do  
(  
if BoneObjList[i].Parent != Undefined then  
(  
CloneObjList[i].Parent = BoneObjList[i]  
)  
)  
// 부모본을 갖는 본의 쌍동이는 원본 본에 링크시켜줘야 합니다.  
// 안그러면 애니메이션을 할때 쌍동이가 제대로 움직이지 않게 되어버리지요.  
  
--Make animation keys  
animate on  
// 애니메이션을 활성화합니다.  
// 이걸 해줘야 뒤쪽에서 as Time 구문으로 현재시각을 바꿔주는 루틴에서 씬 전체가 반응을 하게 됩니다.  
  
for iObj = 1 to CloneObjList.Count do -- 각 본 별로  
(  
// 쌍동이들 각각에 대해 다음과 같은 정보를 끄집어내어 파일에 써줘야 합니다.  
local RData  
local RKeyList = #()  
local RKeyCount = 0  
local TData  
local TKeyList = #()  
local TKeyCount = 0  
local SData  
local SKeyList = #()  
local SKeyCount = 0  
// 회전(R), 이동(T), 확대축소(S) 정보를 배열로 저장할 것입니다.  
// 각각의 배열 길이는 카운터 변수를 두구요.  
  
local Loop = True --시간을 잘게 쪼개서 애니 데이타 배열을 만든다  
local CurrTime = AnimationRange.Start  
// 현재 시각 변수(CurrTime)를 애니메이션 시작 시각에 맞춰놓습니다.  
  
while Loop do at Time CurrTime  
(  
// Loop 변수가 True 인 동안은 While 문을 계속 돌게 됩니다.  
// at Time CurrTime 이라는 구문은 맥스 스크립트의 특징적인 문법이 적용된건데요,  
// 씬 전체가 CurrTime 이라는 시각의 애니메이션 상태가 됩니다.  
// 마치 맥스의 애니메이션 프레임바를 스크롤하는 셈이죠.  
// 이렇게 시각을 세팅한 후에 현재의 본 상태값을 읽어오면 애니메이션 정보를 얻는게 되죠.  
  
// 우선 회전값을 알아냅니다.  
--Rotate--------------------------------------------  
RData = TTimeAndValue Time: CurrTime Value: CloneObjList[iObj].Rotation  
// RData 에 현재 시각의 iObj 번째 본의 회전값을 저장합니다.  
// 이때 본이 아니라 그 본의 쌍동이 오브젝트로부터 회전값을 얻어옵니다.  
  
// 이제 값을 배열에 추가합니다.  
// 참고로, 맥스의 배열은 모두 가변배열입니다.  
// 편리하지만 느리고 무겁죠.  
if RKeyCount <= 1 then  
(  
Append RKeyList RData  
RKeyCount = RKeyCount + 1  
)  
else  
(  
if (RKeyList[RKeyCount-1].Value == RData.Value) and (RKeyList[RKeyCount].Value == RData.Value) then  
(  
-- 아끼자  
RKeyList[RKeyCount-1].Time = RData.Time  
)  
else  
(  
Append RKeyList RData  
RKeyCount = RKeyCount + 1  
)  
)  
// 배열에 값을 넣는 내용이 좀 복잡하게 되어있지요 ?  
// 동일한 값이 계속 들어가는 경우에 중간값들을 생략하도록 만들어서 그렇습니다.  
// 예를 들어, 애니메이션 시작후 1초간 회전값이 0 도라면...  
// 0초때와 1초때의 회전값만 저장하면 충분하겠지요.  
// 그런데 프레임마다의 값을 모두 저장한다면 메모리 낭비이고, 애니메이션 속도에도 지장을 주겠죠.  
// 위의 코드에서는 그런 경우에 중간값들을 저장하지 않도록 하고 있습니다.  
  
// 이동, 확대축소 값도 회전값을 얻는 과정과 동일합니다.  
--Trans--------------------------------------------  
TData = TTimeAndValue Time: CurrTime Value: CloneObjList[iObj].Position  
if TKeyCount <= 1 then  
(  
Append TKeyList TData  
TKeyCount = TKeyCount + 1  
)  
else  
(  
if (TKeyList[TKeyCount-1].Value == TData.Value) and (TKeyList[TKeyCount].Value == TData.Value) then  
(  
-- 아끼자  
TKeyList[TKeyCount-1].Time = TData.Time  
)  
else  
(  
Append TKeyList TData  
TKeyCount = TKeyCount + 1  
)  
)   
--Scale--------------------------------------------  
SData = TTimeAndValue Time: CurrTime Value: CloneObjList[iObj].Scale  
if SKeyCount <= 1 then  
(  
Append SKeyList SData  
SKeyCount = SKeyCount + 1  
)  
else  
(  
if (SKeyList[SKeyCount-1].Value == SData.Value) and (SKeyList[SKeyCount].Value == SData.Value) then  
(  
-- 아끼자  
SKeyList[SKeyCount-1].Time = SData.Time  
)  
else  
(  
Append SKeyList SData  
SKeyCount = SKeyCount + 1  
)  
)   
  
--마무리--------------------------------------------  
if CurrTime < AnimationRange.End then  
(  
// 애니메이션이 아직 계속되고 있다면  
  
// 현재 시각을 샘플링 간격만큼 증가시킵니다.  
CurrTime = CurrTime + SamplingGap  
  
// 애니메이션 끝 시각 이후로 벗어나지 않도록 보정을 해주고요...  
if CurrTime > AnimationRange.End then CurrTime = AnimationRange.End  
)  
else  
(  
// 애니메이션이 끝났다면...  
  
// While 루프를 빠져나오도록 변수를 조작해주고요...  
Loop = False  
  
-- 하나라도 아끼자  
if (RKeyCount>1) and (RKeyList[RKeyCount-1].Value == RKeyList[RKeyCount].Value) then  
(  
DeleteItem RKeyList RKeyCount  
RKeyCount = RKeyCount - 1  
)  
if (TKeyCount>1) and (TKeyList[TKeyCount-1].Value == TKeyList[TKeyCount].Value) then  
(  
DeleteItem TKeyList TKeyCount  
TKeyCount = TKeyCount - 1  
)  
if (SKeyCount>1) and (SKeyList[SKeyCount-1].Value == SKeyList[SKeyCount].Value) then  
(  
DeleteItem SKeyList SKeyCount  
SKeyCount = SKeyCount - 1  
)  
// 앞에서 같은 값이 반복되는 경우에 대한 처리를 했는데  
// 맨 마지막 값에 대해서는 처리되지 않는 문제가 있습니다.  
// 그래서 마지막 하나라도 아끼려고 요런 코드가 들어갔습니다.  
)  
)   
  
// 이제 파일로 저장하는 부분입니다.  
-- 만들어진 배열을 파일로 저장하고...  
  
// 먼저 회전값 배열을 저장합니다.  
WriteLong AnimFile RKeyCount  
for iFrame = 1 to RKeyCount do  
(  
WriteLong AnimFile (RKeyList[iFrame].Time \* TickToMS)  
// 시각을 저장할때 TickToMS 값을 곱해서 ms 단위로 환산하고 있지요...  
  
WriteFloat AnimFile RKeyList[iFrame].Value.x  
WriteFloat AnimFile RKeyList[iFrame].Value.z -- y ↔ z  
WriteFloat AnimFile RKeyList[iFrame].Value.y --  
// y 와 z 값이 바뀌어야 한다는 이야기는 지난시간에도 했지요 ?  
  
WriteFloat AnimFile (-RKeyList[iFrame].Value.w)  
// 웬 w 값일까요 ???  
// 맥스에서의 회전값은 X, Y, Z 축에 대한 회전각으로 표시(오일러각 방식)되는게 아니라  
// 쿼터니온으로 표시가 됩니다.  
// 회전에 대한 표현방법중 하나라고 생각하시면 됩니다.  
// 회전만 이렇게 표현하구요, 이동과 확대축소는 일반적인 벡터를 사용합니다.  
// 쿼터니온에 대한 설명은 생략할터이니 관심있는 분께서는 인터넷이나 책을 참고해보셔요...  
// 그래도 잘 모르시겠다면 리플 달아주시구요...  
)  
// 맥스의 좌표계가 DX 와 다르기 때문입니다.  
  
// 회전, 확대축소 값의 배열도 같은 방법으로 저장하구요...  
WriteLong AnimFile TKeyCount  
for iFrame = 1 to TKeyCount do  
(  
WriteLong AnimFile (TKeyList[iFrame].Time \* TickToMS)  
WriteFloat AnimFile TKeyList[iFrame].Value.x  
WriteFloat AnimFile TKeyList[iFrame].Value.z -- y ↔ z  
WriteFloat AnimFile TKeyList[iFrame].Value.y --  
)   
WriteLong AnimFile SKeyCount  
for iFrame = 1 to SKeyCount do  
(  
WriteLong AnimFile (SKeyList[iFrame].Time \* TickToMS)  
WriteFloat AnimFile SKeyList[iFrame].Value.x  
WriteFloat AnimFile SKeyList[iFrame].Value.z -- y ↔ z  
WriteFloat AnimFile SKeyList[iFrame].Value.y --  
)   
)  
  
--마무리  
animate off  
// 앞서 animate on 했던걸 끕니다.  
  
undo on  
// undo off 했던걸 원래 상태로 돌리구요...  
  
--Delete Clone  
for iObj in CloneObjList do Delete iObj  
// 쌍동이 오브젝트들을 모두 없애줍니다.  
  
// 나머지는 지난번 내용과 비슷하군요...  
if fClose AnimFile then  
(  
MessageBox "DAN 파일로 Export 되었습니다."  
)  
else  
(  
MessageBox "파일 닫기 실패"  
)  
)  
else  
(  
MessageBox "파일 열기 실패"  
)  
)  
)  
)  
else  
(  
MessageBox "본을 찾지 못했습니다."  
)  
  
gc()   
)  
  
-----------------------------------------------------------------------------------  
맥스 스크립트가 어려운 이유는 문법이 어렵거나 로직이 어려워서가 아니라  
명령어, 함수 등등을 찾아내기가 어려워서입니다.  
이미 만들어진 것을 분석하는 내용은 그리 어렵지 않습니다.  
  
오늘은 여기까지입니다.  
다음 시간에는 모델 익스포터를 다루어보겠습니다.  
이번 강좌 내용보다 한층 복잡해질 것이고,  
3D 모델링에 대한 기초적인 지식이 없으면 난해한 부분도 있을텐데요,  
모든걸 완전히 이해하는 것 보다는 흐름을 이해하는 것이 중요하다는 점 잊지 마시기 바랍니다.  
  
궁금하신 내용이 있으시면 질문리플 달아주셔요...  
  
그럼 좋은 하루 되셔요.  
www.delmadang.com  
===================================================================================