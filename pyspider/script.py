#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-08-28 17:42:51
# Project: fzdm

from pyspider.libs.base_handler import *

import time
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    def get_time_str(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+8*3600))

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://manhua.fzdm.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div>li:first-child>a').items():
            doc = {
                "title": each.attr.title,
                "href": each.attr.href,
                "img": each.find("img").attr.src,
                "name": each.attr.title[:-2],
                "datetime": self.get_time_str(),
            }
            print(doc)
            self.crawl(each.attr.href, callback=self.sub_page)

    @config(priority=2)
    def sub_page(self, response):
        for subs in response.doc("li>a").items():
            sub_doc = {
                "title": subs.attr.title,
                "href": subs.attr.href,
                "datetime": self.get_time_str(),
            }
            # print(sub_doc)
            self.crawl(sub_doc["href"],
                       callback=self.detail_page,
                       fetch_type='js',
                       js_script="""console.log("success")""")

    @config(priority=3)
    def detail_page(self, response):
        # print(response.text())
        # response = response.js_script_result()

        mhss_p = r'{mhss='
        mhurl_p = r'var-mhurl1=\"(.*)\";'
        ans = []
        # ans.append(re.match(mhurl_p, s, re.M|re.S)[1])
        # ans.append(re.match(mhss_p, s, re.M|re.S)[1])

        return ans
