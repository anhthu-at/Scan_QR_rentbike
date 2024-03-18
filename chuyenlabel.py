import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

class login_w(QMainWindow):
    submitClicked = qtc.pyqtSignal(str)
    def __init__(self):
        super(login_w,self).__init__()
        uic.loadUi('login.ui',self)

        # self.btnLogin.clicked.connect(self.passingInformation)
        self.btnLogin.clicked.connect(self.confirm)
        self.setFixedSize(700, 550)


        user = self.mssv.text()
        psw = self.passw.text()

    def confirm(self):  # <-- Here, the signal is emitted *along with the data we want*
            self.submitClicked.emit(self.mssv.text())
            self.close()

class home_w(QMainWindow):
    def __init__(self):
        super(home_w,self).__init__()
        uic.loadUi('home.ui',self)

        self.label_4 = qtw.QLabel("Current URL: None")