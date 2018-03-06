#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dom_bs4 as dom
import urllib.request
import time
import os
import di


class Fzdm:

    def __init__(self, name=''):
        if name == '':
            print("请输入名称")
        self.url = "http://manhua.fzdm.com"  # 风之动漫网址
        self.name = name  # 漫画名称
    
        self.tools = dom.Tools() #工具对象
        self.di = di.Di()
        self.mongodb  = self.di.getMongoDb()
        self.redis    = self.di.getRedis()

        self.co = self.mongodb["fzdm"] # 集合

        # 程序运行时间统计
        self.start = time.time()
        self.end = 0
        self.record = []
        self.faild_pic = 0

    def cost(self, log=''):
        tmp = time.time()
        total, last = tmp - self.start, tmp - self.end
        self.end = tmp
        print("%s 总消耗时间:%s s,距上次%s s" % (log, total, last))

    def run(self):    # 主程序
        url = self.find_from_list(self.name)
        sub_list = self.get_sub_list(url)
        self.analyse_sub(sub_list)
        self.tools.close_browser()
        self.cost("下载完成")

    def find_from_list(self,name):    # 获取漫画列表地址(http://manhua.fzdm.com/)
        self.cost("开始下载漫画 %s" % self.name)
        # 检查列表中是否有该漫画的地址
        rec = self.co["mh_list"].find_one({"name":self.name})
        if rec["url"] != None:
            return rec["url"]
        else:   
            html = self.tools.browser_get_html(self.url)
            page = {
                "url":self.url,
                "name":"风之动漫列表",
                "cached":True,
                "text":html,
                "status":1,
                "date_time":self.tools.get_time()
            }
            self.co["cached_url"].insert(page)
            soup = self.tools.get_dom_by_html(html)
            for block in soup.select(".round"):
                mh_info = {
                    "name": block.select("li")[1].string,
                    "url":self.url + "/" + block.select("li a")[1].get("href"),
                    "date_time":self.tools.get_time()
                } 
                self.co["mh_list"].insert(mh_info)
            self.cost("风之动漫列表解析完毕")

    def get_sub_list(self,url):  # 获取子列表页面的每一话地址
        soup = self.tools.get_dom_obj(url,True)
        li_list = soup.find_all("li", "pure-u-1-2 pure-u-lg-1-4")
        sublist = []
        for i in li_list:  # i是每一话的名字和地址
            sub_info = {
                "url": url + i.a.get("href"), 
                "sub_name": i.a.get("title"),
                "created": self.tools.get_time(),
                "commic_name":self.name
            }
            sublist.append(sub_info)
            self.co["mh_sub_list"].save(sub_info)
        return sublist

    def analyse_sub(self,sub_list):  # 解析当前这一话的地址
        
        for sub in sub_list:
            self.cost("开始解析" + self.name + sub['sub_name'])
            n = 1  # 页数
            loop = True
            current_url = sub['url']  # 当前页面的具体地址
            lis = []
            t = time.time()
            while loop:
                page = self.tools.get_dom_obj(current_url,True)
                if page:
                    plist = page.find_all("a", id="mhona")
                    for i in plist:
                        loop = (i.string == '下一页') # 是否最后一页
                        if loop:
                            current_url = sub['url'] + i.get('href')
                            n = n + 1
                    img = page.find("img", id="mhpic")
                    obj = {
                        "src":self.url_filter(img.get('src')),
                        "pic_name":img.get('alt'),
                        "pic_num":n,
                        "commic_name":self.name,
                        "sub_name":sub["sub_name"],
                        "cteated":self.tools.get_time()
                    }
                    self.co["mh_pic_list"].save(obj)
                    lis.append(obj)
                else:
                    loop = False
        
        
    def url_filter(self, pic):
        if pic.find('http:') == -1:
            url = 'http:' + pic
        else:
            url = pic
        return url

    def down_obj(self, obj):  # 下载
        if default_config.app_config['root']:
            root_dic = default_config.app_config['root'] + self.name
        else:
            root_dic = self.name
        r_path = self.tools.open_dir(root_dic)  # 作品目录
        s_path = os.path.join(r_path, obj['name'])
        if not os.path.isdir(s_path):
            os.mkdir(s_path)
        for j in obj['list']:
            filename = s_path + "/" + j['name'] + "_" + str(j['num']) + ".jpg"
            if not os.path.exists(filename):
                try:
                    pic = j['pic']
                    test_code = urllib.request.urlopen(pic, timeout=self.timeout).code
                    if test_code == 200:
                        urllib.request.urlretrieve(pic, filename)
                    else:
                        print("code:%d \n", test_code)
                except:
                    self.faild_pic = self.faild_pic + 1
                    print("pic: %s request is timeout" % j['pic'])
