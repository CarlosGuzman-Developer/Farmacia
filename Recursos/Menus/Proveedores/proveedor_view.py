import tkinter as tk
from tkinter import ttk, messagebox
from .proveedor import Proveedor
from .dbproveedor import DBProveedor

class ProveedoresView:

    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Proveedores")

        self.db = DBProveedor()
        self.id = None

        # FORMULARIO
        tk.Label(self.root, text="Nombre").grid(row=0, column=0)
        self.nombre = tk.Entry(self.root)
        self.nombre.grid(row=0, column=1)

        tk.Label(self.root, text="Correo").grid(row=1, column=0)
        self.correo = tk.Entry(self.root)
        self.correo.grid(row=1, column=1)

        tk.Label(self.root, text="Teléfono").grid(row=2, column=0)
        self.telefono = tk.Entry(self.root)
        self.telefono.grid(row=2, column=1)

        # BOTONES CRUD
        tk.Button(self.root, text="Guardar", command=self.guardar).grid(row=3, column=0)
        tk.Button(self.root, text="Actualizar", command=self.actualizar).grid(row=3, column=1)
        tk.Button(self.root, text="Eliminar", command=self.eliminar).grid(row=3, column=2)

        # TABLA
        self.tabla = ttk.Treeview(self.root, columns=("ID","Nombre","Correo","Telefono"), show="headings")
        for col in ("ID","Nombre","Correo","Telefono"):
            self.tabla.heading(col, text=col)
        self.tabla.grid(row=4, column=0, columnspan=3)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        # 🔍 BUSQUEDA
        tk.Label(self.root, text="Buscar ID").grid(row=5, column=0)
        self.buscar_id = tk.Entry(self.root)
        self.buscar_id.grid(row=5, column=1)
        tk.Button(self.root, text="Buscar", command=self.buscar_por_id).grid(row=5, column=2)

        tk.Label(self.root, text="Buscar Nombre").grid(row=6, column=0)
        self.buscar_nombre = tk.Entry(self.root)
        self.buscar_nombre.grid(row=6, column=1)
        tk.Button(self.root, text="Buscar", command=self.buscar_por_nombre).grid(row=6, column=2)

        tk.Label(self.root, text="Buscar Correo").grid(row=7, column=0)
        self.buscar_correo = tk.Entry(self.root)
        self.buscar_correo.grid(row=7, column=1)
        tk.Button(self.root, text="Buscar", command=self.buscar_por_correo).grid(row=7, column=2)

        tk.Button(self.root, text="Mostrar Todos", command=self.cargar).grid(row=8, column=1)

        self.cargar()

    # CRUD
    def guardar(self):
        p = Proveedor(None, self.nombre.get(), self.correo.get(), self.telefono.get())
        self.db.insertar(p)
        self.cargar()

    def actualizar(self):
        if self.id:
            p = Proveedor(self.id, self.nombre.get(), self.correo.get(), self.telefono.get())
            self.db.actualizar(p)
            self.cargar()

    def eliminar(self):
        if self.id:
            confirmar = messagebox.askyesno("Confirmar", "¿Eliminar proveedor?")
            if confirmar:
                eliminado = self.db.eliminar(self.id)

                if eliminado:
                    messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
                    self.cargar()
                    self.limpiar()
                else:
                    messagebox.showerror(
                        "Error",
                        "No se puede eliminar porque tiene productos asociados"
                    )

    def limpiar(self):
        self.id = None
        self.nombre.delete(0, tk.END)
        self.correo.delete(0, tk.END)
        self.telefono.delete(0, tk.END)

    def cargar(self):
        self.mostrar_datos(self.db.obtener())

    # TABLA
    def mostrar_datos(self, datos):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for p in datos:
            self.tabla.insert("", "end", values=p)

    def seleccionar(self, event):
        if not self.tabla.selection():
            return

        item = self.tabla.selection()[0]
        datos = self.tabla.item(item, "values")

        self.id = datos[0]

        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, datos[1])

        self.correo.delete(0, tk.END)
        self.correo.insert(0, datos[2])

        self.telefono.delete(0, tk.END)
        self.telefono.insert(0, datos[3])

    # 🔍 BUSQUEDAS
    def buscar_por_id(self):
        datos = self.db.buscar_por_id(self.buscar_id.get())
        self.mostrar_datos(datos)

    def buscar_por_nombre(self):
        datos = self.db.buscar_por_nombre(self.buscar_nombre.get())
        self.mostrar_datos(datos)

    def buscar_por_correo(self):
        datos = self.db.buscar_por_correo(self.buscar_correo.get())
        self.mostrar_datos(datos)