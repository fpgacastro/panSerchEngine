#!/usr/bin/env python3
# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
import tkinter.ttk as ttk
import sqlite3

class MForm(tk.Frame):
    '''继承自Frame类，master为Tk类顶级窗体（带标题栏、最大、最小、关闭按钮）'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initComponent(master)
    def initComponent(self,master):
        '''初始化GUI组件'''
        #设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        master.rowconfigure(0,weight=1);master.columnconfigure(0,weight=1)
        self.ft=tkFont.Font(family='微软雅黑',size=12,weight='bold')#创建字体  
        #设置继承类MWindow的grid布局位置，并向四个方向拉伸以填充顶级窗体
        self.grid(row=0,column=0,sticky=tk.NSEW)
        #设置继承类MWindow的行列权重，保证内建子组件会拉伸填充
        self.rowconfigure(0,weight=1);self.columnconfigure(0,weight=1)
       
        self.panewin=ttk.Panedwindow(self,orient=tk.VERTICAL)#添加水平方向的推拉窗组件
        self.panewin.grid(row=0,column=0,sticky=tk.NSEW)#向四个方向拉伸填满MWindow帧
       
        self.frm_high=ttk.Frame(self.panewin,relief=tk.SUNKEN,padding=0)#左侧Frame帧用于放置播放列表
        self.frm_high.grid(row=0,column=0,sticky=tk.NSEW);#左侧Frame帧拉伸填充
        self.frm_high.columnconfigure(0,weight=5);#右侧Frame帧两行一列，配置列的权重
        self.frm_high.columnconfigure(1,weight=1);#右侧Frame帧两行一列，配置列的权重
        self.frm_high.rowconfigure(0,weight=1);  #右侧Frame帧两行的权重8:1
        self.panewin.add(self.frm_high,weight=1)  #将左侧Frame帧添加到推拉窗控件，左侧权重1

        #右侧Frame帧第一行添加视频区Frame
        self.Entry_serch=ttk.Entry(self.frm_high)
        self.Entry_serch.grid(row=0,column=0,sticky=tk.NSEW)
        # self.Entry_serch.bind("<Return>",self.quary_baiduyun_filelist)
        #右侧Frame帧第一行第二列
        self.Button_serch=ttk.Button(self.frm_high,text='搜索', command= self.quary_baiduyun_filelist)
        self.Button_serch.grid(row=0,column=1,sticky=tk.NSEW)
       
        self.frm_low=ttk.Frame(self.panewin,relief=tk.SUNKEN,padding=1)#右侧Frame帧用于放置视频区域和控制按钮
        self.frm_low.grid(row=0,column=0,sticky=tk.NSEW)#右侧Frame帧四个方向拉伸
        self.frm_low.columnconfigure(0,weight=1);#右侧Frame帧两行一列，配置列的权重
        self.frm_low.rowconfigure(0,weight=1);  #右侧Frame帧两行的权重8:1
        self.panewin.add(self.frm_low,weight=50)    #将右侧Frame帧添加到推拉窗控件,右侧权重10
       
        #右侧Frame帧第二行添加搜索结果
        self.tree = ttk.Treeview(self.frm_low, selectmode='browse',show='tree')
        self.tree.grid(row=0,column=0,sticky=tk.NSEW)

    def quary_baiduyun_filelist(self):
        # self.tree.insert("", 0, None,open=True,text=type(self.Entry_serch.get()))
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        file_dict = {}
        db=['./direction_baidu1.db','./direction_baidu2.db']
        for db_index in db:
            conn = sqlite3.connect(db_index)
            cursor = conn.cursor()
            command = "select * from cache_file where server_filename like ?"
            cursor.execute(command,("%"+self.Entry_serch.get()+"%",))
            while True:
                value = cursor.fetchone()
                if not value:
                    break
                tr_root=self.tree.insert("", 0, None,open=True,text=value[3])#树视图添加根节点
                self.tree.insert(tr_root, 0, None,open=True,text=value[2])#根节点下添加一级节点
if(__name__=='__main__'):
    root = tk.Tk()
    root.geometry('800x480+200+100')
    root.title('Media Player')
    #root.option_add("*Font", "宋体")
    root.minsize(800, 480)
    app = MForm(root)
    root.mainloop()