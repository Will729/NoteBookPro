import pymysql
import traceback  # 错误跟踪模块
import sys

class MysqlUtil(object):
    def __init__(self):
        '''
        初始化方法，连接MySQL数据库
        '''
        host = '127.0.0.1'
        user='root'
        password='zuohuiziji'
        database='notebook'
        self.db = pymysql.connect(host=host,user=user,password=password,db=database)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor) #设置游标，并将游标设置为字典类型

    # 将错误日志输入到目录文件中
    def log2file(self):
        f = open('\log.txt','a')
        traceback.print_exc(file=f)
        f.flush() # 强行写入
        f.close()


    def insert(self, sql):
        '''
        插入数据库操作
        :param sql:  插入数据库的sql语句
        :return:
        '''
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.log2file()
            #如果发生异常，回滚
            self.db.rollback()
        finally:
            # 最终关闭数据库连接
            self.db.close()

    def fetchone(self,sql):
        '''
        查询单条数据
        :param sql:
        :return:
        '''
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:
            self.log2file()
            self.db.rollback()
        finally:
            self.db.close()

    def update(self, sql):
        '''
            更新结果集
        '''
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.log2file()
            self.db.rollback()
        finally:
            self.db.close()

