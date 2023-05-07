from data.sinhvien import SinhVien
from .utils import connect
from pyodbc import DatabaseError

def findAll() -> list[SinhVien]:
    query = """
                SELECT sv.ma, ten, ngay_sinh, gioi_tinh, lop, nganh, ma_ho_so, he_dao_tao
                FROM 
                    SinhVien as sv 
                    JOIN Hoso as hs ON sv.ma_ho_so = hs.ma
            """
    conn = connect()
    cursor = conn.execute(query)
    
    res = []
    for row in cursor:
        res.append(SinhVien(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    conn.close()
    return res

def update(sv: SinhVien):
    query = """
                UPDATE SinhVien SET ma_ho_so = ?, lop = ?, he_dao_tao = ?, WHERE ma = ?
            """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query, sv.ma_ho_so, sv.lop, sv.he_dao_tao, sv.ma)
        conn.commit()
        conn.close()
    except DatabaseError as e:
        print(e)
        return None
    return sv

def insert(sv: SinhVien):
    query = """
                INSERT INTO SinhVien(ma, ma_ho_so, lop, he_dao_tao, nganh)
                VALUES(?, ?, ?, ?, ?)
            """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query, sv.ma, sv.ma_ho_so, sv.lop, sv.he_dao_tao, sv.nganh)
        cursor.commit()
    except DatabaseError as e:
        print(e)
        return None
    return sv

def delete(sv: SinhVien):
    conn = connect()
    cursor = conn.cursor()

    query = f"DELETE FROM SinhVien WHERE ma = ?"
    cursor.execute(query, sv.ma)
