# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'project changed.ui'
#
# Created by: Qt User Interface Compiler version 5.15.2
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
# ? CHANGED Actions: from original UI file
# ?         import list, copy functions, connect button <-> functions
# ?         delete / comment table widget row
# ?         update LabelPicture.setGeometry (1500, 900)
# ?         LabelPictureSize
# ?         update frame.setGeometry
# ?         self.LabelPicture.mousePressEvent = self.getPos  # DRAWING POLYGON
# ?         self.ButtonEdit.setFont(QFont(u"Arial", 18))
###############################################################################
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2 import QtCore, QtGui
from PySide2.QtMultimedia import QSound

import os
import xml.etree.ElementTree as ET

# DRAWING POLYGON
import numpy as np
import cv2
from shapely.geometry import Point, Polygon
LabelPictureSize = (1500, 900)
ButtonHeight = 40

ClickedDetectSize = 10

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1031, 882)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.LabelPicture = QLabel(self.centralwidget)
        self.LabelPicture.setObjectName(u"LabelPicture")
        self.LabelPicture.setGeometry(QRect(20, 20, *LabelPictureSize))
        self.LabelPicture.mousePressEvent = self.getPos  # DRAWING POLYGON
        self.LabelPicture.mouseMoveEvent = self.mouseMove
        self.LabelPicture.mouseReleaseEvent = self.mouseRelease
        self.LabelPicture.setMouseTracking(True)
        # self.LabelPicture.setScaledContents(True)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(1550, 30, 350, 1000))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 300, 60))
        font_14 = QFont()
        font_14.setPointSize(14)
        self.groupBox_2.setFont(font_14)
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 70, 20))
        self.LabelPictureName = QLabel(self.groupBox_2)
        self.LabelPictureName.setObjectName(u"LabelPictureName")
        self.LabelPictureName.setGeometry(QRect(100, 30, 180, 20))
        self.tableWidget = QTableWidget(self.frame)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 90, 300, 300))
        self.tableWidget.selectionModel().selectionChanged.connect(self.TableSelectionChange)
        font_Arial18 = QFont()
        font_Arial18.setFamily(u"Arial")
        font_Arial18.setPointSize(18)
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(40, 500, 240, 300)) # x, y, x_len, y_len
        self.groupBox.setFont(font_Arial18)
        # ADD region
        self.ButtonAddRegion = QPushButton(self.groupBox)
        self.ButtonAddRegion.setObjectName(u"ButtonAddRegion")
        self.ButtonAddRegion.setGeometry(QRect(20, 40+(ButtonHeight+10)*0, 200, ButtonHeight))
        self.ButtonAddRegion.setFont(font_Arial18)
        # Edit
        self.ButtonEdit = QPushButton(self.groupBox)
        self.ButtonEdit.setObjectName(u"ButtonEdit")
        self.ButtonEdit.setGeometry(QRect(20, 40+(ButtonHeight+10)*1, 200, ButtonHeight))
        self.ButtonEdit.setFont(font_Arial18)
        # Remove Polygon
        self.ButtonRemove = QPushButton(self.groupBox)
        self.ButtonRemove.setObjectName(u"ButtonRemove")
        self.ButtonRemove.setGeometry(QRect(20, 40+(ButtonHeight+10)*2, 200, ButtonHeight))
        self.ButtonRemove.setFont(font_Arial18)
        # Camera / Pause
        self.ButtonCamera = QPushButton(self.groupBox)
        self.ButtonCamera.setObjectName(u"ButtonCamera")
        self.ButtonCamera.setGeometry(QRect(20, 40+(ButtonHeight+10)*3, 200, ButtonHeight))
        self.ButtonCamera.setFont(font_Arial18)
        # Transformation
        self.ButtonTransformation = QPushButton(self.groupBox)
        self.ButtonTransformation.setObjectName(u"ButtonTransformation")
        self.ButtonTransformation.setGeometry(QRect(20, 40+(ButtonHeight+10)*4, 200, ButtonHeight))
        self.ButtonTransformation.setFont(font_Arial18)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1031, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

		##### CONNECT funcs & BUTTONs
        self.actionOpen.triggered.connect(self.BrowseFiles)
        self.actionSave.triggered.connect(self.SaveFile)
        self.ButtonAddRegion.clicked.connect(self.AddRegion)
        self.ButtonEdit.clicked.connect(self.EditPolygon)
        self.ButtonRemove.clicked.connect(self.DelPolygon)
        self.ButtonCamera.clicked.connect(self.CameraMode)
        self.ButtonTransformation.clicked.connect(self.ToTrans)
        
        ##### STATUS
        self.status = None
        # status: {'edit' | 'add_poly' | 'del_poly' | 'trans' | None}
        self.map_Button_to_status = {
            self.ButtonEdit: 'edit',
            self.ButtonAddRegion: 'add_poly',
            self.ButtonRemove: 'del_poly',
            self.ButtonTransformation: 'trans'
        }
        # for mouseMoveEvent, status=='edit' and (False -> highlight dots, True -> change self.attribute)
        self.moving_dot = None
        
        self.pixHeight = None  # to check whether a image is read
        self.tracking = False
        self.semi_color = [
            # QtGui.QColor(255, 0, 0, 100),
            QtGui.QColor(0, 0, 255, 100), QtGui.QColor(0, 255, 0, 100),
            QtGui.QColor(255, 255, 0, 100), QtGui.QColor(0, 0, 0, 100),
            QtGui.QColor(255, 128, 0, 100), QtGui.QColor(0, 255, 255, 100),
            QtGui.QColor(255, 0, 255, 100), QtGui.QColor(128, 128, 128, 100)
        ]
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        #if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        #endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        #if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
        #endif // QT_CONFIG(shortcut)
        self.LabelPicture.setText(QCoreApplication.translate("MainWindow", u"Picture Place", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Picture:", None))
        self.LabelPictureName.setText(QCoreApplication.translate("MainWindow", u"picturename.jpg", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Attribute", None));

        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Functions", None))
        self.ButtonAddRegion.setText(QCoreApplication.translate("MainWindow", u"ADD region", None))
        #if QT_CONFIG(shortcut)
        self.ButtonAddRegion.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
        #endif // QT_CONFIG(shortcut)
        self.ButtonEdit.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.ButtonCamera.setText(QCoreApplication.translate("MainWindow", u"Camera / Pause", None))
        self.ButtonTransformation.setText(QCoreApplication.translate("MainWindow", u"Transformation", None))
        #remove polygon
        self.ButtonRemove.setText(QCoreApplication.translate("MainWindow", u"Remove Polygon", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

    # connect to --> self.actionOpen
    def BrowseFiles(self):
        if self.status is not None:
            self.ShowErrorToStatusbar(f'[ERROR] Try to open file when Button(s) are still active: [{self.status}]')
            return

        filename = QFileDialog.getOpenFileName(self.centralwidget, 'Open file', os.getcwd(), 'Image files (*.jpg *.png)')
        # filename: (filepath: str, image type(same as I write): str)

        # ? Find Picutre
        if not filename[0]:
            self.ShowErrorToStatusbar('[ERROR] No picture file select')
            return

        print(filename[0])
        self.full_pic_path = filename[0]
        self.LabelPictureName.setText(self.full_pic_path.split('/')[-1])
        self.RemoveAllRows()

        pixmap = QPixmap(self.full_pic_path)
        pixmap = pixmap.scaled(*LabelPictureSize, Qt.KeepAspectRatio)  # SCALING METHOD
        # 300: 最大寬度, 1000: 最大高度 -> LabelPictureSize
        print('Pixmap W, H:', pixmap.width(), pixmap.height())  # 顯示出的實際圖片大小
        self.LabelPicture.setPixmap(pixmap)
        self.pixHeight = self.LabelPicture.pixmap().height()
        
        
        # DRAWING POLYGON
        self.for_delete = pixmap
        self.image = cv2.imread(self.full_pic_path)
        self.resize = self.image.shape[1] / pixmap.width()
        self.attribute = []
        self.color_index = []
        self.matrix_pix_to_cm = None
        print(self.image.shape[:2])

        # Find XML file
        self.full_xml_path = self.full_pic_path.rsplit('.')[0] + '.xml'
        if os.path.isfile(self.full_xml_path):
            # load data
            print(f'Find corresponding .xml file for {self.full_pic_path}')
            self.OpenXmlFile()

    def OpenXmlFile(self):
        tree = ET.parse(self.full_xml_path)
        root = tree.getroot()

        # fetch data from xml to table
        for obj in root.iter('object'):
            # get data
            name = obj.find('name').text
            attribute = obj.find('attribute').text
            print(f'get obj name: {name}')

            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + 1)

            # Build empty row
            __qtablewidgetitem0 = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(row, __qtablewidgetitem0)
            __qtablewidgetitem1 = QTableWidgetItem(name)
            self.tableWidget.setItem(row, 0, __qtablewidgetitem1)

            __qtablewidgetitem2 = QTableWidgetItem(attribute)
            self.tableWidget.setItem(row, 1, __qtablewidgetitem2)

            # DRAW POLYGON
            polygon_pos_list = []
            polygon = obj.find('polygon')
            for pt in polygon.iter('pt'):
                x = float(pt.find('x').text) / self.resize
                y = float(pt.find('y').text) / self.resize
                polygon_pos_list += [[x, y]]
                # print(f'get points: (x, y) = ({x}, {y})')
            self.attribute.append(polygon_pos_list)
        # DRAW POLYGON FUNCTION(polygon_pos_list)
        for i in range(len(self.attribute)):
            self.polygon(self.attribute[i], 2, None)
        self.for_tracking_pixmap = QPixmap(self.LabelPicture.pixmap())

    def RemoveAllRows(self):
        for i in range(self.tableWidget.rowCount()-1, -1, -1):
            self.tableWidget.removeRow(i)

    # connect to --> ButtonAddRegion
    def AddRegion(self):
        if self.pixHeight is None:  # don't read a file
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [Add Polygon]')
            return

        if self.status is None:
            self.set_status(self.ButtonAddRegion, True)
            self.fun()  # DRAWING POLYGON
            # AfterPolygon() should be CALL by the last operation in drawing polygon
        else:
            self.ShowErrorToStatusbar(f'[ERROR] try to set status [add_poly] on while status [{self.status}] on')

    def AfterPolygon(self):
        name, okPressed = QInputDialog.getText(self.centralwidget, "Get Name", "Your name:", QLineEdit.Normal, "")
        if okPressed and name != '':
            print(name)
        attr, okPressed = QInputDialog.getText(self.centralwidget, "Get Attr", "Your attribute:", QLineEdit.Normal, "")
        if okPressed and attr != '':
            print(attr)

        self.add_row((name, attr))

    def add_row(self, content=None):
        row = self.tableWidget.rowCount()
        # print(f'add row: {row}')
        self.tableWidget.setRowCount(row + 1)
        
        # Build empty row
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(row, __qtablewidgetitem3)
        if content is not None:
            __qtablewidgetitem4 = QTableWidgetItem(content[0])
            self.tableWidget.setItem(row, 0, __qtablewidgetitem4)
            __qtablewidgetitem5 = QTableWidgetItem(content[1])
            self.tableWidget.setItem(row, 1, __qtablewidgetitem5)
        else:
            __qtablewidgetitem4 = QTableWidgetItem(u"edit...")
            # __qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"edit..", None));
            self.tableWidget.setItem(row, 0, __qtablewidgetitem4)

            __qtablewidgetitem5 = QTableWidgetItem(u"edit...")
            # __qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"edit...", None));
            self.tableWidget.setItem(row, 1, __qtablewidgetitem5)
        
        # edit content method
        # ___qtablewidgetitem2 = self.tableWidget.item(0, 0)
        # ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"1231321", None));
        # ___qtablewidgetitem3 = self.tableWidget.item(0, 1)
        # ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"1231321333333", None));

    # tableWidget (de)select event
    def TableSelectionChange(self, selected, deselected):
        if self.status not in [None, 'del_poly']:
            return

        if self.tableWidget.rowCount() == 0:
            return
        
        if self.status == None:
            deselected_row = [ind.row() for ind in deselected.indexes()]
            # deselect
            if deselected_row:
                self.ReDraw(update_for_tracking_pixmap=False)
            # if self.selected_row is not None and self.selected_row in deselected_row:
            #     self.selected_row = None
            #     self.ReDraw(update_for_tracking_pixmap=False)
            
            # select
            if len(selected.indexes()) > 0:
                selected_row = selected.indexes()[0].row()
                self.ReDraw(update_for_tracking_pixmap=False)
                self.polygon(self.attribute[selected_row], 3, self.color_index[selected_row])

        elif self.status == 'del_poly':
            if len(selected.indexes()) > 0:
                self.TryDeletePolygon(selected.indexes()[0].row())

        # print(f'+{self.selected_row} - {deselected_row}')

    # connect to --> self.actionSave
    def SaveFile(self):
        if self.pixHeight is None:  # don't read a file
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [File > Save]')
            return
        if self.status is not None:
            self.ShowErrorToStatusbar(f'[ERROR] Try to save file when Button(s) are still active: [{self.status}]')
            return

        # save data to pic_name.xml
        root = ET.Element('annotation')
        filename = ET.SubElement(root, 'filename')
        filename.text = self.full_pic_path.split('/')[-1]
        for i in range(self.tableWidget.rowCount()):
            object = ET.SubElement(root, 'object')
            
            name = ET.SubElement(object, 'name')
            name.text = self.tableWidget.item(i, 0).text()
            attribute = ET.SubElement(object, 'attribute')
            attribute.text = self.tableWidget.item(i, 1).text()
            polygon = ET.SubElement(object, 'polygon')
            # print('Attr:', self.attribute)
            for pos_x, pos_y in self.attribute[i]:  # 第 i 個 row (polygon)
                pt = ET.SubElement(polygon, 'pt')
                x = ET.SubElement(pt, 'x')
                x.text = str(pos_x * self.resize)
                y = ET.SubElement(pt, 'y')
                y.text = str(pos_y * self.resize)
        
        tree = ET.ElementTree(root)
        tree.write(self.full_xml_path, encoding="utf-8")
        print(f'save data to: [{self.full_xml_path}]')

        if self.matrix_pix_to_cm is not None:
            np.save(self.full_pic_path.rsplit('.')[0] + '.npy', self.matrix_pix_to_cm)
            print(f'save transfrom matrix to: [{self.full_pic_path.rsplit(".")[0] + ".npy"}]')

    # connect to --> self.ButtonEdit
    def EditPolygon(self):
        if self.pixHeight is None:  # don't read a file
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [Edit]')
            return

        if self.status == 'edit':
            self.set_status(self.ButtonEdit, False)
        elif self.status is None:
            self.set_status(self.ButtonEdit, True)
        else:
            self.ShowErrorToStatusbar(f'[ERROR] try to set status [edit] on while status [{self.status}] on')

    # connect to --> self.ButtonCamera
    def CameraMode(self):
        pass

    # connect to --> self.ButtonTransformation
    def ToTrans(self):
        if self.pixHeight is None:  # don't read a file
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [Transformation]')
            return

        if self.status == 'trans':
            return
        elif self.status is not None and self.status != 'edit':  # 唯一可以跳過去 trans 的狀態就是 'edit'
            self.ShowErrorToStatusbar(f'[ERROR] try to set status [trans] on while status [{self.status}] on')
            return

        status_edit = self.status  # None or 'edit'
        
        idx = -1
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).text() == 'TRANS':
                idx = i
                break
        if idx == -1:
            # not found
            self.ShowErrorToStatusbar('[ERROR] polygon with name [TRANS] not found')
            return

        # status is None AND found a polygon
        self.set_status(self.ButtonTransformation, True)
        
        # position text parser
        attr_text = self.tableWidget.item(idx, 1).text()

        attr = [e.strip('[](){} ') for e in attr_text.split(',')]
        # 先用 ',' 作分隔，再去除左右邊的括弧空格 '[](){} '

        src = np.array(self.attribute[i], np.float32) * self.resize
        src = src.reshape(-1, 2)
        attr = np.float32(attr).reshape((4, 2))
        
        # calculate the matrix for real world, we will not use it!
        # self.SaveFile()
        self.matrix_pix_to_cm = cv2.getPerspectiveTransform(src, attr)

        # calculte the ratio of pixel/cm
        ratio = 0
        for i in range(0, 3):
            ratio = ratio + self.size(src[i][0], src[i+1][0], src[i][1], src[i+1][1],
                                      attr[i][0], attr[i+1][0], attr[i][1], attr[i+1][1])
        ratio = ratio + self.size(src[0][0], src[3][0], src[0][1], src[3][1],
                                  attr[0][0], attr[3][0], attr[0][1], attr[3][1])
        ratio /= 4
        # compute matrix for pixel to pixel
        attr = attr * ratio  # change cm to pixel in the image
        matrix = cv2.getPerspectiveTransform(src, attr)

        ww = self.image.shape[1]
        hh = self.image.shape[0]
        width, height, shift_x, shift_y = self.shift(src, matrix)
        # move the selected region to the center, and avoid some part of image be cut off
        for i in range(0, 4):
            attr[i][0] = attr[i][0] - shift_x + 100
            attr[i][1] = attr[i][1] - shift_y + 100

        matrix = cv2.getPerspectiveTransform(src, attr)
        result = cv2.warpPerspective(
            self.image, matrix, (int(width), int(height)),
            cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0)
        )

        # show the result
        fx = 1200 / int(width)
        fy = 800 / int(height)
        f = min(fx, fy)

        print(int(width)*f, int(height)*f)
        resized = cv2.resize(result, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        
	attr *= f
        p = attr.astype(int)
	
        cv2.line(resized, tuple(p[0]), tuple(p[1]), (255, 0, 0), 3)
        cv2.line(resized, tuple(p[1]), tuple(p[2]), (255, 0, 0), 3)
        cv2.line(resized, tuple(p[2]), tuple(p[3]), (255, 0, 0), 3)
        cv2.line(resized, tuple(p[3]), tuple(p[0]), (255, 0, 0), 3)
	
        cv2.imshow('transform', resized)
        cv2.moveWindow('transform', 200, 200)
        cv2.waitKey(0)
        
        self.set_status(self.ButtonTransformation, False)
        if status_edit == 'edit':
            self.set_status(self.ButtonEdit, True)

    # connect to --> self.ButtonRemove
    def DelPolygon(self):
        if self.pixHeight is None:  # don't read a file
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [Remove]')
            return

        if self.status == 'del_poly':
            self.set_status(self.ButtonRemove, False)
        elif self.status is None:
            self.set_status(self.ButtonRemove, True)
        else:
            self.ShowErrorToStatusbar(f'[ERROR] try to set status [del_poly] on while status [{self.status}] on')

    def TryDeletePolygon(self, idx):
        '''
            Highlight polygon idx
            MessageBox to double check
        '''
        # TODO Highlight polygon i
        self.polygon(self.attribute[idx], 3, self.color_index[idx])

        reply = QMessageBox.question(self.centralwidget, "刪除", "刪除這個多邊形?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            # print('reply Yes')
            del self.attribute[idx]
            del self.color_index[idx]
            self.tableWidget.removeRow(idx)  # Remove table[idx]
            # self.ReDraw(update_for_tracking_pixmap=True) # set_status 裡面就會做一次了
            self.set_status(self.ButtonRemove, False)

        elif reply == QMessageBox.No:
            # 把全部都重畫
            self.ReDraw(update_for_tracking_pixmap=False)

    def set_status(self, button, onoff):
        # ! daugerous, direct change status no matter what status is

        if onoff:
            self.status = self.map_Button_to_status[button]
            button.setStyleSheet('QPushButton {background-color: cyan;}')
        else:
            self.status = None
            button.setStyleSheet('QPushButton {background-color: None;}')
        
        # 換狀態順便重畫一次
        self.tableWidget.clearSelection()
        # ! REDRAW
        self.ReDraw(update_for_tracking_pixmap=True)
        # self.LabelPicture.setPixmap(self.for_delete)
        # for i, poly in enumerate(self.attribute):
        #     self.polygon(poly, 1, self.color_index[i])

    def ShowErrorToStatusbar(self, text):
        print(text)
        self.statusbar.showMessage(text, 3000)
    # ---------------------------------------------------------------- DRAWING POLYGON
    # mouseMoveEvent
    def mouseMove(self, event):
        if not self.LabelPicture.pixmap():
            return

        # map pixel on LabelPicture to pixel on image file
        x = event.pos().x()  # real x point on the image
        y = event.pos().y() - 450 + self.pixHeight / 2

        # self.attribute: [polygons], polygon: [points], point: [x, y]
        if self.status == 'edit':
            if self.moving_dot:
                # plot after editing
                i, j = self.moving_dot
                self.attribute[i][j][0] = x
                self.attribute[i][j][1] = y

                # ! REDRAW
                self.LabelPicture.setPixmap(self.for_editing_pixmap)
                self.polygon(self.attribute[i], 1, self.color_index[i])  # polygon() will copy another pixmap
                # self.ReDraw(update_for_tracking_pixmap=True)
                # for i, poly in enumerate(self.attribute):
                #     self.polygon(poly, 1, self.color_index[i])
            else:
                # plot before editing
                # ! REDRAW
                self.ReDraw(update_for_tracking_pixmap=False)
                # self.LabelPicture.setPixmap(self.for_delete)
                # for i, poly in enumerate(self.attribute):
                #     self.polygon(poly, 1, self.color_index[i])
                
                for i, poly in enumerate(self.attribute):
                    for j, point in enumerate(poly):
                        p_x, p_y = point
                        if abs(p_x-x) < ClickedDetectSize and abs(p_y-y) < ClickedDetectSize:
                            # highlight this point: self.attribute[i][j]
                            self.draw_point(p_x, p_y, ClickedDetectSize)

        elif self.status == 'add_poly':
            if self.tracking:
                self.pos_x = event.pos().x() 
                self.pos_y = event.pos().y() - 450 + self.pixHeight/2
                self.Draw()
        else:
            pass

    # mousePressEvent
    def mouseRelease(self, event):
        # self.pos_x, self.pos_y = event.pos().x(), event.pos().y() - 450 + pixHeight/2
        if self.status == 'edit':
            self.LabelPicture.setMouseTracking(True)
            self.ReDraw(update_for_tracking_pixmap=True)
            self.moving_dot = None

    # mousePressEvent
    def getPos(self, event):
        if self.pixHeight is None:
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [Label region]')
            return

        # real pixmap height
        x = event.pos().x()  # real x point on the image
        y = event.pos().y() - 450 + self.pixHeight / 2

        if self.status == 'add_poly':
            if len(self.tmp) == 0:
                self.start_x = x
                self.start_y = y
                self.tracking = True

            # 第二個點不能點回第一個點
            if len(self.tmp)==2 and \
               abs(x-self.start_x) < ClickedDetectSize and\
               abs(y-self.start_y) < ClickedDetectSize:
               self.tmp = []

            self.tmp.append([x, y])
            self.PreviousPair = (x, y)
            
            # 刪掉不小心點兩下的點
            if len(self.tmp) >=2 and \
               abs(x-self.tmp[-2][0]) < 3 and\
               abs(y-self.tmp[-2][1]) < 3:
               del self.tmp[-1]

            # 一定要三個點以上才能組成多邊形
            if len(self.tmp) > 2 and \
               abs(x-self.start_x) < ClickedDetectSize and\
               abs(y-self.start_y) < ClickedDetectSize:
                self.tracking = False
                del self.tmp[-1]
                print(self.tmp)

                self.attribute.append(self.tmp)
                self.ReDraw(update_for_tracking_pixmap=True)
                self.AfterPolygon()  # add name and attribute on the table

                self.set_status(self.ButtonAddRegion, False)
            # LabelPic 的座標(1500, 900)
            # print(f'original x: {event.pos().x()}, y: {event.pos().y()}')
            # print(f'  Move to ({event.pos().x()}, {(event.pos().y() - 450 + pixHeight/2)})')
            # print(f'  Pix On Pic ({x}, {y})')  # OK

        # choose which polygon has to be deleted -> after DelPolygon(self)
        elif self.status == 'del_poly':
            p = Point(x, y)
            idx = -1
            for i in range(len(self.attribute)):
                if p.within(Polygon(self.attribute[i])) == True:
                   idx = i
                   break
            if idx != -1:
                self.TryDeletePolygon(idx)
    
        elif self.status == 'edit':
            for i, poly in enumerate(self.attribute):
                for j, point in enumerate(poly):
                    p_x, p_y = point
                    if abs(p_x-x) < ClickedDetectSize and abs(p_y-y) < ClickedDetectSize:
                        # highlight this point: self.attribute[i][j]
                        # self.draw(p_x, p_y, 20 / self.resize)
                        self.moving_dot = (i, j)
                        self.ReDraw(False, except_row=i)  # update_for_tracking_pixmap not important here
                        # print(f'Edit polygon [{i}]')
                        break
        
        elif self.status == None:
            # Highlight corresponding table row
            p = Point(x, y)
            idx = -1
            for i in range(len(self.attribute)):
                if p.within(Polygon(self.attribute[i])) == True:
                   idx = i
                   break
            if idx != -1:
                self.tableWidget.selectRow(idx)
            else:
                self.selected_row = None
                self.tableWidget.clearSelection()
                # ! REDRAW
                self.ReDraw(update_for_tracking_pixmap=False)
                # self.LabelPicture.setPixmap(self.for_delete)
                # for i, poly in enumerate(self.attribute):
                #     self.polygon(poly, 1, self.color_index[i])

        # ----------------------------------------------------------------

    def draw_point(self, x, y, pen_size=5):
        pixmap = QPixmap(self.LabelPicture.pixmap())
        qp = QPainter(pixmap)
        pen = QPen(Qt.black, pen_size)
        qp.setPen(pen)
        qp.drawPoint(x, y)
        qp.end()
        self.LabelPicture.setPixmap(pixmap)

    def polygon(self, tmp, load, idx):
        p = []
        for qpoint in tmp:
            x = qpoint[0]
            y = qpoint[1]
            p.append(QtCore.QPoint(x, y))
        pixmap = QtGui.QPixmap(self.LabelPicture.pixmap())
        qp = QtGui.QPainter(pixmap)
        pen = QtGui.QPen(Qt.black, 3)
        qp.setPen(pen)

        # for new polygon
        if load == 0:
            qp.setBrush(self.semi_color[self.index])

        # for delete polygon
        elif load == 1:
            qp.setBrush(self.semi_color[idx])

        # for load old polygon
        elif load == 2:
            c = np.random.randint(len(self.semi_color))  # [0, 7]
            qp.setBrush(self.semi_color[c])
            self.color_index.append(c)

        # for highlight the polygon
        elif load == 3:
            # qp.setBrush(self.semi_color[idx].darker(int=1000000))
            qp.setBrush(QtGui.QColor(255, 0, 0, 200))

        qp.drawPolygon(p)
        qp.end()
        self.LabelPicture.setPixmap(pixmap)

    def fun(self):
        self.number = 0
        self.tmp = []

        # random choose a color
        self.index = np.random.randint(len(self.semi_color))  # [0, 7]
        self.color_index.append(self.index)
        self.for_tracking_pixmap = QtGui.QPixmap(self.LabelPicture.pixmap())

    # ---- for transfrom ----
    def distance(self, a1, a2, a3, a4):
        # sqrt(x*x + y*y)
        length = round(np.linalg.norm([a1-a2, a3-a4]))
        
        return length

    def size(self, a1, a2, a3, a4, b1, b2, b3, b4):
        return self.distance(a1, a2, a3, a4)/self.distance(b1, b2, b3, b4)

    def cal_point(self, x, y, m):
        dst_x = (m[0][0]*x+m[0][1]*y+m[0][2])/(m[2][0]*x+m[2][1]*y+m[2][2])
        dst_y = (m[1][0]*x+m[1][1]*y+m[1][2])/(m[2][0]*x+m[2][1]*y+m[2][2])
        return dst_x, dst_y

    def shift(self, pts, m):
        p1_x, p1_y = self.cal_point(pts[0][0], pts[0][1], m)
        p2_x, p2_y = self.cal_point(pts[1][0], pts[1][1], m)
        p3_x, p3_y = self.cal_point(pts[2][0], pts[2][1], m)
        p4_x, p4_y = self.cal_point(pts[3][0], pts[3][1], m)
        x = [p1_x, p2_x, p3_x, p4_x]
        y = [p1_y, p2_y, p3_y, p4_y]
        shift_x = min(x)
        shift_y = min(y)
        width = max(x) - min(x) + 200
        height = max(y) - min(y) + 200
        return width, height, shift_x, shift_y
    # ---- for transfrom ----

    def Draw(self):
        # for mouseMove, 'add_poly', tracing

        # self.empty_pixmap = QPixmap(self.for_tracking_pixmap)
        # self.LabelPicture.setPixmap(self.empty_pixmap)
        # pixmap = QPixmap(self.LabelPicture.pixmap())
        pixmap = QPixmap(self.for_tracking_pixmap)
        painter = QPainter(pixmap)

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        if self.PreviousPair:
            painter.drawLine(*self.PreviousPair, self.pos_x, self.pos_y)

        # Draw Dots
        if len(self.tmp) >= 1:
            prev = self.tmp[0]
            if abs(self.pos_x-prev[0]) < ClickedDetectSize and \
               abs(self.pos_y-prev[1]) < ClickedDetectSize:
                painter.setPen(QPen(Qt.black, ClickedDetectSize))
                painter.drawPoint(prev[0], prev[1])

            painter.setPen(QPen(Qt.black, 5))
            for pair in self.tmp:
                painter.drawPoint(*pair)

        # Draw old lines
        if len(self.tmp) >= 2:
            painter.setPen(QPen(Qt.black, 2))
            previous_pair = self.tmp[0]
            for pair in self.tmp[1: ]:
                painter.drawLine(*previous_pair, *pair)
                previous_pair = pair

        painter.end()
        self.LabelPicture.setPixmap(pixmap)

    def ReDraw(self, update_for_tracking_pixmap, except_row=None):
        # except_row == None -> for tracking pixmap
        if except_row is None:
            if update_for_tracking_pixmap:
                self.LabelPicture.setPixmap(self.for_delete)
                for i, poly in enumerate(self.attribute):
                    self.polygon(poly, 1, self.color_index[i])
                self.for_tracking_pixmap = QPixmap(self.LabelPicture.pixmap())
            else:
                self.LabelPicture.setPixmap(self.for_tracking_pixmap)
        # except_row != None -> for editing pixmap
        else:
            self.LabelPicture.setPixmap(self.for_delete)
            for i, poly in enumerate(self.attribute):
                if i == except_row:
                    continue
                self.polygon(poly, 1, self.color_index[i])

            self.for_editing_pixmap = QPixmap(self.LabelPicture.pixmap())
            # 取得需要的 pixmap 之後，再把圖畫完整( 避免剛點下去的瞬間少一個多邊形 )
            self.polygon(self.attribute[except_row], 1, self.color_index[except_row])

