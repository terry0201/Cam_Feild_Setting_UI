from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
import numpy as np
import cv2

LabelPictureSize = (1500, 900)
ButtonHeight = 40

class CameraWidget(QWidget):
    def __init__(self, centralwidget):
        super().__init__()
        self.centralwidget = centralwidget
        self.image = None
    
    def setupUi(self, MainWindow):
        self.setObjectName(u"camerawidget")
        self.setFont(QFont(u"Arial", 12))

        self.LabelCamera = QLabel('Label to show Camera', self)
        self.LabelCamera.setObjectName(u"LabelCamera")
        self.LabelCamera.setGeometry(QRect(20, 20, *LabelPictureSize))
        # self.LabelCamera.setText(QCoreApplication.translate("camerawidget", u"Label to show Camera", None))
        self.LabelCamera.setStyleSheet("background-color: lightgreen")

        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(1550, 30, 350, 1000))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        font_Arial18 = QFont("Arial", 18)

        self.groupBox = QGroupBox('Functions', self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(40, 500, 240, 300)) # x, y, x_len, y_len
        self.groupBox.setFont(font_Arial18)

        # Buttons: Connect Camera | Correction | Play Pause | ... | Skip
        self.ButtonConnectCamera = QPushButton('Connect Camera', self.groupBox)
        self.ButtonConnectCamera.setObjectName(u"ButtonConnectCamera")
        self.ButtonConnectCamera.setGeometry(QRect(20, 40+(ButtonHeight+10)*0, 200, ButtonHeight))
        self.ButtonConnectCamera.setFont(font_Arial18)

        self.ButtonCalibration = QPushButton('Calibration', self.groupBox)
        self.ButtonCalibration.setObjectName(u"ButtonCalibration")
        self.ButtonCalibration.setGeometry(QRect(20, 40+(ButtonHeight+10)*1, 200, ButtonHeight))
        self.ButtonCalibration.setFont(font_Arial18)

        self.ButtonPlayPause = QPushButton('Play / Pause', self.groupBox)
        self.ButtonPlayPause.setObjectName(u"ButtonPlayPause")
        self.ButtonPlayPause.setGeometry(QRect(20, 40+(ButtonHeight+10)*2, 200, ButtonHeight))
        self.ButtonPlayPause.setFont(font_Arial18)

        self.ButtonChangeQWidget = QPushButton('Skip', self.groupBox)
        self.ButtonChangeQWidget.setObjectName(u"ButtonChangeQWidget")
        self.ButtonChangeQWidget.setGeometry(QRect(20, 40+(ButtonHeight+10)*4, 200, ButtonHeight))
        self.ButtonChangeQWidget.setFont(font_Arial18)

        self.ButtonConnectCamera.clicked.connect(self.DisplayCV2ImageToLabel)
        self.ButtonChangeQWidget.clicked.connect(lambda: MainWindow.setCentralWidget(self.centralwidget))

    def DisplayCV2ImageToLabel(self):
        self.ReadPicture()

        # image shape: (H, W, 3)
        height, width, channel = self.image.shape
        bytesPerLine = 3 * width

        BGR_img = QImage(self.image.data, width, height, bytesPerLine, QImage.Format_BGR888)
        pixmap = QPixmap(BGR_img)
        pixmap = pixmap.scaled(*LabelPictureSize, Qt.KeepAspectRatio)  # SCALING METHOD
        self.LabelCamera.setPixmap(pixmap)

    def ReadPicture(self):
        # Make a picuture (H, W, 3), and store to self.image

        row_1_172 = np.arange(172)
        picture = np.zeros((128, 172, 3), dtype=np.uint8)
        for i in range(128):
            picture[i, :, 0] = np.copy(row_1_172)  # B -> R
            picture[i, :, 1] = np.copy(row_1_172)  # G -> G
            # picture[i, :, 2] = np.copy(row_1_172)  # R -> B

            row_1_172 += 1
        self.image = picture

        # self.image = cv2.imread(u'camera.jpg')  # H: 128, W: 172

        # cv2.imshow('Picture', self.image)
        # cv2.waitKey(0)
