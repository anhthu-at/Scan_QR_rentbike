import binascii
import sys

import pyzbar.pyzbar
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qrcode
import cv2
import MySQLdb as mdb
from datetime import datetime, timedelta
from pyzbar.pyzbar import decode
import numpy as np


def connectDB():
    db = mdb.connect(
        'localhost',
        'root',
        '',
        'qr')
    return db


# CUA SO LOGIN
class login_w(QMainWindow):
    def __init__(self):
        super(login_w, self).__init__()
        uic.loadUi('login.ui', self)

        self.secondWindow = home_w()
        self.thirdWindow = getqr_w()

        self.btnLogin.clicked.connect(self.login)
        self.btnDangky.clicked.connect(self.dangky)

        self.setFixedSize(700, 550)

    # XU KY DANG KY
    def dangky(self):
        if self:
            QMessageBox.information(self, "Registe output", "Register success")
            withget.setCurrentIndex(5)
        else:
            QMessageBox.information(self, "Registe output", "Registe fail")

    # XU LY ENTER SE LOGIN VAO HOME
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.login()

    # XU LY BUTTON DANG NHAP
    def login(self):
        user = self.mssv.text()
        psw = self.passw.text()
        db = connectDB()
        query = db.cursor()
        query.execute("SELECT * FROM user WHERE MS = '" + user + "' and password = '" + psw + "' ")
        test = query.fetchone()
        if test:
            if test[4] == "admin":
                QMessageBox.information(self, "Login output", "Login ADMIN")

                withget.setCurrentIndex(1)
                # self.secondWindow.label_4.setText(self.mssv.text())
                # self.secondWindow.displayInfo()
                # self.close()
            else:
                QMessageBox.information(self, "Login output", "Login USER")

                self.thirdWindow.label_6.setText(self.mssv.text())
                self.thirdWindow.displayInfo()
                self.close()
        # KIEM TRA LAI HAM NHAP KHI NHAP SAI PHAI THONG BAO NHAP SAI
        else:
            QMessageBox.information(self, "Login output", "Login fail")


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h, w, c = img.shape
            step = c * w

            qImg = QImage(img.data, w, h, step, QImage.Format.Format_RGB888)

            # decodes = pyzbar.pyzbar.decode(img)
            for barcode in decode(img):
                myData = barcode.data.decode("utf-8")
                # myData = barcode.data.encode('cp1258').decode('utf-8')
                # myData = binascii.unhexlify(barcode.data).decode('unicode-escape')
                pts = np.array([barcode.polygon], np.int32)

                # sap xep thanh ma tran -1 co the la 1 ma tran 1 dong 2 cot
                pts = pts.reshape((-1, 1, 2))
                # ve hinh vuong khi nhan ra qrcode
                cv2.polylines(img, [pts], True, (255, 0, 255), 3)
                pts2 = barcode.rect

                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)

                # print(myData)
                # if len(myData) > 0:
                #     break
                chuoikq = myData.split("|")
                self.parent().getDatafromQR(chuoikq, cap)

            self.parent().label.setPixmap(QPixmap.fromImage(qImg))


# CUA SO DANG KY CHO KHACH BEN NGOAI
class dangky_w(QMainWindow):
    def __init__(self):
        super(dangky_w, self).__init__()
        uic.loadUi('passdata.ui', self)
        self.th = Thread(self)

        # self.btnOpen.clicked.connect(self.openCam)
        self.btnOpen.clicked.connect(lambda _: self.th.start())
        self.btnStop.clicked.connect(self.stopCam)
        self.btnOK.clicked.connect(self.dangky)
        self.cam = None

    def stopCam(self):
        if self.cam:
            QMessageBox.information(self, "Stop output", "Stop success")
            self.cam.release()
            self.th.exit()
        else:
            QMessageBox.information(self, "Stop output", "Stop fail")

    def openCam(self):
        pass
        # self.cap.set(3, 640)
        # self.cap.set(4, 480)
        #
        # while True:
        #     ret, img = self.cap.read()
        #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #
        #     h, w, c = img.shape
        #     step = c * w
        #
        #     qImg = QImage(img.data, w, h, step, QImage.Format.Format_RGB888)
        #
        #     # decodes = pyzbar.pyzbar.decode(img)
        #     for barcode in decode(img):
        #         myData = barcode.data.decode("utf-8")
        #         # myData = barcode.data.encode('cp1258').decode('utf-8')
        #         # myData = binascii.unhexlify(barcode.data).decode('unicode-escape')
        #         pts = np.array([barcode.polygon], np.int32)
        #
        #         # sap xep thanh ma tran -1 co the la 1 ma tran 1 dong 2 cot
        #         pts = pts.reshape((-1, 1, 2))
        #         # ve hinh vuong khi nhan ra qrcode
        #         cv2.polylines(img, [pts], True, (255, 0, 255), 3)
        #         pts2 = barcode.rect
        #
        #         cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)
        #
        #         print(myData)
        #         # if len(myData) > 0:
        #         #     break
        #         # chuoikq = myData.split("|")
        #         #
        #         # self.getDatafromQR(chuoikq)
        #
        #     self.label.setPixmap(QPixmap.fromImage(qImg))

    def getDatafromQR(self, maso_qr, cam):
        self.cam = cam
        maso = maso_qr[0]
        hoten = maso_qr[2]
        ngaysinh = maso_qr[3]
        gioitinh = maso_qr[4]
        diachi = maso_qr[5]

        con = connectDB()
        cursor = con.cursor()
        sql = "SELECT * FROM user WHERE MS = '" + maso + "' and HoTen = '" + hoten + "'"
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) > 0:
            QMessageBox.information(self, "Register out", "Register is values")
        else:
            QMessageBox.information(self, "Register in", "Scan QR success")
            self.editCCCD.setText(maso)
            self.editTen.setText(hoten)
            self.editDiachi.setText(diachi)
            self.editPhai.setText(gioitinh)
            self.editNgay.setText(ngaysinh)

    def dangky(self):
        maso = self.editCCCD.text()
        hoten = self.editTen.text()
        sdt = self.editSDT.text()
        psw = self.editPass.text()
        chucnang = ""
        if self.cbThue.isChecked() == 1:
            chucnang = "khach"
        elif self.cbAdmin.isChecked() == 1:
            chucnang = "admin"

        con = connectDB()
        cursor = con.cursor()
        sql = "INSERT INTO user (MS, HoTen, SDT, password, chucnang) VALUES ('" + maso + "','" + hoten + "','" + sdt + "','" + psw + "','" + chucnang + "')"
        cursor.execute(sql)
        con.commit()
        cursor.close()
        if self:
            QMessageBox.information(self, "Register out", "Register success")
            withget.setCurrentIndex(0)
        else:
            QMessageBox.information(self, "Register out", "Register fail")


# CUA SO HOME
class home_w(QMainWindow):
    def __init__(self):
        super(home_w, self).__init__()
        uic.loadUi('home.ui', self)

        # ADIMIN
        self.btnsetting.clicked.connect(self.setting)
        self.btnInfor.clicked.connect(self.infor)
        # XU LY BUTTON CHUC NANG

    def displayInfo(self):
        self.show()

    # ADMIN
    def setting(self):
        if self:
            QMessageBox.information(self, "Setting output", "Setting success")
            withget.setCurrentIndex(2)
        else:
            QMessageBox.information(self, "Setting output", "Setting fail")

    def infor(self):
        if self:
            QMessageBox.information(self, "Setting output", "Update infor success")
            withget.setCurrentIndex(4)
        else:
            QMessageBox.information(self, "Setting output", "Update infor fail")


# THEM XE VAO BANG THU CONG GHI BANG CHU
class add_w(QMainWindow):
    def __init__(self):
        super(add_w, self).__init__()
        uic.loadUi('chucnang.ui', self)
        self.btnAdd.clicked.connect(self.addxe)
        self.btnExit.clicked.connect(self.back)
        self.btnFind.clicked.connect(self.search)
        self.btnDelete.clicked.connect(self.delete)

    # XU LY BUTTON CHUC NANG THEM
    def addxe(self):
        numberXe = self.edtMaxe.text()
        address = self.edtDau.text()

        if numberXe == '' and address == '':
            QMessageBox.information(self, "Add output", "Add fail")

        db = connectDB()
        query = db.cursor()
        query.execute("SELECT * FROM xedap WHERE Ma_xe = '" + numberXe + "' and Diadiem_dau = '" + address + "'")
        test = query.fetchone()
        print(test)
        if test:
            QMessageBox.information(self, "Add output", "Number is values")
        else:
            query.execute(
                "INSERT INTO xedap (Ma_Xe, Diadiem_dau, Trang_thai) VALUES ('" + numberXe + "','" + address + "','0')")
            db.commit()
            QMessageBox.information(self, "Add output", "Add success")

    # XU LY BUTTON CHUC NANG XOA
    def delete(self):
        numberXe = self.edtMaxe.text()
        address = self.edtDau.text()
        db = connectDB()
        query = db.cursor()
        query.execute("SELECT * FROM xedap WHERE Ma_Xe = '" + numberXe + "' and Diadiem_dau = '" + address + "' ")
        test = query.fetchone()
        if test:
            query.execute("DELETE FROM xedap WHERE Ma_xe = '" + numberXe + "'")
            db.commit()
            QMessageBox.information(self, "Delete output", "Delete success")
        else:
            QMessageBox.information(self, "Delete output", "Delete fail")

    def search(self):
        numberXe = self.edtMaxe.text()
        address = self.edtDau.text()
        db = connectDB()
        query = db.cursor()
        query.execute("SELECT * FROM xedap WHERE Ma_Xe = '" + numberXe + "' or Diadiem_dau = '" + address + "' ")
        test = query.fetchone()
        if test:
            if test[0] == numberXe:
                sql = ("SELECT * FROM xedap WHERE Ma_xe = '" + numberXe + "'")
                query.execute(sql)
                result = query.fetchall()
                for row in result:
                    print(row)
                    self.label_8.setText(str(row[0]))
                    self.label_9.setText(str(row[1]))
                    self.label_10.setText(str(row[2]))

                db.commit()
                QMessageBox.information(self, "Search output", "Search success")

            elif test[1] == address:
                sql = ("SELECT * FROM xedap WHERE Diadiem_dau = '" + address + "'")
                query.execute(sql)
                result = query.fetchall()
                for row in result:
                    print(row)
                    self.label_8.setText(str(row[0]))
                    self.label_9.setText(str(row[1]))
                    self.label_10.setText(str(row[2]))

                db.commit()
                QMessageBox.information(self, "Search output", "Search success")

        else:
            QMessageBox.information(self, "Search output", "Search fail")

    # XU LY BUTTON CHUC NANG THOAT
    def back(self):
        if self:
            QMessageBox.information(self, "Buying output", "Back success")
            withget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, "Buying output", "Back fail")


# THEM XE VA TAO QR CHO XE
class taoqrchoxe_w(QMainWindow):
    def __init__(self):
        super(taoqrchoxe_w, self).__init__()
        uic.loadUi('taoqr_choxe.ui', self)

        self.current_file = ""
        self.actionSave.triggered.connect(self.save_img)
        self.actionLoad.triggered.connect(self.load_img)
        self.actionExit.triggered.connect(self.exit_img)

        self.btnQR.clicked.connect(self.creat_QR)
        self.btnRead.clicked.connect(self.read_QR)

    def load_img(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All File (*)",
                                                  options=options)

        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(300, 300)
            self.QR.setScaledContents(True)
            self.QR.setPixmap(pixmap)

    def save_img(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG (*.png)",
                                                  options=options)
        if filename != "":
            img = self.QR.pixmap()
            img.save(filename, "PNG")

    def exit_img(self):
        if self:
            QMessageBox.information(self, "Buying output", "Back success")
            withget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, "Buying output", "Back fail")

    def creat_QR(self):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=20,
                           border=2)
        qr.add_data(self.edtContent.toPlainText())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("currentqr.png")
        pixmap = QtGui.QPixmap("currentqr.png")
        pixmap = pixmap.scaled(300, 300)
        self.QR.setScaledContents(True)
        self.QR.setPixmap(pixmap)

    def read_QR(self):
        img = cv2.imread(self.current_file)
        detector = cv2.QRCodeDetector()
        data, _, _, = detector.detectAndDecode(img)
        self.edtContent.setText(data)


# CHON HINH THUC THUE XE THEO THOI GIAN (CO THE BO DUOC)
class getqr_w(QMainWindow):
    def __init__(self):
        super(getqr_w, self).__init__()
        uic.loadUi('getdata.ui', self)

        self.secondWindow = thue_w()

        self.btnHuy.clicked.connect(self.back)
        self.btnThue.clicked.connect(self.thue)
        self.btnMocam.clicked.connect(self.openCam)
        self.btnStop.clicked.connect(self.stopCam)
        # self.btnThue.clicked.connect(self.passingInformation)

    def displayInfo(self):
        self.show()

    def stopCam(self):
        if self:
            QMessageBox.information(self, "Stop output", "Stop success")
            # self.cap.release()
        else:
            QMessageBox.information(self, "Stop output", "Stop fail")

    def thue(self):
        numberXe = self.editNumberxe.text()
        addressXe = self.editAddress.text()

        # HAM TINH THOI GIAN CHO THUE
        db = connectDB()
        cursor = db.cursor()

        # HAM KT TRANG THAI XE TRUOC KHI THUE
        # CAN SUA CHO NAY KHI THUE PHAI CAP NHAT BEN BANG CSDL

        sql = "SELECT xedap.Ma_xe, xedap.Trang_thai FROM xedap"
        cursor.execute(sql)
        result = cursor.fetchall()

        # HAM KT TRANG THAI CUA XEDAP
        for row in result:
            checkXe = row[0]
            checkState = row[1]
            if numberXe == checkXe:
                if checkState == '1':
                    msg = QtWidgets.QMessageBox()
                    msg.setInformativeText(f'XE DA DUOC THUE')
                    msg.exec()
                    break
                else:

                    # CO THE THAY DOI THONG BAO VA HOI CO MUON THUE KHONG
                    # THUE SE CAP NHAT GIO
                    ret = QMessageBox.question(self, 'MessageBox', "XE TRONG. BAN MUON THUE XE?",
                                               QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                               QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                        # CHINH SUA CHO NAY
                        self.passingInformation()
                        break

    def passingInformation(self):
        self.secondWindow.edtNumber.setText(self.editNumberxe.text())
        self.secondWindow.edtAddress.setText(self.editAddress.text())
        self.secondWindow.label_7.setText(self.label_6.text())
        self.secondWindow.displayInfo()

    def back(self):
        if self:
            QMessageBox.information(self, "Buying output", "Back success")
            withget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, "Buying output", "Back fail")

    def openCam(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        while True:
            ret, img = self.cap.read()

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h, w, c = img.shape
            step = c * w

            qImg = QImage(img.data, w, h, step, QImage.Format.Format_RGB888)

            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')

                pts = np.array([barcode.polygon], np.int32)

                # sap xep thanh ma tran -1 co the la 1 ma tran 1 dong 2 cot
                pts = pts.reshape((-1, 1, 2))
                # ve hinh vuong khi nhan ra qrcode
                cv2.polylines(img, [pts], True, (255, 0, 255), 3)
                pts2 = barcode.rect

                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)

                # print(myData, flush=True)
                maxe = myData[13:]

                # print(maxe)
                self.getDatafromQR(maxe)

            self.label_4.setPixmap(QPixmap.fromImage(qImg))

            if cv2.waitKey(1) == ord('q'):
                break

    def getDatafromQR(self, maxe_qr):
        con = connectDB()
        cursor = con.cursor()
        sql = "SELECT * FROM xedap WHERE Ma_Xe = %s"
        cursor.execute(sql, (maxe_qr,))
        result = cursor.fetchall()

        for row in result:
            maxe = row[0]
            if maxe == maxe_qr:
                diadiem = row[1]
                self.editNumberxe.setText(maxe)
                self.editAddress.setText(diadiem)


class thue_w(QMainWindow):
    def __init__(self):
        super(thue_w, self).__init__()
        uic.loadUi('luachon_thue.ui', self)
        self.tinh_tien.clicked.connect(self.tinhtien)
        self.btnBack.clicked.connect(self.back)

    def displayInfo(self):
        self.show()

    def back(self):
        if self:
            QMessageBox.information(self, "Buying output", "Back success")
            withget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, "Buying output", "Back fail")

        # HAM TINH TIEN CAC DICH VU

    def tinhtien(self):
        numberXe = self.edtNumber.text()
        addressXe = self.edtAddress.text()

        print("Ma xe: ", self.edtNumber.text())
        print("Dia diem dau: ", self.edtAddress.text())

        # # HAM THEM THOI GIAN THUE (TACH RA VIET HAM )
        self.updateTime()

    def updateTime(self):
        numberXe = self.edtNumber.text()
        addressXe = self.edtAddress.text()
        print(numberXe)

        db = connectDB()
        cursor = db.cursor()
        sql = "SELECT * FROM bang_gia"
        cursor.execute(sql, )
        result = cursor.fetchall()

        # CAU IF NEU CHECK VAO O LUA CHON THI BANG 1
        # CON KHONG CHECK THI == 0

        total = (0 if self.hours.isChecked() == 0 else result[0][1]) \
                + (0 if self.day.isChecked() == 0 else result[1][1]) \
                + (0 if self.month.isChecked() == 0 else result[2][1]) \
                + (0 if self.week.isChecked() == 0 else result[3][1]) \

        print(total)

        loaithue = ""
        if self.hours.isChecked() == 1:
            loaithue = "Gio"
            print("1")
        elif self.day.isChecked() == 1:
            loaithue = "Ngay"
            print("2")
        elif self.month.isChecked() == 1:
            loaithue = "Thang"
            print("3")
        elif self.week.isChecked() == 1:
            loaithue = "Tuan"
            print("4")
        else:
            print("LOI")

        mssv = self.label_7.text()

        print(mssv)

        sql = "INSERT INTO thue (Mahieu_thue, Ma_xe, Loai_thue, Gio_thue, Gio_hethan) VALUES ('','"+numberXe+"','"+mssv+ "','"+loaithue+"',NOW(),'NULL')"
        cursor.execute(sql)
        result = cursor.fetchall()

        # # HAM TINH THOI GIAN HET HAN THUE
        # # SUA CHO NAY
        sql = "UPDATE thue SET Gio_Hethan = %s WHERE Ma_Xe = %s"

        now = datetime.now()
        date_in = now.strftime("%Y/%m/%d  %H:%M:%S")
        if (self.day.isChecked()):
            date_out = now + timedelta(days=1)
        elif self.week.isChecked():
            date_out = now + timedelta(days=7)
        elif self.month.isChecked():
            date_out = now + timedelta(days=30)
        else:
            date_out = now + timedelta(hours=1)

        date_outdata = date_out.strftime("%Y/%m/%d  %H:%M:%S")
        cursor.execute(sql, (date_outdata, numberXe))
        db.commit()

        sql = "UPDATE xedap SET Trang_thai = %s WHERE Ma_xe = %s"
        numberXe = self.edtNumber.text()
        cursor.execute(sql, ('1', numberXe))

        db.commit()
        cursor.close()
        db.close()

        print("Xe duoc thue vao luc:  ", date_in)
        print("Xe het han vao luc:  ", date_outdata)
        #
        # # DUA TIEN VAO KHUNG TONG TIEN
        self.edtNumberTotal.setText(str(total))

        # BAT THONG BAO SO TIEN PHAI TRA
        msg = QtWidgets.QMessageBox()
        msg.setInformativeText(
            f'Tong tien phai tra: {total}, Thue vao ngay: {date_in} va het han vao luc: {date_outdata}')
        msg.exec()


app = QApplication(sys.argv)
withget = QtWidgets.QStackedWidget()
login_f = login_w()
dangky_f = dangky_w()
home_f = home_w()
add_f = add_w()
thue_f = thue_w()
taoqrchoxe_f = taoqrchoxe_w()
# mocam_f = MoCam_w()

# theo stt trong mang mac dinh la 0
withget.addWidget(login_f)
withget.addWidget(home_f)
withget.addWidget(add_f)
withget.addWidget(thue_f)
withget.addWidget(taoqrchoxe_f)
withget.addWidget(dangky_f)
# withget.addWidget(mocam_f)
withget.setCurrentIndex(0)
withget.setFixedHeight(600)
withget.setFixedWidth(600)
withget.show()
app.exec()
