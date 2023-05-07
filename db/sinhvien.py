from data.sinhvien import SinhVien
from .utils import connect

def findAll() -> list[SinhVien]:
    query = """
                SELECT ma, ten, gioi_tinh, ngay_sinh, gioi_tinh, lop, nganh
                FROM 
                    SinhVien JOIN Hoso ON SinhVien.ma_ho_so
            """
    conn = connect()
    cursor = conn.execute(query)
    for row in cursor:
        print(row)