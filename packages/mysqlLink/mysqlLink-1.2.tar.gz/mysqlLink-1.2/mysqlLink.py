# -*- coding:utf-8 -*-
# Made by Azrael
# Author Email: 1341449544@qq.com

import pymysql
import sys

def mysql_connect(Host, Port, User, Passwd, Db, Charset):# Make a link object
    new_connect = pymysql.Connect\
        (
            host=Host,
            port=Port,
            user=User,
            passwd=Passwd,
            db=Db,
            charset=Charset
        )
    return new_connect

def execute_sql(connect, sql):# Execute sql after making a link object
    cursor = connect.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        connect.rollback()
        print('Fail!', e)
    else:
        connect.commit()
        print('Success!', cursor.rowcount)
    finally:
        cursor.close()
        connect.close()

if __name__ == '__main__':
    print("please input:localhost port user password db_name charset!")
    cur = sys.stdin.readline()
    localhost, port, user, passwd, db, charset = cur.split()
    port = int(port)
    newConnect = mysql_connect(localhost, port, user, passwd, db, charset)
    print("please input sql!")
    sql = sys.stdin.readline()
    execute_sql(newConnect, sql)
