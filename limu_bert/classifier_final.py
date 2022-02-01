#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 11:20
# @Author  : Huatao
# @Email   : 735820057@qq.com
# @File    : classifier.py
# @Description :
import argparse
import os
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader
from sklearn.metrics.pairwise import cosine_similarity
from scipy import stats

import train
from config import load_dataset_label_names
from embedding import load_embedding_label
from models import fetch_classifier

from utils import (
    get_device,
    handle_argv,
    IMUDataset,
    load_classifier_config,
    prepare_classifier_dataset,
)


def classify_embeddings(
    args,
    data,
    labels,
    label_index,
    training_rate,
    label_rate,
    balance=False,
    method=None,
):
    train_cfg, model_cfg, dataset_cfg = load_classifier_config(args)
    label_names, label_num = load_dataset_label_names(dataset_cfg, label_index)

    data_test, label_test = prepare_classifier_dataset(
        data,
        labels,
        label_index=label_index,
        training_rate=training_rate,
        label_rate=label_rate,
        merge=model_cfg.seq_len,
        seed=train_cfg.seed,
        balance=balance,
    )

    data_set_test = IMUDataset(data_test, label_test)

    data_loader_test = DataLoader(
        data_set_test, shuffle=False, batch_size=train_cfg.batch_size
    )

    criterion = nn.CrossEntropyLoss()
    model = fetch_classifier(
        method, model_cfg, input=data_test.shape[-1], output=label_num
    )
    optimizer = torch.optim.Adam(
        params=model.parameters(), lr=train_cfg.lr
    )  # , weight_decay=0.95
    trainer = train.Trainer(
        train_cfg, model, optimizer, args.save_path, get_device(args.gpu)
    )

    def func_loss(model, batch):
        inputs, label = batch
        logits = model(inputs, True)
        loss = criterion(logits, label)
        return loss

    def func_forward(model, batch):
        inputs, label = batch
        logits = model(inputs, False)
        return logits, label

    def func_evaluate(label, predicts):
        final_preds = np.argmax(predicts.cpu().numpy(), 1)
        final_preds = final_preds.tolist()
        act_dict = {0: "DWS", 1: "UPS", 2: "SIT", 3: "STD", 4: "WLK", 5: "JOG"}

        output_labels = [act_dict[el] for el in final_preds]

        with open(args.output_predictions, "w") as out_file:
            for label in output_labels:
                out_file.write(label + "\n")

        print("Saved output as: ", args.output_predictions)

        return ""

    print("Evaluating input BERT embeddings...")
    label_estimate_test = trainer.run(
        func_forward,
        func_evaluate,
        data_loader_test,
        model_file=os.path.join(
            "saved", "classifier_base_gru_" + args.dataset + "_20_120", args.dataset
        ),
    )
    # label_estimate_test = trainer.run(func_forward, func_evaluate, data_loader_test,model_file='saved/classifier_base_gru_shoaib_20_120/shoaib')
    print(label_estimate_test)
    return label_test, label_estimate_test


if __name__ == "__main__":

    training_rate = 0.8  # unlabeled sample / total sample
    label_rate = 0.01  # labeled sample / unlabeled sample
    balance = True

    mode = "base"
    method = "gru"
    args = handle_argv("classifier_" + mode + "_" + method, "train.json", method)
    embedding, labels = load_embedding_label(
        args.model_file, args.dataset, args.dataset_version
    )
    label_test, label_estimate_test = classify_embeddings(
        args,
        embedding,
        labels,
        args.label_index,
        training_rate,
        label_rate,
        balance=balance,
        method=method,
    )

    label_names, label_num = load_dataset_label_names(
        args.dataset_cfg, args.label_index
    )
    # acc, matrix, f1 = stat_results(label_test, label_estimate_test)
    # matrix_norm = plot_matrix(matrix, label_names)
