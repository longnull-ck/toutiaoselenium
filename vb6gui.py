# -*- coding: utf-8 -*-
import io
import os
import queue
import threading
import sys
from tkinter import *
from tkinter.ttk import *
from sele import monitor_network


import sele
sys.path.append(os.getcwd())

# 获取sele pritn 的内容
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert(END, str, (self.tag,))
        self.widget.configure(state='disabled')
        self.widget.see(END)

    def flush(self):
        pass


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('极目')
        self.master.geometry('1070x694')

        self.createUI()

    # 生成界面

    def createUI(self):
        self.top = self.winfo_toplevel()
        self.style = Style()
        self.style.theme_use('alt')
        self.style.configure('TFrame3.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame3.TLabelframe.Label', font=('宋体', 9))
        self.Frame3 = LabelFrame(self.top, text='运行日志', style='TFrame3.TLabelframe')
        self.Frame3.place(relx=0.344, rely=0.565, relwidth=0.644, relheight=0.416)

        self.style.configure('TFrame2.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame2.TLabelframe.Label', font=('宋体', 9))
        self.Frame2 = LabelFrame(self.top, text='用户列表', style='TFrame2.TLabelframe')
        self.Frame2.place(relx=0.336, rely=0.012, relwidth=0.651, relheight=0.52)

        self.style.configure('TFrame1.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame1.TLabelframe.Label', font=('宋体', 9))
        self.Frame1 = LabelFrame(self.top, text='操作台', style='TFrame1.TLabelframe')
        self.Frame1.place(relx=0.007, rely=0.012, relwidth=0.315, relheight=0.336)

        self.Combo1List = ['情感', '健康养生', '财经', '社会', '娱乐', "文化"]
        self.Combo1Var = StringVar(value='情感')
        self.Combo1 = Combobox(self.Frame1, state='readonly', text='情感', textvariable=self.Combo1Var,
                               values=self.Combo1List,
                               font=('宋体', 9))
        self.Combo1.setText = lambda x: self.Combo1Var.set(x)
        self.Combo1.text = lambda: self.Combo1Var.get()
        self.Combo1.place(relx=0.57, rely=0.549, relwidth=0.335)

        self.Text1Var = StringVar(value='3')
        self.Text1 = Entry(self.Frame1, textvariable=self.Text1Var, font=('宋体', 9))
        self.Text1.setText = lambda x: self.Text1Var.set(x)
        self.Text1.text = lambda: self.Text1Var.get()
        self.Text1.place(relx=0.57, rely=0.343, relwidth=0.335, relheight=0.107)

        self.alselectList = ['文心一言', 'CHATGPT4.0', 'CHATGPT3.5', ]
        self.alselectVar = StringVar(value='文心一言')
        self.alselect = Combobox(self.Frame1, state='readonly', text='文心一言', textvariable=self.alselectVar,
                                 values=self.alselectList, font=('宋体', 9))
        self.alselect.setText = lambda x: self.alselectVar.set(x)
        self.alselect.text = lambda: self.alselectVar.get()
        self.alselect.place(relx=0.57, rely=0.137, relwidth=0.335)

        self.delNumberVar = StringVar(value='删除账号')
        self.style.configure('TdelNumber.TButton', font=('宋体', 9))
        self.delNumber = Button(self.Frame1, text='删除账号', textvariable=self.delNumberVar,
                                command=lambda: self.thread_it(self.delNumber_Cmd), style='TdelNumber.TButton')
        self.delNumber.setText = lambda x: self.delNumberVar.set(x)
        self.delNumber.text = lambda: self.delNumberVar.get()
        self.delNumber.place(relx=0.047, rely=0.343, relwidth=0.264, relheight=0.142)

        self.startVar = StringVar(value='开始执行')
        self.style.configure('Tstart.TButton', font=('宋体', 9))
        self.start = Button(self.Frame1, text='开始执行', textvariable=self.startVar,
                            command=lambda: self.thread_it(self.start_Cmd),
                            style='Tstart.TButton')
        self.start.setText = lambda x: self.startVar.set(x)
        self.start.text = lambda: self.startVar.get()
        self.start.place(relx=0.712, rely=0.79, relwidth=0.24, relheight=0.142)

        self.endbtnVar = StringVar(value='结束')
        self.style.configure('Tstart.TButton', font=('宋体', 9))
        self.endbtn = Button(self.Frame1, text='结束', textvariable=self.endbtnVar,
                             command=self.endbtn_Cmd,
                             style='endbtn.TButton')
        self.endbtn.setText = lambda x: self.endbtnVar.set(x)
        self.endbtn.text = lambda: self.endbtnVar.get()
        self.endbtn.place(relx=0.412, rely=0.79, relwidth=0.24, relheight=0.142)

        self.addNumberVar = StringVar(value='添加账号')
        self.style.configure('TaddNumber.TButton', font=('宋体', 9))
        self.addNumber = Button(self.Frame1, text='添加账号', textvariable=self.addNumberVar,
                                command=lambda: self.thread_it(self.addNumber_Cmd), style='TaddNumber.TButton')
        self.addNumber.setText = lambda x: self.addNumberVar.set(x)
        self.addNumber.text = lambda: self.addNumberVar.get()
        self.addNumber.place(relx=0.047, rely=0.103, relwidth=0.264, relheight=0.142)

        self.Label3Var = StringVar(value='文章类型')
        self.style.configure('TLabel3.TLabel', anchor='w', font=('宋体', 9))
        self.Label3 = Label(self.Frame1, text='文章类型', textvariable=self.Label3Var, style='TLabel3.TLabel')
        self.Label3.setText = lambda x: self.Label3Var.set(x)
        self.Label3.text = lambda: self.Label3Var.get()
        self.Label3.place(relx=0.38, rely=0.549, relwidth=0.169, relheight=0.107)

        self.Label2Var = StringVar(value='存稿数量')
        self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体', 9))
        self.Label2 = Label(self.Frame1, text='存稿数量', textvariable=self.Label2Var, style='TLabel2.TLabel')
        self.Label2.setText = lambda x: self.Label2Var.set(x)
        self.Label2.text = lambda: self.Label2Var.get()
        self.Label2.place(relx=0.38, rely=0.358, relwidth=0.155, relheight=0.107)

        self.Label1Var = StringVar(value='AI选择')
        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体', 9))
        self.Label1 = Label(self.Frame1, text='AI选择', textvariable=self.Label1Var, style='TLabel1.TLabel')
        self.Label1.setText = lambda x: self.Label1Var.set(x)
        self.Label1.text = lambda: self.Label1Var.get()
        self.Label1.place(relx=0.404, rely=0.135, relwidth=0.131, relheight=0.12)

        self.tree = Treeview(self.Frame2, columns=("用户id", "用户名", "总收益", "昨天收益",), show='headings')
        self.tree.place(relx=0.012, rely=0.055, relwidth=0.977, relheight=0.917)
        self.tree.heading("用户id", text="用户id")
        self.tree.heading("用户名", text="用户名")
        self.tree.heading("总收益", text="总收益")
        self.tree.heading("昨天收益", text="昨天收益")
        self.tree.column("用户id", width=30)
        self.tree.column("用户名", width=60)
        self.tree.column("总收益", width=40)
        self.tree.column("昨天收益", width=40)

        self.text = Text(self.Frame3, state='disabled', )
        self.text.place(relx=0.012, rely=0.055, relwidth=0.977, relheight=0.917)
        self.redirector = TextRedirector(self.text)
        sys.stdout = self.redirector

    def addNumber_Cmd(self, event=None):
        sele.get_user_cookie()

    def start_Cmd(self):
        # 创建一个StringIO对象来捕获输出
        # print(self.Combo1.text())
        sele.start(int(self.Text1Var.get()),str(self.Combo1.text()))

        # baijia.start(int(self.Text1Var.get()), str(self.Combo1.text()), "百度")

    def delNumber_Cmd(self, event=None):
        pass
        # 打包进线程（耗时的操作）

    def endbtn_Cmd(self):
        sele.get_process_id()
        os._exit(0)
        pass
        # 结束线程

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.start()  # 启动

    def thread_function(self, q):
        result = monitor_network()
        q.put(result)

    def update_text(self):
        q = queue.Queue()
        thread = threading.Thread(target=self.thread_function, args=(q,))
        thread.start()
        thread.join()
        results = []
        data = []
        while not q.empty():
            results.append(q.get())
        try:
            for result in results:
                for i in result:
                    data.append((i['user_id'], i['user_name'], i['total_income'], i["yesterday_income"]))
            for row in data:
                self.tree.insert("", END, values=row)
                print('获取结束')
        except Exception as e:
            print("当前未添加账号，请添加用户后获取用户信息，或者添加用户后重新打开")




app = Application()
app.thread_it(app.update_text)
app.mainloop()
