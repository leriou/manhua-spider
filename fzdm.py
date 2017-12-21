#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dom_bs4 as dom
import urllib.request
import time
import os
import default_config


class Fzdm:

    def __init__(self, name=''):
        self.url = "http://manhua.fzdm.com"  # 风之动漫网址
        self.name = name  # 漫画名称
        self.timeout = 2000

        self.tools = dom.Tools()
        if name == '':
            print("请输入名称")

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
        self.cost("开始下载" + self.name)
        self.find_by_name(self.name)
        self.cost("共有张" + str(self.faild_pic) + "图片下载失败")

    def find_by_name(self, name):    # 根据漫画名字获取漫画地址(http://manhua.fzdm.com/39/)
        soup = self.tools.get_dom_obj(self.url)
        title = name + "漫画"
        href = self.url + "/" + soup.find("a", title=title).get('href')
        self.sub_commic_url = href  # 漫画地址
        self.cost("已获取到漫画" + self.name + "的地址:" + href)
        self.get_sub_list()

    def get_sub_list(self):  # 获取子列表页面的每一话地址
        soup = self.tools.get_dom_obj(self.sub_commic_url)
        li_list = soup.find_all("li", "pure-u-1-2 pure-u-lg-1-4")
        for i in li_list:  # i是每一话的名字和地址
            url = self.sub_commic_url + i.a.get("href")
            name = i.a.get("title")
            subs = {"url": url, "name": name}
            self.current_sub = subs
            self.analyse_sub()

    def analyse_sub(self):  # 解析当前这一话的地址
        self.cost("开始解析" + self.name + self.current_sub['name'])
        self.get_sub_pic()

    def get_sub_pic(self):  # 下载图片
        sub = self.current_sub
        n = 1  # 页数
        loop = True
        sub_current_url = sub['url']  # 当前页面的具体地址
        lis = []
        t = time.time()
        while loop:
            page = self.tools.get_dom_obj(sub_current_url)
            if page:
                plist = page.find_all("a", id="mhona")
                for i in plist:
                    loop = (i.string == '下一页')
                    if loop:
                        sub_current_url = sub['url'] + i.get('href')
                        n = n + 1
                img = page.find("img", id="mhpic")
                obj = {}
                obj['pic'] = self.url_filter(img.get('src'))
                obj['name'] = img.get('alt')
                obj['num'] = n
                lis.append(obj)
            else:
                loop = False
        if default_config.app_config['download']:
            obj = {'name': sub['name'], 'list': lis}  # 每一话的对象
            self.down_obj(obj)

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
