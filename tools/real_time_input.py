from threading import Thread

from picture_capture import capture
from write_wav import record

import pyaudio
import cv2
import time
import os

def real_time_input(name):
    dst_dir_path = 'data/Joy'
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)
    if not os.path.exists(dst_dir_path+"/"+name):
        os.mkdir(dst_dir_path+"/"+name)
    if not os.path.exists(dst_dir_path+"/"+name+"/images/"):
        os.mkdir(dst_dir_path+"/"+name+"/images/")
    if not os.path.exists(dst_dir_path+"/"+name+"/mp3/"):
        os.mkdir(dst_dir_path+"/"+name+"/mp3/")
        os.mkdir(dst_dir_path+"/"+name+"/mp3/mp3/")
    images_path = dst_dir_path+"/"+name+"/images/"
    audio_path = dst_dir_path+"/"+name+"/mp3/mp3/"

    # 创建PyAudio对象
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    # 录音时间
    RECORD_SECONDS = 2

    my_camera = cv2.VideoCapture(0)
    i=0
    j=-56

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
    while True:
        tsk = []
        i+=1
        j+=56
        t1 = Thread(target=record,args=(p,stream,i,CHUNK,FORMAT,CHANNELS,RECORD_SECONDS,RATE,audio_path,))
        t2 = Thread(target=capture,args=(i,j,my_camera,images_path,))
        tsk.append(t1)
        tsk.append(t2)
        t2.start()
        t1.start()
        for tt in tsk:
            tt.join()
        if i==10:
            break
    
    my_camera.release()
    cv2.destroyAllWindows()
    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

if __name__ == "__main__":
    name = time.time()
    name = str(name).split(".")[0]

    real_time_input(name)
