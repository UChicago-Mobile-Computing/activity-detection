"""

Write a script that takes in labeled data in data/train/ and
outputs the validation dataset in data/validation/.

You may also want to create a modified data/train/ folder
(or a modified copy of the folder) that does not include your validation
data. Be sure to document how to run this script here or in your report.

Your validation set should contain at least 8 samples of IMU data per
activity, with each sample being 12+ seconds long.

"""
import os
import shutil
import pandas as pd

# Creating the validation directory
parent_dir = 'data/'
val = 'validation/'
val_dir = os.path.join(parent_dir, val)
print(val_dir)
os.mkdir(val_dir)

# Copying train so we can have a full training set and then also the training
# and validation sets. Directories will be named train (for without the 
# validation set) and train_full (for the full training data)
train_path = os.path.join(parent_dir, "train/")
train_partial_path = train_path
train_full_path = shutil.copytree(train_path, os.path.join(parent_dir, 'train_full/'))

# Creating validation set for each mode
modes = ['DWS', 'JOG', 'SIT', 'STD', 'UPS', 'WLK']

for mode in modes:
    print(mode)
    samples_taken = 0
    i = 0
    num = ''
    while samples_taken < 8:
        if i < 10:
            num = '0' + str(i)
        else:
            num = str(i)
        file_name = mode + '_' + num + '.txt'
        file_path = train_path + mode + '/' + file_name
        df = pd.read_csv(file_path, delim_whitespace=True)
        new_file_path = os.path.join(val_dir, file_name)
        for j in df.time:
            if j == 12000:
                os.rename(file_path, new_file_path)
                samples_taken += 1
        i += 1
