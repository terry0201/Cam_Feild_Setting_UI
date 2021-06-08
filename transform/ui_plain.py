from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
import numpy as np
import cv2

pts  = np.empty([4, 2], dtype=float)
pts1 = np.float32([[169, 33], [496, 61], [24, 445], [413, 551]])
pts2 = np.float32([[0,0], [325, 0], [0, 460], [325, 460]])
image = cv2.imread('before.jpg')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(968, 794)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(140, 450, 211, 121))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        #before
        self.left_upLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.left_upLineEdit.setObjectName("left_upLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.left_upLineEdit)
        self.rightLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rightLineEdit.setObjectName("rightLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rightLineEdit)

        self.left_downLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.left_downLabel.setObjectName("left_downLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.left_downLabel)
        self.left_downLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.left_downLineEdit.setObjectName("left_downLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.left_downLineEdit)

        self.right_downLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.right_downLabel.setObjectName("right_downLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.right_downLabel)
        self.right_downLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.right_downLineEdit.setObjectName("right_downLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.right_downLineEdit)

        self.left_upLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.left_upLabel.setObjectName("left_upLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.left_upLabel)
        self.rightLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.rightLabel.setObjectName("rightLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rightLabel)

        #after
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(510, 450, 221, 121))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")

        self.left_upLabel_2 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.left_upLabel_2.setObjectName("left_upLabel_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.left_upLabel_2)
     
        #line edit for transform
        self.left_upLineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.left_upLineEdit_2.setObjectName("left_upLineEdit_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.left_upLineEdit_2)

        self.rightLineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.rightLineEdit_2.setObjectName("rightLineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rightLineEdit_2)

        self.left_downLabel_2 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.left_downLabel_2.setObjectName("left_downLabel_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.left_downLabel_2)

        self.left_downLineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.left_downLineEdit_2.setObjectName("left_downLineEdit_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.left_downLineEdit_2)

        self.right_downLabel_2 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.right_downLabel_2.setObjectName("right_downLabel_2")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.right_downLabel_2)
        self.right_downLineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.right_downLineEdit_2.setObjectName("right_downLineEdit_2")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.right_downLineEdit_2)
        self.rightLabel_2 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.rightLabel_2.setObjectName("rightLabel_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rightLabel_2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(540, 80, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 80, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(220, 410, 160, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(630, 410, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 410, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 580, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(640, 580, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 120, 265, 281.5))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("before.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label.mousePressEvent = self.getPos

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        #self.label_2.setGeometry(QtCore.QRect(520, 130, 200, 300))
        self.label_2.setText("")
        #self.label_2.setPixmap(QtGui.QPixmap(self.after))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 968, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.left_downLabel.setText(QtWidgets.QApplication.translate("MainWindow", "p3", None, -1))
        self.right_downLabel.setText(QtWidgets.QApplication.translate("MainWindow", "p4", None, -1))
        self.left_upLabel.setText(QtWidgets.QApplication.translate("MainWindow", "p1", None, -1))
        self.rightLabel.setText(QtWidgets.QApplication.translate("MainWindow", "p2", None, -1))
        self.left_upLabel_2.setText(QtWidgets.QApplication.translate("MainWindow", "p1", None, -1))
        self.left_downLabel_2.setText(QtWidgets.QApplication.translate("MainWindow", "p3", None, -1))
        self.right_downLabel_2.setText(QtWidgets.QApplication.translate("MainWindow", "p4", None, -1))
        self.rightLabel_2.setText(QtWidgets.QApplication.translate("MainWindow", "p2", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "After", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "Before", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Choose four points", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("MainWindow", "(x,y)", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Add points", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "OK", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("MainWindow", "Save", None, -1))
        
        self.pushButton.clicked.connect(self.Addpoints)
        self.pushButton_2.clicked.connect(self.transform)
        self.pushButton_3.clicked.connect(self.ButtonExit)
    
    def ButtonExit(self):
        self.points = []
        self.left_upLineEdit.setText("")
        self.rightLineEdit.setText("")
        self.left_downLineEdit.setText("")
        self.right_downLineEdit.setText("")
        self.left_upLineEdit_2.setText("")
        self.rightLineEdit_2.setText("")
        self.left_downLineEdit_2.setText("")
        self.right_downLineEdit_2.setText("")
        #exit()
    
    def Addpoints(self):
        print('Choose 4 points.')
        self.points = []
    
    def getPos(self , event):
        x = event.pos().x() *2
        y = event.pos().y() *2
        text = str(x)+ ", " +str(y)
        self.points.append(text)

        if len(self.points)==1:
            self.left_upLineEdit.setText(self.points[0])
            pts[0][0] = x
            pts[0][1] = y
            self.draw(x,y)

        elif len(self.points)==2:
            self.rightLineEdit.setText(self.points[1])
            pts[1][0] = x
            pts[1][1] = y
            self.draw(x,y)
            #self.drawline(pts[0][0], pts[0][1], pts[1][0], pts[1][1])

        elif len(self.points)==3:
            self.left_downLineEdit.setText(self.points[2])
            pts[2][0] = x
            pts[2][1] = y
            self.draw(x,y)
            #self.drawline(pts[1][0], pts[1][1],pts[2][0], pts[2][1])

        else:
            self.right_downLineEdit.setText(self.points[3])
            pts[3][0] = x
            pts[3][1] = y
            self.draw(x,y)
            #self.drawline(pts[0][0], pts[0][1],pts[3][0], pts[3][1])
            #self.drawline(pts[2][0], pts[2][1],pts[3][0], pts[3][1])

    def transform(self):
        self.left_upLineEdit_2.setText(str(pts2[0][0]) + ", " + str(pts2[0][1]))
        self.rightLineEdit_2.setText(str(pts2[1][0]) + ", " + str(pts2[1][1]))
        self.left_downLineEdit_2.setText(str(pts2[2][0]) + ", " + str(pts2[2][1]))
        self.right_downLineEdit_2.setText(str(pts2[3][0]) + ", " + str(pts2[3][1]))
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(image, matrix, (329, 461))
        cv2.imwrite('./tmp.jpg',result)
        self.label_2.setGeometry(QtCore.QRect(520, 120, 260, 300))
        self.label_2.setPixmap(QtGui.QPixmap('./tmp.jpg'))
        self.drawline(pts2[0][0], pts2[0][1],pts2[1][0], pts2[1][1])
        self.drawline(pts2[1][0], pts2[1][1],pts2[3][0], pts2[3][1])
        self.drawline(pts2[0][0], pts2[0][1],pts2[2][0], pts2[2][1])
        self.drawline(pts2[2][0], pts2[2][1],pts2[3][0], pts2[3][1])

    def draw(self,x,y):
        pixmap = QtGui.QPixmap(self.label.pixmap())
        qp = QtGui.QPainter(pixmap)
        pen = QtGui.QPen(Qt.red, 20)
        qp.setPen(pen)
        qp.drawPoint(x,y)
        qp.end()
        self.label.setPixmap(pixmap)

    def drawline(self,x1,y1,x2,y2):
        pixmap = QtGui.QPixmap(self.label_2.pixmap())
        qp = QtGui.QPainter(pixmap)
        pen = QtGui.QPen(Qt.red, 10)
        qp.setPen(pen)
        qp.drawLine(x1, y1, x2, y2)
        qp.end()
        self.label_2.setPixmap(pixmap)
