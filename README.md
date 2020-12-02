# 教學
[Restful Flask](https://www.youtube.com/watch?v=GMppyAPbLYk&t=3043s&ab_channel=TechWithTim)

[Cloud firestore](https://firebase.google.com/docs/firestore/quickstart?hl=zh-cn#python)

[Pytest](https://myapollo.com.tw/zh-tw/pytest/)

# 注意事項
- 添加套件需在`requirements.txt`內定義
- 安裝套件 : `pip install -r requirements.txt`
- 在test內需要添加此行避免import錯誤`sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))`
- Resource直接繼承`BaseResource`即可使用`self.db`和`self.uid`獲取連線訊息

# Api 說明
## User
* path: /user, method:GET
    *  獲得所有使用者資訊
    * paras:
        * None
* path: /user/{uid}, method:GET 
    * 獲得指定使用者資訊
    * paras:
        * uid: str, 使用者
## Project
- path: /project/{name}, method: 
    - GET 獲得所有project資訊
    * paras:
        * None
- path: /project/{name}, method: GET 
    - 獲得指定project資訊
    * paras:
        * name: str, 專案明稱
- path: /project, method: POST 
    - 刪除指定project資訊
    * paras: 
        * name: str, 專案名稱
        * owner: list, 所屬的擁有者
         
- path: /project, method: DELETE 
    - 刪除指定project資訊
    * paras:
        * name: str, 專案名稱
- path: /project, method: PATCH 
    - 修改指定project資訊(加入新的onwer, repository)
    * paras:
        * name: str,專案名稱
        * repsitories: str, 新增的RP[optional]
        * owner: str, 新增的擁有者[optional]

- path: /project/code_frq, method: POST
    - 獲得指定專案的code frequency
    - paras:
        - name: str, 專案名稱



