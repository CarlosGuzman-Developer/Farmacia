import tkinter as tk
from tkinter import ttk, messagebox, END
from .dbCompra import dbCompra

#from collections import defaultdict

from ... import estilo

class CompraView(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Compras a proveedor")
        self.geometry("670x530")
        self.configure(bg = estilo.backgroundColor)

        #configuración del estilo de los botones
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("BotonesEstilo.TButton",**estilo.buttonstyle)
        self.style.map("BotonesEstilo.TButton",**estilo.buttonmap)

        self.style.configure("BotonesAceptar.TButton",**estilo.buttonstyle_aceptar)
        self.style.map("BotonesAceptar.TButton",**estilo.buttonmap_aceptar)
        self.style.configure("BotonesRechazar.TButton",**estilo.buttonstyle_rechazar)
        self.style.map("BotonesRechazar.TButton",**estilo.buttonmap_rechazar)

        self.db = dbCompra()

        self.ID = self.db.obtener_maxID() + 1
        ttk.Label(self, text="ID:",background=estilo.backgroundColor).place(x=500, y=40)
        self.entry_id = ttk.Entry(self, width=30)
        self.entry_id.insert(0,self.ID)
        self.entry_id.config(state = "disabled")
        self.entry_id.place(x=480, y=60)
        
        ttk.Label(self, text="Producto",background=estilo.backgroundColor).place(x=40, y=40)
        self.combo_producto = ttk.Combobox(self, state="readonly", width=30)
        self.combo_producto.place(x=180, y=40)

        ttk.Label(self, text="Proveedor",background=estilo.backgroundColor).place(x=40, y=90)
        self.entry_proveedor = ttk.Entry(self,state ="disabled", width=30)
        self.entry_proveedor.place(x=180, y=90)

        ttk.Label(self, text="Cantidad",background=estilo.backgroundColor).place(x=40, y=140)
        self.txt_cantidad = ttk.Entry(self, width=32)
        self.txt_cantidad.place(x=180, y=140)

        ttk.Label(self, text="Precio unitario",background=estilo.backgroundColor).place(x=40, y=190)
        self.lbl_precio = ttk.Label(self,text = "$0",background="White")
        self.lbl_precio.place(x=180, y=190)

        ttk.Label(self, text="Total: ",background=estilo.backgroundColor,font=("Arial",15)).place(x=500, y=480)
        self.str_total = tk.StringVar(value = "$0")
        self.txt_total = ttk.Label(self,textvariable = self.str_total,background="White",font=("Arial",15))
        self.txt_total.place(x=560, y=480)

        #definicion del arbol de compras
        self.compras_tree = ttk.Treeview(self,columns=("Producto","Proveedor","Cantidad","Precio_compra"),show="headings",selectmode="browse")
        
        self.compras_tree.column("Producto", width=220, stretch=True)
        self.compras_tree.heading("Producto", text="Producto")

        self.compras_tree.column("Proveedor", width=220, stretch=True)
        self.compras_tree.heading("Proveedor", text="Proveedor")

        self.compras_tree.column("Cantidad", width=80, anchor=tk.CENTER)
        self.compras_tree.heading("Cantidad", text="Cantidad")

        self.compras_tree.column("Precio_compra", width=120, anchor=tk.CENTER)
        self.compras_tree.heading("Precio_compra", text="Precio compra")

        self.compras_tree.place(x = 10, y = 230)

        ttk.Button(self,text = "Añadir",style="BotonesAceptar.TButton",command=self.añadir).place(x=430, y=190)
        self.btt_eliminar = ttk.Button(self,text = "Eliminar",style="BotonesRechazar.TButton",state="disabled",command = self.eliminar)
        self.btt_eliminar.place(x=520, y=190)
        
        ttk.Button(self, text="Registrar compra",style="BotonesEstilo.TButton", command=self.registrar_compra).place(x=180, y=480)
        #ttk.Button(self, text="Limpiar", style="BotonesEstilo.TButton", command=self.limpiar).place(x=320, y=250)

        self.cargar_productos()
        self.cargar_proveedores()

        self.combo_producto.bind("<<ComboboxSelected>>", self.mostrar_producto)
        self.compras_tree.bind("<<TreeviewSelect>>",self.desbloquearEliminar)

    def añadir(self):
        if any(c.get() == "" for c in [self.combo_producto,self.entry_proveedor,self.txt_cantidad]):
            messagebox.showerror(title="Error campos faltantes",message="Rellene todos los campos")
            return
             
        precios = self.db.obtener_productos()
        for precio in precios:
            if precio["nombre"] == self.combo_producto.get():
             precios = float(precio["precio_compra"])


        if self.compras_tree.get_children():
            encontrado = False
            for item in self.compras_tree.get_children():
                producto = self.compras_tree.item(item,"values")
                if producto[0] == self.combo_producto.get():
                 encontrado = True
                 self.compras_tree.item(item, values=(producto[0],producto[1],str(int(producto[2]) + int(self.txt_cantidad.get())), str(precios * (int(producto[2]) + int(self.txt_cantidad.get())))))
            if encontrado == False:
                self.compras_tree.insert("",END,values=(self.combo_producto.get(),self.entry_proveedor.get(),self.txt_cantidad.get(),str(int(self.txt_cantidad.get()) * precios)))
        else:
            self.compras_tree.insert("",END,values=(self.combo_producto.get(),self.entry_proveedor.get(),self.txt_cantidad.get(),str(int(self.txt_cantidad.get()) * precios)))

        self.actualizarTotal()    
    
    def eliminar(self):
        producto = self.compras_tree.selection()
        nombre = str(self.compras_tree.item(producto,"values")[0])

        confirmacion = messagebox.askyesno(title="Confirmación",message="¿Está seguro que desea elimiar " + nombre,parent=self)


        if confirmacion == True:
            self.compras_tree.delete(producto)
            self.actualizarTotal()    
    
    def mostrar_producto(self, event=None):
        producto = self.obtener_producto(self.combo_producto.get())
        if producto:
            self.entry_proveedor.config(state="normal")
            self.entry_proveedor.delete(0,END)
            self.entry_proveedor.insert(0,str(self.obtener_nombre_proveedor(producto["id_proveedor"])))
            self.entry_proveedor.config(state="disabled")

            self.lbl_precio.config(text = "$" + str(producto["precio_compra"]))

    def actualizarTotal(self):
        costo_total = 0
        for item in self.compras_tree.get_children(): 
         producto = self.compras_tree.item(item,"values")
         costo_total = costo_total + float(producto[3])
        
        self.str_total.set("$" + str(costo_total))

    def desbloquearEliminar(self,event=None):
        seleccion = self.compras_tree.selection()

        if seleccion:
         self.btt_eliminar.config(state = "normal")
        else:
           self.btt_eliminar.config(state = "disabled")
    
    def cargar_productos(self):
        self.lista_productos = self.db.obtener_productos()
        self.combo_producto["values"] = [p["nombre"] for p in self.lista_productos]

    def obtener_producto(self,nombre):
        for p in self.lista_productos:
            if p["nombre"] == nombre:
                return p
        return None    

    def cargar_proveedores(self):
        self.lista_proveedores = self.db.obtener_proveedores()

    def obtener_id_producto(self, nombre):
        for p in self.lista_productos:
            if p["nombre"] == nombre:
                return p["id"]
        return None

    def obtener_nombre_proveedor(self,id):
        for p in self.lista_proveedores:
            if p["id"] == id:
                return p["nombre"]
        return None
    
    def obtener_id_proveedor(self,nombre):
        for p in self.lista_proveedores:
            if p["nombre"] == nombre:
                return p["id"]
        return None

    def registrar_compra(self):
        carrito = []
        proveedores = {}
        #productos_separados = defaultdict(list)
        productos_separados = {}
        for item in self.compras_tree.get_children():
         producto = self.compras_tree.item(item,"values")
         datos = [self.obtener_id_producto(producto[0]),self.obtener_id_proveedor(producto[1]),int(producto[2]),float(producto[3])]
         carrito.append(datos)

         proveedor = self.db.obtener_proveedor(producto[1])
         nombre = proveedor["nombre"]
         correo = proveedor["correo"]

         if nombre not in proveedores:
             proveedores[nombre] = correo
         
         producto_para_separar = {
             "nombre": producto[0],
             "cantidad": producto[2],
             "precio": producto[3]
         }

         productos_separados.setdefault(correo,[]).append(producto_para_separar)


        ok, mensaje= self.db.registrar_multiple(self.ID, carrito,productos_separados)

        if ok:
            messagebox.showinfo(title ="OK", message =  mensaje + "\nRevise la factura en /facturas/compras", parent=self)
            self.limpiar()
        else:
            messagebox.showerror(message ="Error" + mensaje, parent=self)

        

    def limpiar(self):
        self.entry_id.config(state = "normal")
        self.entry_id.delete(0,END) 
        
        self.ID = self.db.obtener_maxID() + 1
        self.entry_id.insert(0,self.ID)
        self.entry_id.config(state = "disabled")        
        
        self.combo_producto.set("")
        self.entry_proveedor.config(state = "normal")
        self.entry_proveedor.delete(0,END)
        self.entry_proveedor.config(state = "disabled")
        self.txt_cantidad.delete(0, END)
        self.lbl_precio.config(text = "$0")

        for item in self.compras_tree.get_children():
          self.compras_tree.delete(item)

        self.actualizarTotal()