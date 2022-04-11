# multimodel-emotion-recongnition-DEMO
A demo for multimodel emotion recongnition

*code is in the branch verion3.0*

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
- pyaudio等
- opencv

## Usage
--------------------------------------------2022.4.11更新-------------------------------------------------
1. 下载ffmepg，[参考链接](https://blog.csdn.net/qq_39516859/article/details/81843419)，注意若安装后仍无显示，可把路径放到用户变量再试试
2. 由于github上的代码有些小问题，我将所有文件，包含所有预训练文件等，都打包到了百度云：[HERE](https://pan.baidu.com/s/1rkLb3C_gqcaiC_4S2y6kxA)，提取码：3oqv。其中我写了一个使用说明文档，理论上讲只要照做就能正常运行（我在另一台电脑上实验成功了）。
3. python Emotion.py
![图片0](https://user-images.githubusercontent.com/60317828/134369543-15611f73-03a4-4a00-add4-b529955d35e6.jpg)
4.选择本地视频
![图片1](https://user-images.githubusercontent.com/60317828/134369887-3e9212ae-723f-41d8-a1c9-ebef7874c65b.png)
![图片2](https://user-images.githubusercontent.com/60317828/134369921-947a7797-f454-4484-b218-cca9216842ee.png)
5.录像检测
![图片3](https://user-images.githubusercontent.com/60317828/134370931-04773e1b-aad5-4335-a7df-5ee841b535cc.jpg)
![图片4](https://user-images.githubusercontent.com/60317828/134371121-57d12ea4-d492-4975-b871-b7116487b5bd.png)
6.实时检测
![图片5](https://user-images.githubusercontent.com/60317828/134369696-cf82d10e-ee32-4eaa-8cbf-bb5c2a858d65.png)

## future Plan

- [x] 完成本地视频实时切片并进行情感识别
- [x] 利用软件进行音频和视频的录制
- [x] 完成打开摄像头进行实时情感识别
- [x] 进一步优化界面，实现上图中8个情感（上图为7个）的实时概率显示
- [x] 制作代码文件树，增强文件可读性

已完成！Done！
（congratulations！）

## 补充说明

这个是我们大二大创的一部分成果，老师当时是让我们做一个基于多模态的可视化工具出来。然而，上网找遍了发现原来模型目前都是在数据集上跑，很少有民间的这种针对多模态的可视化界面（大公司不知道有没有），所以我们就花了大概3个月时间做了一个这个界面出来，效果就是上面展示的那样。整体就是摄像头录视频，然后调电脑音频录音，将这两个拼到一起输到网络，输出情感分类结果。但是毕竟大二代码能力有限，所以整体虽然能用但是属于那种小心使用的状态。21年我们大创结题了可能以后也不会继续维护了，我看挺多人star，还有一些人发邮件来求助，我们也感到十分意外和惊喜。所以也欢迎各位在我们的基础上进行各种修改，感激不尽！！！
