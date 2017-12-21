# 风之动漫漫画下载

最近一直在看漫画,每次从浏览器网页上看有点不方便,于是自己做了个小程序把漫画下载过来方便在本地看

功能比较简单,后来又改进了一下,提供了可以保存为数据库的版本

具体流程就是从风之动漫获取漫画相关的信息进行解析并下载

## Proccess

    大致使用深度优先(DFS)来进行下载

    proccess: 解析漫画地址->每一话的地址->每一页的图片地址->下载

## Usage

* mongodb

提供了mongodb存储数据的选项

* 使用pipenv进行依赖管理,安装pipenv

    pip install pipenv

* 依赖

    pipenv install 

* 运行

    pipenv run python2 main.py



## 该项目需要用到以下三个Python库,需要先安装

```python

pip install beautifulsoup4  // DOM解析器
pip install requests        // 网络请求库
pip install pymongo

需求版本:Python 3.x

```

## 后续更新计划

1. 多线程下载
2. 增加源站点
3. 多种存储方式
