# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Emotion.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
from threading import Thread  # 导入线程函数
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from torch._C import R

#from real_time_video_me import Emotion_Rec
from os import getcwd
import numpy as np
import cv2
import time
import logging
from base64 import b64decode
from os import remove
from slice_png import img as bgImg
import image1_rc
from PyQt5.QtWidgets import QApplication,QMainWindow;
from PyQt5.QtMultimediaWidgets import QVideoWidget
from myVideoWidget import myVideoWidget
import dlib

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from main import *
from face_detect import show_face
import time
class Ui_MainWindow(QMainWindow):
    def __init__(self,MainWindow):
        super(Ui_MainWindow, self).__init__()
        self.path = getcwd()
        self.timer_camera = QtCore.QTimer(self) # 定时器

        self.setupUi(MainWindow)
        self.retranslateUi(MainWindow)
        self.slot_init() #槽函数设置

        # 设置界面动画
        gif = QMovie(':/newPrefix/images_test/scan.gif')
        self.label_face.setMovie(gif)
        gif.start()

        self.cap = cv2.VideoCapture() # 屏幕画面对象
        self.CAM_NUM = 0 # 摄像头标号
        self.model_path = None # 模型路径
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)  # 视频播放输出的widget，就是上面定义的

    #    self.player.positionChanged.connect(self.changeSlide)  #进度条
        self.timePlay = ' '

        # 配置日志文件和日志级别
        """currentTime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        logging.basicConfig(filename=currentTime + '_logger.log', level=logging.INFO)"""
        #不通"""currentTime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())logging.basicConfig(filename=currentTime + '_logger.log', level=logging.INFO)"""
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1544, 849)
        MainWindow.setMinimumSize(1544, 849)
        MainWindow.setMaximumSize(1544, 849)
        MainWindow.setAutoFillBackground(False)

        MainWindow.setStyleSheet("#MainWindow{border-image: url(:/newPrefix/images_test/background.png);}\n"
                                 "\n"
                                 "#QInputDialog{border-image: url(:/newPrefix/images_test/light.png);}\n"
                                 "\n"
                                 "QMenuBar{border-color:transparent;}\n"
                                 "QToolButton[objectName=pushButton_doIt]{\n"
                                 "border:5px;}\n"
                                 "\n"
                                 "QToolButton[objectName=pushButton_doIt]:hover {\n"
                                 "image:url(:/newPrefix/images_test/run_hover.png);}\n"
                                 "\n"
                                 "QToolButton[objectName=pushButton_doIt]:pressed {\n"
                                 "image:url(:/newPrefix/images_test/run_pressed.png);}\n"
                                 "\n"
                                 "QScrollBar:vertical{\n"
                                 "background:transparent;\n"
                                 "padding:2px;\n"
                                 "border-radius:8px;\n"
                                 "max-width:14px;}\n"
                                 "\n"
                                 "QScrollBar::handle:vertical{\n"
                                 "background:#9acd32;\n"
                                 "min-height:50px;\n"
                                 "border-radius:8px;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::handle:vertical:hover{\n"
                                 "background:#9eb764;}\n"
                                 "\n"
                                 "QScrollBar::handle:vertical:pressed{\n"
                                 "background:#9eb764;\n"
                                 "}\n"
                                 "QScrollBar::add-page:vertical{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "                               \n"
                                 "QScrollBar::sub-page:vertical{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::add-line:vertical{\n"
                                 "background:none;}\n"
                                 "                                 \n"
                                 "QScrollBar::sub-line:vertical{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "QScrollArea{\n"
                                 "border:0px;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar:horizontal{\n"
                                 "background:transparent;\n"
                                 "padding:0px;\n"
                                 "border-radius:6px;\n"
                                 "max-height:4px;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::handle:horizontal{\n"
                                 "background:#9acd32;\n"
                                 "min-width:50px;\n"
                                 "border-radius:6px;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::handle:horizontal:hover{\n"
                                 "background:#9eb764;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::handle:horizontal:pressed{\n"
                                 "background:#9eb764;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::add-page:horizontal{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::sub-page:horizontal{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "QScrollBar::add-line:horizontal{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "\n"
                                 "QScrollBar::sub-line:horizontal{\n"
                                 "background:none;\n"
                                 "}\n"
                                 "QToolButton::hover{\n"
                                 "border:0px;\n"
                                 "} ")


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.wgt_video = myVideoWidget(self.centralwidget)
        self.wgt_video.setObjectName("centralwidget")
        self.wgt_video.setGeometry(QtCore.QRect(10, 10, 1051, 631))
        #self.wgt_video.setAlignment(QtCore.Qt.AlignCenter)
        self.wgt_video.setObjectName("wgt_video")

        self.label_face = QtWidgets.QLabel(self.centralwidget)
        self.label_face.setGeometry(QtCore.QRect(1100, 10, 401, 301))
        self.label_face.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label_face.setFont(font)
        self.label_face.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_face.setStyleSheet("border-image: url(:/newPrefix/images_test/scan.gif);")
        self.label_face.setObjectName("label_face")

        self.pushButton_openfile = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_openfile.setGeometry(QtCore.QRect(240, 740, 113, 51))
        self.pushButton_openfile.setObjectName("pushButton_openfile")

        self.pushButton_play = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_play.setGeometry(QtCore.QRect(400, 740, 113, 51))
        self.pushButton_play.setObjectName("pushButton_play")

        self.pushButton_pause = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pause.setGeometry(QtCore.QRect(560, 740, 113, 51))
        self.pushButton_pause.setObjectName("pushButton_pause")

        self.pushButton_close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_close.setGeometry(QtCore.QRect(720, 740, 113, 51))
        self.pushButton_close.setObjectName("pushButton_close")

        #后加的
        #self.pushButton_op
        self.pushButton_op = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_op.setGeometry(QtCore.QRect(880, 740, 113, 51))
        self.pushButton_op.setObjectName("实时分析")


        self.label_scanResult = QtWidgets.QLabel(self.centralwidget)
        self.label_scanResult.setGeometry(QtCore.QRect(1210, 720, 281, 31))
        self.label_scanResult.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_scanResult.setFont(font)
        #self.label_scanResult.setStyleSheet("color: rgb(0, 189, 189);")
        self.label_scanResult.setObjectName("label_scanResult")

        #self.sld_video = QtWidgets.QSlider(self.centralwidget)
        #self.sld_video.setGeometry(QtCore.QRect(170, 680, 731, 31))
        #self.sld_video.setMaximum(100)
        #self.sld_video.setOrientation(QtCore.Qt.Horizontal)
        #self.sld_video.setObjectName("sld_video")

        self.lab_video = QtWidgets.QLabel(self.centralwidget)
        self.lab_video.setGeometry(QtCore.QRect(900, 650, 81, 31))
        self.lab_video.setObjectName("lab_video")
        #self.sld_video.setObjectName("sld_video")

        self.label_outputResult = QtWidgets.QLabel(self.centralwidget)
        self.label_outputResult.setGeometry(QtCore.QRect(1100, 360, 401, 281))
        self.label_outputResult.setText("")
        self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/images_test/ini.png);")
        self.label_outputResult.setObjectName("label_outputResult")

        self.pushButton_play.setEnabled(False)
        self.pushButton_pause.setEnabled(False)
        self.pushButton_close.setEnabled(True)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1140, 720, 71, 31))
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")


        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(1090, 330, 421, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(1100, 670, 411, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1544, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Emotion Recongnition v1.0"))
        self.pushButton_openfile.setText(_translate("MainWindow", "选择文件"))
        self.pushButton_play.setText(_translate("MainWindow", "播放"))
        self.pushButton_op.setText(_translate("MainWindow", "实时"))#自己加的
        self.pushButton_pause.setText(_translate("MainWindow", "暂停"))
        self.pushButton_close.setText(_translate("MainWindow", "关闭"))
        self.label.setText(_translate("MainWindow", "结果"))
        self.label_scanResult.setText(_translate("MainWindow", ""))
    #    self.lab_video.setText(_translate("MainWindow", "0%"))
        self.label_face.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))

    #定义槽函数
    def slot_init(self):
        self.pushButton_openfile.clicked.connect(self.button_openfile)
        #self.pushButton_openfile.clicked.connect(self.button_open_camera_click)#原来有
        self.pushButton_op.clicked.connect(self.button_open_camera_click)#后加的
        self.pushButton_play.clicked.connect(self.button_play)
        #self.pushButton_play.clicked.connect(self.button_open_camera_click)
        self.pushButton_pause.clicked.connect(self.button_pause)
        self.pushButton_close.clicked.connect(QCoreApplication.quit)
        self.timer_camera.timeout.connect(self.show_camera)

    def main_function(self,x):
        xx=str(x)
        y=xx[27:-2]
        y=str(y)
        print(y)
        tsk = []
        show_face(y)
        self.label_face.setStyleSheet("border-image: url(detected.png);")
        #gif.stop()
        #self.label_face.clear()
        name = y.split('/')
        name = name[-1].split(".")
        name = name[0]

        self.player.setMedia(QMediaContent(x)) 
        #t3 = Thread()
        t1 = Thread(target=output_result, args=(y,))
        tsk.append(t1)
        #tsk.append(t3)
        t2 = Thread(target=self.player.play())
        tsk.append(t2)

        t1.start()
        t2.start()
        #t3.start()
        for tt in tsk:
            tt.join()
        #以上使用了多线程，并且设置为子线程结束后主线程才进行
        result,preds = results(name)
        print("Emotion:",result)

        ############################################################################
        ####################
        tmp = open('slice.png', 'wb')
        tmp.write(b64decode(bgImg))
        tmp.close()
        canvas = cv2.imread('slice.png')  # 用于数据显示的背景图片

        EMOTIONS = ["Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]

        label = None  # 预测的标签
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            # 用于显示各类别概率
            text = "{}: {:.2f}%".format(emotion, prob * 100)
            # 绘制表情类和对应概率的条形图
            w = int(prob * 300) + 7
            cv2.rectangle(canvas, (7, (i * 30) + 5), (w, (i * 30) + 30), (224, 200, 130), -1)
            cv2.putText(canvas, text, (10, (i * 30) + 23), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)
        # 在显示结果的label中显示结果
        cv2.imwrite('new.png',canvas)
        self.label_outputResult.clear()
        self.label_outputResult.setStyleSheet("border-image: url(new.png);")
        #*************************************************
        preds = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3]  # 预测的结果
        ###############################################################################################

        #if self.player.duration() > 0:  # 开始播放后才允许打开摄像头
        #self.button_open_camera_click()
        self.label_scanResult.setText(result)


    #选择文件路径
    def button_openfile(self):
        #后加的，从实时转到播放

        self.timer_camera.stop()
 
        self.cap.release()
        self.label_face.clear()
        #gif = QMovie(':/newPrefix/images_test/scan.gif')
        #self.label_face.setMovie(gif)
        #gif.start()


        self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/images_test/ini.png);")
        self.label_scanResult.setText('process...')
        #

        self.pushButton_play.setEnabled(False)
        self.pushButton_pause.setEnabled(True)
        self.pushButton_close.setEnabled(True)
        
        x=QtWidgets.QFileDialog.getOpenFileUrl()[0]
        t1 = Thread(target=self.main_function,args=(x,))
        t1.start()
        
 
   
    #播放视频
    def button_play(self):
        self.pushButton_play.setEnabled(False)
        self.pushButton_pause.setEnabled(True)
        self.pushButton_close.setEnabled(False)
        self.player.setVideoOutput(self.wgt_video)
        self.player.play()
        #if self.player.duration() > 0:  # 开始播放后才允许打开摄像头
        #    self.button_open_camera_click()
            #QApplication.processEvents()

    #暂停播放且停止录像
    def button_pause(self):
        self.pushButton_play.setEnabled(True)
        self.pushButton_pause.setEnabled(False)
        self.pushButton_close.setEnabled(True)
        if self.player.duration() > 0:  # 开始播放后才允许暂停
            self.timer_camera.stop()
            self.cap.release()  # 停止摄像
            self.player.pause()

    #进度条
    #def changeSlide(self,position):
    #    self.vidoeLength = self.player.duration()+0.1
    #    self.sld_video.setValue(round((position/self.vidoeLength)*100))
    #    self.lab_video.setText(str(round((position/self.vidoeLength)*100,2))+'%')
    #    self.timePlay = str(round((position/self.vidoeLength)*100,2))+'%'
    

    #打开摄像头  实时分析
    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False: # 检查定时状态
            flag = self.cap.open(self.CAM_NUM) # 检查相机状态
            if flag == False: # 相机打开失败提示
                msg = QtWidgets.QMessageBox.warning(self.centralwidget, u"Warning",
                                                    u"请检测相机与电脑是否连接正确！ ",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                # 准备运行识别程序
                QtWidgets.QApplication.processEvents()
                self.label_face.setText('正在启动识别系统...\n\nleading')
                # 新建对象
                #self.emotion_model = Emotion_Rec(self.model_path)
                QtWidgets.QApplication.processEvents()
                # 打开定时器
                self.timer_camera.start(30)
        else:
            # 定时器未开启，界面回复初始状态
            self.timer_camera.stop()
            self.cap.release()
            self.label_face.clear()
            gif = QMovie(':/newPrefix/images_test/scan.gif')
            self.label_face.setMovie(gif)
            gif.start()
            self.label_outputResult.clear()
            self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/images_test/ini.png);")

            self.label_scanResult.setText('None')

    def show_camera(self):
        # 定时器槽函数，每隔一段时间执行
        flag, self.image = self.cap.read() # 获取画面
        self.image=cv2.flip(self.image, 1) # 左右翻转

        tmp = open('slice.png', 'wb')
        tmp.write(b64decode(bgImg))
        tmp.close()
        canvas = cv2.imread('slice.png') # 用于数据显示的背景图片
        remove('slice.png')

        # 使用模型预测
        #result = self.emotion_model.run(self.image, canvas, self.label_face, self.label_outputResult)
        #self.logFile = '[' + self.timePlay + ']' + str(self.emotion_model.preds)
        #logging.info(self.logFile)
        # 在界面显示结果
        #self.label_scanResult.setText(result)


if __name__ == "__main__":  
    app = QApplication(sys.argv)
    form = QMainWindow()
    w = Ui_MainWindow(form)
    form.show()

    #w.setupUi(form)

    sys.exit(app.exec_())
