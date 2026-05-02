---
layout: post
title: "Plan을 4면으로 나누고 Detach 하는 맥스 스크립트"
date: 2007-05-17 11:48:43
categories: [이글루스 백업, "2007-05"]
---

{% raw %}
![](/assets/images/posts/20070517_114843_c0055803_11053246.jpg)  
  
인터페이스를 만들어서 할 만큼 거창한 작업도 아니고... 해서  
간단하게 만들어서 실행.   
  
a = $            --$(현재 선택된 오브젝트) 를 a 라는 변수에 넣는다.

--subobjectLevel = 1                 
--a.EditablePoly.SetSelection #Vertex #{1..4}  
--a.EditablePoly.tessellate #Vertex

-- 3줄은 주석처리. 무식한 방법이다. 리스너에서 그냥 따온 방법  
-- 우선 sub-object level을 1로 만든다. 1이면 단축키와 동일하게 vertex다.   
-- 변수 a 가 ($로 해도 된다) 에디터블 폴리 상태라는 전제가 필요하다. 폴리에서 버텍스를 1~4까지 선택한다. 역시 그냥 따온거.   
-- a 를 vertex tessellate 한다. 그럼 4면이 되겠지? 이후에 각각 면을 선택해서 떼는 작업을 하면 된다.  
  
polyOp.tessellateByFace a #{1}

polyOp.detachFaces a #{1} asNode:true   
polyOp.detachFaces a #{1} asNode:true   
polyOp.detachFaces a #{1} asNode:true   
polyOp.detachFaces a #{1} asNode:true  
delete a  
  
-- polyOp 는 폴리 오퍼레이션을 위한 메소드를 지닌, 라이브러리 안의 클래스라 할 수 있다. 좀 더 고급 조작이 가능.   
-- 참고로 라이브러리 >클래스>함수 이다. ㅎㅎㅎ  
-- 여기서 첫 줄이 앞의 3줄을 모두 커버하고 있다. (게다가 더 옵션도 많이 줄 수 있다. 옵션과 예제는 헬프에서 찾을 수 있다)  
-- 첫 줄에서 polyOp 명령의 tessellate 에서 a의 페이스 1번을 가지고 작업한다. 뭐 어차피 1면밖에 없는 놈이니까.   
-- 두 번째 줄에서 detach 명령을 실행한다. 역시 a의 1번 페이스. asNode 는 아마도 원본을 남겨 둘 것이냐에 대한 옵션으로 보인다.  
-- 나머지 세줄도 동일하게 작동한다. 어차피 하나 떼어내면 페이스 번호가 재정렬하니까. 1번을 계속 떼어내면 된다.   
-- 생각해보니 저 네 줄도 for 문으로 반복 처리하면 한줄로 처리 가능 OTL   
-- 마지막이 중요하다. 네 면을 전부 떼어내도, 원본은 남아있는걸로 인식된다. 즉 허공 오브젝트 (Node) 만 남아 있는 셈.   
-- 네 면을 다 떼어냈으니 a를 삭제하도록 하자. 이것 역시 리스너에서 컨닝 ㅋㅋ  
-- 이대로 Evaluate를 하면 선택한 plan (에디터블 메쉬 상태여야 한다. 음... 이것도 넣을걸 그랬나) 이 4개의 면으로 나눠진다.   
  
  
그래서 내친김에 for 문을 사용. 중괄호가 아니고 그냥 괄호라는걸 주의하자 OTL 이것땜네 syntax error ㅡ,.ㅡ   
최종 결과물   
  
a = $  
polyOP.tessellateByFace a #{1}  
for t = 1 to 4 do   
(   
polyOp.detachFaces a #{1} asNode:true   
)  
delete a  
  
미친 척 줄여쓰면 4줄로도 완성 ㅡ,.ㅡ   
   
**a = $  
polyOP.tessellateByFace a #{1}  
for t = 1 to 4 do ( polyOp.detachFaces a #{1} asNode:true )  
delete a**
{% endraw %}