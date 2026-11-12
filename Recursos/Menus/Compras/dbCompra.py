from ...conexion import conectar
from ..Ventas.factura import generar_factura_compra
from .email_service import enviar_correo_proveedor

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

sucursal = {}

class dbCompra:

    sucursal = abrir_sucursal()
    
    def obtener_proveedores(self):
        con = conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, correo FROM proveedores")
        datos = cursor.fetchall()
        con.close()
        return datos
    
    def obtener_proveedor(self,nombre):
        con = conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT nombre, correo FROM proveedores WHERE nombre=%s",(nombre,))
        datos = cursor.fetchone()
        con.close()
        return datos

    def obtener_productos(self):
        con = conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, id_proveedor,precio_compra, stock FROM productos WHERE sucursal_id=%s ",(self.sucursal['id'],))
        datos = cursor.fetchall()
        con.close()
        return datos
    
    def obtener_producto_id(self,id):
        con = conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT nombre FROM productos WHERE id=%s AND sucursal_id = %s",(id,self.sucursal['id']))
        datos = cursor.fetchone()
        con.close()
        return datos["nombre"]
    
    def obtener_proveedor_id(self,id):
        con = conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT nombre FROM proveedores WHERE id=%s",(id,))
        datos = cursor.fetchone()
        con.close()
        return datos["nombre"]
    
    def obtener_maxID(self):
        id = 0
        con = conectar()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT max(id) FROM compras")
        row = cursor.fetchone()
        if row['max(id)'] is not None:
            id = int(row['max(id)'])
        return id 

    # =========================
    # COMPRA SIMPLE
    # =========================
    def registrar(self, id_proveedor, id_producto, cantidad):
        con = conectar()

        try:
            cursor = con.cursor(dictionary=True)
            cantidad = int(cantidad)

            cursor.execute("SELECT * FROM productos WHERE id=%s", (id_producto,))
            producto = cursor.fetchone()

            cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id_proveedor,))
            proveedor = cursor.fetchone()

            if not producto or not proveedor:
                return False, "Datos inválidos"

            precio = float(producto["precio_compra"])
            total = precio * cantidad

            cursor.execute("""
                INSERT INTO compras (id_proveedor, total, fecha)
                VALUES (%s, %s, NOW())
            """, (id_proveedor, total))

            cursor.execute("""
                UPDATE productos
                SET stock = stock + %s
                WHERE id = %s
            """, (cantidad, id_producto))

            con.commit()

            generar_factura_compra(
                proveedor["nombre"],
                producto["nombre"],
                cantidad,
                precio,
                total
            )

            return True, f"Compra realizada. Total: ${total}"

        except Exception as e:
            print("Error compra:", e)
            con.rollback()
            return False, "Error en compra"

        finally:
            con.close()

    # =========================
    # COMPRA MULTIPLE (CARRITO)
    # =========================
    def registrar_multiple(self,id, carrito,productos_separados):
        con = conectar()

        sucursal = abrir_sucursal()
        
        try:
            cursor = con.cursor(dictionary=True)
            total_general = 0

            producto_para_factura = []

            for item in carrito:

                id_producto = item[0]
                id_proveedor = item[1]
                cantidad = int(item[2])
                precio = float(item[3]) / float (item[2])
                subtotal = precio * cantidad
                total_general += subtotal

                producto = "Producto: " + str(id_producto) + " - " + str(self.obtener_producto_id(id_producto)) + \
                  " /Proveedor: " +  str(self.obtener_proveedor_id(id_proveedor)) + \
                  " /Cantidad: " + str(cantidad) + \
                  " /Precio: " + str(precio) + \
                  " /Total: " + str(subtotal)
                producto_para_factura.append(producto) 
                
                cursor.execute("""
                    UPDATE productos
                    SET stock = stock + %s
                    WHERE id = %s 
                """, (cantidad, id_producto))

                cursor.execute("""
                    INSERT INTO compras (id,id_producto,id_proveedor, cantidad , precio_compra , fecha , sucursal_id)
                    VALUES (%s, %s,%s,%s,%s, NOW(),%s)
                """, (id,id_producto,id_proveedor,cantidad,precio,self.sucursal['id']))
            

            con.commit()

            generar_factura_compra(id,producto_para_factura,total_general,self.sucursal)

            for destinatario,productos in productos_separados.items():
              enviar_correo_proveedor(destinatario,productos,sucursal['direccion'])            

            return True, f"Compra realizada. Total: ${total_general}"

        except Exception as e:
            print("Error compra multiple:", e)
            con.rollback()
            return False, "Error en compra"

        finally:
            con.close()