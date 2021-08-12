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

from train import train_epoch
from validation import val_epoch

from torch.utils.data import DataLoader
from torch.cuda import device_count
import torch
from test import test
from tools import processing

from tensorboardX import SummaryWriter


os.environ['CUDA_VISIBLE_DIVICES']='0'

result1 = None

def main(name):
    image_path = "data/Joy/"+name
    audio_path = "data/Joy/"+name+"/mp3/mp3"
    test_flag = True
    log_dir = "save_30.pth"

    opt = parse_opts()
    opt.device_ids = list(range(device_count()))
    local2global_path(opt)
    model, parameters = generate_model(opt)

    criterion = get_loss(opt)
    criterion = criterion.cuda()
    optimizer = get_optim(opt, parameters)

    writer = SummaryWriter(logdir=opt.log_path)

    #test
    if test_flag:
        spatial_transform = get_spatial_transform(opt, 'test')
        temporal_transform = TSN(seq_len=opt.seq_len, snippet_duration=opt.snippet_duration, center=False)
        target_transform = ClassLabel()
        validation_data = get_validation_set(image_path,audio_path,opt, spatial_transform, temporal_transform, target_transform)
        val_loader = get_data_loader(opt, validation_data, shuffle=False)

        checkpoint = torch.load(log_dir,map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        result = test(1, val_loader, model, criterion, opt, writer, optimizer)
        return result

    writer.close()


def output_result(path):
    name = processing.video(path)

def results(name):
    result1 = main(name)
    return result1

#这里给我路径,只要调用这个函数就可以了，返回的是情感结果
#output_result("D:/research/大创/project/emotion/多模态情感识别/Emotion_rec/4dac1f7abf38e1887e3cf70b1516beaa.mp4")
