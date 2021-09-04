"""
    使用python实现：读取USB摄像头的画面
"""
# 导入CV2模块
import cv2
import os
import datetime
import sys

from tools.processing import *

def read_usb_capture():
    # 选择摄像头的编号
    cap = cv2.VideoCapture(0)
    # 添加这句是可以用鼠标拖动弹出的窗体
    cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)

    # .mp4格式 , 25为 FPS 帧率， （640,480）为大小
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp.mp4', fourcc, 25, (640, 480))
    i=0
    while(cap.isOpened()):
        i+=1
        # 读取摄像头的画面
        ret, frame = cap.read()

        # 进行写操作
        out.write(frame)
        # 真实图
        cv2.imshow('real_img', frame)
        # 按下'esc'就退出
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # 释放画面
    cap.release()
    cv2.destroyAllWindows()

def video_record():
    os.system("start cmd_.vbe") #启动录音
    read_usb_capture() # 启动摄像
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # 当前的时间
    os.system("ffmpeg -i temp.mp4 -i temp.wav -strict -2 -f mp4 " + name + ".mp4")  # 利用ffmpeg 进行合并
    video2jpg(name+".mp4",name)
    video2mp3(name+".mp4",name)
    n_frame(name)
    os.remove('temp.mp4') # 删除中间视频文件
    os.remove("temp.wav") # 删除中间音频文件
    return name

if __name__=="__main__":
    name = video_record()
    print(name)