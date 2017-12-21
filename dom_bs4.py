#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import os
from bs4 import BeautifulSoup


class Tools:

    def get_html(self, url):
        try:
            times = 3
            while times:
                data = urllib.request.urlopen(url)
                code = data.code
                if code == 200:
                    times = False
                else:
                    times = times - 1
            if code == 200:
                data = data.read().decode("utf-8")
                return data
            else:
                return False
        except:
            return False

    def get_dom_obj(self, url):
        data = self.get_html(url)
        if data:
            return BeautifulSoup(data, 'html.parser')
        else:
            return False

    def open_dir(self, name):
        now = os.path.abspath('.')
        newpath = os.path.join(now, name)
        if os.path.isdir(newpath):
            return newpath
        else:
            os.mkdir(newpath)
            return newpath
