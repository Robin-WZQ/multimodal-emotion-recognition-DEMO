from datasets.ve8 import VE8Dataset
from torch.utils.data import DataLoader


def get_ve8(image_path,audio_path,opt, subset, transforms):
    spatial_transform, temporal_transform, target_transform = transforms
    return VE8Dataset(image_path,
                      audio_path,
                      opt.annotation_path,
                      subset,
                      opt.fps,
                      spatial_transform,
                      temporal_transform,
                      target_transform,
                      need_audio=True)


def get_training_set(opt, spatial_transform, temporal_transform, target_transform):
    if opt.dataset == 've8':
        transforms = [spatial_transform, temporal_transform, target_transform]
        return get_ve8(opt, 'training', transforms)
    else:
        raise Exception

#新增了path在输入
def get_validation_set(image_path,audio_path,opt, spatial_transform, temporal_transform, target_transform):
    if opt.dataset == 've8':
        transforms = [spatial_transform, temporal_transform, target_transform]
        return get_ve8(image_path,audio_path , opt, 'validation', transforms)
    else:
        raise Exception


def get_test_set(opt, spatial_transform, temporal_transform, target_transform):
    if opt.dataset == 've8':
        transforms = [spatial_transform, temporal_transform, target_transform]
        return get_ve8(opt, 'validation', transforms)
    else:
        raise Exception


def get_data_loader(opt, dataset, shuffle, batch_size=0):
    batch_size = opt.batch_size if batch_size == 0 else batch_size
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=opt.n_threads,
        pin_memory=True,
        drop_last=opt.dl
    )
