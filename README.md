# 风之动漫漫画下载

最近一直在看漫画,每次从浏览器网页上看有点不方便,于是自己做了个小程序把漫画下载过来方便在本地看
功能比较简单,后来又改进了一下,提供了可以保存为数据库的版本

具体流程就是从风之动漫获取漫画相关的信息并下载

## How To Use

* 项目地址:

    https://github.com/leriou/mh/blob/master/mh_down.py

* 依赖

该项目需要用到以下三个Python库,需要先安装

```python

pip install beautifulsoup4  //DOM解析器
pip install requests        //请求库
// pip install peewee          //ORM库(数据库存储版本)


需求版本:Python 3.x

```

## 后续更新计划

1. 多线程下载
2. 增加源站点
