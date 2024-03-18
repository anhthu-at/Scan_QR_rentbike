# #CHUYEN BANG INPUT
#
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from PyQt5 import QtCore as qtc
# class login_w(QMainWindow):
#     # submitClicked = qtc.pyqtSignal(str)
#     def __init__(self):
#         super(login_w,self).__init__()
#         uic.loadUi('login.ui',self)
#
#         self.secondWindow = home_w()
#
#         # self.btnLogin.clicked.connect(self.login)
#         self.btnLogin.clicked.connect(self.passingInformation)
#         self.setFixedSize(700, 550)
#
#         # self.name = QLineEdit()
#         # self.age = QLineEdit()
#
#         user = self.mssv.text()
#         psw = self.passw.text()
#
#     def passingInformation(self):
#             self.secondWindow.label_4.setText(self.mssv.text())
#             # self.secondWindow.label_4.setText(user.text())
#             self.secondWindow.displayInfo()
#
# class home_w(QMainWindow):
#     def __init__(self):
#         super(home_w,self).__init__()
#         uic.loadUi('home.ui',self)
#         # self.closeButton.clicked.connect(self.close)
#
#     def displayInfo(self):
#             self.show()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     demo = login_w()
#     demo.show()
#     sys.exit(app.exec())
# #
# #
#
# ################################################
# # CHUYEN BANG LABEL
import sys

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw


class SubWindow(qtw.QWidget):
    submitClicked = qtc.pyqtSignal(str)  # <-- This is the sub window's signal

    def __init__(self, parent=None): #LOGIN
        super().__init__(parent)
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        self.line_edit = qtw.QLineEdit(placeholderText="Enter URL here:")
        self.btn = qtw.QPushButton("Submit")
        layout.addWidget(self.line_edit)
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.confirm)

    def confirm(self):  # <-- Here, the signal is emitted *along with the data we want*
        self.submitClicked.emit(self.line_edit.text())
        self.close()


class MainWindow(qtw.QWidget): #HOME
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sub_window = None  # placeholder attribute for the sub window
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        self.label = qtw.QLabel("Current URL: None")
        self.btn = qtw.QPushButton("Get new URL...")
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.show_sub_window)

    def show_sub_window(self):  # <-- Here, we create *and connect* the sub window's signal to the main window's slot
        self.sub_window = SubWindow()
        self.sub_window.submitClicked.connect(self.on_sub_window_confirm)
        self.sub_window.show()

    def on_sub_window_confirm(self, url):  # <-- This is the main window's slot
        self.label.setText(f"Current URL: {url}")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())