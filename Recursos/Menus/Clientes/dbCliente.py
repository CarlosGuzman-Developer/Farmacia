from ...conexion import conectar

class dbCliente:

    def buscar(self, id_cliente):
        con = conectar()
        if con is None:
            return None

        try:
            cursor = con.cursor(dictionary=True)
            sql = "SELECT * FROM clientes WHERE id=%s"
            cursor.execute(sql, (id_cliente,))
            return cursor.fetchone()

        except Exception as e:
            print("Error buscar:", e)
            return None

        finally:
            con.close()


    def insertar(self, nombre, telefono, correo, rfc, ciudad, puntos):
        con = conectar()
        if con is None:
            return False

        try:
            cursor = con.cursor()
            sql = """
            INSERT INTO clientes (nombre, telefono, correo, rfc, ciudad, puntos)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, telefono, correo, rfc, ciudad, puntos))
            con.commit()
            return True

        except Exception as e:
            print("Error insertar:", e)
            return False

        finally:
            con.close()


    def actualizar(self, id_cliente, nombre, telefono, correo, rfc, ciudad, puntos):
        con = conectar()
        if con is None:
            return False

        try:
            cursor = con.cursor()
            sql = """
            UPDATE clientes
            SET nombre=%s, telefono=%s, correo=%s, rfc=%s, ciudad=%s, puntos=%s
            WHERE id=%s
            """
            cursor.execute(sql, (nombre, telefono, correo, rfc, ciudad, puntos, id_cliente))
            con.commit()
            return True

        except Exception as e:
            print("Error actualizar:", e)
            return False

        finally:
            con.close()


    def eliminar(self, id_cliente):
        con = conectar()
        if con is None:
            return False

        try:
            cursor = con.cursor()
            sql = "DELETE FROM clientes WHERE id=%s"
            cursor.execute(sql, (id_cliente,))
            con.commit()
            return True

        except Exception as e:
            print("Error eliminar:", e)
            return False

        finally:
            con.close()