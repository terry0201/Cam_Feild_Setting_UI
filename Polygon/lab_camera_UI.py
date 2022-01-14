from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
import numpy as np
import time
import os
from utils import *
import cv2

from lab_question import AddressDialog, LoadPickleDialog

LabelPictureSize = (1500, 900)
ButtonHeight = 40
address=None
img=None
for_saving=None
cv_img = np.array([None])
Cali_Fixed_Param = None
Is_Finish_Alibrate = False

        
class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    connect_yes = Signal()
    connect_no = Signal()
    def __init__(self):
        super().__init__()
        self._run_flag = False
        self.exit=True
    def run(self):
        # capture from web cam
        global LabelPictureSize 
        global img
        global for_saving
        global address
        global cv_img
        global Is_Finish_Alibrate
        global Cali_Fixed_Param
        self.add=None
        do_cali = False
        while(self.exit):
            if(self.add!=address):
              if(address=="0" or address=="1"):
                  address=int(address)
              self.cap = cv2.VideoCapture(address)
              fps = self.cap.get(cv2.CAP_PROP_FPS)
              threadn = cv2.getNumberOfCPUs()
              print(fps)
              print(threadn)
            #   self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 20)
              if(self.cap.isOpened()):
                  self.connect_yes.emit()
                  break
              else:
                  self.connect_no.emit()
                  self.add = address
        while(self.exit):
            while self._run_flag:
                do_cali = False
                ret, cv_img = self.cap.read()
                if ret:
                    # if Is_Finish_Alibrate:
                    #     cv_img = get_new_calibrate_img(cv_img, Cali_Fixed_Param)
                    #     # pass
                    # self.msleep(10)
                    for_saving = cv_img
                    rgbImage = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    img=convertToQtFormat
                    p = convertToQtFormat.scaled(*LabelPictureSize, Qt.KeepAspectRatio)
                    self.change_pixmap_signal.emit(p)
            # TODO: WHILE? IF? cvimg判斷現在很醜
            if not self._run_flag and cv_img.any()!=None and not do_cali:
                cv_img = get_new_calibrate_img(cv_img, Cali_Fixed_Param)
                print(cv_img)
                for_saving = cv_img
                rgbImage = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                img=convertToQtFormat
                p = convertToQtFormat.scaled(*LabelPictureSize, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
                do_cali = True
        # shut down capture system
        self.cap.release()

    def stop(self):
        #Sets run flag to False and waits for thread to finish
        self._run_flag = False
        self.exit=False
        self.wait()
    def sstop(self):
        self._run_flag = False
    def sstart(self):
        self._run_flag = True

class CameraWidget(QWidget):
    def __init__(self, centralwidget):
        super().__init__()
        self.centralwidget = centralwidget
    def setupUi(self, MainWindow, basicFontSize):
        self.setObjectName(u"camerawidget")
        self.BasicFontSize = basicFontSize
        basic_font = QFont(u"Arial", basicFontSize)
        title_font = QFont(u"Arial", basicFontSize + 2)
        self.setFont(basic_font) 

        self.LabelCamera = QLabel('Label to show Camera', self)
        self.LabelCamera.setObjectName(u"LabelCamera")
        # self.LabelCamera.setStyleSheet("background-color: lightgreen")

        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.groupBox_2 = QGroupBox('Info', self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(title_font) 

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setText('Connect Camera is for connecting camera.\nOpen Calibration parameters  is for open pickle file.\nStart Calibration  is for opening camera to calibrate.')
        self.label.move(20, 30)
        self.label.setFont(basic_font)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignJustify) # Qt.AlignTop

        self.groupBox = QGroupBox('Functions', self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(title_font)
        
        # Buttons: Connect Camera | Correction | Play Pause | ... | Skip
        self.ButtonConnectCamera = QPushButton('Connect Camera', self.groupBox)
        self.ButtonConnectCamera.setObjectName(u"ButtonConnectCamera")
        self.ButtonConnectCamera.setFont(basic_font)

        self.ButtonOpenPickle = QPushButton('Open Calibration parameters', self.groupBox)
        self.ButtonOpenPickle.setObjectName(u"ButtonOpenPickle")
        self.ButtonOpenPickle.setFont(basic_font)

        self.ButtonStartCalibration = QPushButton('Start Calibration', self.groupBox)
        self.ButtonStartCalibration.setObjectName(u"ButtonStartCalibration")
        self.ButtonStartCalibration.setFont(basic_font)
        
        self.ButtonChangeQWidget = QPushButton('Skip', self.groupBox)
        self.ButtonChangeQWidget.setObjectName(u"ButtonChangeQWidget")
        self.ButtonChangeQWidget.setFont(basic_font)
        
        self.ButtonReserveImage = QPushButton('Reserve Image',self.groupBox)
        self.ButtonReserveImage.setObjectName(u"ButtonReserveImage")
        self.ButtonReserveImage.setFont(basic_font)
        self.ButtonReserveImage.hide()

        #---------- layout begin--------- 
        self.main_layout = QHBoxLayout(self)  
        self.main_layout.setObjectName(u"main_layout")  
        self.main_layout.addWidget(self.LabelCamera, 8)  
        self.main_layout.addWidget(self.frame, 2)  

        self.layout_frame = QVBoxLayout(self.frame) 
        self.layout_frame.setObjectName(u"layout_frame")
        self.layout_frame.addWidget(self.groupBox_2, 4) 
        self.layout_frame.addWidget(self.groupBox, 5) 

        self.layout_button = QVBoxLayout(self.groupBox) 
        self.layout_button.setObjectName(u"layout_button")
        self.layout_button.addWidget(self.ButtonOpenPickle, 1)
        self.layout_button.addWidget(self.ButtonConnectCamera, 1)
        self.layout_button.addWidget(self.ButtonStartCalibration, 1)
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.ButtonReserveImage, 1)
        self.layout_button.addWidget(self.ButtonChangeQWidget, 1)

        self.layout_info = QVBoxLayout(self.groupBox_2) # for the new line
        self.layout_info.addWidget(self.label) # for the new line
        #---------- layout end --------- 

        self.ButtonConnectCamera.clicked.connect(self.ConnectCamera)
        self.ButtonOpenPickle.clicked.connect(self.OpenPickle)
        self.ButtonStartCalibration.clicked.connect(self.StartCalibration)

        self.MainWindow=MainWindow
        self.ButtonChangeQWidget.clicked.connect(self.skip)
        self.ButtonReserveImage.clicked.connect(self.reserve)
        self.CameraOpening=False
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_cali)
        self.status="Connect"
        self.saved_img=None
        # self.cali_thread=calithread()
        self.started=False
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.connect_yes.connect(self.after_connect)
        self.thread.connect_no.connect(self.connect_error)
        self.MainWindow.ui.menubar.setEnabled(False)
        self.cali_param = None

    def OpenPickle(self):
        global Cali_Fixed_Param
        pickles = LoadPickleDialog(self.BasicFontSize)
        okPressed = pickles.exec()
        if okPressed and pickles.getInputs() :
            print("pickle name: " + pickles.getInputs())
            pickle_file_name = pickles.getInputs()
            self.cali_param = open_camera_pickle(pickle_file_name)
            Cali_Fixed_Param = open_camera_pickle(pickle_file_name)
            print(self.cali_param)
            self.change_word("Open a pickle file named {}.".format(pickle_file_name))
        else :
            self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] There is no input pickle file.')
            return


    def StartCalibration(self):
        global address
        ad = AddressDialog(self.BasicFontSize)
        okPressed = ad.exec()
        if okPressed and ad.getInputs() :
            print("address: " + ad.getInputs())
            address = ad.getInputs()
            if(address=="0" or address=="1"):
                address = int(address)
            self.capture_param = capture(input_address=address)
            save_fixed_path = os.getcwd() + '\Polygon\calibration_parameter'
            pickle_filename = QFileDialog.getSaveFileName(self, 'Save file', save_fixed_path,
                             'Pickle files (*.pickle)')
            if not pickle_filename[0]:
                self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] Not select path to save pickle file.')
                return
            save_file = open(pickle_filename[0],'wb')
            pickle.dump(self.capture_param, save_file)   
            # print('Save picture to {}'.format(pickle_filename[0]))
            self.change_word('Save pickle to {}'.format(pickle_filename[0]))
        else :
            self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] There is no input pickle name.')
            return


    def ConnectCamera(self):
        global LabelPictureSize
        global address
        LabelPictureSize = self.LabelCamera.size().toTuple()
        if(self.status=="Connect"):
            if(not self.CameraOpening and self.cali_param):
                ad = AddressDialog(self.BasicFontSize)
                okPressed = ad.exec()
                if okPressed and ad.getInputs() :
                    print("address: " + ad.getInputs())
                    address = ad.getInputs()
                    if(not self.started):
                        self.thread.start()
                        self.started=True
                        self.change_word("Open camera...")
                else :
                    self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] There is no input address')
                    return
            else:
                self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] There is no calibration param.')
                return 
        elif(self.status=="PlayPause"):
           self.PlayPause()
    
    def after_connect(self):
        self.thread.sstart()
        self.CameraOpening=True
        self.start_cali()


    def connect_error(self):
        self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] Connect error')
    
    def start_cali(self):
        global Is_Finish_Alibrate
        global address
        global Cali_Fixed_Param
        self.ButtonChangeQWidget.hide()
        self.ButtonOpenPickle.hide()
        self.ButtonStartCalibration.hide()
        self.timer.stop()

        self.button_change()
        self.change_word("Finish!")

        
        
    def button_change(self):
        self.ButtonConnectCamera.setText("Play / Pause")
        self.ButtonReserveImage.show()
        self.ButtonChangeQWidget.show()
        self.ButtonChangeQWidget.setText("Save")
        self.status="PlayPause"
        
    def change_word(self,word):
        self.label.setText(word)
    
    def PlayPause(self):
        global LabelPictureSize 
        global img
        global for_saving
        global cv_img
        if(self.CameraOpening):
            self.thread.sstop()
            self.CameraOpening=False
        else:
             self.thread.sstart()
             self.CameraOpening=True
             
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.LabelCamera.setPixmap(QPixmap.fromImage(cv_img))
    

    def skip(self):
        from lab_UI import resetLabelPictureSize
        resetLabelPictureSize(self.LabelCamera.size().toTuple())
        if(self.status=="Connect"):
           self.MainWindow.setCentralWidget(self.centralwidget)
           self.MainWindow.ui.menubar.setEnabled(True)
           self.thread.stop()
           print('LabelPictureSize:', self.LabelCamera.size())  
        else:
           self.save()
           
    def reserve(self):
        global img
        global for_saving
        print(self.CameraOpening)
        if(not self.CameraOpening):
            self.saved_img=for_saving
            tt=img
            g=self.label.size().toTuple()
            ttt=tt.scaled(*g, Qt.KeepAspectRatio)
            tx=QPixmap.fromImage(ttt)
            self.label.setPixmap(tx)
        elif(self.CameraOpening):
            self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] Reserve image while playing')
    
    def save(self):
        if self.saved_img is None:
            self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] No Image to Save')
            return
        filename = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(),
                                                   'Image files (*.jpg *.png)')
        if not filename[0]:
            self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] Not select path to save picture')
            return
            
        print(f'Save picture to {filename[0]}')
        cv2.imencode('.jpg', self.saved_img)[1].tofile(filename[0])
        self.thread.stop()

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.MainWindow.ui.menubar.setEnabled(True)
        self.MainWindow.ui.OpenPictureFile(filename[0])
