from pathlib import Path
import os 
from datetime import datetime
from tkinter import messagebox

from fpdf import FPDF

ruta_logo = Path(__file__)
ruta_logo = ruta_logo.parents[2]
ruta_logo = ruta_logo / "Logo.png"

# =========================
# FACTURA DE VENTA
# =========================
def generar_factura_venta(cliente, productos, total, descuento,sucursal):

    
    carpeta = ruta_logo.parents[1]

    carpeta = os.path.join(
        carpeta,
        "Facturas",
        "Ventas"
    )

    os.makedirs(carpeta, exist_ok=True)

    nombre_archivo = os.path.join(
        carpeta,
        f"factura_venta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    pdf = FPDF()

    pdf.add_page()

    pdf.image(ruta_logo,x = 0,y = 0, w = 50) 

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        200,
        10,
        "FACTURA DE VENTA",
        ln=True,
        align="C"
    )

    pdf.ln(35)

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.cell(
        200,
        10,
        f"Cliente: {cliente}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        ln=True
    )

    pdf.ln(10)

    for producto in productos:

        nombre = producto[0]

        cantidad = int(producto[1])

        subtotal = float(producto[2])

        precio_unitario = subtotal / cantidad

        texto = \
            f"Producto: {nombre} | " +\
            f"Cantidad: {cantidad} | " + \
            f"Precio: ${precio_unitario:.2f} | " + \
            f"Subtotal: ${subtotal:.2f}"  
        

        pdf.cell(
            0,
            10,
            texto
        )

        pdf.ln(10)

    pdf.ln(30)

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        f"Subtotal: ${total:.2f}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Descuento: ${descuento:.2f}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"TOTAL: ${(total - descuento):.2f}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Sucursal: {sucursal['id']} - {sucursal['direccion']}",
        ln=True
    )

    pdf.output(nombre_archivo)

    messagebox.showinfo(
        "Factura",
        "Factura generada correctamente"
    )

    return nombre_archivo


# =========================
# FACTURA DE COMPRA
# =========================
def generar_factura_compra(id,productos, total,sucursal):

    carpeta = ruta_logo.parents[1]

    carpeta = os.path.join(
        carpeta,
        "Facturas",
        "Compras"
    )

    os.makedirs(carpeta, exist_ok=True)

    nombre_archivo = os.path.join(
        carpeta,
        f"factura_compra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    pdf = FPDF()

    pdf.add_page()

    pdf.image(ruta_logo,x = 0,y = 0, w = 50) 

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        200,
        10,
        "FACTURA DE COMPRA",
        ln=True,
        align="C"
    )

    pdf.ln(35)

    pdf.set_font(
        "Arial",
        "",
        10
    )

    pdf.cell(
        200,
        10,
        f"Folio: {id}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        ln=True
    )

    pdf.ln(10)

    for producto in productos:

        pdf.cell(
            0,
            10,
            producto
        )
        pdf.ln(10)

    pdf.ln(30)

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        f"Sucursal: {sucursal['id']} - {sucursal['direccion']}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"TOTAL: ${total:.2f}",
        ln=True
    )

    pdf.output(nombre_archivo)

    messagebox.showinfo(
        "Factura",
        "Factura de compra generada"
    )

    return nombre_archivo