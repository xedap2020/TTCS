# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox

from image_flipper import Image_Flipper


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.te_filename_export = None
        self.te_export_folder = None
        self.lbl_edited_image = None
        self.lbl_image = None
        self.te_file_path = None
        self.load_ui()
        self.image_flipper = None

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)

        self.te_file_path = self.findChild(QtWidgets.QTextEdit, 'te_file_path')

        self.lbl_image = self.findChild(QtWidgets.QLabel, 'lbl_image')

        self.lbl_edited_image = self.findChild(QtWidgets.QLabel, 'lbl_edited_image')

        self.findChild(QtWidgets.QPushButton, 'btn_choose_picture').clicked.connect(self.choose_picture)
        self.findChild(QtWidgets.QPushButton, 'btn_flip_vtc').clicked.connect(self.flip_vertical)
        self.findChild(QtWidgets.QPushButton, 'btn_flip_hrz').clicked.connect(self.flip_horizon)
        self.findChild(QtWidgets.QPushButton, 'btn_flip_both').clicked.connect(self.flip_both)

        self.te_export_folder = self.findChild(QtWidgets.QTextEdit, 'te_export_folder')
        self.te_filename_export = self.findChild(QtWidgets.QTextEdit, 'te_filename_export')
        self.findChild(QtWidgets.QPushButton, 'btn_choose_folder').clicked.connect(self.choose_folder)
        self.findChild(QtWidgets.QPushButton, 'btn_export').clicked.connect(self.export_to_file)
        ui_file.close()

    def choose_picture(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Jpeg file (*.jpeg);;JPG file (*.jpg);;PNG file (*.png)")
        if check:
            self.image_flipper = Image_Flipper(file_path=file)
            self.lbl_image.setPixmap(self.scaled_image(self.image_flipper.get_img()))
            self.image_flipper.edited_img = None
            self.te_file_path.setPlainText(file)

    def scaled_image(self, pixmap):
        return pixmap.scaled(self.lbl_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def flip_horizon(self):
        self.lbl_edited_image.setPixmap(self.scaled_image(self.image_flipper.flip_horizon()))

    def flip_vertical(self):
        self.lbl_edited_image.setPixmap(self.scaled_image(self.image_flipper.flip_vertical()))

    def flip_both(self):
        self.lbl_edited_image.setPixmap(self.scaled_image(self.image_flipper.flip_both()))

    def choose_folder(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.te_export_folder.setPlainText(file)

    def export_to_file(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Notification")

        filename = self.te_file_path.toPlainText()
        if filename == "":
            msg.setText("Please choose a picture")
            msg.exec_()
            return

        extension = filename.split(".")[-1]

        exp_folder = self.te_export_folder.toPlainText()
        if exp_folder == "":
            msg.setText("Invalid export folder")
            msg.exec_()
            return

        exp_filename = self.te_filename_export.toPlainText()
        if exp_filename == "":
            msg.setText("Empty export filename")
            msg.exec_()
            return

        exp_filename = exp_filename + "." + extension

        if self.image_flipper.save_file(path=exp_folder, filename=exp_filename):
            msg.setText("Export successfully!")
            msg.exec_()
        else:
            msg.setText("Please choose an edit mode")
            msg.exec_()


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
