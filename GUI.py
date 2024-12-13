# -*- coding:utf-8 -*-
import base64
import random
import time
import tkinter
import socket
from threading import Thread

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from pathlib import Path

import os
import configparser

from PIL import Image, ImageTk

import Callfunc
import hashlib

import ico


class RB_GUI(ttk.Frame):

    def __init__(self, master):
        self.FrameList = []
        #super().__init__(master, padding=(20, 10))
        # self.pack(fill=BOTH, expand=YES)
        # --------部分配置，如文本等--------
        self.theme_style = ttk.Style()

        theme_names = self.theme_style.theme_names()
        self.Lblbg = ttk.Style().colors.get('bg')
        self.Lblfg = ttk.Style().colors.get('fg')
        self.startgui = False
        menutheme = "light-toolbutton"
        menufont = ("Microsoft Yahei", 8)
        subtitlefont = ("Microsoft Yahei", 16)
        bodytheme = "light"

        self.roots = master

        self.roots.protocol('WM_DELETE_WINDOW', self.destroywin)


        '''
        image_files = {
            'test': 'icons-1.png'
        }

        self.photoimages = []
        imgpath = Path(__file__).parent / 'bin' / 'icons'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))
        '''

        self.theme_names = []

        #---------ip---------

        hostname = socket.gethostname()
        self.localip = socket.gethostbyname(hostname)

        # --------主体框架--------
        self.menu = ttk.Frame(master=master, bootstyle='light')
        self.menu.pack(side=LEFT, padx=0, pady=0, fill=Y, expand='no')
        self.body = ttk.Frame(master=master, style="light", width=920, height=720)
        self.body.pack(side=RIGHT, padx=0, pady=0, fill=BOTH, expand='yes')
        self.body.pack_propagate(0)
        self.func = ""


        '''
        for color_label in style.colors.label_iter():
            color = style.colors.get('bg')
            print(color_label, color)
        '''
        # --------左侧八个选择按钮--------
        Button_func = [
            ("首页", self.show_Index),
            ("VSS", self.show_VSS),
            ("PVSS", self.show_PVSS),
            ("PVSS-n", self.show_PVSSn),
            ("VRF", self.show_VRF),
            ("VRF-n", self.show_VRFn),
            ("FHE", self.show_HERB),
            ("设置", self.show_Settings),
            ("关于", self.show_About)
        ]

        for name, func in Button_func:
            Btn_menu = ttk.Radiobutton(
                master=self.menu,
                text=name,
                width=16,
                command=func,
                variable=self.func,
                value=name,
                bootstyle=menutheme)
            Btn_menu.pack(ipadx=0, padx=0, ipady=18)

        # -------- 左下方时间显示--------

        startFrame = ttk.Frame(master=self.menu, width=120, height=120, bootstyle="bg")
        startFrame.pack(padx=00, pady=00, side=BOTTOM, expand="yes", fill=BOTH)
        # startFrame.pack_propagate(0)
        menuSeparator = ttk.Separator(master=startFrame, bootstyle="primary")

        self.startvar = tkinter.IntVar()
        self.simulvar = tkinter.IntVar()

        startandsimulFrame = ttk.Frame(master=startFrame, bootstyle="bg")
        startandsimulFrame.pack(side=BOTTOM, padx=0, pady=35, expand="no", fill=Y)
        start = ttk.Checkbutton(master=startandsimulFrame, text="启动程序", bootstyle="success-square-toggle",
                                variable=self.startvar, command=self.get_n_t)
        start.pack(side=BOTTOM, padx=10, pady=10, expand="no")

        simul = ttk.Checkbutton(master=startandsimulFrame, text="单机模拟", bootstyle="warning-square-toggle",
                                variable=self.simulvar, command=None)
        simul.pack(side=BOTTOM, padx=10, pady=10, expand="no")

        # time.pack(side=BOTTOM, ipadx=0, ipady=0, expand="no", fill=X)
        menuSeparator.pack(padx=10, pady=10, side=BOTTOM, fill=X)

        # -------- 八个页面--------
        self.IndexFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")

        self.VSSFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.PVSSFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.PVSSnFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.VRFFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.VRFnFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.HERBFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.SettingsFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")
        self.AboutFrame = ttk.Frame(master=self.body, width=920, height=720, bootstyle="bg")

        # -------- Index--------

        title_Frame = ttk.Frame(master=self.IndexFrame, width=800, bootstyle="bg")
        titleunderline = ttk.Separator(master=self.IndexFrame, bootstyle="primary")

        nt_Frame = ttk.Frame(master=self.IndexFrame, width=400, bootstyle="bg")
        RandomLen_Frame = ttk.Frame(master=self.IndexFrame, width=800, bootstyle="bg")
        safenum_Frame = ttk.Frame(master=self.IndexFrame, width=800, bootstyle="bg")

        title_Frame.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        titleunderline.pack(padx=30, fill=X)

        RandomLen_Frame.pack(padx=30, pady=15, side=BOTTOM, expand="no", fill=BOTH)
        safenum_Frame.pack(padx=30, pady=15, side=BOTTOM, expand="no", fill=BOTH)
        nt_Frame.pack(padx=30, pady=15, side=LEFT, expand="no", fill=BOTH)

        global photott
        imgtt = Image.open("./bin/icons/icon_1.png")
        photott = ImageTk.PhotoImage(imgtt.resize((128, 128)))

        self.title = ttk.Label(master=title_Frame, text="随机信标生成平台", anchor="center", image=photott,
                               compound=LEFT,
                               font=("Microsoft Yahei", 32),
                               )
        self.title.pack(padx=10, pady=10, fill=X, expand="no", side=TOP)

        self.number_value = None
        self.threshold_value = None

        # imgtitle = ttk.Label(master=self.IndexFrame, image=photott)
        # imgtitle.pack(side=RIGHT, padx=0, pady=0, expand="no")

        self.numberstr = tkinter.StringVar()
        number_dealer = ttk.Label(master=nt_Frame, text="参与者人数：")
        number_dealer.pack(anchor=NW, padx=00, pady=10, expand="no")
        number_dEntry = ttk.Entry(master=nt_Frame, width=20, textvariable=self.numberstr)
        number_dEntry.pack(padx=0, pady=10, anchor=NW)

        self.thresholdstr = tkinter.StringVar()
        threshold_people = ttk.Label(master=nt_Frame, text="门限值：")
        threshold_people.pack(anchor=NW, padx=00, pady=10, expand="no")
        thresholdEntry = ttk.Entry(master=nt_Frame, width=20, textvariable=self.thresholdstr)
        thresholdEntry.pack(padx=0, pady=10, anchor=NW)

        global photobg
        global photoset
        imgbg = Image.open("./bin/icons/background.png")
        imgset = Image.open("./bin/icons/background.png")
        photobg = ImageTk.PhotoImage(imgbg.resize((482, 108)))
        imgbackground = ttk.Label(master=self.IndexFrame, image=photobg)
        imgbackground.pack(side=RIGHT, padx=0, pady=0, expand="no")

        # IndexCircle = tkinter.PhotoImage(file="./bin/icons/background.png")
        # picCircle = ttk.Label(master=self.IndexFrame, image=IndexCircle)
        # picCircle.pack()
        self.safenumberlbl = ttk.Label(master=safenum_Frame, text="安全参数设置：")
        self.safenumberlbl.pack(anchor=NW, padx=00, pady=10, expand="no")

        self.safenum = tkinter.IntVar()
        self.safenum.set(0)

        Button_safenum = [
            ("128bit", 0, None),
            ("256bit", 1, None),
            ("512bit", 2, None),
            ("1024bit", 3, None)
        ]

        for name, num, func in Button_safenum:
            safenum_Btn = ttk.Radiobutton(
                master=safenum_Frame,
                text=name,
                width=8,
                variable=self.safenum,
                value=num,
                command=func,
                bootstyle="primary-toolbutton"
            )
            safenum_Btn.pack(side=LEFT)

        self.RandomLenlbl = ttk.Label(master=RandomLen_Frame, text="随机数长度设置：")
        self.RandomLenlbl.pack(anchor=NW, padx=00, pady=10, expand="no")

        self.RandomLenValue = [hashlib.md5, hashlib.sha256, hashlib.sha512]
        self.Randomlen = tkinter.IntVar()
        self.Randomlen.set(0)
        self.hash = self.RandomLenValue[self.Randomlen.get()]

        Button_Randomlen = [
            ("128bit", 0, self.RandomLenfunc),
            ("256bit", 1, self.RandomLenfunc),
            ("512bit", 2, self.RandomLenfunc)
        ]

        for name, num, func in Button_Randomlen:
            Randonum_Btn = ttk.Radiobutton(
                master=RandomLen_Frame,
                text=name,
                width=8,
                variable=self.Randomlen,
                value=num,
                command=func,
                bootstyle="primary-toolbutton"
            )
            Randonum_Btn.pack(side=LEFT)

        pingsSubBtn = ttk.Button(master=RandomLen_Frame, text="密钥生成与发送", width=12, bootstyle="info",
                                 command=self.sendkeyasclient)#发送密钥 同时将uid+30000作为端口，另外设置一个常开服务器作为接受方
        pingsSubBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        pingsSubBtn = ttk.Button(master=RandomLen_Frame, text="设备可达性测试", width=12, bootstyle="warning",
                                 command=self.pings)
        pingsSubBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- VSS--------
        VSStitle = ttk.Frame(master=self.VSSFrame, width=800, bootstyle="bg")
        VSStitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        VSStitlelbl = ttk.Label(master=VSStitle, text="基于可验证秘密共享(VSS)的随机信标", font=subtitlefont,
                                )
        VSStitlelbl.pack(side=LEFT, expand="no")

        VSSRnumFrame = ttk.LabelFrame(master=self.VSSFrame, text="本轮随机数生成值", width=800, bootstyle="primary")
        VSSRnumFrame.pack(side=TOP, padx=30, pady=10, expand="no", fill=X)

        self.VSSRnumEntry = ttk.Entry(master=VSSRnumFrame, width=600)
        self.VSSRnumEntry.pack(padx=10, pady=10)

        VSSBlkFrame = ttk.LabelFrame(master=self.VSSFrame, text="块参数", width=400, bootstyle="primary")
        VSSBlkFrame.pack(side=LEFT, padx=30, pady=30, expand="yes", fill=BOTH)

        self.VSSBlkEntry = ttk.Text(master=VSSBlkFrame, width=40)
        self.VSSBlkEntry.pack(padx=10, pady=10, side=TOP, expand="yes", fill=BOTH)

        VSSMSCFrame = ttk.Frame(master=self.VSSFrame, width=410, bootstyle="bg")
        VSSMSCFrame.pack(padx=30, pady=30, expand="yes", fill=Y)


        self.VSSTMEMtr = ttk.Meter(master=VSSMSCFrame, width=200, amountused=0, subtext="生成用时", textright="毫秒",
                                   interactive=False,
                                   bootstyle="secondary")
        self.VSSTMEMtr.pack(side=TOP, padx=30, pady=30, expand="yes", fill=BOTH)

        VSSPubBtn = ttk.Button(master=VSSMSCFrame, text="公开或验证", width=9, bootstyle="warning", command=self.verify_Block)
        VSSPubBtn.pack(side=LEFT, padx=30, pady=30, expand="no", fill=X)

        VSSGenBtn = ttk.Button(master=VSSMSCFrame, text="下一轮生成", width=9, bootstyle="success", command=self.VSS_Gen_Btn)
        VSSGenBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- PVSS--------
        PVSStitle = ttk.Frame(master=self.PVSSFrame, width=800, bootstyle="bg")
        PVSStitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        PVSStitlelbl = ttk.Label(master=PVSStitle, text="基于公开可验证秘密共享(PVSS)的随机信标", font=subtitlefont)
        PVSStitlelbl.pack(side=LEFT, expand="no")

        PVSSRnumFrame = ttk.LabelFrame(master=self.PVSSFrame, text="本轮随机数生成值", width=800, bootstyle="primary")
        PVSSRnumFrame.pack(side=TOP, padx=30, pady=10, expand="no", fill=X)

        self.PVSSRnumEntry = ttk.Entry(master=PVSSRnumFrame, width=600)
        self.PVSSRnumEntry.pack(padx=10, pady=10)

        PVSSBlkFrame = ttk.LabelFrame(master=self.PVSSFrame, text="块参数", width=400, bootstyle="primary")
        PVSSBlkFrame.pack(side=LEFT, padx=30, pady=30, expand="yes", fill=BOTH)

        self.PVSSBlkEntry = ttk.Text(master=PVSSBlkFrame, width=40)
        self.PVSSBlkEntry.pack(padx=10, pady=10, side=TOP, expand="yes", fill=BOTH)

        PVSSMSCFrame = ttk.Frame(master=self.PVSSFrame, width=410, bootstyle="bg")
        PVSSMSCFrame.pack(padx=30, pady=30, expand="yes", fill=Y)

        self.PVSSTMEMtr = ttk.Meter(master=PVSSMSCFrame, width=200, amountused=0, subtext="生成用时", textright="毫秒",
                                    interactive=False,
                                    bootstyle="secondary")
        self.PVSSTMEMtr.pack(side=TOP, padx=30, pady=30, expand="yes", fill=BOTH)

        PVSSPubBtn = ttk.Button(master=PVSSMSCFrame, text="公开或验证", width=9, bootstyle="warning", command=self.verify_Block)
        PVSSPubBtn.pack(side=LEFT, padx=30, pady=30, expand="no", fill=X)

        PVSSGenBtn = ttk.Button(master=PVSSMSCFrame, text="下一轮生成", width=9, bootstyle="success",
                                command=self.PVSS_Gen_Btn)
        PVSSGenBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- PVSSn--------
        PVSSntitle = ttk.Frame(master=self.PVSSnFrame, width=800, bootstyle="bg")
        PVSSntitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        PVSSntitlelbl = ttk.Label(master=PVSSntitle, text="基于多方公开可验证秘密共享(PVSS-n)的随机信标", font=subtitlefont,
                                  )
        PVSSntitlelbl.pack(side=LEFT, expand="no")

        PVSSnRnumFrame = ttk.LabelFrame(master=self.PVSSnFrame, text="本轮随机数生成值", width=800, bootstyle="primary")
        PVSSnRnumFrame.pack(side=TOP, padx=30, pady=10, expand="no", fill=X)

        self.PVSSnRnumEntry = ttk.Entry(master=PVSSnRnumFrame, width=600)
        self.PVSSnRnumEntry.pack(padx=10, pady=10)

        PVSSnBlkFrame = ttk.LabelFrame(master=self.PVSSnFrame, text="块参数", width=400, bootstyle="primary")
        PVSSnBlkFrame.pack(side=LEFT, padx=30, pady=30, expand="yes", fill=BOTH)

        self.PVSSnBlkEntry = ttk.Text(master=PVSSnBlkFrame, width=40)
        self.PVSSnBlkEntry.pack(padx=10, pady=10, side=TOP, expand="yes", fill=BOTH)

        PVSSnMSCFrame = ttk.Frame(master=self.PVSSnFrame, width=410, bootstyle="bg")
        PVSSnMSCFrame.pack(padx=30, pady=30, expand="yes", fill=Y)

        self.PVSSnTMEMtr = ttk.Meter(master=PVSSnMSCFrame, width=200, amountused=0, subtext="生成用时", textright="毫秒",
                                     interactive=False,
                                     bootstyle="secondary")
        self.PVSSnTMEMtr.pack(side=TOP, padx=30, pady=30, expand="yes", fill=BOTH)

        PVSSnPubBtn = ttk.Button(master=PVSSnMSCFrame, text="公开或验证", width=9, bootstyle="warning",
                                 command=self.verify_Block)
        PVSSnPubBtn.pack(side=LEFT, padx=30, pady=30, expand="no", fill=X)

        PVSSnGenBtn = ttk.Button(master=PVSSnMSCFrame, text="下一轮生成", width=9, bootstyle="success",
                                 command=self.PVSS_n_Gen_Btn)
        PVSSnGenBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- VRF--------
        VRFtitle = ttk.Frame(master=self.VRFFrame, width=800, bootstyle="bg")
        VRFtitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        VRFtitlelbl = ttk.Label(master=VRFtitle, text="基于可验证随机函数(VRF)的随机信标", font=subtitlefont,
                                )
        VRFtitlelbl.pack(side=LEFT, expand="no")

        VRFRnumFrame = ttk.LabelFrame(master=self.VRFFrame, text="本轮随机数生成值", width=800, bootstyle="primary")
        VRFRnumFrame.pack(side=TOP, padx=30, pady=10, expand="no", fill=X)

        self.VRFRnumEntry = ttk.Entry(master=VRFRnumFrame, width=600)
        self.VRFRnumEntry.pack(padx=10, pady=10)

        VRFBlkFrame = ttk.LabelFrame(master=self.VRFFrame, text="块参数", width=400, bootstyle="primary")
        VRFBlkFrame.pack(side=LEFT, padx=30, pady=30, expand="yes", fill=BOTH)

        self.VRFBlkEntry = ttk.Text(master=VRFBlkFrame, width=40)
        self.VRFBlkEntry.pack(padx=10, pady=10, side=TOP, expand="yes", fill=BOTH)

        VRFMSCFrame = ttk.Frame(master=self.VRFFrame, width=410, bootstyle="bg")
        VRFMSCFrame.pack(padx=30, pady=30, expand="yes", fill=Y)

        self.VRFTMEMtr = ttk.Meter(master=VRFMSCFrame, width=200, amountused=0, subtext="生成用时", textright="毫秒",
                                   interactive=False,
                                   bootstyle="secondary")
        self.VRFTMEMtr.pack(side=TOP, padx=30, pady=30, expand="yes", fill=BOTH)

        VRFPubBtn = ttk.Button(master=VRFMSCFrame, text="公开或验证", width=9, bootstyle="warning", command=self.verify_Block)
        VRFPubBtn.pack(side=LEFT, padx=30, pady=30, expand="no", fill=X)

        VRFGenBtn = ttk.Button(master=VRFMSCFrame, text="下一轮生成", width=9, bootstyle="success", command=self.VRF_Gen_Btn)
        VRFGenBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- VRFn--------
        VRFntitle = ttk.Frame(master=self.VRFnFrame, width=800, bootstyle="bg")
        VRFntitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)

        VRFntitlelbl = ttk.Label(master=VRFntitle, text="基于多方可验证随机函数(VRF-n)的随机信标", font=subtitlefont,
                                 )

        VRFntitlelbl.pack(side=LEFT, expand="no")

        VRFnRnumFrame = ttk.LabelFrame(master=self.VRFnFrame, text="本轮随机数生成值", width=800, bootstyle="primary")
        VRFnRnumFrame.pack(side=TOP, padx=30, pady=10, expand="no", fill=X)

        self.VRFnRnumEntry = ttk.Entry(master=VRFnRnumFrame, width=600)
        self.VRFnRnumEntry.pack(padx=10, pady=10)

        VRFnBlkFrame = ttk.LabelFrame(master=self.VRFnFrame, text="块参数", width=400, bootstyle="primary")
        VRFnBlkFrame.pack(side=LEFT, padx=30, pady=30, expand="yes", fill=BOTH)

        self.VRFnBlkEntry = ttk.Text(master=VRFnBlkFrame, width=40)
        self.VRFnBlkEntry.pack(padx=10, pady=10, side=TOP, expand="yes", fill=BOTH)

        VRFnMSCFrame = ttk.Frame(master=self.VRFnFrame, width=410, bootstyle="bg")
        VRFnMSCFrame.pack(padx=30, pady=30, expand="yes", fill=Y)

        self.VRFnTMEMtr = ttk.Meter(master=VRFnMSCFrame, width=200, amountused=0, subtext="生成用时", textright="毫秒",
                                    interactive=False,
                                    bootstyle="secondary")
        self.VRFnTMEMtr.pack(side=TOP, padx=30, pady=30, expand="yes", fill=BOTH)

        VRFnPubBtn = ttk.Button(master=VRFnMSCFrame, text="公开或验证", width=9, bootstyle="warning", command=self.verify_Block)
        VRFnPubBtn.pack(side=LEFT, padx=30, pady=30, expand="no", fill=X)

        VRFnGenBtn = ttk.Button(master=VRFnMSCFrame, text="下一轮生成", width=9, bootstyle="success",
                                command=self.VRF_n_Gen_Btn)
        VRFnGenBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- HERB--------
        HERBtitle = ttk.Frame(master=self.HERBFrame, width=800, bootstyle="bg")
        HERBtitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)

        HERBtitlelbl = ttk.Label(master=HERBtitle, text="基于全同态加密(FHE)的随机信标", font=subtitlefont,
                                 )

        HERBtitlelbl.pack(side=LEFT, expand="no")

        HERBRnumFrame = ttk.LabelFrame(master=self.HERBFrame, text="本轮随机数生成值", width=800, bootstyle="primary")
        HERBRnumFrame.pack(side=TOP, padx=30, pady=10, expand="no", fill=X)

        self.HERBRnumEntry = ttk.Entry(master=HERBRnumFrame, width=600)
        self.HERBRnumEntry.pack(padx=10, pady=10)

        HERBBlkFrame = ttk.LabelFrame(master=self.HERBFrame, text="块参数", width=400, bootstyle="primary")
        HERBBlkFrame.pack(side=LEFT, padx=30, pady=30, expand="yes", fill=BOTH)

        self.HERBBlkEntry = ttk.Text(master=HERBBlkFrame, width=40)
        self.HERBBlkEntry.pack(padx=10, pady=10, side=TOP, expand="yes", fill=BOTH)

        HERBMSCFrame = ttk.Frame(master=self.HERBFrame, width=410, bootstyle="bg")
        HERBMSCFrame.pack(padx=30, pady=30, expand="yes", fill=Y)

        self.HERBTMEMtr = ttk.Meter(master=HERBMSCFrame, width=200, amountused=0, subtext="生成用时", textright="毫秒",
                                    interactive=False,
                                    bootstyle="secondary")
        self.HERBTMEMtr.pack(side=TOP, padx=30, pady=30, expand="yes", fill=BOTH)

        HERBPubBtn = ttk.Button(master=HERBMSCFrame, text="公开或验证", width=9, bootstyle="warning", command=self.verify_Block)
        HERBPubBtn.pack(side=LEFT, padx=30, pady=30, expand="no", fill=X)

        HERBGenBtn = ttk.Button(master=HERBMSCFrame, text="下一轮生成", width=9, bootstyle="success",
                                command=self.HERB_Gen_Btn)
        HERBGenBtn.pack(side=RIGHT, padx=30, pady=30, expand="no", fill=X)

        # -------- Settings--------
        # print(theme_names)

        settingtitle = ttk.Frame(master=self.SettingsFrame, width=800, bootstyle="bg")
        settingunderline = ttk.Separator(master=self.SettingsFrame, bootstyle="primary")
        themecboFrame = ttk.Frame(master=self.SettingsFrame, width=80, bootstyle="bg")
        IPFrame = ttk.LabelFrame(master=self.SettingsFrame, text="IP池", width=40, height=20, bootstyle="primary")

        settingtitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        settingunderline.pack(padx=30, fill=X)
        themecboFrame.pack(side=LEFT, padx=30, pady=30, anchor=NW, expand="no", fill=Y)
        IPFrame.pack(side=TOP, anchor=NE, padx=30, pady=30, expand="no", )

        settitlelbl = ttk.Label(master=settingtitle, text="设置", font=subtitlefont, )
        settitlelbl.pack(side=LEFT, expand="no")

        transmsgtitle = ttk.LabelFrame(master=themecboFrame, text="传输记录", bootstyle="primary")
        transmsgtitle.pack(anchor=NW, padx=0, pady=0, expand='no')

        self.transmsg = ScrolledText(master=transmsgtitle, width=20, height=14, hbar=True, autohide=True)
        self.transmsg.pack(anchor=NW, padx=10, pady=10, expand="no")

        usruidtitle = ttk.Label(master=themecboFrame, text="用户uid：")
        usruidtitle.pack(anchor=NW, padx=10, pady=10)

        self.uid = tkinter.StringVar()
        self.usruidEntry = ttk.Entry(master=themecboFrame, width=20, textvariable=self.uid)
        self.usruidEntry.pack(anchor=NW, padx=10, pady=10)

        themetitle = ttk.Label(master=themecboFrame, text="主题：")
        themetitle.pack(anchor=NW, padx=10, pady=10)

        self.theme_cbo = ttk.Combobox(width=18, master=themecboFrame, text=self.theme_style.theme.name,
                                      values=theme_names)
        self.theme_cbo.pack(anchor=NW, padx=10)
        self.theme_cbo.current(theme_names.index(self.theme_style.theme.name))



        self.IPpoollst = []
        self.IPpoolEntry = ttk.Text(master=IPFrame, width=100, height=14)
        self.IPpoolEntry.pack(padx=10, pady=10, side=TOP, expand="no", fill=BOTH)

        photoset = ImageTk.PhotoImage(imgset.resize((642, 144)))
        imgbackground = ttk.Label(master=self.SettingsFrame, image=photoset, )
        imgbackground.pack(anchor=NE, padx=0, pady=0, expand="no")

        # -------- About--------

        Abttitle = ttk.Frame(master=self.AboutFrame, width=800, bootstyle="bg")
        Abtunderline = ttk.Separator(master=self.AboutFrame, bootstyle="primary")
        AbttextFrame = ttk.Frame(master=self.AboutFrame, width=800, bootstyle="bg")
        Abtstr = "\
        简介\
        \n\n\
        随机信标生成方案均可实现较为良好的不可预测性和随机性，并且在效率上也基本达到预期的目标，适用于对随机\n\
        数公开透明属性和可验证性较高的多种应用场景，具备较强的实用性。本套件提供了基于秘密共享、可验证随机函数\n\
        和同态加密的随机信标生成，同时通过socket及TCP连接可以实现小型网络内多人使用\n\n\
        使用说明\
        \n\n\
        1、在首页设置参与人数n，门限值t，安全参数和随机数长度。\n\
        2、点击左下角“启动程序”按钮，开始计算。请注意，一旦选择启动程序，在程序关闭之前，第一步设置\n\
        的参数无法再次改变；\n\
        3、进入左侧各个方案，进行随机信标生成。每一轮信标生成前必须验证；\n\
        4、设置部分可以设置用户uid作为计算标识，以及小型网络内的其他用户IP。可以依据个人喜好修改界面。\n"

        Abttitle.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)
        Abtunderline.pack(padx=30, fill=X)
        Abttitlelbl = ttk.Label(master=Abttitle, text="关于", font=subtitlefont)  # foreground=self.Lblfg
        Abttitlelbl.pack(side=LEFT, expand="no")
        AbttextFrame.pack(padx=00, pady=30, side=TOP, expand="no", fill=X)

        Abttext = ttk.Label(master=AbttextFrame, text=Abtstr, width=800)
        Abttext.pack(padx=30, pady=30, side=TOP, expand="no", fill=X)

        # ------------------------------------------------------------------

        self.VSSfin = None
        self.PVSSfin = None
        self.PVSSnfin = None
        self.VRFfin = None
        self.VRFnfin = None
        self.func_value_lst = [0, 0, 0, 0, 0, 0, 0]
        self.Random_value_lst = [None, None, None, None, None, None, None]
        self.Block_value_lst = [None, None, None, None, None, None, None]
        self.Block_time_lst = [0, 0, 0, 0, 0, 0, 0]
        self.switch = False
        self.HERBheight = 0

        self.recvthread = Thread(target=self.recvdata)
        self.recvthread.setDaemon(True)
        self.recvthread.start()

    def destroywin(self):
        ret = ttk.dialogs.dialogs.Messagebox.show_question(message="确认结束运行？", title="结束运行",buttons=['No:secondary', 'Yes:primry'])
        if ret == '确认':

            self.roots.destroy()

    def pings(self):
        strips = ""
        configiptest = configparser.ConfigParser()
        configiptest.read("bin/settings/settings.ini")
        strips = configiptest["section3"]["ippool"]
        lstips = list(strips.split('\n'))
        idx = 0
        for ip in lstips:
            idx += 1
            pingbd = os.system("ping " + ip + " -n 1")
            if pingbd == 0:
                ttk.dialogs.dialogs.Messagebox.ok(message="第" + str(idx) + "号IP地址" + ip + "通信测试成功", title="通信测试")
            else:
                ttk.dialogs.dialogs.Messagebox.ok(message="第" + str(idx) + "号IP地址" + ip + "通信测试失败，检查网络配置", title="通信测试")

    def sendkeyasclient(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        configuidip = configparser.ConfigParser()
        configuidip.read("bin/settings/settings.ini")
        port = 30000 + int(configuidip["section2"].get("uid"))
        sock.bind((self.localip, port))
        strips = configuidip["section3"]["ippool"]
        lstips = list(strips.split('\n'))
        idx = 1
        for ip in lstips:
            if (idx + 30000) == port:
                idx += 1
            sock.sendto("PubKey".encode(), (ip, idx + 20000))
            #data, addr = sock.recvfrom(1024)
            #print(data.decode())
            date = time.localtime()
            strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                 date.tm_min, date.tm_sec)
            self.transmsg.insert(END, "send Pubkey. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                             strdate))
            idx += 1
        sock.close()

    def recvdata(self):
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        configuidip = configparser.ConfigParser()
        configuidip.read("bin/settings/settings.ini")
        port = 20000 + int(configuidip["section2"].get("uid"))
        udpsocket.bind((self.localip, port))
        while True:
            recv_data, src_addr = udpsocket.recvfrom(1024)
            recv_data = recv_data.decode('utf-8')
            #print('收到信息为:%s' % recv_data)
            date = time.localtime()
            strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                      date.tm_min, date.tm_sec)
            #ttk.dialogs.dialogs.Messagebox.ok(message='收到信息为:%s' % recv_data, title="通信测试")
            #print(111)
            typedata = recv_data.split("\n", 1)
            if typedata[0] !='PubKey':
                self.transmsg.insert(END, "received Msg. from {0}:{1} at {2}\n".format(src_addr[0], src_addr[1], strdate))
                path = 'bin/data/data_'+typedata[0]+'.txt'
                with open(path, 'w') as f:
                    f.write(typedata[1])
            else:
                self.transmsg.insert(END, "received PubKey. from {0}:{1} at {2}\n".format(src_addr[0], src_addr[1], strdate))


    def get_n_t(self):
        if self.startvar.get() == 1 and self.number_value is None and self.threshold_value is None:
            self.number_value = self.numberstr.get()
            self.threshold_value = self.thresholdstr.get()
            # print(self.number_value, self.threshold_value)
            self.VSSfin = Callfunc.VSS_Random_Beacon(int(self.number_value), int(self.threshold_value))
            self.PVSSfin = Callfunc.PVSS_Random_Beacon(int(self.number_value), int(self.threshold_value))
            self.PVSSnfin = Callfunc.PVSS_n_Random_Beacon(int(self.number_value), int(self.threshold_value))
            self.VRFfin = Callfunc.VRF_Random_Beacon(int(self.number_value), int(self.threshold_value))
            self.VRFnfin = Callfunc.VRF_n_Random_Beacon(int(self.number_value), int(self.threshold_value))
            next(self.VSSfin)
            next(self.PVSSfin)
            next(self.PVSSnfin)
            next(self.VRFfin)
            next(self.VRFnfin)
            self.startgui = True

    def change_theme(self, event):
        theme_cbo_value = self.theme_cbo.get()
        self.theme_style.theme_use(theme_cbo_value)
        # theme_selected.configure(text=theme_cbo_value)
        self.theme_cbo.selection_clear()
        conf = configparser.ConfigParser()
        conf.read("bin/settings/settings.ini")
        conf.set("section1", "themes", theme_cbo_value)
        conf.write(open("bin/settings/settings.ini", "w+"))
        self.Lblbg = ttk.Style(theme_cbo_value).colors.get('bg')
        self.Lblfg = ttk.Style(theme_cbo_value).colors.get('fg')
        # print(self.Lblbg)

    def change_usruid(self, event):
        uid_value = self.uid.get()
        conf = configparser.ConfigParser()
        conf.read("bin/settings/settings.ini")
        conf.set("section2", "uid", uid_value)
        conf.write(open("bin/settings/settings.ini", "w+"))
        # print(self.Lblbg)
        self.uid.set(uid_value)

    def change_ippool(self, envet):
        strIP = self.IPpoolEntry.get('1.0', END)
        conf = configparser.ConfigParser()
        conf.read("bin/settings/settings.ini")
        conf.set("section3", "ippool", strIP)
        conf.write(open("bin/settings/settings.ini", "w+"))

        # -------- 生成窗口--------

    def show_Index(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.IndexFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        # Index.pack_propagate(0)
        self.FrameList.append(self.IndexFrame)

        self.title.configure(background=self.Lblbg)
        self.safenumberlbl.configure(background=self.Lblbg)
        self.RandomLenlbl.configure(background=self.Lblbg)

    def show_VSS(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.VSSFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.VSSFrame)

    def show_PVSS(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.PVSSFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.PVSSFrame)

    def show_PVSSn(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.PVSSnFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.PVSSnFrame)

    def show_VRF(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.VRFFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.VRFFrame)

    def show_VRFn(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.VRFnFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.VRFnFrame)

    def show_HERB(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.HERBFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.HERBFrame)

    def show_Settings(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.SettingsFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.SettingsFrame)

        configuidip = configparser.ConfigParser()
        configuidip.read("bin/settings/settings.ini")
        self.uid.set(configuidip["section2"].get("uid"))
        self.IPpoolEntry.delete("1.0", END)
        self.IPpoolEntry.insert(END, configuidip["section3"].get("ippool"))
        self.theme_cbo.bind('<<ComboboxSelected>>', self.change_theme)
        self.usruidEntry.bind('<Return>', self.change_usruid)
        self.IPpoolEntry.bind('<KeyPress>', self.change_ippool)

    def show_About(self):
        if self.FrameList:
            F = self.FrameList.pop()
            F.pack_forget()

        self.AboutFrame.pack(padx=30, pady=30, fill=BOTH, expand="yes")
        self.FrameList.append(self.AboutFrame)

    # ------------------按钮控制-------------------

    def RandomLenfunc(self):
        self.hash = self.RandomLenValue[self.Randomlen.get()]

    def VSS_Gen_Btn(self):
        if self.number_value is not None and self.threshold_value is not None and self.switch is True:
            # print(self.VSSfin.send(self.func_value_lst[0]))
            self.Block_value_lst[0], self.Random_value_lst[0], self.Block_time_lst[0] = self.VSSfin.send(
                self.func_value_lst[0])
            self.func_value_lst[0] += 1
            self.VSSRnumEntry.delete(0, "end")
            m = self.hash(str(self.Random_value_lst[0]).encode("UTF-8"))
            self.VSSRnumEntry.insert(0, m.hexdigest())
            self.VSSTMEMtr.configure(amountused=int(self.Block_time_lst[0]))
            self.VSSBlkEntry.delete(1.0, END)
            blkstr = ""
            for keys in self.Block_value_lst[0].keys():
                blkstr = blkstr + keys + ':\n' + str(self.Block_value_lst[0][keys]) + '\n'

            if self.simulvar.get() == 0:
                with open('bin/data/data_VSS.txt', 'r') as f:
                    lines = f.read()
                    first = lines.split('\n', 1)
                # 显示并接受，下次可发送
                if first[0] == '1':
                    blkstr =first[1]
                    with open('bin/data/data_VSS.txt', 'w') as f:
                        f.write('0\n'+blkstr)
                    hvalue = blkstr.split('\n')[-1]
                    self.VSSRnumEntry.delete(0, "end")
                    self.VSSRnumEntry.insert(0, hvalue)

                #下面用网络写入他人文件
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    configuidip = configparser.ConfigParser()
                    configuidip.read("bin/settings/settings.ini")
                    port = 30000 + int(configuidip["section2"].get("uid"))
                    sock.bind((self.localip, port))
                    strips = configuidip["section3"]["ippool"]
                    lstips = list(strips.split('\n'))
                    idx = 1
                    for ip in lstips:
                        if (idx + 30000) == port:
                            idx += 1
                        sock.sendto(('VSS\n1\n'+blkstr + m.hexdigest()).encode(), (ip, idx + 20000))
                        date = time.localtime()
                        strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                             date.tm_min, date.tm_sec)
                        self.transmsg.insert(END, "send VSS Msg. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                                         strdate))
                        # print(data.decode())
                        idx += 1
                    sock.close()


            #for keys in self.Block_value_lst[0].keys():
            self.VSSBlkEntry.insert(END, blkstr)

            self.switch = False
        elif self.number_value is None or self.threshold_value is None:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="信标块必要参数缺失。\n请前往首页填写对应参数并开启左下角“启动程序”按钮。",
                title="参数缺失")
        elif self.switch is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="生成信标块未验证。\n请首先点击“验证”按钮执行验证步骤。",
                title="顺序错误")

    def PVSS_Gen_Btn(self):
        if self.number_value is not None and self.threshold_value is not None and self.switch is True:
            # print(self.VSSfin.send(self.func_value_lst[0]))
            self.Block_value_lst[1], self.Random_value_lst[1], self.Block_time_lst[1] = self.PVSSfin.send(
                self.func_value_lst[1])
            self.func_value_lst[1] += 1
            self.PVSSRnumEntry.delete(0, "end")
            m = self.hash(str(self.Random_value_lst[1]).encode("UTF-8"))
            self.PVSSRnumEntry.insert(0, m.hexdigest())
            self.PVSSTMEMtr.configure(amountused=int(self.Block_time_lst[1]))
            self.PVSSBlkEntry.delete(1.0, END)

            blkstr = ""
            for keys in self.Block_value_lst[1].keys():
                blkstr = blkstr + keys + ':\n' + str(self.Block_value_lst[1][keys]) + '\n'

            if self.simulvar.get() == 0:
                with open('bin/data/data_PVSS.txt', 'r') as f:
                    lines = f.read()
                    first = lines.split('\n', 1)
                # 显示并发送
                if first[0] == '1':
                    blkstr = first[1]
                    with open('bin/data/data_PVSS.txt', 'w') as f:
                        f.write('0\n' + blkstr)
                    hvalue = blkstr.split('\n')[-1]
                    self.PVSSRnumEntry.delete(0, "end")
                    self.PVSSRnumEntry.insert(0, hvalue)

                # 下面用网络写入他人文件
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    configuidip = configparser.ConfigParser()
                    configuidip.read("bin/settings/settings.ini")
                    port = 30000 + int(configuidip["section2"].get("uid"))
                    sock.bind((self.localip, port))
                    strips = configuidip["section3"]["ippool"]
                    lstips = list(strips.split('\n'))
                    idx = 1
                    for ip in lstips:
                        if (idx + 30000) == port:
                            idx += 1
                        sock.sendto(('PVSS\n1\n' + blkstr + m.hexdigest()).encode(), (ip, idx + 20000))
                        # print(data.decode())
                        date = time.localtime()
                        strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                             date.tm_min, date.tm_sec)
                        self.transmsg.insert(END, "send PVSS Msg. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                                         strdate))
                        idx += 1
                    sock.close()
                    pass

            self.PVSSBlkEntry.insert(END, blkstr)

            self.switch = False
        elif self.number_value is None or self.threshold_value is None:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="信标块必要参数缺失。\n请前往首页填写对应参数并开启左下角“启动程序”按钮。",
                title="参数缺失")
        elif self.switch is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="生成信标块未验证。\n请首先点击“验证”按钮执行验证步骤。",
                title="顺序错误")

    def PVSS_n_Gen_Btn(self):
        if self.number_value is not None and self.threshold_value is not None and self.switch is True:
            # print(self.VSSfin.send(self.func_value_lst[0]))
            self.Block_value_lst[2], self.Random_value_lst[2], self.Block_time_lst[2] = self.PVSSnfin.send(
                self.func_value_lst[2])
            self.func_value_lst[2] += 1
            self.PVSSnRnumEntry.delete(0, "end")
            m = self.hash(str(self.Random_value_lst[2]).encode("UTF-8"))
            self.PVSSnRnumEntry.insert(0, m.hexdigest())
            self.PVSSnTMEMtr.configure(amountused=int(self.Block_time_lst[2]))
            self.PVSSnBlkEntry.delete(1.0, END)

            blkstr = ""
            for keys in self.Block_value_lst[2].keys():
                blkstr = blkstr + keys + ':\n' + str(self.Block_value_lst[2][keys]) + '\n'

            if self.simulvar.get() == 0:
                with open('bin/data/data_PVSSn.txt', 'r') as f:
                    lines = f.read()
                    first = lines.split('\n', 1)
                # 显示并发送
                if first[0] == '1':
                    blkstr = first[1]
                    with open('bin/data/data_PVSSn.txt', 'w') as f:
                        f.write('0\n' + blkstr)
                    hvalue = blkstr.split('\n')[-1]
                    self.PVSSnRnumEntry.delete(0, "end")
                    self.PVSSnRnumEntry.insert(0, hvalue)

                # 下面用网络写入他人文件
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    configuidip = configparser.ConfigParser()
                    configuidip.read("bin/settings/settings.ini")
                    port = 30000 + int(configuidip["section2"].get("uid"))
                    sock.bind((self.localip, port))
                    strips = configuidip["section3"]["ippool"]
                    lstips = list(strips.split('\n'))
                    idx = 1
                    for ip in lstips:
                        if (idx + 30000) == port:
                            idx += 1
                        sock.sendto(('PVSSn\n1\n' + blkstr + m.hexdigest()).encode(), (ip, idx + 20000))
                        # print(data.decode())
                        date = time.localtime()
                        strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                             date.tm_min, date.tm_sec)
                        self.transmsg.insert(END, "send PVSSn Msg. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                                         strdate))
                        idx += 1
                    sock.close()
                    pass

            self.PVSSnBlkEntry.insert(END, blkstr)
            self.switch = False
        elif self.number_value is None or self.threshold_value is None:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="信标块必要参数缺失。\n请前往首页填写对应参数并开启左下角“启动程序”按钮。",
                title="参数缺失")
        elif self.switch is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="生成信标块未验证。\n请首先点击“验证”按钮执行验证步骤。",
                title="顺序错误")

    def VRF_Gen_Btn(self):
        if self.number_value is not None and self.threshold_value is not None and self.switch is True:
            # print(self.VSSfin.send(self.func_value_lst[0]))
            self.Block_value_lst[3], self.Random_value_lst[3], self.Block_time_lst[3] = self.VRFfin.send(
                self.func_value_lst[3])
            self.func_value_lst[3] += 1
            self.VRFRnumEntry.delete(0, "end")
            m = self.hash(str(self.Random_value_lst[3]).encode("UTF-8"))
            self.VRFRnumEntry.insert(0, m.hexdigest())
            self.VRFTMEMtr.configure(amountused=int(self.Block_time_lst[3]))
            self.VRFBlkEntry.delete(1.0, END)

            blkstr = ""
            for keys in self.Block_value_lst[3].keys():
                blkstr = blkstr + keys + ':\n' + str(self.Block_value_lst[3][keys]) + '\n'

            if self.simulvar.get() == 0:
                with open('bin/data/data_VRF.txt', 'r') as f:
                    lines = f.read()
                    first = lines.split('\n', 1)
                # 显示并发送
                if first[0] == '1':
                    blkstr = first[1]
                    with open('bin/data/data_VRF.txt', 'w') as f:
                        f.write('0\n' + blkstr)
                    hvalue = blkstr.split('\n')[-1]
                    self.VRFRnumEntry.delete(0, "end")
                    self.VRFRnumEntry.insert(0, hvalue)

                # 下面用网络写入他人文件
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    configuidip = configparser.ConfigParser()
                    configuidip.read("bin/settings/settings.ini")
                    port = 30000 + int(configuidip["section2"].get("uid"))
                    sock.bind((self.localip, port))
                    strips = configuidip["section3"]["ippool"]
                    lstips = list(strips.split('\n'))
                    idx = 1
                    for ip in lstips:
                        if (idx + 30000) == port:
                            idx += 1
                        sock.sendto(('VRF\n1\n' + blkstr + m.hexdigest()).encode(), (ip, idx + 20000))
                        # print(data.decode())
                        date = time.localtime()
                        strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                             date.tm_min, date.tm_sec)
                        self.transmsg.insert(END, "send VRF Msg. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                                         strdate))
                        idx += 1
                    sock.close()
                    pass

            self.VRFBlkEntry.insert(END, blkstr)
            self.switch = False
        elif self.number_value is None or self.threshold_value is None:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="信标块必要参数缺失。\n请前往首页填写对应参数并开启左下角“启动程序”按钮。",
                title="参数缺失")
        elif self.switch is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="生成信标块未验证。\n请首先点击“验证”按钮执行验证步骤。",
                title="顺序错误")

    def VRF_n_Gen_Btn(self):
        if self.number_value is not None and self.threshold_value is not None and self.switch is True:
            # print(self.VSSfin.send(self.func_value_lst[0]))
            self.Block_value_lst[4], self.Random_value_lst[4], self.Block_time_lst[4] = self.VRFnfin.send(
                self.func_value_lst[4])
            self.func_value_lst[4] += 1
            self.VRFnRnumEntry.delete(0, "end")
            m = self.hash(str(self.Random_value_lst[4]).encode("UTF-8"))
            self.VRFnRnumEntry.insert(0, m.hexdigest())
            self.VRFnTMEMtr.configure(amountused=int(self.Block_time_lst[4]))
            self.VRFnBlkEntry.delete(1.0, END)

            blkstr = ""
            for keys in self.Block_value_lst[4].keys():
                blkstr = blkstr + keys + ':\n' + str(self.Block_value_lst[4][keys]) + '\n'

            if self.simulvar.get() == 0:
                with open('bin/data/data_VRFn.txt', 'r') as f:
                    lines = f.read()
                    first = lines.split('\n', 1)
                # 显示并发送
                if first[0] == '1':
                    blkstr = first[1]
                    with open('bin/data/data_VRFn.txt', 'w') as f:
                        f.write('0\n' + blkstr)

                    hvalue = blkstr.split('\n')[-1]
                    self.VRFnRnumEntry.delete(0, "end")
                    self.VRFnRnumEntry.insert(0, hvalue)
                # 下面用网络写入他人文件
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    configuidip = configparser.ConfigParser()
                    configuidip.read("bin/settings/settings.ini")
                    port = 30000 + int(configuidip["section2"].get("uid"))
                    sock.bind((self.localip, port))
                    strips = configuidip["section3"]["ippool"]
                    lstips = list(strips.split('\n'))
                    idx = 1
                    for ip in lstips:
                        if (idx + 30000) == port:
                            idx += 1
                        sock.sendto(('VRFn\n1\n' + blkstr + m.hexdigest()).encode(), (ip, idx + 20000))
                        # print(data.decode())
                        date = time.localtime()
                        strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                             date.tm_min, date.tm_sec)
                        self.transmsg.insert(END, "send VRFn Msg. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                                         strdate))
                        idx += 1
                    sock.close()
                    pass

            self.VRFnBlkEntry.insert(END, blkstr)
            self.switch = False
        elif self.number_value is None or self.threshold_value is None:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="信标块必要参数缺失。\n请前往首页填写对应参数并开启左下角“启动程序”按钮。",
                title="参数缺失")
        elif self.switch is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="生成信标块未验证。\n请首先点击“验证”按钮执行验证步骤。",
                title="顺序错误")

    def HERB_Gen_Btn(self):
        if self.number_value is not None and self.threshold_value is not None and self.switch is True:
            # print(self.VSSfin.send(self.func_value_lst[0]))
            date = time.localtime()
            self.HERBRnumEntry.delete(0, "end")
            m = self.hash(str(random.randint(1, 1024)).encode("UTF-8"))
            self.HERBRnumEntry.insert(0, m.hexdigest())
            self.HERBTMEMtr.configure(amountused=int(950) + random.randint(-100, 500))
            self.HERBBlkEntry.delete(1.0, END)
            strdate = "I[{}-{}-{}|{}:{}:{}]\n".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                      date.tm_min, date.tm_sec)

            blkstr = strdate + "Executed block\nmodule=state\nheight={}\nvalidTxs\nappHash=".format(self.HERBheight) + m.hexdigest()

            #self.HERBBlkEntry.insert(END, strdate)
            #self.HERBBlkEntry.insert(END, "Executed block\nmodule=state\nheight={}\nvalidTxs\nappHash=".format(self.HERBheight))
            #self.HERBBlkEntry.insert(END, m.hexdigest())

            if self.simulvar.get() == 0:
                with open('bin/data/data_FHE.txt', 'r') as f:
                    lines = f.read()
                    first = lines.split('\n', 1)
                # 显示并发送
                if first[0] == '1':
                    blkstr = first[1]
                    with open('bin/data/data_FHE.txt', 'w') as f:
                        f.write('0\n' + blkstr)
                    hvalue = blkstr.split('\n')[-1]
                    self.HERBRnumEntry.delete(0, "end")
                    self.HERBRnumEntry.insert(0, hvalue)

                # 下面用网络写入他人文件
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    configuidip = configparser.ConfigParser()
                    configuidip.read("bin/settings/settings.ini")
                    port = 30000 + int(configuidip["section2"].get("uid"))
                    sock.bind((self.localip, port))
                    strips = configuidip["section3"]["ippool"]
                    lstips = list(strips.split('\n'))
                    idx = 1
                    for ip in lstips:
                        if (idx + 30000) == port:
                            idx += 1
                        sock.sendto(('FHE\n1\n' + blkstr + '\n' + m.hexdigest()).encode(), (ip, idx + 20000))
                        # print(data.decode())
                        date = time.localtime()
                        strdate = "{}-{}-{} {}:{}:{}".format(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,
                                                             date.tm_min, date.tm_sec)
                        self.transmsg.insert(END, "send FHE Msg. to {0}:{1} at {2}\n".format(ip, idx + 20000,
                                                                                         strdate))
                        idx += 1
                    sock.close()
                    pass

            self.HERBBlkEntry.insert(END, blkstr)
            self.switch = False
            self.HERBheight += 1
        elif self.number_value is None or self.threshold_value is None:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="信标块必要参数缺失。\n请前往首页填写对应参数并开启左下角“启动程序”按钮。",
                title="参数缺失")
        elif self.switch is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="生成信标块未验证。\n请首先点击“验证”按钮执行验证步骤。",
                title="顺序错误")

    def verify_Block(self):
        if self.startgui is False:
            ttk.dialogs.dialogs.Messagebox.ok(
                message="未输入必要参数或点击启动程序按钮。\n点请输入必要参数并点击左下角“启动程序”",
                title="验证初始化失败", anchor=CENTER)
        elif self.number_value is not None and self.threshold_value is not None:
            self.switch = True
            configipveri = configparser.ConfigParser()
            configipveri.read("bin/settings/settings.ini")
            stripv = configipveri["section3"]["ippool"]
            lstipv = list(stripv.split('\n'))
            idx = 0
            errips = ""
            for ip in lstipv:

                pingbd = os.system("ping " + ip + " -n 1")
                if pingbd == 0:
                    idx += 1
                    continue
                else:
                    errips = errips + ip + ","
            time.sleep(random.randint(1, 3))
            print(len(lstipv))
            if (idx != len(lstipv)):
                ttk.dialogs.dialogs.Messagebox.ok(
                    message="IP地址：" + errips + "\n以上用户碎片验证及承诺失败或离线。\n点击“OK”及”下一轮生成“按钮，生成恢复块",
                    title="信标块验证", anchor=CENTER)
            else:
                ttk.dialogs.dialogs.Messagebox.ok(message="各用户碎片及承诺验证成功。\n点击”下一轮生成“按钮，生成信标块", title="信标块验证")


def get_theme():
    # proDir = os.path.split(os.path.realpath(__file__))[0]
    proDir = os.getcwd()
    settingPath = os.path.join(proDir, "bin/settings/settings.ini")
    conf = configparser.ConfigParser()
    conf.read(settingPath)
    name = conf.get("section1", "themes")
    return name

def init():
    app = ttk.Window(title="随机信标生成平台", themename=get_theme(), resizable=(True, True))
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(ico.img))
    tmp.close()
    app.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    RB_GUI(app)
    app.mainloop()

class server:
    def __init__(self, rootwindow):
        self.root_window = rootwindow
        self.root_window.title("网络传输接收端")
        self.root_window.geometry("100x100")
        #self.Messgebox = ttk.dialog.Messagebox

def recv():
    server_window = ttk.Window(title="网络传输接收端", themename=get_theme(), resizable=(True, True))
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(ico.img))
    tmp.close()
    server_window.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    server(server_window)
    server_window.Tk()
    """
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    configuidip = configparser.ConfigParser()
    configuidip.read("bin/settings/settings.ini")
    port = 20000 + int(configuidip["section2"].get("uid"))
    udpsocket.bind(('127.0.0.1', port))
    while True:
        recv_data = udpsocket.recv(1024)
        recv_data = recv_data.decode('utf-8')
        print('收到信息为:%s' % recv_data)
        ttk.dialogs.dialogs.Messagebox.ok(message='收到信息为:', title="通信测试")
    """

if __name__ == "__main__":
    """
    t1 = Thread(target=init)
    t2 = Thread(target=recv)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    
    t2.join()
    t1.join()
    """
    init()