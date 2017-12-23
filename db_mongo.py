#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Db:

    def getConn(self,conf):
        self.host = conf['host'] 
        self.port = conf['port']
        self.username = conf['username']

    def getClient(self)
        if Db.Client:
            return Db.Client
        else:
            return False
        
    # 插入数据
    def insert(self,data):
        pass
    # 更新数据
    def update(self,data):
        pass

    def delete(self,data):
        self.update()