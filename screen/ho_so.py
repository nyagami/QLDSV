import sys
from PyQt5.QtWidgets import QDialog,QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
from data.hoso import HoSo
from db.hoso import insert
from db.sinhvien import delete, findAll
class HoSoTable(QDialog):
    
    def __init__(self, data,datas):
        super().__init__()
        self.datas = datas 
        self.data = data
        self.current_row = None
        self.initUI()

    def initUI(self):
        # Tạo bảng dữ liệu
        self.table = QTableWidget(self)
        self.count_data = len(self.data)
        self.height_table = self.count_data*30
        self.table.setGeometry(QtCore.QRect(90, 90, 821, self.height_table+25))
        self.table.setColumnCount(5)
        self.table.cellClicked.connect(self.select_data)
        
        # Đặt tiêu đề cho các cột
        headers = ['Mã', 'Họ và tên', 'Ngày sinh', 'Giới tính','Địa chỉ']
        self.table.setHorizontalHeaderLabels(headers)
        self.load_data()
        
        # Tạo các nút điều khiển
        self.add_btn = QPushButton(self)
        self.add_btn.setGeometry(QtCore.QRect(840, 50, 71, 23))
        self.add_btn.setText("Thêm")
        self.update_btn = QPushButton(self)
        self.update_btn.setGeometry(QtCore.QRect(690, 50, 71, 23))
        self.update_btn.setText("Cập nhật")
        self.update_btn.hide()
        self.delete_btn = QPushButton(self)
        self.delete_btn.setGeometry(QtCore.QRect(765, 50, 71, 23))
        self.delete_btn.setText('Xóa')
        self.delete_btn.hide()

        self.sort_name_increase_btn = QPushButton('Sắp xếp theo tên tăng dần')
        self.sort_name_reduce_btn = QPushButton('Sắp xếp theo tên giảm dần')
        self.sort_gpa_increase_btn = QPushButton('Sắp xếp theo gpa tăng dần')
        self.sort_gpa_reduce_btn = QPushButton('Sắp xếp theo gpa giảm dần')

        # Khởi tạo QLineEdit cho từ khóa tìm kiếm
        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(QtCore.QRect(90, 50, 71, 23))
        self.search_input.textChanged.connect(self.search_by_fullname)

        # Tạo layout cho các widget nhập liệu và nút điều khiển
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.sort_name_increase_btn)
        button_layout.addWidget(self.sort_name_reduce_btn)
        button_layout.addWidget(self.sort_gpa_increase_btn)
        button_layout.addWidget(self.sort_gpa_reduce_btn)
        # form_layout.addWidget(self.search_input)
        form_layout.addLayout(button_layout)

        # Tạo layout chính
        vbox = QVBoxLayout()

        # vbox.addWidget(self.search_input)
        # vbox.addWidget(self.add_btn)
        vbox.addWidget(self.table)
        vbox.addLayout(form_layout)
        
        vbox2 = QVBoxLayout()
        # Thiết lập layout
        # self.setLayout(vbox)
        # self.setLayout(vbox2)


        # Kết nối các nút điều khiển với hàm xử lý tương ứng
        self.add_btn.clicked.connect(self.add_data)
        self.update_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)
        self.sort_name_increase_btn.clicked.connect(self.sort_name_increase)
        self.sort_name_reduce_btn.clicked.connect(self.sort_name_reduce)
        self.sort_gpa_increase_btn.clicked.connect(self.sort_gpa_increase)
        self.sort_gpa_reduce_btn.clicked.connect(self.sort_gpa_reduce)

        # Hiển thị cửa sổ

        self.setGeometry(0, 0, 1000, 700)
        self.setWindowTitle('Danh sách hồ sơ')
        self.show()

    def add_data(self):
    # Mở class PersonalInfo để thêm mới
        info = PersonalInfo(self)
        info.exec_()
        self.count_data = len(self.data)
        self.height_table = self.count_data*30
        self.table.setGeometry(QtCore.QRect(90, 90, 821, self.height_table+30))

        
    def update_data(self):
        if self.current_row is None:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng chọn một hàng để cập nhật')
        else:
            info = EditPersonalInfo(self)
            info.exec_()
            self.update_btn.hide()
            self.delete_btn.hide()

    def delete_data(self):
        # print(self.data[self.current_row]['code'])
        found_object = None
        for obj in self.datas:
            if obj.ma == self.data[self.current_row]['code']:
                found_object = obj
                break
        
        # Kiểm tra hàng được chọn
        if self.current_row is None:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng chọn một hàng để xóa')
            return

        # Xóa dữ liệu trên bảng
        # if found_object:
        self.table.removeRow(self.current_row)

        # Xóa dữ liệu trong danh sách
        del self.data[self.current_row]
        # delete(found_object)
        # Bỏ chọn hàng hiện tại
        self.current_row = None
        self.table.clearSelection()
        self.update_btn.hide()
        self.delete_btn.hide()


    def select_data(self, row, column):
        # Lưu vị trí hàng được chọn
        self.current_row = row
        self.update_btn.show()
        self.delete_btn.show()

        
    def search_by_fullname(self):
        fullname = self.search_input.text()
        
        # If search query is not empty, filter the data by full name
        if fullname:
            filtered_data = [row for row in self.data if fullname.lower() in row['code'].lower()]
            self.table.setRowCount(len(filtered_data))
            for i, row in enumerate(filtered_data):
                self.table.setItem(i, 0, QTableWidgetItem(row['name']))
                self.table.setItem(i, 1, QTableWidgetItem(row['code']))
                # self.table.setItem(i, 2, QTableWidgetItem(row['gpa']))
                self.table.setItem(i, 2, QTableWidgetItem(row['gender']))
                self.table.setItem(i, 3, QTableWidgetItem(row['date']))
                self.table.setItem(i, 4, QTableWidgetItem(row['lop']))
                # self.table.setItem(i, 5, QTableWidgetItem(row['major']))
        # If search query is empty, show the original data
        else:
            self.load_data()

    def load_data(self):
        self.table.setRowCount(len(self.data))
        len_table = self.table.width()
        for i in range(4):
            self.table.setColumnWidth(i, int(len_table/5))
            

        for i, row in enumerate(self.data):
            self.table.setItem(i, 0, QTableWidgetItem(row['name']))
            self.table.setItem(i, 1, QTableWidgetItem(row['code']))
            # self.table.setItem(i, 2, QTableWidgetItem(row['gpa']))
            self.table.setItem(i, 2, QTableWidgetItem(row['gender']))
            self.table.setItem(i, 3, QTableWidgetItem(row['date']))
            self.table.setItem(i, 4, QTableWidgetItem(row['lop']))

    def sort_name_increase(self):
        self.data = sorted(self.data, key=lambda city: city['name'], reverse=False)
        self.load_data()

    def sort_name_reduce(self):
        self.data = sorted(self.data, key=lambda city: city['name'], reverse=True)
        self.load_data()

    def sort_gpa_increase(self):
        self.data = sorted(self.data, key=lambda city: city['gpa'], reverse=False)
        self.load_data()

    def sort_gpa_reduce(self):
        self.data = sorted(self.data, key=lambda city: city['gpa'], reverse=True)
        self.load_data()


class PersonalInfo(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Tạo các widget nhập liệu
        self.name_input = QLineEdit()
        self.code_input = QLineEdit()
        # self.gpa_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.date_input = QLineEdit()
        self.class_input = QLineEdit()
        # self.major_input = QLineEdit()

        #Tạo form nhập liệu
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel('Mã Hồ Sơ'))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel('Họ và tên'))
        form_layout.addWidget(self.code_input)
        # form_layout.addWidget(QLabel('GPA'))
        # form_layout.addWidget(self.gpa_input)
        form_layout.addWidget(QLabel('Ngày sinh'))
        form_layout.addWidget(self.gender_input)
        form_layout.addWidget(QLabel('Giới tính'))
        form_layout.addWidget(self.date_input)
        form_layout.addWidget(QLabel('Địa chỉ'))
        form_layout.addWidget(self.class_input)
        # form_layout.addWidget(QLabel('Ngành'))
        # form_layout.addWidget(self.major_input)
        
        self.save = QPushButton('Thêm')
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save)
        form_layout.addLayout(button_layout)

        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        self.setLayout(vbox)

        # Tạo kết nối với button
        self.save.clicked.connect(self.save_info)

        # Tùy chỉnh kích thước cho class
        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle('Thông tin cá nhân')
        self.show()

    def save_info(self):
        # Lấy giá trị từ các ô nhập liệu
        name = self.name_input.text()
        code = self.code_input.text()
        # gpa = self.gpa_input.text()
        gender = self.gender_input.text()
        date = self.date_input.text()
        lop = self.class_input.text()
        # major = self.major_input.text()

        # Tạo 1 đối tượng và ép thành đối tượng HoSo
        
        # Kiểm tra các giá trị nhập liệu
        if not name or not gender or not code or not date or not lop :
            QMessageBox.warning(self, 'Lỗi', 'Họ và tên, mã sinh viên, giới tính, ngày sinh, lớp, ngành là các trường bắt buộc')
            return
        ho_so_new = HoSo(name,code,date,gender,lop)
        success = insert(ho_so_new)
        if success is None:
            QMessageBox.warning(self, 'Lỗi', 'Thêm hồ sơ thất bại')
        else:    
            # Thêm dữ liệu vào bảng
            row_count = self.parent().table.rowCount()
            self.parent().table.insertRow(row_count)
            self.parent().table.setItem(row_count, 0, QTableWidgetItem(name))
            self.parent().table.setItem(row_count, 1, QTableWidgetItem(code))
            # self.parent().table.setItem(row_count, 2, QTableWidgetItem(gpa))
            self.parent().table.setItem(row_count, 2, QTableWidgetItem(gender))
            self.parent().table.setItem(row_count, 3, QTableWidgetItem(date))
            self.parent().table.setItem(row_count, 4, QTableWidgetItem(lop))
            # self.parent().table.setItem(row_count, 5, QTableWidgetItem(major))

            # Thêm dữ liệu vào danh sách
            self.parent().data.append({"name":name,"code":code, "gender":gender, "date":date, "lop":lop})
            
            # Đóng class
            self.close()

class EditPersonalInfo(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        
        # Tạo các widget nhập liệu
        self.name_input = QLineEdit()
        self.code_input = QLineEdit()
        # self.gpa_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.date_input = QLineEdit()
        self.class_input = QLineEdit()
        # self.major_input = QLineEdit()

        #Tạo form nhập liệu
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel('Mã Sinh Viên'))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel('Họ và tên'))
        form_layout.addWidget(self.code_input)
        # form_layout.addWidget(QLabel('GPA'))
        # form_layout.addWidget(self.gpa_input)
        form_layout.addWidget(QLabel('Ngày sinh'))
        form_layout.addWidget(self.gender_input)
        form_layout.addWidget(QLabel('Giới tính'))
        form_layout.addWidget(self.date_input)
        form_layout.addWidget(QLabel('Địa chỉ'))
        form_layout.addWidget(self.class_input)
        # form_layout.addWidget(QLabel('Ngành'))
        # form_layout.addWidget(self.major_input)
        
        self.save = QPushButton('Lưu')
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save)
        form_layout.addLayout(button_layout)

        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        self.setLayout(vbox)

        # Tạo kết nối với button
        self.save.clicked.connect(self.save_info)
        
        # Tùy chỉnh kích thước cho class
        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle('Sửa thông tin cá nhân')
        self.show()
        
        #
        name = self.parent().table.item(self.parent().current_row, 0).text()
        code = self.parent().table.item(self.parent().current_row, 1).text()
        # gpa = self.parent().table.item(self.parent().current_row, 2).text()
        gender = self.parent().table.item(self.parent().current_row, 2).text()
        date = self.parent().table.item(self.parent().current_row, 3).text()
        lop = self.parent().table.item(self.parent().current_row, 4).text()
        # major = self.parent().table.item(self.parent().current_row, 5).text()
        self.name_input.setText(name)
        self.code_input.setText(code)
        # self.gpa_input.setText(gpa)
        self.gender_input.setText(gender)
        self.date_input.setText(date)
        self.class_input.setText(lop)
        # self.major_input.setText(major)
        
    def save_info(self):
        
        # Lấy giá trị từ các widget nhập liệu
        name = self.name_input.text()
        code = self.code_input.text()
        # gpa = self.gpa_input.text()
        gender = self.gender_input.text()
        date = self.date_input.text()
        lop = self.class_input.text()
        # major = self.major_input.text()

        # Kiểm tra các giá trị nhập liệu
        if not name or not gender or not code or not date or not lop :
            QMessageBox.warning(self, 'Lỗi', 'Họ và tên, giới tính, email, số điện thoại là các trường bắt buộc')
            return

        # Cập nhật dữ liệu trên bảng
        self.parent().table.setItem(self.parent().current_row, 0, QTableWidgetItem(name))
        self.parent().table.setItem(self.parent().current_row, 1, QTableWidgetItem(code))
        # self.parent().table.setItem(self.parent().current_row, 2, QTableWidgetItem(gpa))
        self.parent().table.setItem(self.parent().current_row, 2, QTableWidgetItem(gender))
        self.parent().table.setItem(self.parent().current_row, 3, QTableWidgetItem(date))
        self.parent().table.setItem(self.parent().current_row, 4, QTableWidgetItem(lop))
        # self.parent().table.setItem(self.parent().current_row, 5, QTableWidgetItem(major))

        # Cập nhật dữ liệu trong danh sách
        self.parent().data[self.parent().current_row] = {"name":name,"code":code, "gender":gender, "date":date, "lop":lop}

        # Bỏ chọn hàng hiện tại
        self.parent().current_row = None
        self.parent().table.clearSelection()
        
        # Đóng class
        self.close()