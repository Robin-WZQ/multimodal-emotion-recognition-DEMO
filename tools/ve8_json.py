import os
import sys
import json
import pandas as pd
import random


def load_labels(label_csv_path):
    """
    :return: ['Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']
    """
    data = pd.read_csv(label_csv_path, delimiter=' ', header=None)
    labels = []
    for i in range(data.shape[0]):
        labels.append(data.iloc[i, 1])
    return labels


def convert_csv_to_dict(csv_path, subset):
    """
    :param csv_path:
    :param subset: str
    :return:
    """
    data = pd.read_csv(csv_path, delimiter=' ', header=None)
    keys = []
    key_labels = []
    for i in range(data.shape[0]):
        row = data.iloc[i, :]
        slash_rows = data.iloc[i, 0].split('/')
        class_name = slash_rows[0]
        basename = slash_rows[1]

        keys.append(basename)
        key_labels.append(class_name)

    database = {}
    for i in range(len(keys)):
        key = keys[i]
        database[key] = {}
        database[key]['subset'] = subset

        label = key_labels[i]
        database[key]['annotations'] = {'label': label}

    print(database)
    return database


def convert_ve8_csv_to_json(label_csv_path, train_csv_path, val_csv_path, dst_json_path):
    labels = load_labels(label_csv_path)
    train_database = convert_csv_to_dict(train_csv_path, 'training')
    val_database = convert_csv_to_dict(val_csv_path, 'validation')

    dst_data = {}
    dst_data['labels'] = labels
    dst_data['database'] = {}
    dst_data['database'].update(train_database)
    dst_data['database'].update(val_database)
    print(dst_data)

    with open(dst_json_path, 'w') as dst_file:
        json.dump(dst_data, dst_file)


def json_processing():
    csv_dir_path = os.getcwd()
    csv_dir_path = os.path.join(csv_dir_path, "tools/annotations/ve8")
    for split_index in range(1, 2):
        label_csv_path = os.path.join(csv_dir_path, 'classInd.txt')
        train_csv_path = os.path.join(csv_dir_path, 'trainlist0{}.txt'.format(split_index))
        val_csv_path = os.path.join(csv_dir_path, 'testlist0{}.txt'.format(split_index))
        dst_json_path = os.path.join(csv_dir_path, 've8_0{}.json'.format(split_index))
        convert_ve8_csv_to_json(label_csv_path, train_csv_path, val_csv_path, dst_json_path)
