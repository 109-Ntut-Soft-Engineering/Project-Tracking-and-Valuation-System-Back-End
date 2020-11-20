# 教學
[Restful Flask](https://www.youtube.com/watch?v=GMppyAPbLYk&t=3043s&ab_channel=TechWithTim)

[Cloud firestore](https://firebase.google.com/docs/firestore/quickstart?hl=zh-cn#python)

[Pytest](https://myapollo.com.tw/zh-tw/pytest/)

# 注意事項
- 添加套件需在`requirements.txt`內定義
- 安裝套件 : `pip install -r requirements.txt`
- 在test內需要添加此行避免import錯誤`sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))`