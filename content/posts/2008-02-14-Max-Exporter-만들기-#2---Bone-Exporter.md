---
layout: post
title: "Max Exporter 만들기 #2 - Bone Exporter"
date: 2008-02-14 16:14:16
categories: [이글루스 백업, "2008-02"]
---

{% raw %}
===================================================================================  
게임 강좌 - 게임개발 문턱 넘기기  
by 조무영  
===================================================================================  
제 4 편 : Max Exporter #2 - Bone Exporter  
-----------------------------------------------------------------------------------  
Max 가 비싸서 공부용으로는 문제가 있다는 지적이 있었습니다만  
딱히 다른 툴로는 제 능력이 모자라는 관계로...  
어쩔 수 없이 계속 Max 스크립트 강좌로 갈까 합니다.  
  
GMax 라는게 있는데요, 이게 Max 의 무료판 정도 됩니다.  
(델마당 게임제작 게시판에서 Divinespear 님이 정보를 주셨습니다.)  
다운받아보니 Max 와 아주 유사한 제품입니다.  
하지만 기능상에 약간의 제약이 있구요, Animation 을 하는 방법을 아직 모르겠군요.  
맥스 스크립트도 호환이 된다고 합니다만, 100% 호환은 아닌 모양입니다.  
맥스 스크립트 레퍼런스에도 GMax 에 관한 챕터가 별도로 나와있더군요.  
암튼, Max 를 구입하기 곤란하시다면 GMax 로 시작하셔도 좋을 듯 합니다.  
https://www.turbosquid.com/gmax 에서 다운로드 하신 후에 등록(Register)을 하시면  
메일로 등록번호를 보내주더군요.  
  
-----------------------------------------------------------------------------------  
0. 들어가며  
  
1) 몇가지 알아둘 점  
  
① Include  
  
다른 스크립트를 불러 쓸 수 있습니다.  
참으로 반가운 일이죠.  
  
② rollout  
  
입출력 창을 띄울 수 있습니다.  
다행스럽네요.  
  
③ string  
  
맥스에서의 string 은 델파이와는 다릅니다.  
특히, 문자열의 길이를 얻는 방법이 애매합니다.  
"abc" 와 "가나다" 모두 길이가 3 으로 나오죠.  
2byte 문자를 길이 2 로 계산해서 문자열 길이를 얻어오는 방법은 잘 모르겠네요.  
암튼 코드 안에서는 아는것만 가지고 꼼수를 썼습니다.  
  
④ 델파이와의 문법 차이  
  
문자열은 ' ' 가 아니라 " " 로 묶어줘야 합니다.  
같은지 비교할때에는 = 가 아니라 == 입니다.  
다른지 비교할때에는 <> 가 아니라 != 입니다.  
대입은 := 가 아니라 = 입니다.  
begin end 대신 ( ) 를 사용합니다.  
변수 선언문이 필요없기 때문에 오타가 발생하면 바로 새로운 변수로 인식해버립니다.  
주석은 -- 로 시작합니다.  
  
더 있는데 요만큼만 적었어요.  
암튼, 델파이랑 헷갈리면 안돼요...  
  
2) 강좌의 내용  
  
오늘은 본을 뽑아내는 Exporter 를 살펴보겠습니다.  
스크립트 소스를 풀로 올리고 주석을 다는 방식으로 진행하겠습니다.  
설명하는 내용은 // 로 처리하겠습니다. (이건 스크립트 실제 주석처리는 아닙니다)  
  
-----------------------------------------------------------------------------------  
1. DelDX\_Bone\_Export.ms 소스 분석  
  
macroScript BoneExport category: "DelDX"  
(  
--==============================================================상수 (어차피 변수로 처리되지만)  
local DelDXBoneVersion = 0010   
local Dir\_Output = "D:\Work\델마당\세미나 강의\예제\Dat\Bone"  
global StrLen\_Comment = 64  
// 상수를 선언했습니다.  
// Dir\_Output 은 익스포트된 파일의 기본 경로이니 각자의 환경에 맞게 바꾸시면 됩니다.  
// StrLen\_Comment 는 파일에 적어넣을 설명 문자열의 최대 길이입니다.  
  
--==============================================================변수  
global ExportNow = False  
global Comment = ""  
// global 은 어디서나 써먹을 수 있는 변수를 뜻합니다.  
// Local 은 해당 지역에서만 유요한 변수입니다.  
// 위에서는 다소 혼용해서 쓰고 있습니다만 Local 은 () 밖으로는 적용되지 않음을 유의하셔요.  
  
--==============================================================라이브러리 파일을 포함하는 부분  
Include "Lib\_Fnc.ms"  
Include "DelDX\_Fnc.ms"  
// 델파이로 말하면 uses 에 해당하는 부분입니다.  
// 여러 스크립트에서 공동으로 사용할 함수, 상수 등을 별도의 스크립트로 빼놓고 이렇게  
// 불러서 쓰도록 하였습니다.  
// 이렇게 사용되는 스크립트를 앞으로는 라이브러리라고 부르겠습니다.  
  
--==============================================================뭔가 입력받기 위한 창 (이벤트 핸들러도 있다 !!!)  
rollout InputInfoBox "DelDX Bone Exporter" width:291 height:141  
(  
label TitleLable "Bone Exporter v" pos:[11,11] width:272 height:17  
label lbl1 "간단한 설명을 적어보셔요..." pos:[11,36] width:272 height:17  
edittext CommentEdit "" pos:[6,57] width:273 height:20 enabled:true  
button OKBtn "OK" pos:[85,89] width:118 height:24  
on InputInfoBox open do  
(  
TitleLable.Caption = ("DelDX Bone Exporter v"+(DelDXBoneVersion as String))  
)  
on OKBtn pressed do  
(  
Comment = CommentEdit.Text  
DestroyDialog InputInfoBox  
ExportNow = True  
)  
)  
// rollout 은 창을 선언하는 부분입니다.  
// InputInfoBox 라는 창을 "DelDX Bone Exporter" 라는 타이틀로 291\*141 크기로  
// 선언해두는 것이죠.  
// 코드 내에서 불러쓸 창은 이렇게 본격적인 프로그램 부분이 등장하는 앞쪽에 미리 선언해두는게  
// 좋겠습니다.  
// 창에는 이벤트핸들러가 붙을 수 있는데요,  
// 위 코드에서 on 으로 시작되는 부분이 바로 이벤트핸들러입니다.  
// 읽어보기만 해도 무슨 이벤트인지 알겠지요 ?  
// rollout 은 이렇게 코드를 직접 써 넣는 방식으로 만들 수도 있지만  
// 맥스 스크립트 메뉴에서 New 나 Open 을 통해 파일을 열었다면  
// F2 버튼을 눌러서 편집기를 이용할 수도 있습니다.  
  
  
--==============================================================본 목록 얻기 (◀ 요기서부터 실제 프로그램 시작)  
// 여기서부터 본격적인 프로그램 시작이라고 보시면 됩니다.  
  
BoneObjList = GetBoneObjList()  
// 본 목록을 얻습니다.  
// GetBoneObjList 는 DelDX\_Fnc.ms 라이브러리에 넣어둔 함수입니다.  
// 함수 본체는 강좌 후반부에서 다룹니다.  
  
if (BoneObjList != Undefined) and (BoneObjList.Count > 0) then  
(  
// if (본 목록 존재한다) and (본의 수량이 0 보다 크다) then ... 이런 뜻입니다.  
// Undefined 는 델파이의 nil 과 비슷하게 생각하시면 됩니다.  
// 변수를 하나 만들고 아무 값도 넣지 않으면 바로 이 Undefined 상태인 것입니다.  
// 맥스 스크립트의 변수는 특별한 변수형을 갖지 않습니다.  
// 따라서 맨 처음 입력되는 값이 해당 변수의 자료형이 되는 것이죠.  
// 물론 다른 자료형의 값으로 덮어쓸 수도 있구요.  
// 이런 자유로움은 개인적으로는 매우 불편하다는 생각입니다만,  
// 맥스 스크립트가 전문적인 프로그래머를 위한 도구가 아닌 디자이너들을 위한 도구인 점을 생각할때  
// 나름대로 이유있는 선택일 듯도 합니다.  
  
--파일 이름 선택  
local BoneFileName = getSaveFileName caption:"DelDX Bone Export" types: "Bone Files (\*.dbn)|\*.dbn|All Files (\*.\*)|\*.\*|" FileName: (Dir\_Output+"\\*.dbn")  
// 델파이에서 OpenDialog 를 Execute 하는 것과 같은 기능입니다.  
// 성공하면 BoneFileName 이라는 지역변수에 선택된 파일 이름이 들어가게 됩니다.  
// getSaveFileName 함수는 맥스 스크립트 함수입니다.  
// 함수 뒤쪽을 보면 파라미터들이 () 없이 그냥 들어가고 있습니다.  
// 마치 도스 커멘드라인을 사용하는 느낌이지요 ?  
// 이런건 그냥 문법적인 차이일 뿐이니 익혀두시기 바랍니다.  
  
if BoneFileName != Undefined then   
(  
// 파일 이름이 존재하면...  
  
CreateDialog InputInfoBox modal:True  
// 앞서 rollout 쪽에서 만들어뒀던 InputInfoBox 를 호출했습니다.  
  
if ExportNow then  
(  
// InputInfoBox 의 OKBtn pressed 이벤트핸들러가 실행되었을 경우, 즉 OK 버튼이 눌렸을 경우에  
// ExportNow 에 True 값이 들어가도록 되어있었지요 ?  
// 그걸 확인하는 부분입니다.  
  
--파일 열기  
BoneFile = fOpen BoneFileName "wb"  
// 선택된 파일 이름으로 바이너리 현태의 파일을 열었습니다.  
// 이제 이 파일에 정보를 쭈욱 써주고 닫으면 익스포트가 끝나는 것이지요...  
  
if BoneFile != Undefined then  
(   
// 파일이 제대로 열렸으면...  
  
WriteLong BoneFile DelDXBoneVersion --버전  
// 우선 파일의 버전을 써줍니다. (앞서 상수로 선언해뒀던 DelDXBoneVersion 입니다)  
// WriteLong 은 맥스 스크립트 함수입니다.  
// 4바이트 정수형의 값을 함수에 써주는 역할을 하지요.  
  
if Comment == Undefined then Comment = ""  
// 앞서 InputInfoBox 에서 익스포트를 하는 디자이너가 설명글(코멘트)을 파일에다가  
// 적어넣을 수 있게 되어있었는데요, 이때 작성한 문자열이 Comment 에 들어가는거죠.   
// 근데 이 코멘트에 아무것도 넣지 않아서 nil 상태라면  
// 설명글을 빈 문자열로 바꿔줍니다.  
// 뒤쪽에서 설명글을 파일에 저장할때 에러를 방지하려고 적어놓은 코드입니다만,  
// Comment 변수 선언부에서 이미 "" 로 초기화를 해놨으니  
// 쓸데없는 노파심코드가 되겠습니다.  
  
WriteStringByLen BoneFile Comment StrLen\_Comment --이 본에 대한 간단한 설명  
// 코멘트를 적어줍니다.  
// WriteStringByLen 은 문자열 길이 문제에 꼼수를 부려서 만들어놓은 함수입니다.  
// Lib\_Fnc.ms 라이브러리에 넣어뒀습니다.  
  
WriteLong BoneFile BoneObjList.Count --본 수  
// 본 목록에 들어있는 본의 수를 적어줍니다.  
  
for iBone = 1 to BoneObjList.Count do --본 정보를 쭈욱 써주고  
(  
// 이제 본의 개수대로 정보를 써주기 위해서 for 문을 돌립니다.  
// 지난번에 말씀드린 대로 맥스 스크립트의 배열은 모두 1 부터 시작하므로  
// for 문도 1 부터 시작하도록 하였습니다.  
  
ParentBoneIndex = GetBoneObjListIndex BoneObjList[iBone].Parent BoneObjList  
// BoneObjList[iBone] 는 해당 인덱스의 본 자체입니다.  
// BoneObjList[iBone].Parent 는 본의 부모로 링크되어있는 무언가가 되겠습니다.  
// 만약 Parent 가 또 다른 본이라면 BoneObjList 안에 들어있겠지요 ?  
// GetBoneObjListIndex 함수는 Parent 가 본일 경우에 본 목록의 몇번 인덱스인지를  
// 알려주는 함수로, DelDX\_Fnc.ms 에 들어있습니다.  
// 본래는 좀 더 복잡했던 함수라서 별도로 만들어져있었습니다만, 단순화된 지금은  
// GetIndexInList 함수(이것은 Lib\_Fnc.ms 에 들어있죠)로 대체해도 충분할 듯 합니다.  
// 본 목록에 부모가 들어있지 않았다면 -1 을 반환합니다.  
  
TMMat = BoneObjList[iBone].Transform  
// 본의 TransformMatrix 를 TMMat 변수에 넣었습니다.  
  
WriteLong BoneFile ParentBoneIndex --부모본 인덱스  
WriteMatrix3 BoneFile TMMat --변환 행렬  
// 구한 값들을 파일이 써줍니다.  
// WriteMatrix3 는 행렬 자료형의 값을 파일에 써주는 함수로,  
// Lib\_Fnc.ms 라이브러리에 넣어두었습니다.  
)  
  
--마무리  
// 벌써 마무리입니다... 본을 뽑는 과정은 참 간단하지요 ???  
  
if fClose BoneFile then  
(  
MessageBox "DelDX Bone 파일로 Export 되었습니다."  
// 파일을 잘 닫았을 경우에는 뿌듯한 메시지를 출력해줍니다.  
// MessageBox 는 맥스 스크립트 함수입니다.  
)  
else  
(  
MessageBox "파일 닫기 실패"  
// 파일이 안 닫히면 대략 낭패...  
)  
)  
else  
(  
MessageBox "파일 열기 실패"  
// 앞서 fOpen 으로 파일을 열때 실패했을 경우엔 요기에서 메시지를...  
)  
)  
)  
)  
else  
(  
MessageBox "해골을 찾을 수 없네요..."  
// 본 목록이 존재하지 않거나 본의 개수가 0 일 경우에는 요기까지 와서 메시지가 나가지요.  
)  
  
gc()  
// 지금까지 사용하면서 어수선해진 메모리를 정리해줍니다.  
// 이런걸 가비지 콜렉션이라고 합니다만... (gc 가 그 약자인 모양입니다)  
// 메모리를 많이 쓰는 경우에는 이렇게 프로그램 끝뿐 아니라 중간중간에 계속 해줘야 합니다.  
)  
  
// 드디어 스크립트가 끝났습니다.  
  
-----------------------------------------------------------------------------------  
2. 라이브러리 함수 분석  
  
DelDX\_Bone\_Export.ms 에서 불러쓴 외부 라이브러리 함수를 살펴보겠습니다.  
중요한 함수만 살펴볼테니 나머지는 스크립트 소스를 참고하셔요...  
  
1) GetBoneObjList  
  
본 목록을 배열로 리턴하는 함수입니다.  
  
fn GetBoneObjList =  
(  
BoneObjList = #()  
// #() 는 빈 배열을 뜻합니다.  
  
local ObjList = $\*  
// $\* 는 맥스 씬에 있는 모든 것을 말합니다.  
// 본을 가려내기 위해 우선 ObjList 에다가 씬 안에 있는 모든걸 다 넣는거죠.  
  
if ObjList == undefined then Return undefined  
if ObjList.Count <= 0 then Return undefined  
// 아무것도 없이 휑하다면 본도 없을테니 그냥 nil 을 리턴하고 프로그램을 나갑니다.  
// 델파이에선 Result 에 값을 넣어줘도 뒤쪽의 코드를 다 수행하게 되어있습니다만  
// 맥스 스크립트에서는 Resunt 구문 뒤쪽은 수행되지 않습니다.  
  
for iObj in ObjList do  
(  
// for 문을 좀 이상하게 쓰고 있지요 ?  
// ObjList 배열의 모든 구성원들에 대해 for 문을 돌리는 것입니다.  
// iObj 는 1부터 시작하는 정수가 아니라 바로 ObjList 배열의 각 구성원이 되는거죠.  
// 좀 묘한 문법이지만 코드를 단순화하는 효과가 있어서 써봤습니다.  
  
case ClassOf iObj of   
(  
// 반가운 case 문입니다.  
// iObj 의 클래스에 따라 다르게 처리를 하겠다는 내용이지요.  
  
Biped\_object : Append BoneObjList iObj  
// Biped\_object 클래스는 흔히 "바이페드"라고 부릅니다.  
// 맥스에 포함된 "캐릭터 스튜디오" 로 만들어내는 뼈대인데요,  
// 손쉽게 캐릭터 애니메이션을 만들어낼 수 있어서 맥스 디자이너들이 많이 씁니다.  
// Append 는 배열에 구성원을 하나 추가하는 맥스 스크립트 함수입니다.  
// 본이라고 판단하게 되면 본 목록에 해당하는 것을 넣는거죠.  
  
Dummy :   
(  
Append BoneObjList iObj -- 더미도 본으로 쓰는 경우가 있다  
)  
// 더미도 뼈대로 이용하는 경우가 있더군요.  
// 그래서 이것도 본으로 인식하도록 하였습니다.  
// 필요하지 않다면 빼버려도 됩니다.  
  
Default :  
(  
if LowerCase (substring iObj.Name 1 4) == "bone" then   
(  
Append BoneObjList iObj -- 이름이 "bone" 으로 시작되면  
)  
)  
// 앞에서 걸리지 않았다면 Default 문으로 들어오게 됩니다.  
// 바이페드나 더미가 아닌 일반적인 오브젝트들도 뼈대로 사용하는 경우가 있지요.  
// 여기서는 오브젝트의 이름이 "bone" 으로 시작되는 경우를  
// 모두 본으로 처리하도록 하였습니다.  
// 이런 부분은 디자이너와 미리 약속을 해야 합니다.  
// 위에서 LowerCase 는 문자열을 소문자로 모두 바꿔주는 함수로, Lib\_Fnc.ms 에 넣어뒀습니다.  
// substring 은 문자열중에서 일부를 잘라내어 리턴하는 맥스 스크립트 함수입니다.  
// 위의 예에서는 오브젝트 이름중 첫번째부터 네글자가 리턴되지요.  
)  
)  
  
Return BoneObjList  
// 함수가 끝날때에는 이렇게 리턴값을 함수 밖으로 내보내줘야 합니다.  
)   
  
2) WriteMatrix3  
  
행렬을 파일에 써주는 함수입니다.  
  
fn WriteMatrix3 DstFile MatValue =  
(  
// 파라미터로 파일, 행렬값을 받습니다.  
local Mat16 = Matrix3ToFloat16 MatValue  
for i = 1 to 16 do  
(  
WriteFloat DstFile Mat16[i]  
)  
// 맥스의 행렬은 기본적으로 4\*3 구조로 되어있습니다.  
// 그래서 Matrix3ToFloat16 이라는 별도의 함수(Lib\_Fnc.ms 에 있어요...)를 만들어서  
// 16개의 실수형으로 변경한 후에 저장하도록 하였습니다.  
  
Return True  
// 파일에 다 썼으면 참값을 리턴합니다.  
)  
  
-----------------------------------------------------------------------------------  
맥스 스크립트에 대해서는 친절한 자료가 많지 않더군요.  
인터넷을 뒤져보면 김용준님의 문서가 있는데요, 나름대로 설명이 친절하고 내용도 자세합니다.  
대부분 맥스 스크립트 레퍼런스의 예제에 대한 번역 및 추가설명이더군요.  
유용한 자료이니 검색해서 살펴보시면 도움이 많이 될겁니다.  
하지만 이 자료만으로는 완전한 익스포터를 만드는데에는 걸림돌이 많습니다.  
  
추후에 이어지는 강좌에서는 좀 더 복잡한 상황에 대한 내용을 다루게 됩니다.  
스크립트 이용법 뿐 아니라 3D 모델 자체에 대한 이해에 도움이 되는 내용이 될 것입니다.  
  
오늘은 여기까지입니다.  
다음번에는 오브젝트를 뽑아내는 익스포터를 분석해보도록 하겠습니다.  
  
궁금하신 내용이 있으시면 질문리플 달아주셔요...  
  
그럼 좋은 하루 되셔요.  
www.delmadang.com  
===================================================================================
{% endraw %}