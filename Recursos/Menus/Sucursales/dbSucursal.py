from ...conexion import conectar

class dbSucursal:

    def obtenerSucursales(self):
        con = conectar()
        if con is None:
            return None

        try:
            cursor = con.cursor(dictionary=True)
            sql = "SELECT * FROM sucursales"
            cursor.execute(sql)
            datos = cursor.fetchall()
            return datos
        except Exception as e:
            print("Error al cargar todas las sucursales:", e)
            return None

        finally:
            con.close()        
    
    def buscar(self, id):
        con = conectar()
        if con is None:
            return None

        try:
            cursor = con.cursor(dictionary=True)
            sql = "SELECT * FROM sucursales WHERE id=%s"
            cursor.execute(sql, (id,))
            return cursor.fetchone()

        except Exception as e:
            print("Error buscar:", e)
            return None

        finally:
            con.close()


    def insertar(self, direccion):
        con = conectar()
        if con is None:
            return False

        try:
            cursor = con.cursor()
            sql = """
            INSERT INTO sucursales (direccion)
            VALUES (%s)
            """
            cursor.execute(sql, (direccion,))
            con.commit()
            return True

        except Exception as e:
            print("Error insertar:", e)
            return False

        finally:
            con.close()


    def actualizar(self, id_sucursal, direccion):
        con = conectar()
        if con is None:
            return False

        try:
            cursor = con.cursor()
            sql = """
            UPDATE sucursales
            SET direccion=%s
            WHERE id=%s
            """
            cursor.execute(sql, (direccion,id_sucursal))
            con.commit()
            return True

        except Exception as e:
            print("Error actualizar:", e)
            return False

        finally:
            con.close()


    def eliminar(self, id_sucursal):
        con = conectar()
        if con is None:
            return False

        try:
            cursor = con.cursor()
            sql = "DELETE FROM clientes WHERE id=%s"
            cursor.execute(sql, (id_sucursal,))
            con.commit()
            return True

        except Exception as e:
            print("Error eliminar:", e)
            return False

        finally:
            con.close()