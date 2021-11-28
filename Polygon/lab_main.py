import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Qt
from lab_UI import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 強制最大化
        self.showMaximized()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

    def closeEvent(self, event):
        self.ui.camerawidget.thread.stop()
        # self.ui.camerawidget.cali_thread.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

# [-1, -1], [1, -1], [1, 1], [-1, 1]
# [-1.00000000000000000000, -1.00000000000000000000], [1.00000000000000000000, -1.00000000000000000000], [1.00000000000000000000, 1.00000000000000000000], [-1.00000000000000000000, 1.00000000000000000000]
# yolo car label: ['bicycle', 'car', 'motorcycle', 'bus', 'train', 'truck']
