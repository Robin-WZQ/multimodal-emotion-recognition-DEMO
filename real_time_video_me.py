import cv2
import imutils
import time
import numpy as np
from PyQt5 import QtGui, QtWidgets
from keras.models import load_model
from keras.preprocessing.image import img_to_array

class Emotion_Rec:
    def __init__(self, model_path=None):

        # 载入数据和图片的参数
        detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'

        if model_path == None: # 若未指定路径，则使用默认模型
            emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
        else:
            emotion_model_path=model_path


        # 载入人脸检测模型
        self.face_detection = cv2.CascadeClassifier(detection_model_path)  # 级联分类器

        # 载入人脸表情识别模型
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        # 表情类别
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
                         "neutral"]


    def run(self, frame_in, canvas, label_face, label_result):
        # frame_in 摄像画面或图像
        # canvas 用于显示的背景图
        # label_face 用于人脸显示画面的label对象
        # label_result 用于显示结果的label对象


        # 调节画面大小
        frame = imutils.resize(frame_in, width=300)  # 缩放画面
        # frame = cv2.resize(frame, (300,300))  # 缩放画面
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转为灰度图

        # 检测人脸
        faces = self.face_detection.detectMultiScale(gray, scaleFactor=1.1,
                                                     minNeighbors=5, minSize=(30, 30),
                                                     flags=cv2.CASCADE_SCALE_IMAGE)

        self.preds = []  # 预测的结果
        label = None # 预测的标签
        (fX, fY, fW, fH) = None,None,None,None # 人脸位置
        if len(faces) > 0:
            # 选择检测到的ROI最大的人脸
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces

            # 从灰度图中提取感兴趣区域（ROI），将其大小转换为64*64 pixels，并为通过CNN的分类器准备ROI
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # 用模型预测各分类的概率
            self.preds = self.emotion_classifier.predict(roi)[0]
            # emotion_probability = np.max(preds)  # 最大的概率
            label = self.EMOTIONS[self.preds.argmax()]  # 选取最大概率的表情类



        frameClone = frame.copy()  # 复制画面
        # canvas = 255* np.ones((250, 300, 3), dtype="uint8")
        # canvas = cv2.imread('slice.png', flags=cv2.IMREAD_UNCHANGED)

        for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS,self.preds)):
            # 用于显示各类别概率
            text = "{}: {:.2f}%".format(emotion, prob * 100)

            # 绘制表情类和对应概率的条形图
            w = int(prob * 300)+7
            cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (224, 200, 130), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)


            # 圈出人脸区域并显示识别结果
            cv2.putText(frameClone, label, (fX, fY - 10),cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0), 1)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (255, 255, 0), 1)


        # 调整画面大小与界面相适应
        frameClone = cv2.resize(frameClone,(420,280))

        # 在Qt界面中显示人脸
        show = cv2.cvtColor(frameClone, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        QtWidgets.QApplication.processEvents()

        # 在显示结果的label中显示结果
        show = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        label_result.setPixmap(QtGui.QPixmap.fromImage(showImage))

        return(label)
