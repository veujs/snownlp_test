import pymysql


HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'hehehehe'
DATABASE = 'jd_goods'
PORT = 3306
"""定义表结构"""
"""
|  id       |  goods          |  comments      |  eval  |  created_at  | 
|   int     |  varchar(100)   |   varchar(100) |  bool  |  datetime    |
"""


"create database jd_data;"
sqlCreateTable = "CREATE TABLE IF NOT EXISTS %s " \
                 "(%s INT NOT NULL AUTO_INCREMENT, " \
                 "%s VARCHAR(100) NOT NULL, " \
                 "%s TEXT , %s BOOL NOT NULL , " \
                 "%s DATETIME DEFAULT CURRENT_TIMESTAMP ," \
                 "%s DATETIME DEFAULT CURRENT_TIMESTAMP ," \
                 "PRIMARY KEY (id)" \
                 ") default CHARSET=utf8" \
                 %("jd_comments", "id", "good", "content", "eval", "created_at", "update_at")



class mysqlDatabaseHandler(object):

    def __init__(self, host, username, password, database, port):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port)
        self.cursor = self.db.cursor()
        self.table = None

    @property
    def cursor_d(self):
        return self.db.cursor()

    def insert_one(self, item={}):
        """
        插入一条数据
        :param sql: sql命令
        :return: False 插入错误， True 插入成功
        """
        if item:
            sql = "insert into jd_comments " \
                  "(good, content, eval, created_at) " \
                  "values ('%s', '%s', %s, '%s') " \
                  %(item['good'], item['content'], item['eval'], item['created_at'])
            print(sql)
            try:
                self.cursor.execute(sql)
            except:
                pass
                self.db.rollback()
                return False
            finally:
                self.db.commit()
                # self.cursor.close()
                return True

    def create_tab(self, sql):
        """
        创建表
        :param sql:
        """
        import re
        result = re.findall('.* IF NOT EXISTS (.*?) ', sql, re.S)[0]
        self.cursor.execute(sql)
        if result:
            self.table = result
        else:
            print("创建表错误！")

    def update(self, sql):
        try:
            self.cursor.execute(sql)
        except:
            pass
            self.db.rollback()
        finally:
            self.db.commit()
            # self.cursor.close()

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
        except:
            self.db.rollback()
        finally:
            self.db.commit()
            self.cursor.close()


jd_sql = mysqlDatabaseHandler(HOST, USERNAME, PASSWORD, DATABASE, PORT)
if __name__ == '__main__':
    pass
    import time

    c_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(c_time)

    item = {
        'goods': 'uawei p30',
        'comment': '垃圾吗',
        'eval': 0,
        'created_at': c_time
    }
    # print(sqlCreateTable)
    # jd_sql.create_tab(sqlCreateTable)
    # jd_sql.insert_one(item)
    # jd_sql.cursor.execute("insert into jd_comments (id, goods, comment, eval, created_at) values (19,'uawei p30', '垃圾1', 0, '2019-09-07 11:20:40') ")
    # jd_sql.cursor.execute("insert into jd_comments (good, content, eval) values ('uawei p29', '垃圾2', 1)")
    # jd_sql.db.commit()




