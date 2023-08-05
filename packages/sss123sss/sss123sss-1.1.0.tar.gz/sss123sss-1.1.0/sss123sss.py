# # -*- coding: utf-8 -*-
# import time
# import sys
# # 判断python的版本然后import对应的模块
# if sys.version < '3':
#     from Tkinter import *
# else:
#     from tkinter import *

# mydelaymin = 30  # 窗口提示的延迟时间，以分钟计

# #------------------def-------------------


# def showMessage():
#     #show reminder message window
#     root = Tk()  # 建立根窗口
#     #root.minsize(500, 200)   #定义窗口的大小
#     #root.maxsize(1000, 400)  #不过定义窗口这个功能我没有使用
#     root.withdraw()  # hide window
#     #获取屏幕的宽度和高度，并且在高度上考虑到底部的任务栏，为了是弹出的窗口在屏幕中间
#     screenwidth = root.winfo_screenwidth()
#     screenheight = root.winfo_screenheight() - 100
#     root.resizable(False, False)
#     #添加组件
#     root.title("Warning!!")
#     frame = Frame(root, relief=RIDGE, borderwidth=3)
#     frame.pack(fill=BOTH, expand=1)  # pack() 放置组件若没有则组件不会显示
#     #窗口显示的文字、并设置字体、字号
#     label = Label(frame, text="You have been working 30 minutes! Please have a break!!",
#                   font="Monotype\ Corsiva -20 bold")
#     label.pack(fill=BOTH, expand=1)
#     #按钮的设置
#     button = Button(frame, text="OK", font="Cooper -25 bold",
#                     fg="red", command=root.destroy)
#     button.pack(side=BOTTOM)

#     root.update_idletasks()
#     root.deiconify()  # now the window size was calculated
#     root.withdraw()  # hide the window again 防止窗口出现被拖动的感觉 具体原理未知？
#     root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10,
#                                    (screenwidth - root.winfo_width()) / 2, (screenheight - root.winfo_height()) / 2))
#     root.deiconify()
#     root.mainloop()

# #showMessage()


# while True:
#     time.sleep(mydelaymin * 60)  # 参数为秒
#     showMessage()
# from tkMessageBox import *
# showinfo(title='Tip', message='Hello World')
# askyesno(message='Are u sure?')  # 消息框上有yes 和no两个按钮

# # 可以使用dir(tkMessageBox) 查看这个模块提供了哪些方法
#coding=utf-8


# import tkinter  #Tkinter是Python自带的可编辑的GUI界面，是一个图像窗口。
import tkinter.messagebox

def show():
    # tkinter.messagebox.showinfo(title='say hello', message='hello world')
    # showinfo
    # tkinter.messagebox.showinfo("弹窗提醒", "hello python")
    # showwarning
    tkinter.messagebox.showwarning(title='showwarning', message='hello python')
    # showerror
    tkinter.messagebox.showerror(title='showerror', message='hello python')
    # askquestion返回是字符串，即返回的是‘yes’或者‘no’
    print(tkinter.messagebox.askquestion(title='askquestion返回是字符串，即返回的是‘yes’或者‘no’', message='hello python'))   
    # askyesno     return True, False
    print(tkinter.messagebox.askyesno(title='askyesno', message='hello python'))   
    # asktrycancel  return True, False
    # print(tkinter.messagebox.asktrycancel(title='asktrycancel', message='hello python'))
    # askokcancel    return True, False
    # print(tkinter.messagebox.askokcancel(title='askokcancel', message='hello python'))
    # askyesnocancel      return, True, False, None
    # print(tkinter.messagebox.askyesnocancel(title="askyesnocancel", message="hello python"))
show()




# from tkinter import *
# from tkinter import messagebox
# def show():
#     messagebox.askokcancel(message="Is Ok")
#     mainloop()

# show()


# import tkinter as tk

# window = tk.Tk()
# window.title('my window')
# window.geometry('900x600')

# # 这里是窗口的内容
# window.mainloop()



# l = tk.Label(window,
#              text='OMG! this is TK!',    # 标签的文字
#              bg='green',     # 背景颜色
#              font=('Arial', 12),     # 字体和字体大小
#              width=15, height=2）  # 标签长宽
# l.pack()    # 固定窗口位置
# window.mainloop()
# import tkinter as tk

# window = tk.Tk()
# window.title('my window')
# window.geometry('300x100')

# var = tk.StringVar()
# l = tk.Label(window, textvariable=var, bg='green', font=('Arial', 12), width=15,
#              height=2)
# l.pack()

# on_hit = False


# def hit_me():
#     global on_hit
#     if on_hit == False:
#         on_hit = True
#         var.set('you hit me')
#     else:
#         on_hit = False
#         var.set('')


# b = tk.Button(window, text='hit me', width=15,
#               height=2, command=hit_me)
# b.pack()

# window.mainloop()
