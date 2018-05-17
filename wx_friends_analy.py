#-*-coding:utf-8-*-
import itchat
import psycopg2
import logging

error_log = 'error'
# 定义日志输出格式
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=error_log,
                    filemode='a')


# 函数writeDb:写入数据库
def writeDb(sql):
    """
    连接Postgresql数据库（写），并进行写的操作，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，
    如果所有执行正常，则返回true
    """
    # 数据库连接
    try:
        # conn = psycopg2.connect(dbname="mydb", user="dbuser", password="123qwe", host="172.27.199.132", port="5432")
        conn = psycopg2.connect(dbname="mydb", user="dbuser", password="1234@qwer",
                                host="rm-2zeg8s69g42akn9659o.pg.rds.aliyuncs.com", port="3432")
        cur = conn.cursor()
        # print('连接成功writeDb')
    except Exception as e:
        print(e)
        logging.error('writeDb:数据库连接失败:%s' % e)
        # print('连接失败writeDb')
        return False

    try:
        cur.execute(sql)
        # print(sql)
        conn.commit()  # 提交事务
    except Exception as e:
        conn.rollback()  # 出错则事务回滚
        logging.error('writeDb:数据写入失败:%s' % e)
        # print('执行失败writeDb')
        return False
    finally:
        cur.close()
        conn.close()
    return True


# 函数readDb:从数据库读取数据
def readDb(sql):
    """
    连接Postgresql数据库（查），并进行数据查询，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，
    如果所有执行正常，则返回查询到的数据，这个数据是经过转换的，转成字典格式，方便模板调用，其中字典的key是数据表里的字段名.
    """
    try:
        # conn = psycopg2.connect(dbname="mydb", user="dbuser", password="123qwe", host="172.27.199.132", port="5432")
        conn = psycopg2.connect(dbname="mydb", user="dbuser", password="1234@qwer",
                                host="rm-2zeg8s69g42akn9659o.pg.rds.aliyuncs.com", port="3432")
        cur = conn.cursor()
        # print('连接成功readDb')
    except Exception as e:
        print(e)
        logging.error('readDb:数据库连接失败:%s' % e)
        # print('连接失败readDb')
        return False
    try:
        cur.execute(sql)
        data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in
                cur.fetchall()]  # 将数据转换成字典格式
        # print(data)
    except Exception as e:
        logging.error('readDb:数据执行失败:%s' % e)
        # print('执行失败readDb')
        return False
    finally:
        cur.close()
        conn.close()
    return data


def main():
    # 微信登陆
    itchat.auto_login(hotReload=True)
    # 获取微信好友信息
    friends = itchat.get_friends(update=True)
    # 判断数据库是否存有数据，有则清空数据表
    sql1 = 'SELECT COUNT(1) FROM wx_friend_list LIMIT 1;'
    row_count = readDb(sql1)
    # print(row_count[0]['count'])
    # sql_test = 'INSERT INTO wx_friend_list (Sex) values(1);'
    # print(sql_test)
    # writeDb(sql_test)
    if row_count[0]['count'] != 0:
        truncate_sql = 'TRUNCATE TABLE wx_friend_list;'
        writeDb(truncate_sql)
        if True:
            print('********************清空表成功.********************')

    print('********************开始写入数据库*****************')
    # 拼接insert Sql语句
    i = 0
    for friend in friends:
        del friend['MemberList']
        cols = ','.join(friend.keys())
        # qmarks = ','.join(['%s']*len(friend))
        values = tuple(friend.values())
        sql = 'INSERT INTO wx_friend_list({}) VALUES {};'.format(cols, values)
        # print(sql)
        writeDb(sql)  # 写入数据库
        if True:
            i += 1
            print('已写入{}条数据'.format(i))
        if friend == friends[-1]:
            print('********************数据写入完成********************')


if __name__ == '__main__':
    main()
