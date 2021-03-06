#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/01/07 15:01
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : motion.py
# @Description : https://github.com/mmalekzadeh/motion-sense

import os
import numpy as np
import pandas as pd
from glob import glob
import argparse
from tqdm import tqdm


ACTIVITY_NAMES = ["dws", "ups", "sit", "std", "wlk", "jog"]
SAMPLE_WINDOW = 20


def label_activity(name):
    for i in range(len(ACTIVITY_NAMES)):
        if name.startswith(ACTIVITY_NAMES[i]):
            return i


def label_user(name):
    temp = name.split(".")[0]
    id = int(temp.split("_")[1])
    return id - 1


def down_sample(data, window_target):
    window_sample = window_target * 1.0 / SAMPLE_WINDOW
    result = []
    if window_sample.is_integer():
        window = int(window_sample)
        for i in range(0, len(data), window):
            slice = data[i : i + window, :]
            result.append(np.mean(slice, 0))
    else:
        window = int(window_sample)
        remainder = 0.0
        i = 0
        while 0 <= i + window + 1 < data.shape[0]:
            remainder += window_sample - window
            if remainder >= 1:
                remainder -= 1
                slice = data[i : i + window + 1, :]
                # print('i: %d, window: %d, start: %d, end: %d' % (i, window, start, end))
                result.append(np.mean(slice, 0))
                i += window + 1
            else:
                slice = data[i : i + window, :]
                result.append(np.mean(slice, 0))
                # print('i: %d, window: %d, start: %d, end: %d' % (i, window +  1, start, end))
                i += window
    return np.array(result)


def load_sensor_data(path, seq_len, target_window, gyro=False):
    data = []
    label = []
    n = 0

    for file in tqdm(sorted(glob(path + "/*"))):
        # Ignore labels
        label_act = 100
        # Ignore user data
        label_u = 100
        sensor = np.loadtxt(file, skiprows=1, delimiter=" ")
        if not gyro:
            sensor_down = down_sample(sensor[:, 1:4], target_window)
        else:
            sensor_down = down_sample(sensor[:, 4:], target_window)
        if sensor_down.shape[0] > seq_len:
            sensor_down = sensor_down[: sensor_down.shape[0] // seq_len * seq_len, :]
            sensor_down = sensor_down.reshape(
                sensor_down.shape[0] // seq_len, seq_len, sensor_down.shape[1]
            )
            sensor_label = np.ones((sensor_down.shape[0], sensor_down.shape[1], 1))
            sensor_label = np.concatenate(
                [sensor_label * label_act, sensor_label * label_u], 2
            )
            data.append(sensor_down)
            label.append(sensor_label)
        else:

            n += 1

    return data, label


def preprocess(path, path_save, version, target_window=50, seq_len=20):
    data_acc, label_acc = load_sensor_data(path, seq_len, target_window)
    data_gyro, label_gyro = load_sensor_data(path, seq_len, target_window, gyro=True)
    data = []
    label = []
    for i in range(len(data_acc)):
        len_min = min(data_acc[i].shape[0], data_gyro[i].shape[0])
        data.append(np.concatenate([data_acc[i][:len_min], data_gyro[i][:len_min]], 2))
        label.append(label_acc[i][:len_min, :, :])
    data = np.concatenate(data, 0)
    label = np.concatenate(label, 0)
    print("All data processed. Size: %d" % (data.shape[0]))

    os.makedirs(path_save, exist_ok=True)

    np.save(os.path.join(path_save, "data_" + version + ".npy"), np.array(data))
    np.save(os.path.join(path_save, "label_" + version + ".npy"), np.array(label))
    return data, label


if __name__ == "__main__":
    print("Processing input and generating BERT embeddings")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_folder",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    path_save = f"{'/'.join(os.path.realpath(__file__).split('/')[:-1])}/motion"
    version = r"20_120"

    data, label = preprocess(args.data_folder, path_save, version, seq_len=120)
