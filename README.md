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
![image-20210810080104442-16285536672481](https://user-images.githubusercontent.com/60317828/128882555-0140237b-62a7-42c5-868f-2ebb5ef8f487.png)
5.选择本地视频
![图片3](https://user-images.githubusercontent.com/60317828/128882596-c6638676-59fb-4753-8ce2-6bcec04a6cde.png)
6.视频播放+后台处理
![图片1](https://user-images.githubusercontent.com/60317828/129351022-94c60390-bf76-4c94-8ebc-855f53afc0f4.png)
7.结果显示
![图片2](https://user-images.githubusercontent.com/60317828/129351038-eea10c29-0ce9-4132-b01b-dca1df7d2b7c.png)

## future Plan

- [x] 完成本地视频实时切片并进行情感识别
- [x] 利用软件进行音频和视频的录制
- [x] 完成打开摄像头进行实时情感识别
- [x] 进一步优化界面，实现上图中8个情感（上图为7个）的实时概率显示
- [x] 制作代码文件树，增强文件可读性

已完成！Done！
