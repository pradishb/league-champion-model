'''Module to classify image using it's hash'''
import hashlib
import json
import os
from functools import lru_cache
from glob import glob

import cv2

from base.logger import log

__all__ = ['predict', 'train_using_directory']


def _hash_image(image):
    return hashlib.md5(image).hexdigest()


def _save_model(file_path, model):
    with open(file_path, 'w') as file_pointer:
        json.dump(model, file_pointer, indent=2)


@lru_cache()
def _get_model(file_path):
    if os.path.isfile(file_path):
        with open(file_path) as file_pointer:
            return json.load(file_pointer)
    return {}


def _train(image):
    background = cv2.resize(image.copy(), None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Enter the label and press enter. Esc to skip.', background)
    label = ''
    while True:
        key = cv2.waitKey()
        if key == 27:  # esc
            return None
        character = chr(key)
        if not character.isalnum():
            break
        label += character
    if label == '':
        return None
    return label


def train_using_directory(directory_path, model_save_path):
    '''Training using a directory of images'''
    model = {}
    for file_path in glob(os.path.join(directory_path, '*/*.png')):
        directory = os.path.split(file_path)[0]
        label = os.path.split(directory)[-1]
        image = cv2.imread(file_path)
        cv2.imshow('', cv2.resize(image, None, fx=20, fy=20, interpolation=0))
        cv2.waitKey()
        image_hash = _hash_image(image)
        model[image_hash] = label
    _save_model(model_save_path, model)


def predict(file_path, image, train=False, train_function=_train):
    '''Predicts the image's label using hash'''
    model = _get_model(file_path)
    image_hash = _hash_image(image.tobytes())
    if image_hash not in model:
        if train:
            label = train_function(image)
            if label is not None:
                model[image_hash] = label
                log(f'{label} written for hash {image_hash}.')
                _save_model(file_path, model)
                return label
        return None
    return model[image_hash]
