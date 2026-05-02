---
title: "shader option changer 백업"
date: 2012-07-05T12:46:15Z
draft: false
---

비공개.  
[TsShaderOptionChanger.cs](http://pds25.egloos.com/pds/201207/05/03//TsShaderOptionChanger.cs)  
  
[TsShaderOptionChangerByFolder.cs](http://pds24.egloos.com/pds/201207/05/03//TsShaderOptionChangerByFolder.cs)  
  
  
if( !System.IO.Path.HasExtension(obj.name) ) // 시스템에서 받은 오브젝트의 확장자 이름이 없으면. (그럼 폴더니까)   
    {  
     string fullPath = System.IO.Path.GetFullPath(Application.dataPath);    
  // 전체 경로를 받아둡니다. Asset 까지만 나옵니다.  D:\AT2\_WEB\Assets  
     string projectPath = fullPath.Remove(fullPath.IndexOf("Assets"));    
// 프로젝트 경로 : 위에서 Assets 를 지웁니다. D:\AT2\_WEB\  
     string selectedPath = System.IO.Path.GetFullPath(AssetDatabase.GetAssetPath(obj));   
// 선택한 오브젝트의 전체 경로를 받습니다. D:\AT2\_WEB\Assets\Scripts\AutoTextureApply\Editor\TsShaderOptionChangerByFolder.cs  
     string folderPath = System.IO.Path.Combine(projectPath, selectedPath);  
// 두 경로를 합칩니다. D:\AT2\_WEB\Assets\Scripts\AutoTextureApply\Editor\TsShaderOptionChangerByFolder.cs