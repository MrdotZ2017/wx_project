import psycopg2

db = {
    'dbname' : 'mydb',
    'user' : 'dbuser',
    'password' : '1234@qwer',
    'host' : 'rm-2zeg8s69g42akn9659o.pg.rds.aliyuncs.com',
    'port' : '3432'
}
# db = (dbname="mydb", user="dbuser", password="1234@qwer", host="rm-2zeg8s69g42akn9659o.pg.rds.aliyuncs.com", port="3432")
conn = psycopg2.connect(dbname="mydb", user="dbuser", password="1234@qwer", host="rm-2zeg8s69g42akn9659o.pg.rds.aliyuncs.com", port="3432")
cur = conn.cursor()
print('连接成功.')