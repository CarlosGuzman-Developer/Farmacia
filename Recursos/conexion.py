#Conexion a la base de datos
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dbfarmacia",
        port = 3306
    )
