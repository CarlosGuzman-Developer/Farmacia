import tkinter as tk
from tkinter import ttk, messagebox, END
from .dbCliente import dbCliente
from ... import estilo

class ClientesView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Clientes")
        self.geometry("500x400")
        self.configure(background=estilo.backgroundColor)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Boton")
        style.configure("BotonesEstilo.TButton",**estilo.buttonstyle)
        style.map("BotonesEstilo.TButton",**estilo.buttonmap)

        style.configure("BotonesRechazar.TButton",**estilo.buttonstyle_rechazar)
        style.map("BotonesRechazar.TButton",**estilo.buttonmap_rechazar)

        # -------- CAMPOS --------
        ttk.Label(self, text="Busqueda por ID:",background=estilo.backgroundColor).place(x=20, y=10)
        self.txt_id = ttk.Entry(self,width=10)
        self.txt_id.place(x=135, y=10)

        ttk.Label(self, text="Nombre",background=estilo.backgroundColor).place(x=20, y=60)
        self.txt_nombre = ttk.Entry(self)
        self.txt_nombre.place(x=120, y=60)

        ttk.Label(self, text="Teléfono",background=estilo.backgroundColor).place(x=20, y=100)
        self.txt_telefono = ttk.Entry(self)
        self.txt_telefono.place(x=120, y=100)

        ttk.Label(self, text="Correo",background=estilo.backgroundColor).place(x=20, y=140)
        self.txt_correo = ttk.Entry(self,width=50)
        self.txt_correo.place(x=120, y=140)

        ttk.Label(self, text="RFC",background=estilo.backgroundColor).place(x=20, y=180)
        self.txt_rfc = ttk.Entry(self)
        self.txt_rfc.place(x=120, y=180)

        ttk.Label(self, text="Ciudad",background=estilo.backgroundColor).place(x=20, y=220)
        self.txt_ciudad = ttk.Entry(self)
        self.txt_ciudad.place(x=120, y=220)

        ttk.Label(self, text="Puntos",background=estilo.backgroundColor).place(x=20, y=260)
        self.txt_puntos = ttk.Entry(self)
        self.txt_puntos.place(x=120, y=260)

        # -------- BOTONES --------
        ttk.Button(self, text="Buscar",style="BotonesEstilo.TButton",command=self.buscar_cliente).place(x=210, y=10)
        ttk.Button(self, text="Guardar",style="BotonesEstilo.TButton", command=self.guardar_cliente).place(x=120, y=320)
        self.EliminarBoton = ttk.Button(self, text="Eliminar",style="BotonesRechazar.TButton",command=self.eliminar_cliente)
        self.EliminarBoton.place(x=220, y=320)
        self.EliminarBoton.config(state="disabled")
        ttk.Button(self, text="Limpiar",style="BotonesEstilo.TButton", command=self.limpiar_campos).place(x=320, y=320)

    # -------- FUNCIONES --------

    def buscar_cliente(self):
        id_cliente = self.txt_id.get().strip()

        if id_cliente == "":
            messagebox.showwarning("Error", "Ingresa un ID")
            return

        db = dbCliente()
        cliente = db.buscar(id_cliente)

        if cliente:
            self.txt_nombre.delete(0, END)
            self.txt_nombre.insert(0, cliente["nombre"])

            self.txt_telefono.delete(0, END)
            self.txt_telefono.insert(0, cliente["telefono"])

            self.txt_correo.delete(0, END)
            self.txt_correo.insert(0, cliente["correo"])

            self.txt_rfc.delete(0, END)
            self.txt_rfc.insert(0, cliente["rfc"])

            self.txt_ciudad.delete(0, END)
            self.txt_ciudad.insert(0, cliente["ciudad"])

            self.txt_puntos.delete(0, END)
            self.txt_puntos.insert(0, cliente["puntos"])

            self.EliminarBoton.config(state="normal")
        else:
            messagebox.showerror(parent=self,title="Error",message="Cliente no encontrado")
            self.txt_id.delete(0,END)

    def guardar_cliente(self):
        id_cliente = self.txt_id.get().strip()
        nombre = self.txt_nombre.get().strip()
        telefono = self.txt_telefono.get().strip()
        correo = self.txt_correo.get().strip()
        rfc = self.txt_rfc.get().strip()
        ciudad = self.txt_ciudad.get().strip()
        puntos = self.txt_puntos.get().strip()

        if nombre == "" or telefono == "":
            messagebox.showwarning("Error", "Nombre y teléfono son obligatorios")
            return

        if puntos == "":
            puntos = 0

        db = dbCliente()

        # 🔥 INSERT o UPDATE automático
        if id_cliente != "":
            ok = db.actualizar(id_cliente, nombre, telefono, correo, rfc, ciudad, puntos)
            if ok:
                messagebox.showinfo("OK", "Cliente actualizado")
            else:
                messagebox.showerror("Error", "No se pudo actualizar")
        else:
            ok = db.insertar(nombre, telefono, correo, rfc, ciudad, puntos)
            if ok:
                messagebox.showinfo("OK", "Cliente guardado")
            else:
                messagebox.showerror("Error", "No se pudo guardar")

        self.limpiar_campos()

    def eliminar_cliente(self):
        id_cliente = self.txt_id.get().strip()

        if id_cliente == "":
            messagebox.showwarning("Error", "Ingresa un ID")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Eliminar cliente?")

        if confirm:
            db = dbCliente()
            ok = db.eliminar(id_cliente)

            if ok:
                messagebox.showinfo("OK", "Cliente eliminado")
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    def limpiar_campos(self):
        self.txt_id.delete(0, END)
        self.txt_nombre.delete(0, END)
        self.txt_telefono.delete(0, END)
        self.txt_correo.delete(0, END)
        self.txt_rfc.delete(0, END)
        self.txt_ciudad.delete(0, END)
        self.txt_puntos.delete(0, END)
        self.EliminarBoton.config(state="disabled")