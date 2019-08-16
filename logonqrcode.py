# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 17:02:41 2019

@author: XuLp
"""

import qrcode 
import zxing
from os import path
from tkinter import filedialog,Tk,StringVar,Button,Label
from PIL import Image
from threading import Thread


def create_qrcode(url,qrcodename):
    '''
    重新生成高容错二维码，并添加logo
    '''
    var.set ('正在创建新的二维码')
    qr = qrcode.QRCode(
        version=1,  # 设置容错率为最高
        error_correction=qrcode.ERROR_CORRECT_H, # 用于控制二维码的错误纠正程度
        box_size=8, # 控制二维码中每个格子的像素数，默认为10
        border=1, # 二维码四周留白，包含的格子数，默认为4
        #image_factory=None,  保存在模块根目录的image文件夹下
        #mask_pattern=None
    )
 
    qr.add_data(url) # QRCode.add_data(data)函数添加数据
    qr.make(fit=True)  # QRCode.make(fit=True)函数生成图片
 
    img = qr.make_image()
    img = img.convert("RGBA") # 二维码设为彩色
    if path.exists('logo.png') == False:
        var.set('缺少logo.png文件')
        return
    logo = Image.open('logo.png') # 传gif生成的二维码也是没有动态效果的
 
    w , h = img.size
    logo_w , logo_h = logo.size
    factor = 4   # 默认logo最大设为图片的四分之一
    s_w = int(w / factor)
    s_h = int(h / factor)
    if logo_w > s_w or logo_h > s_h:
        logo_w = s_w
        logo_h = s_h
 
    logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
    l_w = int((w - logo_w) / 2)
    l_h = int((h - logo_h) / 2)
    logo = logo.convert("RGBA")
    img.paste(logo, (l_w, l_h), logo)
    img.save(qrcodename, quality=100)
    var.set('生成新二维码成功')
    
def decode(file):
    '''
    传入二维码路径，识别出其中内容
    '''
    var.set ('正在分析二维码')
    if path.exists(file):
        reader = zxing.BarCodeReader(classpath='java/*') 
        qrfile = 'file:/'+file
        barcode = reader.decode(qrfile)
        var.set ('正在获取二维码地址')
        if barcode == None:
            var.set('无法正确识别二维码')
            return
    savepath = path.splitext(file)[0] + '_new.png'
    var.set ('准备创建二维码'+savepath)
    create_qrcode(barcode.parsed, savepath )
    return True


def open_file():
    '''
    打开文件对话框 选择要处理的文件,启动新线程，防止卡屏
    '''
    file_name = filedialog.askopenfilename(filetypes=[("PNG",".png")])
    if len(file_name) == 0:
        var.set ('没有打开任何文件')
        return
    var.set ('正在打开二维码')
    thread = Thread(target=decode,args=(file_name,), name='qrdecode')
    thread.start()
    
if __name__ == '__main__':
    '''
    主程序入口，初始化窗口
    '''
    global var
    window = Tk()
    var = StringVar() 
    # 第2步，给窗口的可视化起名字
    window.title('二维码logo生成器')
     
    # 第3步，设定窗口的大小(长 * 宽)
    #设置窗口大小
    width = 380
    height = 300
    #获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
    window.geometry(alignstr)
    #设置窗口是否可变长、宽，True：可变，False：不可变
    window.resizable(width=False, height=False)
    

    
    var.set('请打开二维码文件')
    btn_open = Button(window,pady=20, text='打开原二维码', font=('宋体', 12), command=open_file)
    
    btn_open.pack()
    Label(window,pady=30, text="先从下载二维码，通过本程序打开，\n会自动在原二维码路径下生成带logo的二维码").pack()
    Label(window, pady=30, text="by TonyHsu").pack(side='right')
    lb_status = Label(window,fg='red',textvariable=var,width=200, height=2,anchor='w')
    lb_status.pack(side='bottom', fill = 'x')
    
    # 第6步，主窗口循环显示
    window.mainloop()



