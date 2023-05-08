import pyodbc
from pyodbc import Connection

Server = "DESKTOP-P9OFUDS"

def connect() -> Connection:
    conn = pyodbc.connect("Driver={SQL Server};"
                          f"Server={Server};"
                          f"Database=QLDSV;"
                          "Trusted_Connection=yes;")
    return conn

def login(email, password):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT ten, quyen FROM TaiKhoan WHERE email = ? AND CONVERT(nvarchar, mat_khau) = ?"
    cursor.execute(query, email, password)
    res = cursor.fetchone()
    return res
