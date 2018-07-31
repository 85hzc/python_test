#!/usr/bin/evn python

import socketserver
import json
import struct
import binascii
import dbfunction
from bottle import default_app, get, run
from beaker.middleware import SessionMiddleware

'''
tcp server code
'''
class echorequestserver(socketserver.BaseRequestHandler):
    def handle(self):
        print('服务端启动...')
        conn = self.request
        print('获得连接：', self.client_address)
        while True:
            print('recv>>>>>>>>>>>>>>>>>>')
            client_data = conn.recv(1024)
            if not client_data:
                print('断开连接')
                break
            print(client_data)

            dbfunction.parse_recv(client_data)
            dbfunction.sendToClient(self)

class M1SocketServer(socketserver.StreamRequestHandler):
    def handle(self):
        print('run')
        print(self.client_address)
        data = self.rfile.readline()
        self.wfile.write('%s %s'%(time.ctime()), data)
        print(data)

        while True:
            pass

# 设置session参数
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600,
    'session.data_dir': '/tmp/sessions/simple',
    'session.auto': True
}

@get('/index/')
def callback(arg):
    print(arg)
    return 'Hello World! index/'

@get('/index')
def callback():
    return 'Hello World index!'


# 函数主入口
if __name__ == '__main__':
    #server = socketserver.TCPServer(("172.17.88.221", 9000),echorequestserver)
    #server.serve_forever()
    print("run")

#    dbfunction.db_init(dbfunction.db_host, dbfunction.db_user, dbfunction.db_pw, dbfunction.db_name)
    # 创建数据表SQL语句
    sql = """CREATE TABLE M1_DEVICES (
             DeviceId  varchar(16),
             MAC  varchar(16),
             Status  int,
             Pm25  int,
             Hcho  int,
             Temperature  int,
             Humidity  int)"""
    #dbfunction.db_create_table(sql, dbfunction.db_host, dbfunction.db_user, dbfunction.db_pw,dbfunction.db_name, "M1_DEVICES")


    server1 = socketserver.ThreadingTCPServer(("172.17.88.221",9000), echorequestserver)
    server1.serve_forever()

    app_argv = SessionMiddleware(default_app(), session_opts)
    run(app=app_argv, host='localhost', port=9090, debug=True, reloader=True)





