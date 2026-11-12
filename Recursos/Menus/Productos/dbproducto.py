from ...conexion import conectar

class dbProducto:

    # Buscar
    def buscar(self, nombre):
        con = conectar()
        cursor = con.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.*, pr.nombre AS proveedor
            FROM productos p
            LEFT JOIN proveedores pr ON p.id_proveedor = pr.id
            WHERE p.nombre=%s
        """, (nombre,))

        dato = cursor.fetchone()
        con.close()
        return dato


    # INSERTAR
    def insertar(self, nombre, tipo, id_proveedor, compra, venta, stock,receta):
        con = conectar()
        cursor = con.cursor()

        sql = """
        INSERT INTO productos (nombre, tipo, id_proveedor, precio_compra, precio_venta, stock,receta)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (nombre, tipo, id_proveedor, compra, venta, stock,receta))

        con.commit()
        con.close()


    # EDITAR
    def editar(self, idp, nombre, tipo, id_proveedor, compra, venta, stock,receta):
        con = conectar()
        cursor = con.cursor()

        sql = """
        UPDATE productos 
        SET nombre=%s, tipo=%s, id_proveedor=%s, 
            precio_compra=%s, precio_venta=%s, stock=%s, receta = %s
        WHERE id=%s
        """
        cursor.execute(sql, (nombre, tipo, id_proveedor, compra, venta, stock, receta,idp))

        con.commit()
        con.close()


    # ELIMINAR
    def eliminar(self, idp):
        con = conectar()
        cursor = con.cursor()

        cursor.execute("DELETE FROM productos WHERE id=%s", (idp,))
        con.commit()
        con.close()


    # OBTENER PROVEEDORES (para combobox)
    def obtener_proveedores(self):
        con = conectar()
        cursor = con.cursor(dictionary=True)

        cursor.execute("SELECT id, nombre FROM proveedores")
        datos = cursor.fetchall()

        con.close()
        return datos


    # OBTENER PRODUCTOS (para compras)
    def obtener_productos(self):
        con = conectar()
        cursor = con.cursor(dictionary=True)

        cursor.execute("SELECT id, nombre FROM productos")
        datos = cursor.fetchall()

        con.close()
        return datos

    #Obtener el ultimo ID registrado    
    def getMaxID(self):
        id = 0
        con = conectar()
        cursor = con.cursor(dictionary=True)

        cursor.execute("SELECT max(id) FROM productos")
        datos = cursor.fetchone()

        if datos is not None:
            id = int(datos["max(id)"])
        con.close()
        return id
