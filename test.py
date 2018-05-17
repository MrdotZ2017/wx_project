import itchat
import psycopg2

#微信登陆
itchat.auto_login(hotReload=True)
# itchat.send('Hello,filehelper',toUserName='filehelper')

# postgresql数据库连接
conn = psycopg2.connect(dbname="mydb",user="dbuser",password="123qwe",host="172.27.199.132",port="5432")
print("Opened database successfuly!")

cur = conn.cursor()
friends = itchat.get_friends(update=True)
owner = friends[0]['NickName']
for friend in friends:
    del friend['MemberList']
    friend['Owner'] = owner
    cols = ','.join(friend.keys())
    qmarks = ','.join(list(['%s'] * len(friend)))
    datas = tuple(friend.values())
    sql = 'insert into wx_friend_list(Owner,{}) values{};'.format(cols,datas)
    print(sql)
    break
    # cur.execute(sql)
    # conn.commit()
# cur.execute('select NickName,Sex from wx_friend_list limit 2;')
# vals = cur.fetchall()
# data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
# print('Now The Table wx_friend_list have %d rows.' %(data[0]['count']))
# print(data['sex'])
conn.close
