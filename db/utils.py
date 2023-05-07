import pyodbc
from pyodbc import Connection

Server = "GAMI\\SERVER01"

def connect() -> Connection:
    conn = pyodbc.connect("Driver={SQL Server};"
                          f"Server={Server};"
                          f"Database=QLDSV;"
                          "Trusted_Connection=yes;")
    return conn
