#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 默认配置项
app_config = {
    "mode": 1,
    "download": True,
    "root": False,
    "db": {
        "mysql": {
            "host": "127.0.0.1",
            "port": 3306,
            "username": "root",
            "password": "",
            "db": "testdb"
        },
        "mongodb": {
            "host": "127.0.0.1",
            "port": 27017
        }
    },
    "cache": {
        "redis": {
            "host": "127.0.0.1",
            "port": 6379
        }
    }
}
