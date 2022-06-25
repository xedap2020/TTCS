import os

import cv2
from PySide2 import QtGui


def cv2_to_pyqt(img):
    image = QtGui.QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QtGui.QImage.Format_RGB888).rgbSwapped()
    return QtGui.QPixmap.fromImage(image)


class Image_Flipper:
    def __init__(self, file_path):
        self.edited_img = None
        self.file_path = file_path

        self.img = cv2.imread(self.file_path)

    def flip_vertical(self):
        self.edited_img = cv2.flip(self.img, 0)
        return cv2_to_pyqt(self.edited_img)

    def flip_horizon(self):
        self.edited_img = cv2.flip(self.img, 1)
        return cv2_to_pyqt(self.edited_img)

    def flip_both(self):
        self.edited_img = cv2.flip(self.img, -1)
        return cv2_to_pyqt(self.edited_img)

    def get_img(self):
        return cv2_to_pyqt(self.img)

    # save edited file to path
    def save_file(self, path, filename):
        if self.edited_img is None:
            return False
        cv2.imwrite(os.path.join(path, filename), self.edited_img)
        return True
