#=========================
# author：Robin_WZQ
# date: 2021/8/12
# infor: code for test.return the probability of all kinds of emotions or the most possiable emotion.
#=========================

from core.utils import AverageMeter, process_data_item, run_model, calculate_accuracy

import time
import torch
import torch.nn as nn

import torch.nn.functional as F


def test(epoch, data_loader, model, criterion, opt, writer, optimizer):
    model.eval()


    for i, data_item in enumerate(data_loader):
        visual, target, audio, visualization_item, batch_size = process_data_item(opt, data_item)
        with torch.no_grad():
            predict = run_model(opt, [visual, target, audio], model, criterion, i)
        result = predict_num(predict)
        result2 = predict_prob(predict)
        return result,result2
    

def predict_num(data):
    '''
    返回概率最高的情感
    '''
    num = data.argmax()
    emotion = ['Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust']
    result = emotion[num]
    return result
    #for i in range(8):
    #    print("{0}:{1}".format(emotion[i],prob[0][i]))

def predict_prob(data):
    '''返回所有情感的概率，其加和为1'''
    prob =  F.softmax(data, dim=1)
    #print(prob[0])
    result = prob[0]
    return result
