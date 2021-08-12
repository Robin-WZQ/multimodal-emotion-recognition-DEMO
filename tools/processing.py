#from __future__ import all_feature_names, print_function, division
import os
import sys
import subprocess
import string
from tools.ve8_json import json_processing

def class_process(video_file_path, dst_dir_path,name):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)
    if not os.path.exists(dst_dir_path+"/"+name):
        os.mkdir(dst_dir_path+"/"+name)
    if not os.path.exists(dst_dir_path+"/"+name+"/images/"):
        os.mkdir(dst_dir_path+"/"+name+"/images/")
    try:
        cmd = 'echo yes| ffmpeg -i \"{}\" -r 4 -vf scale=-1:240 \"{}/%06d.jpg\"'.format(video_file_path, dst_dir_path+"/"+name+"/images/")
    except:
        print("路径错误\n")
        return 0
    print(cmd)
    subprocess.call(cmd, shell=True)
    print('\n')

def video2jpg(path,name):
    '''将视频切为图片帧，jpg格式'''
    video_file_path = path # avi directory
    #dst_dir_path = "./data/"+ str(name)  # jpg directory
    dst_dir_path = "./data/Joy"  # jpg directory
    class_process(video_file_path, dst_dir_path,name)
    return 0

def class_process2(video_file_path, dst_dir_path,name):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)
    if not os.path.exists(dst_dir_path+"/"+name+"/mp3/"):
        os.mkdir(dst_dir_path+"/"+name+"/mp3/")
        os.mkdir(dst_dir_path+"/"+name+"/mp3/mp3/")
    #cmd = 'ffmpeg -i \"{}\" \"{}\"'.format(video_file_path, dst_dir_path+"/mp3/mp3/"+name+".mp3")
    cmd = 'echo yes| ffmpeg -i \"{}\" \"{}\"'.format(video_file_path, dst_dir_path+"/"+name+"/mp3/mp3/Joy.mp3")
    print(cmd)
    subprocess.call(cmd, shell=True)
    print('\n')

def video2mp3(path,name):
    '''提取视频音频信息，保存为mp3格式'''
    video_file_path = path
    #dst_dir_path = "./data/"+ str(name)
    dst_dir_path = "./data/Joy"
    class_process2(video_file_path, dst_dir_path,name)

def class_process3(video_dir_path):
    image_indices = []
    print('Processing: {}'.format(video_dir_path))
    for image_file_name in os.listdir(video_dir_path):
        if '.jpg' not in image_file_name or image_file_name[0]=='.':
            print(image_file_name)
            os.remove(os.path.join(video_dir_path, image_file_name))
            continue
        image_indices.append(int(image_file_name[:6]))

    # video level
    if len(image_indices) < 3:
        print("Insufficient image files: ", video_dir_path)
        print(len(image_indices))
        n_frames = 0
    else:
        image_indices.sort(reverse=True)
        n_frames = image_indices[0]
        print('N frames: ', n_frames)
    with open(os.path.join(video_dir_path, 'n_frames'), 'w+') as dst_file:
        dst_file.write(str(n_frames))

def n_frame(name):
    '''计算帧数共有多少张'''
    #dir_path = "data/"+name+"/images/"
    dir_path = "data/Joy"+"/"+name+"/images/"
    class_process3(dir_path)

def rewrite_josn(name):
    '''重写josn文件'''
    f = open("tools/annotations/ve8/testlist01.txt","w+")
    #f.write(name+"/images")
    f.write("Joy/images")

def video(path):
    name = path.split('/')
    name = name[-1].split(".")
    name = name[0]
    print(name)
    video2jpg(path,name)
    video2mp3(path,name)
    n_frame(name)
    rewrite_josn(name)
    json_processing()
    return name

#在这里给我路径
#video("D:/research/大创/project/emotion/多模态情感识别/Emotion_rec/4dac1f7abf38e1887e3cf70b1516beaa.mp4")