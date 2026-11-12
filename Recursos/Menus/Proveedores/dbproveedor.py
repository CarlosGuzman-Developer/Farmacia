from ...conexion import conectar

class DBProveedor:

    def insertar(self, proveedor):
        con = conectar()
        cursor = con.cursor()
        sql = "INSERT INTO proveedores (nombre, correo, telefono) VALUES (%s,%s,%s)"
        cursor.execute(sql, (proveedor.nombre, proveedor.correo, proveedor.telefono))
        con.commit()
        con.close()

    def obtener(self):
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM proveedores")
        datos = cursor.fetchall()
        con.close()
        return datos

    def actualizar(self, proveedor):
        con = conectar()
        cursor = con.cursor()
        sql = "UPDATE proveedores SET nombre=%s, correo=%s, telefono=%s WHERE id=%s"
        cursor.execute(sql, (proveedor.nombre, proveedor.correo, proveedor.telefono, proveedor.id))
        con.commit()
        con.close()

    def eliminar(self, id):
        con = conectar()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM proveedores WHERE id=%s", (id,))
            con.commit()
            return True
        except Exception:
            return False
        finally:
            con.close()

    # 🔍 BUSQUEDAS
    def buscar_por_id(self, id):
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
        datos = cursor.fetchall()
        con.close()
        return datos

    def buscar_por_nombre(self, nombre):
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE nombre LIKE %s", ('%' + nombre + '%',))
        datos = cursor.fetchall()
        con.close()
        return datos

    def buscar_por_correo(self, correo):
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE correo LIKE %s", ('%' + correo + '%',))
        datos = cursor.fetchall()
        con.close()
        return datos