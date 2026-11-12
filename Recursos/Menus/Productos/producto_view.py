import tkinter as tk
from tkinter import ttk, messagebox, END
from .dbproducto import dbProducto

from ... import estilo


class ProductosView(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de productos")
        self.geometry("700x500")
        self.configure(bg=estilo.backgroundColor)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("BotonesEstilo.TButton",**estilo.buttonstyle)
        self.style.map("BotonesEstilo.TButton",**estilo.buttonmap)

        self.style.configure("BotonesAceptar.TButton",**estilo.buttonstyle_aceptar)
        self.style.map("BotonesAceptar.TButton",**estilo.buttonmap_aceptar)
        self.style.configure("BotonesRechazar.TButton",**estilo.buttonstyle_rechazar)
        self.style.map("BotonesRechazar.TButton",**estilo.buttonmap_rechazar)

        self.db = dbProducto()

        # -------- BUSCAR --------
        tk.Label(self, text="Buscar producto por nombre:", bg=estilo.backgroundColor).place(x=50, y=30)

        self.txt_buscar = ttk.Entry(self, width=40)
        self.txt_buscar.place(x=230, y=30)

        ttk.Button(self, text="Buscar",style="BotonesEstilo.TButton", command=self.buscar_producto).place(x=480, y=30)

        # -------- CAMPOS --------
        
        self.ID = self.db.getMaxID() + 1
        tk.Label(self, text="ID:", bg=estilo.backgroundColor).place(x=100, y=100)
        self.txt_id = ttk.Entry(self)
        self.txt_id.place(x=200, y=100)
        self.txt_id.insert(0,self.ID)
        self.txt_id.config(state = "disabled")

        tk.Label(self, text="Nombre:", bg=estilo.backgroundColor).place(x=100, y=140)
        self.txt_nombre = ttk.Entry(self)
        self.txt_nombre.place(x=200, y=140)

        tk.Label(self, text="Tipo:", bg=estilo.backgroundColor).place(x=400, y=140)
        self.cmb_tipo = ttk.Combobox(self, values=["Medicamento", "Higiene","Bebidas","Snacks","Otro"])
        self.cmb_tipo.place(x=450, y=140)

        # 🔥 PROVEEDORES (COMBOBOX REAL)
        tk.Label(self, text="Proveedor:", bg=estilo.backgroundColor).place(x=100, y=180)
        self.cmb_proveedor = ttk.Combobox(self, state="readonly")
        self.cmb_proveedor.place(x=200, y=180)

        tk.Label(self, text="Precio compra:", bg=estilo.backgroundColor).place(x=100, y=220)
        self.txt_compra = ttk.Entry(self)
        self.txt_compra.place(x=200, y=220)

        tk.Label(self, text="Precio venta:", bg=estilo.backgroundColor).place(x=100, y=260)
        self.txt_venta = ttk.Entry(self)
        self.txt_venta.place(x=200, y=260)

        tk.Label(self, text="Stock:", bg=estilo.backgroundColor).place(x=100, y=300)
        self.txt_stock = ttk.Entry(self)
        self.txt_stock.place(x=200, y=300)

        tk.Label(self, text="Total:", bg=estilo.backgroundColor).place(x=100, y=340)
        self.txt_total = ttk.Entry(self, state="readonly")
        self.txt_total.place(x=200, y=340)

        #tk.Label(self,text = "¿Necesita receta?",background=estilo.backgroundColor).place(x = 430,y = 180)
        self.receta = tk.IntVar()
        self.Check_receta = tk.Checkbutton(self,text="¿Necesita receta?",variable=self.receta,background=estilo.backgroundColor)
        #self.receta.place(x = 470,y = 200)
        self.Check_receta.place(x = 430,y = 180)

        # -------- EVENTOS --------
        self.txt_venta.bind("<KeyRelease>", self.calcular_total)
        self.txt_stock.bind("<KeyRelease>", self.calcular_total)

        # -------- BOTONES --------
        self.agregar_button = ttk.Button(self, text="Agregar",style="BotonesAceptar.TButton", command=self.agregar)
        self.agregar_button.place(x=450, y=260)

        self.editar_button = ttk.Button(self, text="Editar",style="BotonesEstilo.TButton",state = "disabled", command=self.editar)
        self.editar_button.place(x=450, y=320)

        self.eliminar_button = ttk.Button(self, text="Eliminar",style="BotonesRechazar.TButton",state = "disabled",command=self.eliminar)
        self.eliminar_button.place(x=550, y=320)

        self.limpiar_button = ttk.Button(self, text="Limpiar",style="BotonesEstilo.TButton", command=self.limpiar)
        self.limpiar_button.place(x=550, y=260)

        # 🔥 cargar proveedores
        self.cargar_proveedores()

    # ==============================
    # 🔥 PROVEEDORES
    # ==============================
    def cargar_proveedores(self):
        self.lista_proveedores = self.db.obtener_proveedores()

        nombres = [p["nombre"] for p in self.lista_proveedores]
        self.cmb_proveedor["values"] = nombres

    def obtener_id_proveedor(self):
        nombre = self.cmb_proveedor.get()

        for p in self.lista_proveedores:
            if p["nombre"] == nombre:
                return p["id"]

        return None

    # ==============================
    # 🔍 BUSCAR
    # ==============================
    def buscar_producto(self):
        nombre = self.txt_buscar.get()

        if nombre == "":
            messagebox.showwarning("Error", "Escribe un nombre",parent=self)
            return

        producto = self.db.buscar(nombre)

        if producto:
            self.txt_id.config(state = "normal")
            self.txt_id.delete(0, END)
            self.txt_id.insert(0, producto["id"])
            self.txt_id.config(state = "disabled")

            self.txt_nombre.delete(0, END)
            self.txt_nombre.insert(0, producto["nombre"])

            self.cmb_tipo.set(producto["tipo"])
            if producto["receta"]:
              self.Check_receta.select()
              self.receta.set(1)
            else:
              self.Check_receta.deselect()
              self.receta.set(0)

            # 🔥 seleccionar proveedor
            for p in self.lista_proveedores:
                if p["id"] == producto["id_proveedor"]:
                    self.cmb_proveedor.set(p["nombre"])

            self.txt_compra.delete(0, END)
            self.txt_compra.insert(0, producto["precio_compra"])

            self.txt_venta.delete(0, END)
            self.txt_venta.insert(0, producto["precio_venta"])

            self.txt_stock.delete(0, END)
            self.txt_stock.insert(0, producto["stock"])

            self.calcular_total()

            self.agregar_button.config(state = "disabled")
            self.editar_button.config(state = "normal") 
            self.eliminar_button.config(state = "normal")
        else:
            messagebox.showerror("Error", "Producto no encontrado",parent=self)

    # ==============================
    # ➕ AGREGAR
    # ==============================
    def agregar(self):
        try:
            id_proveedor = self.obtener_id_proveedor()

            if not id_proveedor:
                messagebox.showwarning("Error", "Selecciona proveedor",parent=self)
                return

            self.db.insertar(
                self.txt_nombre.get(),
                self.cmb_tipo.get(),
                id_proveedor,
                float(self.txt_compra.get()),
                float(self.txt_venta.get()),
                int(self.txt_stock.get()),
                self.receta.get()
            )

            messagebox.showinfo("OK", "Producto agregado",parent=self)
            self.limpiar()

        except Exception as e:
            messagebox.showerror("Error", str(e),parent=self)

    # ==============================
    # ✏️ EDITAR
    # ==============================
    def editar(self):
        try:
            id_proveedor = self.obtener_id_proveedor()

            self.db.editar(
                self.txt_id.get(),
                self.txt_nombre.get(),
                self.cmb_tipo.get(),
                id_proveedor,
                float(self.txt_compra.get()),
                float(self.txt_venta.get()),
                int(self.txt_stock.get()),
                self.receta.get()
            )

            messagebox.showinfo("OK", "Producto actualizado",parent=self)

        except Exception as e:
            messagebox.showerror("Error", str(e),parent=self)

    # ==============================
    # ❌ ELIMINAR
    # ==============================
    def eliminar(self):
        idp = self.txt_id.get()

        if idp == "":
            messagebox.showwarning("Error", "Selecciona producto",parent=self)
            return

        self.db.eliminar(idp)

        messagebox.showinfo("OK", "Producto eliminado",parent=self)
        self.limpiar()

    # ==============================
    # 🧮 TOTAL
    # ==============================
    def calcular_total(self, event=None):
        try:
            venta = float(self.txt_venta.get())
            stock = int(self.txt_stock.get())

            total = venta * stock

            self.txt_total.config(state="normal")
            self.txt_total.delete(0, END)
            self.txt_total.insert(0, str(total))
            self.txt_total.config(state="readonly")
        except:
            pass

    # ==============================
    # 🧹 LIMPIAR
    # ==============================
    def limpiar(self):
        self.txt_id.config(state = "normal")
        self.txt_id.delete(0, END)
        self.txt_id.insert(0,self.ID)
        self.txt_id.config(state = "disabled")
        self.txt_nombre.delete(0, END)
        self.txt_compra.delete(0, END)
        self.txt_venta.delete(0, END)
        self.txt_stock.delete(0, END)

        self.cmb_tipo.set("")
        self.cmb_proveedor.set("")

        self.txt_total.config(state="normal")
        self.txt_total.delete(0, END)
        self.txt_total.config(state="readonly")

        self.agregar_button.config(state = "normal")
        self.editar_button.config(state = "disabled") 
        self.eliminar_button.config(state = "disabled")

        self.Check_receta.deselect()
        self.receta.set(0)