#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb

db = MySQLdb.connect("localhost", "root", "lebron", "testdb")

cursor = db.cursor()
# 如果数据表已经存在使用 execute() 方法删除表。
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 创建数据表SQL语句
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""

insert_sql = "INSERT INTO EMPLOYEE(FIRST_NAME,LAST_NAME,AGE,SEX,INCOME)\
                VALUES ('%s','%s','%d','%c','%d')" % \
                ('He', 'Yong', 20, 'M', 50000)

try:
    cursor.execute(insert_sql)
    db.commit()
except:
    db.rollback()


# 关闭数据库连接
db.close()
