import sys
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QAction, QLineEdit, QLabel, QFormLayout, QDialog, QComboBox, QGridLayout
from PySide2.QtCore import QRect, QCoreApplication
from PySide2.QtGui import QFont


class QuestionDialog(QDialog):
    def __init__(self):
        super().__init__()
        COMBO_BOX_ITEM = ['', 'TRANS', 'Tree', 'Car']

        self.setFont(QFont('Arial', 18))
        self.setGeometry(QRect(700, 400, 400, 180))

        # --------------------------
        
        self.A1 = QLineEdit(self)
        self.A2 = QLineEdit(self)

        self.Q1_Box = QComboBox(self)
        self.Q1_Box.addItems(COMBO_BOX_ITEM)
        self.Q1_Box.currentIndexChanged.connect(lambda: self.A1.setText(self.Q1_Box.currentText()))

        # --------- Button ---------
        
        self.OK = QPushButton('OK', self)
        self.OK.setGeometry(QRect(110, 120, 100, 40))

        self.Cancel = QPushButton('Cancel', self)
        self.Cancel.setGeometry(QRect(280, 120, 100, 40))

        self.OK.clicked.connect(self.accept)
        self.Cancel.clicked.connect(self.reject)

        #!################################################################
        UPPER_REGION = QWidget(self)
        UPPER_REGION.setGeometry(QRect(0, 0, 400, 100))

        gridLayout = QGridLayout(UPPER_REGION)
        # gridLayout.setGeometry(QRect(0, 0, 400, 120))
        # UPPER_REGION.setLayout(gridLayout)

        ROW = 0
        gridLayout.addWidget(QLabel('Name:'), ROW, 0)
        gridLayout.addWidget(self.A1, ROW, 1)
        gridLayout.addWidget(self.Q1_Box, ROW, 2)

        ROW = 1
        gridLayout.addWidget(QLabel('Attribute:'), ROW, 0)
        gridLayout.addWidget(self.A2, ROW, 1, 1, -1)

        # gridLayout.addWidget(self.OK, 2, 1)
        # gridLayout.addWidget(self.Cancel, 2, 2)
        #!################################################################

    def getInputs(self):
        return (self.A1.text(), self.A2.text())

def main():
    app = QApplication(sys.argv)

    ex = QuestionDialog()
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