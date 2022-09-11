#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- auteur chen_zhao_shi -*-
import jieba
import time
from tkinter import *
from tkinter import filedialog
import os

LOG_LINE_NUM = 0


def get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


# 界面化
class MY_GUI:
    def __init__(self, init_window_name):
        self.str_trans_to_md5_button = None
        self.log_data_Text = None
        self.result_data_Text = None
        self.log_label = None
        self.result_data_label = None
        self.init_data_label = None
        self.init_data_Text = None
        self.init_window_name = init_window_name

    def callback(self):
        default_dir = r"文件路径"
        fileName = filedialog.askopenfilename(defaultextension=".*",
                                              initialdir=(os.path.expanduser(default_dir)))
        my_txt_file = fileName
        if os.path.exists(my_txt_file):
            a = open(my_txt_file, 'r', encoding='utf-8')
            self.init_data_Text.delete(1.0, END)
            for id_names in a:
                self.init_data_Text.insert('insert', id_names)
            a.close()

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("欢迎使用三位一体汉语词法分析字标记系统")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"
        # #窗口背景色，其他背景色见
        # 虚化，值越小虚化程度越高 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=1, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=1, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=2, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=68, height=47)  # 处理结果展示
        self.result_data_Text.grid(row=2, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="分词标记", bg="lightblue", width=10,
                                              command=self.out_put_data)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=2, column=11)
        path = StringVar()
        path.set(os.path.abspath("."))

        # 文档路径选择
        Label(self.init_window_name, text="目标路径:").grid(row=0, column=0)
        Entry(self.init_window_name, textvariable=path, state="readonly").grid(row=0, column=1, ipadx=90)
        Button(self.init_window_name, text="选择文件", command=self.callback).grid(row=0, column=2)  # 调用选择文件路径函数

    # 功能函数
    def out_put_data(self):

        def seg_sentence(sentence):
            sentence_seged = jieba.cut(sentence.strip())
            stopwords = {" ", "，", "。", "“", "”", '“', "？", "！", "：", "《",
                         "》", "、", "；", "·", "‘ ", "’", "──", ",", ".", "?",
                         "!", "`", "~", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                         "-", "_", "+", "=", "[", "]", "{", "}",
                         '"', "'", "<", ">", "\\", "|" "\r", "\n", "\t"}  # 这里加载停用词
            out_str = ""
            for word in sentence_seged:
                if word not in stopwords:
                    if word != '\t':
                        out_str += word
                        out_str += " "
            return out_str

        src = self.init_data_Text.get(1.0, END)  # 读取文本框内容
        # print("src =", src)
        if src:
            try:
                # 将文本框内容转化为字符
                src = (src,)
                # 将处理结果输出到输出文本框
                self.result_data_Text.delete(1.0, END)
                for str in src:
                    line_seg = seg_sentence(str)
                    self.result_data_Text.insert('insert', line_seg)
                self.write_log_to_Text("分词标注成功！")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "标记失败！")
        else:
            self.write_log_to_Text("ERROR:标记失败！")

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
