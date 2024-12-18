#!/bin/bash

curl -L -o ./readmission_dataset.zip https://www.kaggle.com/api/v1/datasets/download/vanpatangan/readmission-dataset

unzip ./readmission_dataset.zip

mkdir ./dataset/data

mv ./train_df.csv ./dataset/data/

rm sample_submission.csv test_df.csv ./readmission_dataset.zip