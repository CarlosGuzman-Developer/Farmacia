#Conexion a la base de datos
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Cruz_Azul",
        database="dbfarmacia",
        port = 3307
    )
