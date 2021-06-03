# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project formal.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os
import xml.etree.ElementTree as ET


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(855, 429)

        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(12)
        MainWindow.setFont(font)

		# TITLE functions
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(560, 240, 300, 160))
        font1 = QFont()
        font1.setPointSize(14)
        self.groupBox.setFont(font1)

        self.splitter_2 = QSplitter(self.groupBox)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setGeometry(QRect(20, 40, 261, 101))
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)

		# BUTTON add region
        self.ButtonAddRegion = QPushButton(self.splitter)
        self.ButtonAddRegion.setObjectName(u"ButtonAddRegion")
        self.splitter.addWidget(self.ButtonAddRegion)

		# BUTTON drag
        self.ButtonDrag = QPushButton(self.splitter)
        self.ButtonDrag.setObjectName(u"ButtonDrag")
        self.splitter.addWidget(self.ButtonDrag)

        self.splitter_2.addWidget(self.splitter)
		# BUTTON camera
        self.ButtonCamera = QPushButton(self.splitter_2)
        self.ButtonCamera.setObjectName(u"ButtonCamera")
        self.splitter_2.addWidget(self.ButtonCamera)

		# BUTTON transform
        self.ButtonTransformation = QPushButton(self.splitter_2)
        self.ButtonTransformation.setObjectName(u"ButtonTransformation")
        self.splitter_2.addWidget(self.ButtonTransformation)

		# Table
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(580, 80, 260, 150))
        font2 = QFont()
        font2.setFamily(u"Comic Sans MS")
        font2.setPointSize(12)
        self.tableWidget.setFont(font2)

		# --- Group Box: pic name
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(570, 0, 291, 61))
        self.groupBox_2.setFont(font1)
        self.splitter_3 = QSplitter(self.groupBox_2)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setGeometry(QRect(20, 30, 240, 20))
        self.splitter_3.setOrientation(Qt.Horizontal)

		# useless label, shows words not changed
        self.label = QLabel(self.splitter_3)
        self.label.setObjectName(u"label")
        self.splitter_3.addWidget(self.label)

		# Label name: should change when open file
        self.LabelPictureName = QLabel(self.splitter_3)
        self.LabelPictureName.setObjectName(u"LabelPictureName")
        self.splitter_3.addWidget(self.LabelPictureName)

		# Label: show pic place
        self.LabelPicture = QLabel(self.centralwidget)
        self.LabelPicture.setObjectName(u"LabelPicture")
        self.LabelPicture.setGeometry(QRect(20, 20, 521, 351))
        # if scalable:
        self.LabelPicture.setScaledContents(True)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 855, 24))
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
        self.ButtonDrag.clicked.connect(self.DragMode)
        self.ButtonCamera.clicked.connect(self.CameraMode)
        self.ButtonTransformation.clicked.connect(self.ToTrans)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
		#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
		#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Functions", None))
        self.ButtonAddRegion.setText(QCoreApplication.translate("MainWindow", u"ADD region", None))
		#if QT_CONFIG(shortcut)
        self.ButtonAddRegion.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
		#endif // QT_CONFIG(shortcut)
        self.ButtonDrag.setText(QCoreApplication.translate("MainWindow", u"Drag", None))
        self.ButtonCamera.setText(QCoreApplication.translate("MainWindow", u"Camera / Pause", None))
        self.ButtonTransformation.setText(QCoreApplication.translate("MainWindow", u"Transformation", None))

        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Attribute", None));
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Picture:", None))
        self.LabelPictureName.setText(QCoreApplication.translate("MainWindow", u"picturename.jpg", None))
        self.LabelPicture.setText(QCoreApplication.translate("MainWindow", u"Picture Place", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

	# Used by menu func --> self.actionOpen
    def BrowseFiles(self):
        filename = QFileDialog.getOpenFileName(self.centralwidget, 'Open file', os.getcwd(), 'Image files (*.jpg *.png)')
        # filename: (filepath: str, image type(just like I write): str)
        print(filename)
        self.full_pic_path = filename[0]

        if filename[0]:
            self.LabelPictureName.setText(filename[0].split('/')[-1])
            self.LabelPicture.setPixmap(QPixmap(filename[0]))
        else:
            print('No file select')
        
        # Find XML file
        self.full_xml_path = self.full_pic_path.rsplit('.')[0] + '.xml'
        if os.path.isfile(self.full_xml_path):
            # load data / delete table
            print(f'Find corresponding .xml file for {self.full_pic_path}')
            tree = ET.parse(self.full_xml_path)
            self.root = tree.getroot()

            self.RemoveAllRows()
            
            # fetch data from xml to table
            polyroot = self.root.find('polyroot')
            for obj in polyroot.iter('object'):
                # get data
                name = obj.find('name').text
                attribute = obj.find('attribute').text
                print(f'get obj name: {name}')

                row = self.tableWidget.rowCount()
                self.tableWidget.setRowCount(row + 1)

                # Build empty row
                __qtablewidgetitem0 = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(row, __qtablewidgetitem0)
                # __qtablewidgetitem4.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
                __qtablewidgetitem1 = QTableWidgetItem(name)
                # __qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", name, None));
                self.tableWidget.setItem(row, 0, __qtablewidgetitem1)

                __qtablewidgetitem2 = QTableWidgetItem(attribute)
                # __qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", attribute, None));
                self.tableWidget.setItem(row, 1, __qtablewidgetitem2)

                # polygon = obj.find('polygon')
                # for pt in polygon.iter('pt'):
                #     print('get points: ', end='')
                #     x = pt.find('x').text
                #     y = pt.find('y').text
                #     print(f'(x, y) = ({x}, {y})')
    
    def RemoveAllRows(self):
        for i in range(self.tableWidget.rowCount()-1, -1, -1):
            self.tableWidget.removeRow(i)
    
    # connect to --> ButtonAddRegion
    def AddRegion(self):
        # polygon drawing
        self.add_row()
        
    def add_row(self):
        row = self.tableWidget.rowCount()
        # print(f'add row: {row}')
        self.tableWidget.setRowCount(row + 1)

        # Build empty row
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(row, __qtablewidgetitem3)
        # __qtablewidgetitem4.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
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
    
    # connect to --> self.actionSave
    def SaveFile(self):
        # save data to pic_name.xml (or json?)
        self.root = ET.Element('data')
        polyroot = ET.SubElement(self.root, 'polyroot')
        
        for i in range(self.tableWidget.rowCount()):
            object = ET.SubElement(polyroot, 'object')
            name = ET.SubElement(object, 'name')
            name.text = self.tableWidget.item(i, 0).text()
            attribute = ET.SubElement(object, 'attribute')
            attribute.text = self.tableWidget.item(i, 1).text()
            polygon = ET.SubElement(object, 'polygon')
            for i in range(1, 4+1):
                pt = ET.SubElement(polygon, 'pt')
                x = ET.SubElement(pt, 'x')
                x.text = str(i * 11)
                y = ET.SubElement(pt, 'y')
                y.text = str(i * 22)
        
        tree = ET.ElementTree(self.root)
        tree.write(self.full_xml_path, encoding="utf-8")
        print('save data to:', self.full_xml_path)

    # connect to --> self.ButtonDrag
    def DragMode(self):
        pass
    # connect to --> self.ButtonCamera
    def CameraMode(self):
        pass
    # connect to --> self.ButtonTransformation
    def ToTrans(self):
        pass


