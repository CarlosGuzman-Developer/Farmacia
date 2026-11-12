from ...conexion import conectar

class dbUsuario:

    def login(self, usuario, password,sucursal_id):
        con = conectar()
        if con is None:
            return None

        try:
            cursor = con.cursor(dictionary=True)
            sql = """
            SELECT id, nombre, rol
            FROM usuarios
            WHERE usuario=%s AND password=%s AND sucursal_id=%s
            """
            cursor.execute(sql, (usuario, password,sucursal_id))
            return cursor.fetchone()

        except Exception as e:
            print("Error login:", e)
            return None

        finally:
            con.close()