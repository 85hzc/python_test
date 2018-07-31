
import json
import binascii
import pymysql


'''数据库创建'''
db_host = 'localhost'
db_user = 'root'
db_pw = 'Hzc123#'
db_name = 'testdb'

def db_init(host, user, pw, name):
    print('Init DB')
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

def db_create_table(sql, host, user, pw, name, table):

    try:
        # 打开数据库连接
        db = pymysql.connect(host, user, pw, name, charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 如果数据表已经存在使用 execute() 方法删除表。
        cursor.execute("DROP TABLE IF EXISTS %s" % table)
        cursor.execute(sql)
    except pymysql.Error as e:
        print("pymysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        print('create table m1_devices finally')

    # 关闭数据库连接
    db.close()


'''
数据库操作
'''
def db_insert_table(sql, host, user, pw, name, mac):

    # 打开数据库连接
    db = pymysql.connect(host, user, pw, name, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sqll = "SELECT * FROM M1_DEVICES WHERE MAC=\'%s\'" % mac
    print(sqll)
    try:
        cursor.execute(sqll)
        results = cursor.fetchall()
        for row in results:
            print("aaaaaa %d" % row[0])
            cursor.execute("DELETE FROM EMPLOYEE WHERE MAC=\'%s\'" % mac)
            db.commit()
    except:
        print("Error: unable to fecth data")

    try:
        cursor.execute(sql)
        db.commit()
    except :
        # Rollback in case there is any error
        db.rollback()

    db.close()

def db_update_table(sql, host, user, pw, name, mac):

    # 打开数据库连接
    db = pymysql.connect(host, user, pw, name, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        db.commit()
    except :
        # Rollback in case there is any error
        db.rollback()

    db.close()

def create_device(deviceid, mac):
    print('create_device')

    sql = "INSERT INTO M1_DEVICES (DeviceId, MAC, Status, Pm25, Hcho, Temperature, Humidity) \
            VALUES ('%s', '%s', '%d', '%d', '%d', '%d', '%d')" % (deviceid, mac, 1, 0, 0, 0, 0)
    db_insert_table(sql, db_host, db_user, db_pw, db_name, mac)

def update_device_info(pm25, hcho, temp, humi, mac):
    print('update device info')

    sql = "UPDATE M1_DEVICES SET Pm25 = %s Hcho = %s Temperature = %s Humidity = %s WHERE MAC = %s" % (pm25, hcho, temp, humi, mac)
    db_update_table(sql, db_host, db_user, db_pw, db_name, mac)


def parse_recv(rx_buff):
    print('parse_buff>>>>>>')

    MAC       = str(binascii.b2a_hex(rx_buff))[36:48]
    messType  = str(binascii.b2a_hex(rx_buff))[56:58]
    print(messType)
    messJsonBytes = rx_buff[28:-6]
    #print(messJsonBytes)
    messJson = str(messJsonBytes, encoding="utf-8")
    #print(messJson)

    if messType == '01':
        #on line event
        print('create device! mac:%s' % MAC)
        create_device(deviceid=0, mac=MAC)

    elif messType == '04':
        #inform event
        print('update info!')
        jsonObj = json.loads(messJson)
        update_device_info(jsonObj['value'], jsonObj['hcho'], jsonObj['humidity'], jsonObj['temperature'], MAC)

    print('parse_buff<<<<<<<<<<<<')

def sendToClient(self):
    dictdata = {}
    dictdata['type'] = 5
    dictdata['sleep'] = 1
    dictdata['startTime'] = 1000
    dictdata['endTime'] = 2000
    dictdata['status'] = 1
    json_data = json.dumps(dictdata, sort_keys=False, indent=1, separators=(',', ':'))
    # json_data = json.dumps(dictdata)
    # server_list1 = struct.pack('B', 'AA'), '%s%X%X%X%X%X%X%s' % ('aaaabbbbccccdddd', 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xFF, 'eeffgg')
    # server_list1 = '%x%s%X%X%X%X%X%X%s' % (int('0xAA', 16),'aaaabbbbccccdddd', 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xFF, 'eeffgg')
    server_list2 = bytes(
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x03\x00\x03\x00\x03\x00\x00\x01\x03\x00\x03\x00\x00\x01\x03\x03\x03').decode(
        'ascii')
    # server_list2 = bytes(b'\x31\x32\x61\x62').decode('ascii')
    # server_data=''
    # server_data[0] = 0xAA
    # hex(0xAA)[2:]
    # server_data =  chr(int('AA', 16)) + server_list2 + json_data+'#END#'
    server_data = server_list2 + json_data + '#END#'
    # print('json:\n%s' % json_data)
    print('开始发送...\n%s' % server_data)
    conn = self.request
    conn.sendall(server_data.encode())
    # conn.sendall(server_data)






