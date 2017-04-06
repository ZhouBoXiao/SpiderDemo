# -*- coding:utf-8 -*-


import MySQLdb
import time

dbconfig = {'host': '112.74.59.117',
                'port': 3306,
                'user': 'root',
                'passwd': '123456',
                'db': 'test',
                'charset': 'utf8'}

class MySQLHelper(object):

    error_code = ''  # MySQL错误号码

    _instance = None  # 本类的实例
    _conn = None  # 数据库conn
    _cur = None  # 游标

    _TIMEOUT = 30  # 默认超时30秒
    _timecount = 0

    def __init__(self):
        # '构造器：根据数据库连接参数，创建MySQL连接'
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                                         port=dbconfig['port'],
                                         user=dbconfig['user'],
                                         passwd=dbconfig['passwd'],
                                         db=dbconfig['db'],
                                         charset=dbconfig['charset'])
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg

            # 如果没有超过预设超时时间，则再次尝试连接，
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(dbconfig)
            else:
                raise Exception(error_msg)

        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self, sql):

        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            result = self._cur.fetchall()  # 
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def update(self, sql):

        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def insert(self, sql):

        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print self.error_code
            return False

    def fetchAllRows(self):

        return self._cur.fetchall()

    def fetchOneRow(self):
        return self._cur.fetchone()

    def getRowCount(self):
        return self._cur.rowcount

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def __del__(self):
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def close(self):
        self.__del__()






