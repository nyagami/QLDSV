from data.hoso import HoSo
from .utils import connect
from pyodbc import DatabaseError

def findAll() -> list[HoSo]:
    conn = connect()
    cursor = conn.cursor()

    query = "SELECT ma, ten, gioi_tinh, ngay_sinh, dia_chi FROM Hoso"
    cursor.execute(query)
    res = []
    for row in cursor:
        res.append(HoSo(row[0], row[1], row[2], row[3], row[4]))
    conn.close()
    return res

def udpate(hoso: HoSo):
    conn = connect()
    cursor = conn.cursor()

    query = f"UPDATE Hoso SET dia_chi = ? WHERE ma = ?"
    try:
        cursor.execute(query, hoso.dia_chi, hoso.ma)
        conn.commit()
        conn.close()
    except DatabaseError as e:
        print(e)
        return None
    return hoso

def delete(hoso: HoSo):
    conn = connect()
    cursor = conn.cursor()

    query = f"DELETE FROM Hoso WHERE ma = ?"
    cursor.execute(query, hoso.ma)

def insert(hoso: HoSo):
    conn = connect()
    cursor = conn.cursor()

    query = "INSERT INTO Hoso (ma, ten, ngay_sinh, gioi_tinh, dia_chi) VALUES(?, ?, ?, ?, ?)"
    try:
        cursor.execute(query, hoso.ma, hoso.ten, hoso.ngay_sinh, hoso.gioi_tinh, hoso.dia_chi)
        cursor.commit()
        conn.close()
    except DatabaseError as e:
        print(e)
        return None
    return hoso
