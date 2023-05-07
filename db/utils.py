import pyodbc
from pyodbc import Connection

Server = "GAMI\\CENTER"

def connect() -> Connection:
    conn = pyodbc.connect("Driver={SQL Server};"
                          f"Server={Server};"
                          f"Database=QLDSV;"
                          "Trusted_Connection=yes;")
    return conn
