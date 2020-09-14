'''Main module'''
import hashlib
import json
import os
from glob import glob

import cv2

from utils import crop

ROI = 331, 721, 15, 15


def _hash_image(image):
    return hashlib.md5(image).hexdigest()


def _save_model(file_path, model):
    with open(file_path, 'w') as file_pointer:
        json.dump(model, file_pointer, indent=2)


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


def main():
    '''Training using a directory of images'''
    os.makedirs('model', exist_ok=True)
    model = {}
    for file_path in glob(os.path.join('train', '*', '*.png')):
        directory = os.path.split(file_path)[0]
        label = os.path.split(directory)[-1]
        image = cv2.imread(file_path)
        image = crop(image, ROI)
        cv2.imshow('', cv2.resize(image, None, fx=20, fy=20, interpolation=0))
        cv2.waitKey()
        image_hash = _hash_image(image.tobytes())
        model[image_hash] = label
    _save_model('model/champion.json', model)


if __name__ == '__main__':
    main()
