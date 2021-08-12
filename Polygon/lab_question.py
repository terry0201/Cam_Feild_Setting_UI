import sys
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QAction, QLineEdit, QLabel, QFormLayout, QDialog, QComboBox, QGridLayout
from PySide2.QtCore import QRect, QCoreApplication
from PySide2.QtGui import QFont
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class QuestionDialog(QDialog):
    def __init__(self, basicFontSize):
        super().__init__()
        COMBO_BOX_ITEM = ['', 'TRANS', 'Tree', 'Car']
        font = QFont('Arial', basicFontSize)
        # self.setFixedSize(400, 180)
        
        # --------------------------
        self.LabelName = QLabel('Name:')
        self.LabelAttr = QLabel('Attribute:')
        
        self.A1 = QLineEdit(self)
        self.A2 = QLineEdit(self)

        self.Q1_Box = QComboBox(self)
        self.Q1_Box.addItems(COMBO_BOX_ITEM)
        self.Q1_Box.currentIndexChanged.connect(lambda: self.A1.setText(self.Q1_Box.currentText()))

        # --------- Button ---------
        
        self.OK = QPushButton('OK', self)
        # self.OK.setFixedSize(100, 40)

        self.Cancel = QPushButton('Cancel', self)
        # self.Cancel.setFixedSize(100, 40)

        self.OK.clicked.connect(self.accept)
        self.Cancel.clicked.connect(self.reject)
        
        self.A1.setFont(font)
        self.A2.setFont(font)
        self.Q1_Box.setFont(font)
        self.OK.setFont(font)
        self.Cancel.setFont(font)
        self.LabelName.setFont(font)
        self.LabelAttr.setFont(font)
        #!################################################################
        self.groupBoxInputs = QGroupBox()
        self.groupBoxInputs.setStyleSheet("QGroupBox{ border: 0px ; }")

        g_layout = QGridLayout()
        g_layout.addWidget(self.LabelName, 0, 0)
        g_layout.addWidget(self.A1, 0, 1)
        g_layout.addWidget(self.Q1_Box, 0, 2)
        g_layout.addWidget(self.LabelAttr, 1, 0)
        g_layout.addWidget(self.A2, 1, 1, 1, 2)

        self.groupBoxInputs.setLayout(g_layout)

        self.groupBoxBtns = QGroupBox()
        self.groupBoxBtns.setStyleSheet("QGroupBox{ border: 0px; }")
        # self.groupBoxBtns.setFixedWidth(self.groupBoxBtns.width()//2)

        forSpacing1 = QWidget()
        forSpacing2 = QWidget()
        g2_layout = QGridLayout()
        g2_layout.addWidget(forSpacing1, 0, 0)
        g2_layout.addWidget(self.OK, 0, 1)
        g2_layout.addWidget(self.Cancel, 0, 2)
        g2_layout.addWidget(forSpacing2, 0, 3)
        self.groupBoxBtns.setLayout(g2_layout)

        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBoxInputs)
        vbox.addWidget(self.groupBoxBtns)
        self.setLayout(vbox)

        #!################################################################

    def getInputs(self):
        return (self.A1.text(), self.A2.text())
    
def main():
    app = QApplication(sys.argv)

    ex = QuestionDialog(16)
    a = ex.show()
    
    if a == QDialog.Accepted:
        print('accepted!')
    elif a == QDialog.Rejected:
        print('rejected!')

    print(ex.getInputs())

    # ex.setGeometry(800, 600, 200, 200)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()