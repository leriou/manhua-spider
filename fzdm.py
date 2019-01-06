#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tools
import time
import sys
import os

class Fzdm:

    def __init__(self):
        self.tools = tools.Tools() #工具对象
        self.mongodb = self.tools.get_mongodb()
        self.dbname = "mh"
        self.cache_name = "mh-cache"
        self.list_name = "mh-list"
        self.subs_name = "mh-subs"
        self.pics_name = "mh-pics"
        self.list_url = "http://manhua.fzdm.com"  # 风之动漫网址

        self.db = self.mongodb[self.dbname]
        self.list_collection = self.db[self.list_name]
        self.pics_collection = self.db[self.pics_name]
        self.subs_collection = self.db[self.subs_name]
        self.tools.set_cache(self.dbname, self.cache_name)

        # 程序运行时间统计
        self.start = time.time()
        self.end = 0

    def cost(self, log=''):
        self.tools.cost(log)

    def run(self):    # 主程序
        self.get_manhua_list()
        self.get_sub_list()
        self.analyse_sub()
        self.tools.close_browser()
        self.cost("下载完成")

    '''
    获取漫画列表
    '''
    def get_manhua_list(self):
        soup = self.tools.get_dom_obj(self.list_url)
        for block in soup.select(".round"):
            mh_id = block.select("li a")[1].get("href").strip("/")
            mh_name = block.select("li")[1].string
            mh_url = self.list_url + "/" + mh_id +"/"
            img = block.select("li a img")[0].get("src")
            title = block.select("li a")[1].get("title")
            mh_info = {
                "_id":mh_id,
                "name": mh_name,
                "commic_url":mh_url,
                "img":img,
                "title":title,
                "datetime":self.tools.get_time()
            } 
            self.list_collection.replace_one({"_id":mh_id}, mh_info, True)
        self.tools.cost("总漫画列表下载完毕 ^_^")

    """
    更新所有漫画章节信息
    """
    def get_sub_list(self):  # 获取漫画子列表页面的每一话地址
        condition = {}
        if len(sys.argv) == 2:
            condition["name"] = sys.argv[1]
        for i in self.list_collection.find(condition):
            url = i["commic_url"]
            soup = self.tools.get_dom_obj(url)
            li_list = soup.find_all("li", "pure-u-1-2 pure-u-lg-1-4")
            self.cost("正在下载:%s的漫画列表" %  i["name"]) 
            for j in li_list:  # j是每一话的名字和地址
                sub_id = j.a.get("href").strip("/")
                doc_id = i["_id"] +"_"+str(sub_id)
                sub_info = {
                    "_id": doc_id,
                    "sub_url": url + sub_id + "/", 
                    "sub_name": j.a.get("title"),
                    "datetime": self.tools.get_time(),
                    "commic_name": i["name"],
                    "download": False
                }
                self.subs_collection.replace_one({"_id":doc_id}, sub_info, True )
            self.cost("%s的漫画列表下载结束" % i["name"])
            self.list_collection.update_one({"_id":i["_id"]}, {"$set":{
                "subs_num": self.subs_collection.count_documents({"commic_name":i["name"]}),
                "latest_subs": self.subs_collection.find_one({"commic_name":i["name"]})
            }}, True)

    """
    获取漫画每一话的信息
    """
    def analyse_sub(self):  
        condition = {"download": False}
        if len(sys.argv) == 2:
            condition["commic_name"] = sys.argv[1]
        for s in self.subs_collection.find(condition):
            self.cost("开始解析%s ---%s " % (s["commic_name"], s['sub_name']))
            page_n = 0  # 页数
            loop = True
            current_url = s['sub_url']  # 当前页面的具体地址
            while loop:
                self.cost("第"+ str(page_n + 1) + "页")
                page = self.tools.get_dom_obj(current_url, True)
                pic_url = current_url
                if page:
                    plist = page.select(".navigation a")
                    for i in plist:
                        loop = (i.string == '下一页') # 是否有下一页
                        if loop:
                            current_url = s['sub_url'] + i.get('href')
                            page_n += 1
                    img = page.find("img", id="mhpic")
                    pic_id = s["_id"] +"_"+ str(page_n)
                    obj = {
                        "_id": pic_id, 
                        "pic_url": pic_url,
                        "pic_src": self.url_filter(img.get('src')),
                        "pic_name": s["sub_name"] + "第"+ str(page_n) + "话",
                        "pic_num": page_n,
                        "commic_name": s["commic_name"],
                        "sub_name": s["sub_name"],
                        "datetime": self.tools.get_time()
                    }
                    self.pics_collection.replace_one({"_id":pic_id}, obj, True)
                else:
                    loop = False
            self.subs_collection.update({"_id":s["_id"]}, 
                {"$set":{
                    "picnum": self.pics_collection.count_documents({"sub_name":s["sub_name"]}),
                    "download":True
                    }}, True)

            
    def url_filter(self, pic):
        url = pic
        if pic.find('http:') == -1:
            url = 'http:' + pic
        return url

