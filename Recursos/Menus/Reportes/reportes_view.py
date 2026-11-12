import tkinter as tk
from tkinter import ttk

from .dbReportes import dbReportes


class ReportesView(tk.Toplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Reportes")

        self.geometry("900x500")

        self.db = dbReportes()

        # =========================
        # TABLA
        # =========================
        self.tabla = ttk.Treeview(self)

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================
        # FRAME BOTONES
        # =========================
        frame = tk.Frame(self)

        frame.pack(pady=10)

        # =========================
        # BOTONES
        # =========================
        ttk.Button(
            frame,
            text="Clientes por ciudad",
            command=self.reporte_clientes
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            frame,
            text="Ventas por fecha",
            command=self.reporte_ventas
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            frame,
            text="Compras por fecha",
            command=self.reporte_compras
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            frame,
            text="Facturas mayores ventas",
            command=self.reporte_facturas
        ).grid(row=0, column=3, padx=5)

    # =========================
    # LIMPIAR TABLA
    # =========================
    def limpiar_tabla(self):

        self.tabla.delete(*self.tabla.get_children())

    # =========================
    # CLIENTES POR CIUDAD
    # =========================
    def reporte_clientes(self):

        self.limpiar_tabla()

        self.tabla["columns"] = (
            "ciudad",
            "total"
        )

        self.tabla.heading("#0", text="")

        self.tabla.heading(
            "ciudad",
            text="Ciudad"
        )

        self.tabla.heading(
            "total",
            text="Clientes"
        )

        self.tabla.column(
            "ciudad",
            width=250
        )

        self.tabla.column(
            "total",
            width=120
        )

        datos = self.db.clientes_por_ciudad()

        print(datos)

        for d in datos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    d["ciudad"],
                    d["total"]
                )
            )

    # =========================
    # VENTAS POR FECHA
    # =========================
    def reporte_ventas(self):

        self.limpiar_tabla()

        self.tabla["columns"] = (
            "fecha",
            "total"
        )

        self.tabla.heading("#0", text="")

        self.tabla.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla.heading(
            "total",
            text="Total Ventas"
        )

        self.tabla.column(
            "fecha",
            width=250
        )

        self.tabla.column(
            "total",
            width=180
        )

        datos = self.db.ventas_por_fecha()

        print(datos)

        for d in datos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    str(d["fecha"]),
                    str(d["total"])
                )
            )

    # =========================
    # COMPRAS POR FECHA
    # =========================
    def reporte_compras(self):

        self.limpiar_tabla()

        self.tabla["columns"] = (
            "fecha",
            "total"
        )

        self.tabla.heading("#0", text="")

        self.tabla.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla.heading(
            "total",
            text="Total Compras"
        )

        self.tabla.column(
            "fecha",
            width=250
        )

        self.tabla.column(
            "total",
            width=180
        )

        datos = self.db.compras_por_fecha()

        print(datos)

        for d in datos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    str(d["fecha"]),
                    str(d["total"])
                )
            )

    # =========================
    # FACTURAS MAYORES VENTAS
    # =========================
    def reporte_facturas(self):

        self.limpiar_tabla()

        self.tabla["columns"] = (
            "id",
            "cliente",
            "total",
            "fecha"
        )

        self.tabla.heading("#0", text="")

        self.tabla.heading(
            "id",
            text="Factura"
        )

        self.tabla.heading(
            "cliente",
            text="Cliente"
        )

        self.tabla.heading(
            "total",
            text="Total Venta"
        )

        self.tabla.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla.column(
            "id",
            width=80
        )

        self.tabla.column(
            "cliente",
            width=120
        )

        self.tabla.column(
            "total",
            width=150
        )

        self.tabla.column(
            "fecha",
            width=220
        )

        datos = self.db.facturas_mayores_ventas()

        print(datos)

        for d in datos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    d["id"],
                    d["id_cliente"],
                    str(d["total"]),
                    str(d["fecha"])
                )
            )