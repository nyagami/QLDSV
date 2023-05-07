import sys
from PyQt5.QtWidgets import QDialog,QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
import db.sinhvien 
import db.hoso 
import db.hoctap
from db.utils import login 

from screen.hoctap import HocTapTable
from screen.ho_so import HoSoTable
from screen.sinhvien import SinhVienTable

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Tạo các trường nhập và nút đăng nhập
        self.label1 = QLabel('Tên đăng nhập')
        self.username = QLineEdit()
        self.label2 = QLabel('Mật khẩu')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.submit_button = QPushButton('Đăng nhập')

        # Set width username, password bằng nhau
        self.username.setFixedWidth(190)
        self.password.setFixedWidth(190)

        # Tạo layout
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.username)
        layout.addLayout(layout1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.password)
        layout.addLayout(layout2)
        layout.addWidget(self.submit_button)

        # Thiết lập layout và kích thước cửa sổ
        self.setLayout(layout)
        self.setWindowTitle('Đăng nhập')
        self.setFixedSize(300, 150)

        # Khi nút đăng nhập được nhấn, kiểm tra thông tin đăng nhập
        self.submit_button.clicked.connect(self.check_login)

    def check_login(self):
        # Lấy giá trị nhập từ các trường
        username = self.username.text()
        password = self.password.text()
        check = login(username, password)
        # Kiểm tra thông tin đăng nhập
        if check:
            self.close()
            self.window = MyMainWindow(check)
            self.window.show()
        else:
            QMessageBox.warning(self, 'Lỗi', 'Tên đăng nhập hoặc mật khẩu không chính xác')

class MyMainWindow(QWidget):
    def __init__(self, user):
        super().__init__()

        #Tạo 1 label để hiển thị người dùng đã đăng nhập thành công
        self.label = QLabel('User: ' + user.ten, self)
        self.label.setGeometry(QtCore.QRect(20, 10, 150, 23))

        

        # Tạo một button để mở dialog
        self.button1 = QPushButton('Danh sách sinh viên', self)
        self.button2 = QPushButton('Danh sách hồ sơ', self)
        self.button3 = QPushButton('Học tập', self)
        self.button1.clicked.connect(self.show_dialog_sv)
        self.button1.setGeometry(QtCore.QRect(180, 50, 150, 23))
        self.button2.clicked.connect(self.show_dialog_hs)
        self.button2.setGeometry(QtCore.QRect(180, 100, 150, 23))
        self.button3.clicked.connect(self.show_dialog_ht)
        self.button3.setGeometry(QtCore.QRect(180, 150, 150, 23))
        self.initUI()
    def initUI(self):
        self.setGeometry(0, 0, 500, 250)
    def show_dialog_sv(self):
        # Tạo một đối tượng dialog và hiển thị nó
        data = [
        ]
        datas = db.sinhvien.findAll()
        for i in datas:
            data.append({"name":i.ten,"code":i.ma, "gender":i.gioi_tinh, "date":i.ngay_sinh, "lop":i.lop, "major":i.nganh})
        dialog = SinhVienTable(data,datas)
        # self.close()
        dialog.exec_()

    def show_dialog_hs(self):
        data = [
        ]
        datas = db.hoso.findAll()
        for i in datas:
            data.append({"name":i.ma,"code":i.ten, "gender":i.ngay_sinh, "date":i.gioi_tinh, "lop":i.dia_chi})
        # Tạo một đối tượng dialog và hiển thị nó
        dialog = HoSoTable(data,datas)
        dialog.exec_()
    def show_dialog_ht(self):
        data = [
        ]
        datas = db.hoctap.findAll()
        for i in datas:
            data.append({"name":i.ma_sinh_vien,"code":i.ma_mon_hoc, "gender":i.diem_chuyen_can, "date":i.diem_kiem_tra, "lop":i.diem_thuc_hanh, "major":i.diem_thi})
        # Tạo một đối tượng dialog và hiển thị nó
        dialog = HocTapTable(data,datas)
        dialog.exec_()
if __name__ == '__main__':
    app = QApplication([])
    window = LoginDialog()
    window.show()
    app.exec_()
