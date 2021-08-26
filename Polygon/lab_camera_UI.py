from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
import numpy as np
import time
import os
from utils import cal_reproject_error, sliding_window_calibrate, scatter_hist
import cv2

from lab_question import AddressDialog

LabelPictureSize = (1500, 900)
ButtonHeight = 40
address=None
img=None
for_saving=None
class calithread(QThread):
    print_error=Signal(str)
    finish_cali=Signal()
    def __init__(self):
        super().__init__()
        
    def run(self):
       
       self.objpoints = []
       self.imgpoints = []
       self.counter=0
       #self.frame_count=20
       self.frame_count=3
       self.slide_threshold=10
       self.corner_x = 7
       self.corner_y = 7
       self.objp = np.zeros((self.corner_x*self.corner_y, 3), np.float32)
       self.objp[:, :2] = np.mgrid[0:self.corner_x, 0:self.corner_y].T.reshape(-1, 2)
       self._width=0
       self._height=0
       
       
       self.running=True
       while(self.running):
        self.print_error.emit("Finish Calibration")
        self.finish_cali.emit()
        break
          
       
    
    def calibrate(self):
       global img
       calibrate_img=img
       gray = cv2.cvtColor(calibrate_img, cv2.COLOR_BGR2GRAY)
       r, corners = cv2.findChessboardCorners(gray, (self.corner_x, self.corner_y), None)
       t=""
       if(r==True):
            self.counter += 1
            t+=("capture success and chessboard is founded, {}/{}".format(self.counter,self.frame_count))
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)
            #above part for finding chessboard
            self._width=calibrate_img.shape[1]
            self._height=calibrate_img.shape[0]
            img_size = (self._width, self._height)
            if self.counter>self.slide_threshold:  #choosing when to do the sliding window
                ret, mtx, dist, rvecs, tvecs, self.imgpoints, self.objpoints, err = sliding_window_calibrate(self.objpoints, self.imgpoints, img_size, self.counter, self.frame_count)
            else:
                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, img_size, None, None)
                err = cal_reproject_error(self.imgpoints,self.objpoints,rvecs,tvecs,mtx,dist)
            t+=("error:{}".format(err))
       else:
           t+=("No chessboard is found in this frame")
       self.print_error.emit(t)
       print("a frame will be captured in three seconds")
   
    def stop(self):
        self.running=False
        self.wait()
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
        self.add=None
        while(self.exit):
            if(self.add!=address):
              if(address=="0" or address=="1"):
                  address=int(address)
              self.cap = cv2.VideoCapture(address)
              if(self.cap.isOpened()):
                  self.connect_yes.emit()
                  break
              else:
                  self.connect_no.emit()
                  self.add=address
        while(self.exit):
          while self._run_flag:
              ret, cv_img = self.cap.read()
              if ret:
                for_saving=cv_img
                rgbImage = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                img=convertToQtFormat
                p = convertToQtFormat.scaled(*LabelPictureSize, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
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
        self.LabelCamera.setStyleSheet("background-color: lightgreen")

        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.groupBox_2 = QGroupBox('Info', self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(title_font) 

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setText("Please click button first.")
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
        self.layout_button.addWidget(self.ButtonConnectCamera, 1)
        # self.layout_button.addWidget(self.ButtonCalibration, 1)
        # self.layout_button.addWidget(self.ButtonPlayPause, 1)
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.ButtonReserveImage, 1)
        self.layout_button.addWidget(self.ButtonChangeQWidget, 1)

        self.layout_info = QVBoxLayout(self.groupBox_2) # for the new line
        self.layout_info.addWidget(self.label) # for the new line
        #---------- layout end --------- 

        self.ButtonConnectCamera.clicked.connect(self.ConnectCamera)
        #self.ButtonPlayPause.clicked.connect(self.PlayPause)
        self.MainWindow=MainWindow
        self.ButtonChangeQWidget.clicked.connect(self.skip)
        self.ButtonReserveImage.clicked.connect(self.reserve)
        self.CameraOpening=False
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_cali)
        self.status="Connect"
        self.saved_img=None
        self.cali_thread=calithread()
        self.started=False
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.connect_yes.connect(self.after_connect)
        self.thread.connect_no.connect(self.connect_error)
        self.MainWindow.ui.menubar.setEnabled(False)
        
    def ConnectCamera(self):
        global LabelPictureSize
        global address
        LabelPictureSize = self.LabelCamera.size().toTuple()
        if(self.status=="Connect"):
           if(not self.CameraOpening):
                ad = AddressDialog(self.BasicFontSize)
                okPressed = ad.exec()
                if okPressed and ad.getInputs() :
                    print("address: " + ad.getInputs())
                    address = ad.getInputs()
                    if(not self.started):
                        self.thread.start()
                        self.started=True
                else :
                    self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] There is no input address')
                    return
        elif(self.status=="PlayPause"):
           self.PlayPause()
    def after_connect(self):
        self.thread.sstart()
        self.CameraOpening=True
        self.label.setText("Start Calibrating...")
        self.timer.start(3000)
    def connect_error(self):
        self.MainWindow.ui.ShowErrorToStatusbar('[ERROR] Connect error')
    def start_cali(self):
        self.ButtonChangeQWidget.hide()
        self.timer.stop()
        self.label.setText("A frame will be captured in three seconds")
        self.cali_thread.start()
        self.cali_thread.print_error.connect(self.change_word)
        self.cali_thread.finish_cali.connect(self.button_change)
        
        
    def button_change(self):
        self.ButtonConnectCamera.setText("Play / Pause")
        self.ButtonReserveImage.show()
        self.ButtonChangeQWidget.show()
        self.ButtonChangeQWidget.setText("Save")
        self.status="PlayPause"
        
    def change_word(self,word):
        self.label.setText(word)
    
    def PlayPause(self):
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
