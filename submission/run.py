# -*- coding: utf-8 -*-
"""
Main file for the second Machine Learning project:
    ### TODO ###

Authors: Kirill IVANOV, Matthias RAMIREZ, Nicolas TALABOT
"""

import argparse

from data_handler import load_images, create_labels, create_submission
from models import get_pretrained_models, train_and_get_models, get_predictions
from processing import extract_windows

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--train_model", help="train the whole model, do not reuse the pre-trained one",
                    action="store_true")
args = parser.parse_args()

# Load datasets, and create labels


data_dir = 'training/'
test_data_dir = 'test_set_images/'
model1, model2, model3 = train_and_get_models(data_dir) if args.train_model else get_pretrained_models()
get_predictions(model1, model2, model3, test_data_dir)