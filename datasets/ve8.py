import torch
import torch.utils.data as data

from torchvision import get_image_backend

from PIL import Image

import json
import os
import functools
import librosa
import numpy as np


def load_value_file(file_path):
    with open(file_path, 'r') as input_file:
        return float(input_file.read().rstrip('\n\r'))


def load_annotation_data(data_file_path):
    with open(data_file_path, 'r') as data_file:
        return json.load(data_file)


def get_video_names_and_annotations(data, subset):
    video_names = []
    annotations = []
    for key, value in data['database'].items():
        if value['subset'] == subset:
            label = value['annotations']['label']
            video_names.append('{}/{}'.format(label, key))
            annotations.append(value['annotations'])
    return video_names, annotations


def get_class_labels(data):
    class_labels_map = {}
    index = 0
    for class_label in data['labels']:
        class_labels_map[class_label] = index
        index += 1
    return class_labels_map


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')


def accimage_loader(path):
    try:
        import accimage
        return accimage.Image(path)
    except IOError:
        # Potentially a decoding problem, fall back to PIL.Image
        return pil_loader(path)


def get_default_image_loader():
    if get_image_backend() == 'accimage':
        return accimage_loader
    else:
        return pil_loader


def video_loader(video_dir_path, frame_indices, image_loader):
    video = []
    for i in frame_indices:
        image_path = os.path.join(video_dir_path, '{:06d}.jpg'.format(i))
        assert os.path.exists(image_path), "image does not exists"
        video.append(image_loader(image_path))
    return video


def get_default_video_loader():
    image_loader = get_default_image_loader()
    return functools.partial(video_loader, image_loader=image_loader)


def preprocess_audio(audio_path):
    "Extract audio features from an audio file"
    y, sr = librosa.load(audio_path, sr=44100)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=32)
    return mfccs


class VE8Dataset(data.Dataset):
    def __init__(self,
                 video_path,
                 audio_path,
                 annotation_path,
                 subset,
                 fps=30,
                 spatial_transform=None,
                 temporal_transform=None,
                 target_transform=None,
                 get_loader=get_default_video_loader,
                 need_audio=True):
        self.data, self.class_names = make_dataset(
            video_root_path=video_path,
            annotation_path=annotation_path,
            audio_root_path=audio_path,
            subset=subset,
            fps=fps,
            need_audio=need_audio
        )
        self.spatial_transform = spatial_transform
        self.temporal_transform = temporal_transform
        self.target_transform = target_transform
        self.loader = get_loader()
        self.fps = fps
        self.ORIGINAL_FPS = 30
        self.need_audio = need_audio

    def __getitem__(self, index):
        data_item = self.data[index]
        video_path = data_item['video']
        frame_indices = data_item['frame_indices']
        snippets_frame_idx = self.temporal_transform(frame_indices)

        if self.need_audio:
            timeseries_length = 4096
            audio_path = data_item['audio']
            feature = preprocess_audio(audio_path).T
            k = timeseries_length // feature.shape[0] + 1
            feature = np.tile(feature, reps=(k, 1))
            audios = feature[:timeseries_length, :]
            audios = torch.FloatTensor(audios)
        else:
            audios = []

        snippets = []
        for snippet_frame_idx in snippets_frame_idx:
            snippet = self.loader(video_path, snippet_frame_idx)
            snippets.append(snippet)

        self.spatial_transform.randomize_parameters()
        snippets_transformed = []
        for snippet in snippets:
            snippet = [self.spatial_transform(img) for img in snippet]
            snippet = torch.stack(snippet, 0).permute(1, 0, 2, 3)
            snippets_transformed.append(snippet)
        snippets = snippets_transformed
        snippets = torch.stack(snippets, 0)

        target = self.target_transform(data_item)
        visualization_item = [data_item['video_id']]

        return snippets, target, audios, visualization_item

    def __len__(self):
        return len(self.data)


def make_dataset(video_root_path, annotation_path, audio_root_path, subset, fps=30, need_audio=True):
    data = load_annotation_data(annotation_path)
    video_names, annotations = get_video_names_and_annotations(data, subset)
    class_to_idx = get_class_labels(data)
    idx_to_class = {}
    for name, label in class_to_idx.items():
        idx_to_class[label] = name

    dataset = []
    for i in range(len(video_names)):
        '''if i % 100 == 0:
            print("Dataset loading [{}/{}]".format(i, len(video_names)))
            这里本来是有的
            '''
        video_name = video_names[i].split("/")
        video_name = video_name[1]
        video_path = os.path.join(video_root_path, video_name)
        video = video_names[i].split("/")
        video = video[1]
        if need_audio:
            audio_path = os.path.join(audio_root_path, "Joy" + '.mp3')
        else:
            audio_path = None

        assert os.path.exists(audio_path), audio_path
        assert os.path.exists(video_path), video_path

        n_frames_file_path = os.path.join(video_path, 'n_frames')
        n_frames = int(load_value_file(n_frames_file_path))
        if n_frames <= 0:
            print(video_path)
            continue
        '''print(audio_path)
        print(video_path)
        print(video_names[i])'''
        begin_t = 1
        end_t = n_frames
        sample = {
            'video': video_path,
            'segment': [begin_t, end_t],
            'n_frames': n_frames,
            'video_id': video_names[i].split('/')[1],
        }
        if need_audio: sample['audio'] = audio_path
        assert len(annotations) != 0
        sample['label'] = class_to_idx[annotations[i]['label']]
        ORIGINAL_FPS = 30
        step = ORIGINAL_FPS // fps

        sample['frame_indices'] = list(range(1, n_frames + 1, step))
        dataset.append(sample)
    return dataset, idx_to_class
