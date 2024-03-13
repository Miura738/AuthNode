# AuthNode

## 部署方式

1. 首先安装数据库

去https://www.mongodb.com/try/download/community-kubernetes-operator 下载mongodb

2. 拉取仓库安装并启动

```sh
git clone https://github.com/Miura738/AuthNode.git
cd AuthNode
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 80
```