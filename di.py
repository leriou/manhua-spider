
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import redis
import pymysql as mysql

# 依赖注入
class Di:

    def __init__(self):
        Di.redis = None
        Di.mongodb = None

    # redis client
    def getRedis(self):
        if Di.redis == None:
            Di.redis = redis.Redis('127.0.0.1',6379) 
        return Di.redis

    # mongodb client 
    def getMongoDb(self):
        if Di.mongodb == None:
            Di.mongodb =  MongoClient('127.0.0.1',27017)
        return Di.mongodb

    def getMysql(self):
        if Di.mysql == None:
            Di.mysql = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='password')
        return Di.mysql.cursor()





