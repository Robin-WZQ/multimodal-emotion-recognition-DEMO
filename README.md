# multimodel-emotion-recongnition-DEMO
A demo for multimodel emotion recongnition

*code is in the branch verion2.0*

## Overview

多模态情感识别demo version1.0. 


功能：

- 选择本地MP4视频
- 将视频处理为jpg、MP3格式，进行json、n_frame文件复写
- 利用模型进行情感输出
- 利用多线程进行任务并行处理

多模态情感识别demo version2.0.

功能：

- 利用多线程进一步解决并行运算问题
- 模型处理后可显示8种情感概率分布情况
- demo右上角显示侦测到的人脸信息
- 增加录制本地的视频（包含音频信息）并进行情感识别的功能

多模态情感识别demo version3.0.

功能：

- 增加实时情感识别模块
- 同时录音+录像+算法分析，目前每6秒显示一次

## Requirements

- python3.x
- pytorch (ver. 0.4+ required)
- ffmepg
- AVL 视频解码器
- opencv

## Usage

1. 修改opts.py文件中一处目录，为Emotion_REC所在绝对路径，已进行注释。
2. 下载ffmepg，[参考链接](https://blog.csdn.net/qq_39516859/article/details/81843419)，注意若安装后仍无显示，可把路径放到用户变量再试试
3. 安装AVL视频解码器，默认安装即可
4. python Emotion.py
![图片0](https://user-images.githubusercontent.com/60317828/134369543-15611f73-03a4-4a00-add4-b529955d35e6.jpg)
5.选择本地视频
6.录像检测
7.实时检测
![图片5](https://user-images.githubusercontent.com/60317828/134369696-cf82d10e-ee32-4eaa-8cbf-bb5c2a858d65.png)

## future Plan

- [x] 完成本地视频实时切片并进行情感识别
- [x] 利用软件进行音频和视频的录制
- [x] 完成打开摄像头进行实时情感识别
- [x] 进一步优化界面，实现上图中8个情感（上图为7个）的实时概率显示
- [x] 制作代码文件树，增强文件可读性

已完成！Done！
（congratulations！）
