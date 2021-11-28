import sys
import os
from PySide2.QtWidgets import QWidget,QPlainTextEdit, QPushButton, QApplication, QLineEdit, QLabel, QGroupBox, QDialog, QComboBox, QGridLayout, QVBoxLayout
from PySide2.QtGui import QFont

class QuestionDialog(QDialog):
    ComboSizeLimit = 700
    def __init__(self, basicFontSize):
        super().__init__()
        file=open("Polygon/name.txt","r")
        read_file=file.read()
        names=read_file.split("\n")
        COMBO_BOX_ITEM = ['']
        for i in range(len(names)):
            COMBO_BOX_ITEM.append(names[i])
        file.close()
        font = QFont('Arial', basicFontSize)
        
        # --------------------------
        self.LabelName = QLabel('Name:')
        self.LabelAttr = QLabel('Attribute:')
        
        self.A2 = QPlainTextEdit(self)

        self.Q1_Box = QComboBox(self)
        self.Q1_Box.setEditable(True)
        self.Q1_Box.addItems(COMBO_BOX_ITEM)
        self.Q1_Box.setFixedWidth(self.ComboSizeLimit)
        self.A2.setFixedWidth(self.ComboSizeLimit)

        
        # --------- Button ---------
        
        self.OK = QPushButton('OK', self)

        self.Cancel = QPushButton('Cancel', self)

        self.OK.clicked.connect(self.accept)
        self.Cancel.clicked.connect(self.reject)
        
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
        g_layout.addWidget(self.Q1_Box, 0, 1)
        g_layout.addWidget(self.LabelAttr, 1, 0)
        g_layout.addWidget(self.A2, 1, 1, 1, 2)

        self.groupBoxInputs.setLayout(g_layout)

        self.groupBoxBtns = QGroupBox()
        self.groupBoxBtns.setStyleSheet("QGroupBox{ border: 0px; }")

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
        # return (self.A1.text(), self.A2.text())
        return (str(self.Q1_Box.currentText()), self.A2.toPlainText())

class AddressDialog(QDialog):
    ComboSizeLimit = 850
    def __init__(self, basicFontSize):
        super().__init__()

        file=open("Polygon/address.txt","r")
        read_file=file.read()
        names=read_file.split("\n")
        COMBO_BOX_ITEM = ['']
        for i in range(len(names)):
            COMBO_BOX_ITEM.append(names[i])
        file.close()

        font = QFont('Arial', basicFontSize)
        self.setWindowTitle("RTSP Camera")

        self.LabelAddr = QLabel('Address:')

        self.Q1_Box = QComboBox(self)
        self.Q1_Box.setEditable(True)
        self.Q1_Box.addItems(COMBO_BOX_ITEM)
        self.Q1_Box.setFixedWidth(self.ComboSizeLimit)


        self.OK = QPushButton('OK', self)
        self.Cancel = QPushButton('Cancel', self)

        self.OK.clicked.connect(self.accept)
        self.Cancel.clicked.connect(self.reject)
        
        self.Q1_Box.setFont(font)
        self.OK.setFont(font)
        self.Cancel.setFont(font)
        self.LabelAddr.setFont(font)
        #------------ Layout -------------
        self.groupBoxInputs = QGroupBox()
        self.groupBoxInputs.setStyleSheet("QGroupBox{ border: 0px ; }")

        g_layout = QGridLayout()
        g_layout.addWidget(self.LabelAddr, 0, 0)
        g_layout.addWidget(self.Q1_Box, 0, 1)
        self.groupBoxInputs.setLayout(g_layout)

        self.groupBoxBtns = QGroupBox()
        self.groupBoxBtns.setStyleSheet("QGroupBox{ border: 0px; }")

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

    def getInputs(self):
        return str(self.Q1_Box.currentText())


class LoadPickleDialog(QDialog):
    ComboSizeLimit = 850
    def __init__(self, basicFontSize):
        super().__init__()

        # pickles = os.listdir("Polygon/calibration_parameter")
        pickles = [_ for _ in os.listdir("Polygon/calibration_parameter") if _.endswith(".pickle")]
        COMBO_BOX_ITEM = ['']
        for i in range(len(pickles)):
            COMBO_BOX_ITEM.append(pickles[i])#.split(".")[0]

        font = QFont('Arial', basicFontSize)
        self.setWindowTitle("Parameter list")

        self.LabelAddr = QLabel('File:')

        self.Q1_Box = QComboBox(self)
        self.Q1_Box.addItems(COMBO_BOX_ITEM)
        self.Q1_Box.setFixedWidth(self.ComboSizeLimit)


        self.OK = QPushButton('OK', self)
        self.Cancel = QPushButton('Cancel', self)

        self.OK.clicked.connect(self.accept)
        self.Cancel.clicked.connect(self.reject)
        
        self.Q1_Box.setFont(font)
        self.OK.setFont(font)
        self.Cancel.setFont(font)
        self.LabelAddr.setFont(font)
        #------------ Layout -------------
        self.groupBoxInputs = QGroupBox()
        self.groupBoxInputs.setStyleSheet("QGroupBox{ border: 0px ; }")

        g_layout = QGridLayout()
        g_layout.addWidget(self.LabelAddr, 0, 0)
        g_layout.addWidget(self.Q1_Box, 0, 1)
        self.groupBoxInputs.setLayout(g_layout)

        self.groupBoxBtns = QGroupBox()
        self.groupBoxBtns.setStyleSheet("QGroupBox{ border: 0px; }")

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

    def getInputs(self):
        return str(self.Q1_Box.currentText())


class EditPolygonData(QDialog):
    ComboSizeLimit = 700
    def __init__(self, basicFontSize, name, attr):
        super().__init__()

        font = QFont('Arial', basicFontSize)
        # --------------------------
        self.LabelName = QLabel('Name:')
        self.LabelAttr = QLabel('Attribute:')
        
        self.A1 = QLineEdit(self)
        self.A2 = QPlainTextEdit(self)
        self.A1.setText(name)
        self.A2.setPlainText(attr)
        self.A1.setFixedWidth(self.ComboSizeLimit)
        self.A2.setFixedWidth(self.ComboSizeLimit)
        
        # --------- Button ---------
        
        self.OK = QPushButton('OK', self)

        self.Cancel = QPushButton('Cancel', self)

        self.OK.clicked.connect(self.accept)
        self.Cancel.clicked.connect(self.reject)
        
        self.A2.setFont(font)
        self.A1.setFont(font)
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
        g_layout.addWidget(self.LabelAttr, 1, 0)
        g_layout.addWidget(self.A2, 1, 1, 1, 2)

        self.groupBoxInputs.setLayout(g_layout)

        self.groupBoxBtns = QGroupBox()
        self.groupBoxBtns.setStyleSheet("QGroupBox{ border: 0px; }")

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
        # return (self.A1.text(), self.A2.text())
        return (str(self.A1.text()), self.A2.toPlainText())
        
def main():
    app = QApplication(sys.argv)

    ex = QuestionDialog(16)
    a = ex.show()
    # ex = QuestionDialog(16)
    # a = ex.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
