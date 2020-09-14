'''Test module'''

import unittest
from glob import glob
from pathlib import Path

import cv2

from base.decorators import timeit
from base.hashmodel import predict
from utils import crop

ROI = 331, 721, 15, 15


@timeit
def _predict(image):
    return predict('model/champion.json', image)


class TestCase(unittest.TestCase):
    '''Test class'''

    def test(self):
        '''Testing function'''
        for file_path in glob('test/*/*.png'):
            label = Path(file_path).parts[1]
            image = cv2.imread(file_path)
            image = crop(image, ROI)
            champion = _predict(image)
            print(file_path, label, champion)
            self.assertEqual(label, champion)


if __name__ == '__main__':
    unittest.main()
