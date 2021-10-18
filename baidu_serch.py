__title__ = ''
__author__ = 'jungle'
__mtime__ = '2019-01-18'

#!/usr/bin/env python3

# -*- coding:utf-8 -*-

import win32con
import win32clipboard as cp

from tkinter import *

from tkinter.filedialog import askopenfilename

from tkinter.filedialog import asksaveasfilename

from tkinter.ttk import *

import sqlite3


def select_db_file():
    db_file = askopenfilename(title="请选择BaiduYunCacheFileV0.db文件", filetypes=[('db', '*.db')])

    db.set(db_file)


def select_save_file():
    save_file = asksaveasfilename(filetypes=[('文件', '*.txt')])

    f.set(save_file + ".txt")


def write_file(file_dict, f, item, gap=""):
    if item == "/":

        f.write("━" + "/" + "\n")

        for i in file_dict["/"]:

            f.write("┣" + "━" + i + "\n")

            i = item + i + "/"

            if i in file_dict:
                write_file(file_dict, f, i, gap="┣━")

    else:

        gap = "┃  " + gap

        for i in file_dict[item]:

            f.write(gap + i + "\n")

            i = item + i + "/"

            if i in file_dict:
                write_file(file_dict, f, i, gap)


def quary_baiduyun_filelist():
    file_dict = {}

    conn = sqlite3.connect(db)

    cursor = conn.cursor()

    cursor.execute("select * from cache_file")

    while True:

        value = cursor.fetchone()

        if not value:
            break

        path = value[2]

        name = value[3]

        size = value[4]

        isdir = value[6]

        if path not in file_dict:

            file_dict[path] = []

            file_dict[path].append(name)

        else:

            file_dict[path].append(name)

    for item in file_dict:
        list_filePath.insert(0,item)

# def copy_path(event):
#     cp.OpenClipboard() 
#     cp.EmptyClipboard() 
#     cp.SetClipboardData(win32con.CF_UNICODETEXT,''.join(list_filePath.curselection()))  
#     cp.CloseClipboard()

root = Tk()
root.title('百度云文件搜索引擎')

db_select = Button(root, text=' 搜索 ', command=quary_baiduyun_filelist)

db_select.grid(row=1, column=2, sticky=W, padx=(2, 0), pady=(2, 0))

db='./direction_baidu.db'

db_path = Entry(root, width=80, textvariable=db)

db_path.grid(row=1, column=1, padx=3, pady=3, sticky=W + E)
li     = ['C','python','php','html','SQL','java']

file_dict = {}

list_filePath=Listbox(root, width=80,xscrollcommand=1,yscrollcommand=1)

# list_filePath.bind('<1>',copy_path)
list_filePath.grid(row=2, column=1, sticky=W, padx=(2, 0), pady=(2, 0))

root.columnconfigure(2, weight=1)

root.mainloop()