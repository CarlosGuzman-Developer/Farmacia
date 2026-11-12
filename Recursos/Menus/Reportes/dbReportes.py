from ...conexion import conectar


class dbReportes:

    # =========================
    # CLIENTES POR CIUDAD
    # =========================
    def clientes_por_ciudad(self):

        con = conectar()

        try:

            cursor = con.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    ciudad,
                    COUNT(*) AS total
                FROM clientes
                GROUP BY ciudad
                ORDER BY total DESC
            """)

            datos = cursor.fetchall()

            print(datos)

            return datos

        except Exception as e:

            print("Error clientes_por_ciudad:", e)

            return []

        finally:

            con.close()

    # =========================
    # VENTAS POR FECHA
    # =========================
    def ventas_por_fecha(self):

        con = conectar()

        try:

            cursor = con.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    DATE(fecha) AS fecha,
                    SUM(total) AS total
                FROM ventas
                GROUP BY DATE(fecha)
                ORDER BY fecha DESC
            """)

            datos = cursor.fetchall()

            print(datos)

            return datos

        except Exception as e:

            print("Error ventas_por_fecha:", e)

            return []

        finally:

            con.close()

    # =========================
    # COMPRAS POR FECHA
    # =========================
    def compras_por_fecha(self):

        con = conectar()

        try:

            cursor = con.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    DATE(fecha) AS fecha,
                    SUM(precio_compra * cantidad) AS total
                FROM compras
                GROUP BY DATE(fecha)
                ORDER BY fecha DESC
            """)

            datos = cursor.fetchall()

            print(datos)

            return datos

        except Exception as e:

            print("Error compras_por_fecha:", e)

            return []

        finally:

            con.close()

    # =========================
    # FACTURAS MAYORES VENTAS
    # =========================
    def facturas_mayores_ventas(self):

        con = conectar()

        try:

            cursor = con.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    id_cliente,
                    total,
                    fecha
                FROM ventas
                ORDER BY total DESC
                LIMIT 10
            """)

            datos = cursor.fetchall()

            print(datos)

            return datos

        except Exception as e:

            print("Error facturas_mayores_ventas:", e)

            return []

        finally:

            con.close()