#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter

top = tkinter.Tk()

# 创建两个列表
me      = ['hzc hello world!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
           'pythonpythonpythonpythonpythonpythonpythonpythonpython',
           'pythonpythonpythonpythonpythonpythonpythonpythonpythonpython',
           'htmlhtmlhtmlhtmlhtmlhtmlhtmlhtmlhtmlhtmlhtmlhtmlhtmlhtml',
           'SQLSQLjavaSQLSQLSQLSQLSQLSQLSQLSQL']
te   = "hzc hello world!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

list   = tkinter.Listbox(top)
text    = tkinter.Label(top, text=te)

#label = Label(root, text=text)
#label.pack()


#for item in me:
#    list.insert(0,item)
#text.insert(0,text)
#list.pack()
text.pack()

# 进入消息循环
top.mainloop()


