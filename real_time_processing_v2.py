from tools.processing import *

import pyaudio
import cv2
import datetime
from threading import Thread

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from threading import Thread
import threading

from torch.cuda.memory import reset_accumulated_memory_stats
from opts import parse_opts

from core.model import generate_model
from core.loss import get_loss
from core.optimizer import get_optim
from core.utils import local2global_path, get_spatial_transform
from core.dataset import get_training_set, get_validation_set, get_test_set, get_data_loader

from transforms.temporal import TSN
from transforms.target import ClassLabel

from torch.cuda import device_count
import torch
from test import test

from tools.picture_capture import capture
from tools.write_wav import record

from tensorboardX import SummaryWriter


os.environ['CUDA_VISIBLE_DIVICES']='0'


def real_time_processing():
    name,images_path,image_path,audio_path,log_dir,opt,opt.device_ids,model,criterion,optimizer,writer=init()
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
        #==================================================
        #test
        result,result2 = real(opt, model, criterion, writer,image_path, optimizer,audio_path,i,log_dir)
        print(result,result2)
        writer.close()
        #==================================================
        if i==3:
            break
    
    my_camera.release()
    cv2.destroyAllWindows()
    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

def init() -> str:
    print("正在初始化相关配置")    
    name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
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
    #audio_path = dst_dir_path+"/"+name+"/mp3/mp3/"

    n_frame_fix(name)
    rewrite_josn(name)
    json_processing()
    image_path = "data/Joy/"+name
    audio_path = "data/Joy/"+name+"/mp3/mp3/"
    log_dir = "save_30.pth"

    opt = parse_opts()
    opt.device_ids = list(range(device_count()))
    local2global_path(opt)
    model, parameters = generate_model(opt)

    criterion = get_loss(opt)
    criterion = criterion.cuda()
    optimizer = get_optim(opt, parameters)

    writer = SummaryWriter(logdir=opt.log_path)
    print("配置结束")
    return name,images_path,image_path,audio_path,log_dir,model,criterion,optimizer,writer

def real(opt, model, criterion, writer,image_path, optimizer,audio_path,i,log_dir):
    spatial_transform = get_spatial_transform(opt, 'test')
    temporal_transform = TSN(seq_len=opt.seq_len, snippet_duration=opt.snippet_duration, center=False)
    target_transform = ClassLabel()
    validation_data = get_validation_set(image_path,audio_path,opt, spatial_transform, temporal_transform, target_transform,i)
    val_loader = get_data_loader(opt, validation_data, shuffle=False)

    checkpoint = torch.load(log_dir,map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    result,result2 = test(1, val_loader, model, criterion, opt, writer, optimizer)
    return result,result2

if __name__ == "__main__":
    real_time_processing()