import torch.nn as nn
from models.vaanet import VAANet


def generate_model(opt):
    model = VAANet(
        snippet_duration=opt.snippet_duration,
        sample_size=opt.sample_size,
        n_classes=opt.n_classes,
        seq_len=opt.seq_len,
        audio_embed_size=opt.audio_embed_size,
        audio_n_segments=opt.audio_n_segments,
        pretrained_resnet101_path=opt.resnet101_pretrained,
    )
    model = model.cuda()

    return model, model.parameters()
