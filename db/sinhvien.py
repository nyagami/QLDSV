from data.sinhvien import SinhVien
from .utils import connect
from pyodbc import DatabaseError

def findAll() -> list[SinhVien]:
    query = """
                SELECT sv.ma, ten, ngay_sinh, gioi_tinh, lop, nganh
                FROM 
                    SinhVien as sv 
                    JOIN Hoso as hs ON sv.ma_ho_so = hs.ma
            """
    conn = connect()
    cursor = conn.execute(query)
    
    res = []
    for row in cursor:
        res.append(SinhVien(row[0], row[1], row[2], row[3], row[4], row[5]))
    cursor.close()
    return res

def update(sinhvien: SinhVien):
    query = """
                UPDATE Sinhvien SET lop = ?, WHERE ma = ?
            """
    conn = connect()
    try:
        conn.execute(query)
    except DatabaseError as e:
        print(e)
        return None
    return sinhvien