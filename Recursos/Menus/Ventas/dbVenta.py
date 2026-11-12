from ...conexion import conectar
from .factura import generar_factura_venta

from pathlib import Path
import json

ruta_sucursal = Path(__file__)
ruta_sucursal = ruta_sucursal.parents[2]

def abrir_sucursal():
    try:
        with open (ruta_sucursal / "sucursal.json","r") as archivo:
            sucursal = json.load(archivo)
            return sucursal
    except (FileNotFoundError,json.JSONDecodeError):
         print("Error, archivo corrupto o no encontradp")

global sucursal


class dbVenta:

    sucursal = abrir_sucursal()

    def obtener_maxID(self):

        id = 0

        con = conectar()

        cursor = con.cursor(dictionary=True)

        cursor.execute("SELECT MAX(id) as maximo FROM ventas")

        row = cursor.fetchone()

        if row["maximo"] is not None:
            id = int(row["maximo"])

        con.close()

        return id

    # =========================
    # CLIENTES
    # =========================
    def obtener_clientes(self):

        con = conectar()

        cursor = con.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                nombre,
                correo,
                puntos
            FROM clientes
        """)

        datos = cursor.fetchall()

        con.close()

        return datos

    # =========================
    # PRODUCTOS
    # =========================
    def obtener_productos(self):

        con = conectar()

        cursor = con.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                nombre,
                precio_venta,
                stock,
                receta
            FROM productos WHERE sucursal_id = %s 
        """,(self.sucursal['id'],))

        datos = cursor.fetchall()

        con.close()

        return datos

    def obtener_productoID(self, nombre):

        con = conectar()

        cursor = con.cursor(dictionary=True)

        cursor.execute(
            "SELECT id FROM productos WHERE nombre = %s",
            (nombre,)
        )

        datos = cursor.fetchone()

        con.close()

        return datos["id"]

    # =========================
    # REGISTRAR VENTA
    # =========================
    def registrar(
        self,
        id_venta,
        id_cliente,
        productos_datos,
        total
    ):

        con = conectar()

        try:

            print("ENTRANDO A REGISTRAR VENTA")

            cursor = con.cursor(dictionary=True)

            # =========================
            # CLIENTE
            # =========================
            cursor.execute(
                "SELECT * FROM clientes WHERE id = %s",
                (id_cliente,)
            )

            cliente = cursor.fetchone()

            if not cliente:
                return False, "Cliente no encontrado"

            # =========================
            # PUNTOS
            # =========================
            puntos = cliente["puntos"]

            descuento = 0

            if puntos >= 50:

                descuento = total * 0.10

                puntos = 0

            else:

                if total > 500:
                    puntos += 10

            # =========================
            # PRODUCTOS
            # =========================
            for dato in productos_datos:

                nombre_producto = dato[0]

                cantidad = int(dato[1])

                subtotal = float(dato[2])

                # =========================
                # BUSCAR PRODUCTO
                # =========================
                cursor.execute(
                    "SELECT * FROM productos WHERE nombre = %s",
                    (nombre_producto,)
                )

                producto = cursor.fetchone()

                if not producto:

                    print("Producto no encontrado")

                    continue

                producto_id = producto["id"]

                stock_actual = int(producto["stock"])

                # =========================
                # VALIDAR STOCK
                # =========================
                if cantidad > stock_actual:

                    return False, (
                        f"Stock insuficiente para "
                        f"{nombre_producto}"
                    )

                # =========================
                # INSERT VENTA
                # =======================

                cursor.execute("""
                    INSERT INTO ventas (
                        id,
                        id_cliente,
                        id_producto,
                        cantidad,
                        total,
                        fecha,
                        sucursal_id
                    )
                    VALUES (%s,%s,%s,%s,%s,NOW(),%s)
                """, (
                    id_venta,
                    id_cliente,
                    producto_id,
                    cantidad,
                    subtotal,
                    self.sucursal["id"]
                ))

                print("INSERTANDO VENTA...")

                # =========================
                # UPDATE STOCK
                # =========================
                cursor.execute("""
                    UPDATE productos
                    SET stock = stock - %s
                    WHERE id = %s
                """, (
                    cantidad,
                    producto_id
                ))

            # =========================
            # UPDATE CLIENTE
            # =========================
            cursor.execute("""
                UPDATE clientes
                SET puntos = %s
                WHERE id = %s
            """, (
                puntos,
                id_cliente
            ))

            # =========================
            # COMMIT MYSQL
            # =========================
            con.commit()

            print("VENTA GUARDADA")

            # =========================
            # FACTURA PDF
            # =========================
            archivo = generar_factura_venta(
                cliente["nombre"],
                productos_datos,
                total,
                descuento,
                self.sucursal
            )

            return True, (
                f"Venta realizada correctamente.\n"
                f"Total pagado: ${total - descuento}"
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            print("ERROR VENTA:", e)

            con.rollback()

            return False, str(e)

        finally:

            con.close()