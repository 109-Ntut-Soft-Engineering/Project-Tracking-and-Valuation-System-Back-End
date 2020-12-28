# 教學
[Restful Flask](https://www.youtube.com/watch?v=GMppyAPbLYk&t=3043s&ab_channel=TechWithTim)

[Cloud firestore](https://firebase.google.com/docs/firestore/quickstart?hl=zh-cn#python)

[Pytest](https://myapollo.com.tw/zh-tw/pytest/)

# 注意事項
- 添加套件需在`requirements.txt`內定義
- 安裝套件 : `pip install -r requirements.txt`
- 在test內需要添加此行避免import錯誤`sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))`
- 測試指令 :  
1.    `pytest --cov=./src --cov-report xml:cov.xml -s`  
2.    `pytest --cov=./src`
- 測試套件 : Coverage Gutters, 可使用watch功能看到哪些已測試過
- Resource直接繼承`BaseResource`即可使用`self.db`和`self.uid`獲取連線訊息

# Api 說明
## User Resource
* path: /user, method: GET
    * 依照當前連線的uid獲得使用者資訊
    * paras:
        * None
* path: /user, method: POST
    * 新增user
    * paras:
        * name: str, user名稱
        * email: str, 註冊的email
        
## Projects Resource
* path: /project, method: GET
    * 依照當前連線的uid獲得所有project的pid
    * paras:
        * None
* path: /project, method: POST
    * 新增project
    * paras:
        * name: str, project名稱
        
## Project Setting Resource
* path: /project/{pid}/setting, method: GET
    * 取得pid相符的project的name, owner, collaborator資訊
    * paras:
        * pid: str, project的id
* path: /project/{pid}/setting, method: DELETE
    * 刪除與pid相符的project
    * paras:
        * pid: str, project的id
* path: /project/{pid}/setting, method: PATCH
    * 修改與pid相符的project的collaborator
    * paras:
        * pid: str, project的id
        * collaborator: list, 欲替代的collaborator
        
## Project Repos Resource
* path: /project/{pid}/repos, method: GET
    * 取得與pid相符的project的repositories
    * paras:
        * pid: str, project的id
* path: /project/{pid}/repos, method: PATCH
    * 修改與pid相符的project的repositories
    * paras:
        * pid: str, project的id
        * collaborator: list, project的collaborator
        * repositories: list, project的repositories
        * name: str, project的名稱
        
## Project Commit Resource
* path: /project/{pid}/commit, method: GET
    * 取得與pid相符的project的commit資訊
    * paras:
        * pid: str, project的id
      
## Project Code Frequency Resource
* path: /project/{pid}/code_freq, method: GET
    * 取得與pid相符的project的code frequency資訊
    * paras:
        * pid: str, project的id
