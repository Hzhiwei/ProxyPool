# coding: utf-8

"""
数据库类
"""

__authot__ = 'Hzhiwei'

import pymysql

class mysqlClient(object):
    def __init__(self):
        self.db_conn = None
        pass

    def connect(self, username, password, databaseName):
        try:
            self.db_conn = pymysql.connect('localhost', username, password, databaseName, charset='utf8')
            return True
        except Exception as e:
            print(e)
            return False

    def disconnect(self):
        try:
            self.db_conn.close()
        except:
            pass

    def isConnect(self):
        return self.db_conn.open

    def ping(self):
        return self.ping()

    def add(self, ip, port, ptype):
        sql = 'INSERT INTO available (ip,port,type,time) VALUES (%s,%s,%s,NOW())'
        c = self.db_conn.cursor()
        try:
            c.execute(sql, (ip, port, ptype))
            self.db_conn.commit()
        finally:
            c.close()


