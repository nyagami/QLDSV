from data.hoctap import HocTap
from .utils import connect
from pyodbc import DatabaseError

def findAll() -> list[HocTap]:
    query = """
                SELECT ma_sinh_vien, ma_mon_hoc, diem_chuyen_can, diem_kiem_tra, diem_thuc_hanh, diem_thi
                FROM HocTap
            """
    conn = connect()
    cursor = conn.execute(query)
    
    res = []
    for row in cursor:
        res.append(HocTap(row[0], row[1], row[2], row[3], row[4], row[5]))
    conn.close()
    return res

def update(ht: HocTap):
    query = """
                UPDATE Hoctap SET diem_chuyen_can = ?, diem_kiem_tra = ?, diem_thuc_hanh = ?, diem_thi = ?
                WHERE ma_sinh_vien = ? AND ma_hoc_tap = ?
            """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query, ht.diem_chuyen_can, ht.diem_kiem_tra, ht.diem_thuc_hanh, ht.diem_thi,
                       ht.ma_sinh_vien, ht.ma_mon_hoc)
        conn.commit()
        conn.close()
    except DatabaseError as e:
        print(e)
        return None
    return ht

def insert(ht: HocTap):
    query = """
                INSERT INTO HocTap(ma_sinh_vien, ma_mon_hoc, diem_chuyen_can, diem_kiem_tra, diem_thuc_hanh, diem_thi)
                VALUES(?, ?, ?, ?, ?, ?)
            """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query, ht.ma_sinh_vien, ht.ma_mon_hoc, ht.diem_chuyen_can,
                       ht.diem_kiem_tra, ht.diem_thuc_hanh, ht.diem_thi)
        cursor.commit()
    except DatabaseError as e:
        print(e)
        return None
    return ht

def delete(ht: HocTap):
    conn = connect()
    cursor = conn.cursor()

    query = f"DELETE FROM HocTap WHERE ma_sinh_vien = ?, ma_mon_hoc = ?"
    cursor.execute(query, ht.ma_sinh_vien, ht.ma_mon_hoc)

