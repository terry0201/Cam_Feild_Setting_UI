# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'project full screen.ui'
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
from sys import base_prefix
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# from PySide2 import QtCore, QtGui
from PySide2.QtMultimedia import QSound

import os
import xml.etree.ElementTree as ET

# DRAWING POLYGON
import numpy as np
import cv2
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

LabelPictureSize = (1500, 900)
ButtonHeight = 40
ClickedDetectSize = 10

#!#############################################
from lab_question import QuestionDialog, EditPolygonData
from lab_camera_UI import CameraWidget
from lab_plot import DraggablePolygonMarker
#!#############################################
from utils import set_font_size

def resetLabelPictureSize(Size):
    global LabelPictureSize
    LabelPictureSize = Size

class Ui_MainWindow(object):
    def __init__(self):
        # STATUS
        self.status = None
        # status: {'edit' | 'add_poly' | 'del_poly' | 'trans' | None}
        
        # for mouseMoveEvent, status=='edit' and (False -> highlight dots, True -> change self.attribute)
        self.moving_dot = None
        
        self.pixHeight = None  # to check whether a image is read
        self.tracking = False
        self.semi_color = [
            QColor(0, 0, 255, 100), QColor(0, 255, 0, 100),
            QColor(255, 255, 0, 100), QColor(0, 0, 0, 100),
            QColor(255, 128, 0, 100), QColor(0, 255, 255, 100),
            QColor(255, 0, 255, 100), QColor(128, 128, 128, 100)
        ]
        self.SoundClicked = QSound(u'Polygon/sounds/clicked.wav')
        self.SoundError = QSound(u'Polygon/sounds/error.wav')
        self.pressInMarker = False

        app = QApplication.primaryScreen()
        dpi = app.logicalDotsPerInch()
        resolution = app.geometry()
        resolution_height = resolution.height()
        resolution_width = resolution.width()
        print("dpi: ", dpi)
        print("resolution height: ", resolution_height)
        print("resolution width: ", resolution_width)
        self.BasicFontSize = set_font_size(dpi, resolution_height, resolution_width)

    def setupUi(self, MainWindow):
        self.change_centralwidget_to = MainWindow.setCentralWidget
        self.MainWindow = MainWindow
        self.MainWindow.setWindowTitle(u"MainWindow")

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1031, 882)

        basic_font = QFont(u"Arial", self.BasicFontSize)
        title_font = QFont(u"Arial", self.BasicFontSize + 2)
        MainWindow.setFont(basic_font)

        self.actionOpen = QAction(u"Open", MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOpen.setShortcut(u"Ctrl+O")
        self.actionSave = QAction(u"Save", MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave.setShortcut(u"Ctrl+S")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.LabelPicture = QLabel(u"Picture Place", self.centralwidget)
        self.LabelPicture.setObjectName(u"LabelPicture")
        self.LabelPicture.mousePressEvent = self.getPos  # DRAWING POLYGON
        self.LabelPicture.mouseMoveEvent = self.mouseMove
        self.LabelPicture.mouseReleaseEvent = self.mouseRelease
        self.LabelPicture.setMouseTracking(True)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.groupBox_2 = QGroupBox(u"Info", self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(title_font) 

        self.TextPictureName = QPlainTextEdit(u"picturename.jpg", self.groupBox_2)
        self.TextPictureName.setFont(basic_font)
        self.TextPictureName.setToolTip(u"picturename.jpg")
        self.TextPictureName.setFrameStyle(QFrame.NoFrame)
        self.TextPictureName.setReadOnly(True)
        self.TextPictureName.viewport().setAutoFillBackground(False)
        # self.TextPictureName.setMinimumHeight(50) 

        self.tableWidget = QTableWidget(self.frame)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem())
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers( QAbstractItemView.NoEditTriggers)
        self.tableWidget.selectionModel().selectionChanged.connect(self.TableSelectionChange)
        self.tableWidget.doubleClicked.connect(self.edit_polygon_attr_name)
        self.tableWidget.horizontalHeaderItem(0).setText(u"Name")
        self.tableWidget.horizontalHeaderItem(1).setText(u"Attribute")

        self.groupBox = QGroupBox(u"Functions", self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(title_font)

        # ADD region
        self.ButtonAddRegion = QPushButton(u"ADD region", self.groupBox)
        self.ButtonAddRegion.setObjectName(u"ButtonAddRegion")
        self.ButtonAddRegion.setFont(basic_font)
        self.ButtonAddRegion.setShortcut(u"Ctrl+N")
        # Edit
        self.ButtonEdit = QPushButton(u"Edit", self.groupBox)
        self.ButtonEdit.setObjectName(u"ButtonEdit")
        self.ButtonEdit.setFont(basic_font)
        # Remove Polygon
        self.ButtonRemove = QPushButton(u"Remove Polygon", self.groupBox)
        self.ButtonRemove.setObjectName(u"ButtonRemove")
        self.ButtonRemove.setFont(basic_font)
        # Transformation
        self.ButtonTransformation = QPushButton(u"Transformation", self.groupBox)
        self.ButtonTransformation.setObjectName(u"ButtonTransformation")
        self.ButtonTransformation.setFont(basic_font)

        #---------- layout begin --------- 
        self.main_layout = QHBoxLayout(self.centralwidget)  
        self.main_layout.setObjectName(u"main_layout")  
        self.main_layout.addWidget(self.LabelPicture, 8)  
        self.main_layout.addWidget(self.frame, 2)  

        self.layout_frame = QVBoxLayout(self.frame) 
        self.layout_frame.setObjectName(u"layout_frame")  
        self.layout_frame.addWidget(self.groupBox_2, 1)
        self.layout_frame.addWidget(self.tableWidget, 3)
        self.layout_frame.addWidget(self.groupBox, 5)

        self.layout_button = QVBoxLayout(self.groupBox) 
        self.layout_button.addWidget(self.ButtonAddRegion, 1)
        self.layout_button.addWidget(self.ButtonEdit, 1)
        self.layout_button.addWidget(self.ButtonRemove, 1)
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.ButtonTransformation, 1)

        self.layout_info = QVBoxLayout(self.groupBox_2) # for the new line
        self.layout_info.addWidget(self.TextPictureName) # for the new line
        #---------- layout end --------- 
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1031, 21))
        self.menuFile = QMenu(u"File", self.menubar)
        self.menuFile.setObjectName(u"menuFile") 

        menuFile_font = QFont(u"Arial", self.BasicFontSize - 3)
        self.menuFile.setFont(menuFile_font) 

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        #--------------------------------- move down camerawidget
        self.camerawidget = CameraWidget(self.centralwidget)
        self.camerawidget.setupUi(MainWindow, self.BasicFontSize)
        MainWindow.setCentralWidget(self.camerawidget)
        #---------------------------------
        # self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

		##### CONNECT funcs & BUTTONs
        self.actionOpen.triggered.connect(self.BrowseFiles)
        self.actionSave.triggered.connect(self.SaveFile)
        self.ButtonAddRegion.clicked.connect(self.AddRegion)
        self.ButtonEdit.clicked.connect(self.EditPolygon)
        self.ButtonRemove.clicked.connect(self.DelPolygon)
        self.ButtonTransformation.clicked.connect(self.ToTrans)
        
        ##### INITIALIZE after setupUI()
        # status: {'edit' | 'add_poly' | 'del_poly' | 'trans' | None}
        self.map_Button_to_status = {
            self.ButtonEdit: 'edit',
            self.ButtonAddRegion: 'add_poly',
            self.ButtonRemove: 'del_poly',
            self.ButtonTransformation: 'trans'
        }
        for button in self.map_Button_to_status: 
            button.setMinimumHeight(30) 
        
        self.centralwidget.keyPressEvent = self.keyPress
    # setupUi

    def edit_polygon_attr_name(self, event):
        self.tableWidget.clearSelection()
        row = event.row()
        column = event.column()
        data = event.data()
        if column == 0: # sibling ATTR
            sibling = event.siblingAtColumn(column+1)
            attr = sibling.data()
            name = data
            # print(attr)
            # print(name)
        else: # NAME
            sibling = event.siblingAtColumn(column-1)
            attr = data
            name = sibling.data()
            # print(attr)
            # print(name)
        editPolygon = EditPolygonData(self.BasicFontSize, name, attr)
        okPressed = editPolygon.exec()
        if okPressed == QDialog.Accepted:
            new_name = editPolygon.getInputs()[0]
            new_attr = editPolygon.getInputs()[1]
            self.tableWidget.item(row, 0).setText(new_name)
            self.tableWidget.item(row, 1).setText(new_attr)
            

    def keyPress(self, event):
        if event.key() == Qt.Key_Escape:
            # print('you Pressed ESC!')
            if self.status is None:
                # click to Highlight polygon
                self.tableWidget.clearSelection()
                self.ReDraw(update_for_tracking_pixmap=False)

            elif self.status == 'add_poly':
                # 1. click 'add region'
                # 2. start add points
                del self.color_index[-1]
                self.tracking = False
                self.set_status(self.ButtonAddRegion, False)
                # 3. finish a polygon and a Window pop up
                #    ESC: close window, add new row, leave add_poly

            elif self.status == 'edit':
                # 1. click 'edit'
                self.set_status(self.ButtonEdit, False)
                # 2-1. click and drag node( not released )
                self.ReDraw(update_for_tracking_pixmap=True)
                self.moving_dot = None
                # 2-2. click 'transform'  # Won't affect

            elif self.status == 'del_poly':
                # 1. click 'remove'
                self.set_status(self.ButtonRemove, False)
                # 2. click polygon and a Dialog pop up
                #    ESC: close dialog window

            elif self.status == 'transfrom':
                plt.close('all')
                # 不過 transform 一瞬間就消失了，應該不會有這個機會

            else:
                self.ShowErrorToStatusbar(f'Strange status: {self.status}')

    # connect to --> self.actionOpen
    def BrowseFiles(self):
        # 主畫面
        if self.MainWindow.centralWidget().objectName() != 'centralwidget':
            self.ShowErrorToStatusbar(f'[ERROR] can\'t open file while correlating camera')
            return
        
        if self.status is not None:
            self.ShowErrorToStatusbar(f'[ERROR] Try to open file when Button(s) are still active: [{self.status}]')
            return

        filename = QFileDialog.getOpenFileName(self.centralwidget, 'Open file', os.getcwd(),
                                               'Image files (*.jpg *.png)')
        # filename: (filepath: str, image type(same as I write): str)
        
        # ? Find Picutre
        if filename[0]:
            # print(filename[0])
            self.OpenPictureFile(filename[0])
        else:
            self.ShowErrorToStatusbar('[ERROR] No picture file select')
            return

    def OpenPictureFile(self, filename):
        # ! Make sure that:
        # ! there is a picture at path [filename]
        # global LabelPictureSize 
        # LabelPictureSize = self.LabelPicture.size().toTuple() 
        # print(f'LabelPicture Size: {LabelPictureSize}') 

        self.full_pic_path = filename
        pic_name = self.full_pic_path.split('/')[-1]
        self.TextPictureName.setPlainText(pic_name)
        self.TextPictureName.setToolTip(pic_name)

        self.RemoveAllRows()

        pixmap = QPixmap(self.full_pic_path)
        pixmap = pixmap.scaled(*LabelPictureSize, Qt.KeepAspectRatio)  # SCALING METHOD
        # 300: 最大寬度, 1000: 最大高度 -> LabelPictureSize
        print('Pixmap W, H:', pixmap.width(), pixmap.height())  # 顯示出的實際圖片大小
        self.LabelPicture.setPixmap(pixmap)
        self.pixHeight = self.LabelPicture.pixmap().height()
        
        
        # DRAWING POLYGON
        self.for_delete = pixmap
        # self.image = cv2.imread(self.full_pic_path)
        self.image = cv2.imdecode(np.fromfile(self.full_pic_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        self.resize = self.image.shape[1] / pixmap.width()
        self.attribute = []
        self.color_index = []
        self.matrix_pix_to_cm = None
        print(f'Image (W, H): {self.image.shape[:2]}')

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
            attribute = obj.find('attributes').text
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
        elif self.status == 'add_poly':
            del self.color_index[-1]
            self.tracking = False
            self.set_status(self.ButtonAddRegion, False)
        else:
            self.ShowErrorToStatusbar(f'[ERROR] try to set status [add_poly] on while status [{self.status}] on')
            # del self.attribute[-1]
            # def self.color_index[-1]
            # self.set_status(self.ButtonAddRegion, False)

    def AfterPolygon(self):
        qd = QuestionDialog(self.BasicFontSize)
        okPressed = qd.exec()
        # qd.move ((QApplication.desktop().width() - self.centralwidget.width())/2, (QApplication.desktop().height() - self.centralwidget.height())/2)
        if okPressed == QDialog.Accepted:
            self.add_row((qd.getInputs()))
        elif okPressed == QDialog.Rejected:
            self.add_row(('', ''))

    def add_row(self, content):
        row = self.tableWidget.rowCount()
        # print(f'add row: {row}')
        self.tableWidget.setRowCount(row + 1)
        
        # Build empty row
        self.tableWidget.setVerticalHeaderItem(row, QTableWidgetItem())

        # content
        self.tableWidget.setItem(row, 0, QTableWidgetItem(content[0]))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(content[1]))
        
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
        # 主畫面
        if self.MainWindow.centralWidget().objectName() == 'centralwidget':
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

            # print(LabelPictureSize)
            width = ET.SubElement(root, 'width')
            w = self.LabelPicture.pixmap().width()
            width.text = str(int(w))
            height = ET.SubElement(root, 'height')
            h = self.LabelPicture.pixmap().height()
            height.text = str(int(h))
            # polygonDict = {}
            # print("SAVE H  ",self.image.shape[0])
            # print("SAVE W  ",self.image.shape[1])
            check_h = self.image.shape[0]
            check_w = self.image.shape[1]
            hw_error = False
            
            for i in range(self.tableWidget.rowCount()):
                object = ET.SubElement(root, 'object')
                
                name = ET.SubElement(object, 'name')
                name.text = self.tableWidget.item(i, 0).text()
                attribute = ET.SubElement(object, 'attributes')
                attribute.text = self.tableWidget.item(i, 1).text()
                polygon = ET.SubElement(object, 'polygon')
                # print('Attr:', self.attribute)
                for pos_x, pos_y in self.attribute[i]:  # 第 i 個 row (polygon)
                    if int(pos_x * self.resize) > check_w or int(pos_y * self.resize) > check_h:
                        hw_error = True
                        break
                    else:
                        pt = ET.SubElement(polygon, 'pt')
                        x = ET.SubElement(pt, 'x')
                        x.text = str(int(pos_x * self.resize))
                        y = ET.SubElement(pt, 'y')
                        y.text = str(int(pos_y * self.resize))
                
                # polygonDict[name.text] = np.array(self.attribute[i]) * self.resize

            # np.save(self.full_pic_path.rsplit('.')[0] + '_dectect.npy', polygonDict) 
            # print(f'save transfrom matrix to: [{self.full_pic_path.rsplit(".")[0] + "_dectect.npy"}]')
            
            # 檢查是否有超過圖片長寬的點
            if not hw_error:
                tree = ET.ElementTree(root)
                tree.write(self.full_xml_path, encoding="utf-8")
                print(f'save data to: [{self.full_xml_path}]')

                if self.matrix_pix_to_cm is not None:
                    np.save(self.full_pic_path.rsplit('.')[0] + '.npy', self.matrix_pix_to_cm)
                    print(f'save transfrom matrix to: [{self.full_pic_path.rsplit(".")[0] + ".npy"}]')

                self.save_xml_notice = QMessageBox.information(
                    self.centralwidget, 'Save Notice',
                    'You have saved the information about the picture!',
                    QMessageBox.Ok)
            else:
                self.save_xml_notice = QMessageBox.warning(
                    self.centralwidget, 'Save Error',
                    'An error occurred while saving because the marker point exceeded the image size!',
                    QMessageBox.Ok)

        # camera Calibration 畫面
        elif self.MainWindow.centralWidget().objectName() == 'camerawidget':
            if self.camerawidget.image is None:
                self.ShowErrorToStatusbar(f'[ERROR] No Image to Save')
                return

            filename = QFileDialog.getSaveFileName(self.camerawidget, 'Save file', os.getcwd(),
                                                   'Image files (*.jpg *.png)')
            # filename: (filepath: str, image type(same as I write): str)
            # ! NOT select save path
            if not filename[0]:
                self.ShowErrorToStatusbar('[ERROR] Not select path to save picture')
                return
            
            # save to filepath[0]
            print(f'Save picture to {filename[0]}')
            # cv2.imwrite(filename[0], self.camerawidget.image)
            cv2.imencode('.jpg', self.camerawidget.image)[1].tofile(filename[0])
         
            # Openfile at self.centralwidget
            self.change_centralwidget_to(self.centralwidget)
            self.camerawidget.thread.stop()
            self.OpenPictureFile(filename[0])

        else:
            self.ShowErrorToStatusbar(
                f'[ERROR] strange centralwidget name: {self.MainWindow.centralWidget().objectName()}')

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

    # connect to --> self.ButtonTransformation
    def ToTrans(self):
        try :
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

            if len(self.attribute[idx]) != 4:
                self.ShowErrorToStatusbar(f'[ERROR] polygon with node: {self.attribute[idx]}, expected: 4')
                return

            # status is None AND found a polygon
            self.set_status(self.ButtonTransformation, True)

            # 讀取實際去量測的座標(手動輸入的)
            attr_text = self.tableWidget.item(idx, 1).text()

            attr = [e.strip('[](){} \n') for e in attr_text.split(',')]
            # 先用 ',' 作分隔，再去除左右邊的括弧空格 '[](){} \n'

            # 主畫面畫出的四個點(順序要跟實際座標給的順序要一樣 左上右上右下左下)
            src = np.array(self.attribute[i], np.float32) * self.resize
            src = src.reshape(-1, 2)
            print("src: ",src)
            attr = np.float32(attr).reshape((4, 2))
            # calculate the matrix for real world, we will not use it!
            # self.SaveFile()
            self.matrix_pix_to_cm = cv2.getPerspectiveTransform(src, attr)

            # 計算pixel轉成cm的比例
            ratio = 0
            for i in range(0, 3):
                ratio = ratio + self.size(src[i][0], src[i+1][0], src[i][1], src[i+1][1],
                                        attr[i][0], attr[i+1][0], attr[i][1], attr[i+1][1])
            ratio = ratio + self.size(src[0][0], src[3][0], src[0][1], src[3][1],
                                    attr[0][0], attr[3][0], attr[0][1], attr[3][1])
            ratio /= 4
            # 把實際座標(cm)轉成主畫面上(pixel)的座標
            attr = attr * ratio
            # 暫用的轉換矩陣
            matrix = cv2.getPerspectiveTransform(src, attr)

            img_w = self.image.shape[1]
            img_h = self.image.shape[0]
            ori = np.float32([[0, 0], [img_w, 0], [img_w, img_h], [0, img_h]])
            # 利用剛剛的暫用的轉換矩陣算出要平移多少
            ox, oy = self.shift(ori, matrix)
            # 由於他們給的座標是以多邊形中心當原點，但是主畫面的座標是以左上角為原點，因此要平移成一樣的坐標系上
            for i in range(0, 4):
                attr[i][0] = attr[i][0] + ox
                attr[i][1] = attr[i][1] + oy

            width = int(2*ox)
            height = int(2*oy)
            # 計算最終正確的轉換矩陣
            matrix = cv2.getPerspectiveTransform(src, attr)
            
            # 轉換後能完整圖片，且將區塊置中
            result = cv2.warpPerspective(self.image, matrix, (width, height), cv2.INTER_LINEAR,
                                        borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
            
            # 限制matplot show出圖片的大小在(1000,1000)
            fx = 1000 / int(width)
            fy = 1000 / int(height)
            # 算出要縮放多少
            f = min(fx, fy)

            print(int(width)*f, int(height)*f)
            resized = cv2.resize(result, None, fx=f, fy=f,
                                interpolation=cv2.INTER_AREA)
            attr *= f
            # attr = attr.astype(int)  #! prevent error

            print("ATTR: ", attr)
            print("Which polygon: ", idx)
            self.transformPolygonID = idx
            self.transformAttr = attr
            self.transformMatrix = matrix
            self.transformF = f
            # If four element in the array, the polygon will have one less side
            self.arrForPlotX = np.array([attr[0][0], attr[1][0], attr[2][0], attr[3][0],attr[0][0], attr[1][0], attr[2][0], attr[3][0]])
            self.arrForPlotY = np.array([attr[0][1], attr[1][1], attr[2][1], attr[3][1],attr[0][1], attr[1][1], attr[2][1], attr[3][1]])

            self.pyplot = DraggablePolygonMarker(self.MainWindow, resized)
            self.pyplot.setup()
            
            self.set_status(self.ButtonTransformation, False)
            if status_edit == 'edit':
                self.set_status(self.ButtonEdit, True)
        except:
            self.save_xml_notice = QMessageBox.warning(
                self.centralwidget, 'Error', 'An error occurred while transforming.')
            if self.save_xml_notice == QMessageBox.Ok:
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

        reply = QMessageBox.question(self.centralwidget, "刪除", " 刪除這個多邊形? ",
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
        self.SoundClicked.play()
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
        self.SoundError.play()
        print(text)
        self.statusbar.showMessage(text, 3000)

    # ---------------------------------------------------------------- DRAWING POLYGON
    # mouseMoveEvent
    def mouseMove(self, event):
        if not self.LabelPicture.pixmap():
            return

        # map pixel on LabelPicture to pixel on image file
        x = event.pos().x()  # real x point on the image
        y = event.pos().y() - (LabelPictureSize[1] - self.pixHeight) / 2

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
                
                for i, poly in enumerate(self.attribute):
                    for j, point in enumerate(poly):
                        p_x, p_y = point
                        if abs(p_x-x) < ClickedDetectSize and abs(p_y-y) < ClickedDetectSize:
                            # highlight this point: self.attribute[i][j]
                            self.draw_point(p_x, p_y, ClickedDetectSize)

        elif self.status == 'add_poly':
            if self.tracking:
                self.pos_x = event.pos().x() 
                self.pos_y = event.pos().y() - (LabelPictureSize[1] - self.pixHeight) / 2
                self.Draw()
        else:
            pass

    # mouseReleaseEvent
    def mouseRelease(self, event):
        # self.pos_x, self.pos_y = event.pos().x(), event.pos().y() - 450 + pixHeight/2
        if self.status == 'edit':
            # self.LabelPicture.setMouseTracking(True)
            self.ReDraw(update_for_tracking_pixmap=True)
            self.moving_dot = None

    # mousePressEvent
    def getPos(self, event):
        if self.pixHeight is None:
            self.ShowErrorToStatusbar(f'[ERROR] not read a picture yet but clicked [Label region]')
            return

        # real pixmap height
        x = event.pos().x()  # real x point on the image
        y = event.pos().y() - (LabelPictureSize[1] - self.pixHeight) / 2

        if self.status == 'add_poly':
            if len(self.tmp) == 0:
                self.start_x = x
                self.start_y = y
                self.tracking = True

            # 第二個點不能點回第一個點
            if len(self.tmp) == 2 and \
               abs(x-self.start_x) < ClickedDetectSize and\
               abs(y-self.start_y) < ClickedDetectSize:
               self.tmp = []

            self.tmp.append([x, y])
            self.PreviousPair = (x, y)
            
            # 刪掉不小心點兩下的點
            if len(self.tmp) >= 2 and \
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
                # add name and attribute on the tables
                self.AfterPolygon()

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
                        # update_for_tracking_pixmap not important here
                        self.ReDraw(False, except_row=i)
                        # print(f'Edit polygon [{i}]')
                        break
        
        elif self.status == None:
            # Highlight corresponding table row
            print("x: ",x,",y; ",y)
            if len(self.attribute) == 0:
                return  # no polygon to highlight

            p = Point(x, y)
            idx = -1
            for i in range(len(self.attribute)):
                if p.within(Polygon(self.attribute[i])) == True:
                   idx = i
                   break
            if idx != -1:
                self.tableWidget.selectRow(idx)
            else:
                self.tableWidget.clearSelection()
                # ! REDRAW
                self.ReDraw(update_for_tracking_pixmap=False)

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
            p.append(QPoint(x, y))
        pixmap = QPixmap(self.LabelPicture.pixmap())
        qp = QPainter(pixmap)
        pen = QPen(Qt.black, 3)
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
            qp.setBrush(QColor(255, 0, 0, 200))

        qp.drawPolygon(p)
        qp.end()
        self.LabelPicture.setPixmap(pixmap)

    def fun(self):
        self.number = 0
        self.tmp = []

        # random choose a color
        self.index = np.random.randint(len(self.semi_color))  # [0, 7]
        self.color_index.append(self.index)
        self.for_tracking_pixmap = QPixmap(self.LabelPicture.pixmap())

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
        for i in range(0, 4):
            x[i] = abs(x[i])
            y[i] = abs(y[i])
        ox = max(x)
        oy = max(y)
        return ox, oy
    


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
            for pair in self.tmp[1:]:
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

