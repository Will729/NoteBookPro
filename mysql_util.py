from datetime import datetime

import pymysql
import traceback  # 错误跟踪模块

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
        f = open('log.txt','a')
        # f.write(datetime.now())
        f.write(str(datetime.now())+'\n')
        traceback.print_exc(file=f)
        traceback.print_exc()
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
        return result

    def fetchall(self,sql):
        '''
        查询数据库：多个结果集
        fetchall():接受全部的返回结果
        :return:
        '''
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            self.log2file()
            self.db.rollback()
        finally:
            self.db.close()
        return result

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

    def delete(self,sql):
        '''
        删除结果集
        :param sql:
        :return:
        '''
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.log2file()
            self.db.rollback()
        finally:
            self.db.close()
