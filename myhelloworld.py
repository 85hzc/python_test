#!/usr/bin/python
import sys
import time
import string
import re
import support
import employee
#from support import print_func
import pymysql
import json

'''
ii=10
print(ii)
print("hello,world!")
print("你好，世界!")
word='1'
word1="2,2,5"
word2='1,2,3'
print (word)
print (word1)
print (word2)

#raw_input("按下 enter 键退出，其他任意键显示...\n")
#print"nihao,shijiebei"

x = 'runOOb.';sys.stdout.write(x+'\n')

dict = {}
dict['one'] = "This is one"
dict[2] = "This is two"

tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}
print('dict len is ',dict.__len__())
print(dict)
print (dict['one'])
print (dict[2])
print('tiny dict len is ',tinydict.__len__())
print (tinydict)
print (tinydict.keys())
print (tinydict.values())

while(ii is 10):
    print('while ok',ii)
    ii -= 1
print ("My name is %s and weight is %d kg!" % ('Zara', 21))

title = str.title(dict[2])
print(title)

list=['a','b',"c",1,2,3]
print(list)
dict = dict.fromkeys(list,88)
print(dict.__len__())
print(dict)

print("当前时间：",time.time())
print("当前时间：",time.localtime())
localtime = time.asctime()
print("当前时间：",localtime)
print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

for x in range(2,10,2):
    print(x*5)

support.print_func("aaa")


line = "Cats are smarter than dogs"
matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
if matchObj:
    print ("matchObj.group() : ", matchObj.group())
    print ("matchObj.group(1) : ", matchObj.group(1))
    print ("matchObj.group(2) : ", matchObj.group(2))
else:
    print ("No match!!")

#myEmpl = Employee
employee.myModule(employee)
'''

'''数据库创建'''
db_host = 'localhost'
db_user = 'root'
db_pw = 'Hzc123#'
db_name = 'testdb'

def cre_db(host, user, pw, name):
    try:
        # 数据库连接
        db = pymysql.connect(host, user, pw, charset='utf8')
        # 创建游标，通过连接与数据通信
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute('show databases')
        rows = cursor.fetchall()
        for row in rows:
            tmp = "%2s" % row
            print("DB[%s]"%tmp)
            # 判断数据库是否存在
            if name == tmp:
                cursor.execute('drop database if exists ' + name)
                cursor.execute('create database if not exists ' + name)

        # 提交到数据库执行
        db.commit()
    except pymysql.Error as e:
        print("pymysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        # 关闭数据库连接
        db.close()

cre_db(db_host, db_user, db_pw, db_name)


'''
数据库操作
'''
# 打开数据库连接
db = pymysql.connect(db_host, db_user, db_pw, db_name, charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print ("Database version : %s " % data)
# 关闭数据库连接
db.close()

dictdata = {}
dictdata['A'] = 'AA'
dictdata['B'] = 'BB'
dictdata['C'] = 'CC'
dictdata['D'] = 'DD'
dictdata['E'] = 1.5
dictdata['F'] = 1
print(dictdata)
server_data = json.dumps(dictdata, sort_keys=True, indent=4, separators=(',',':'))
print('开始发送...\n%s' % server_data)
