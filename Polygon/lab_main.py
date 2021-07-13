import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtCore import QFile, Qt
from lab_UI2 import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 強制最大化
        self.showMaximized()
        # self.setFixedSize(1920, 1280)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# [-1, -1], [1, -1], [1, 1], [-1, 1]
