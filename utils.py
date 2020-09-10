'''Module for utility fucntions'''


def crop(img, rect):
    '''Crops an cv2 image using coordinate and size'''
    return img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
