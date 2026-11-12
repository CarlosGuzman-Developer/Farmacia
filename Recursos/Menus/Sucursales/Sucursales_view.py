import tkinter as tk
from tkinter import ttk, messagebox, END
from .dbSucursal import dbSucursal
from ... import estilo

import json

class SucursalesView(tk.Toplevel):
    def __init__(self,sucursal,ruta, master=None):
        super().__init__(master)
        self.title("Sucursales")
        self.geometry("700x150")
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

        ttk.Label(self, text="direccion",background=estilo.backgroundColor).place(x=20, y=60)
        self.txt_direccion = ttk.Entry(self,width=80)
        self.txt_direccion.place(x=120, y=60)

        # -------- BOTONES --------
        ttk.Button(self, text="Buscar",style="BotonesEstilo.TButton",command=self.buscar_sucursal).place(x=210, y=10)
        ttk.Button(self, text="Guardar",style="BotonesEstilo.TButton", command=self.guardar_sucursal).place(x=120, y=100)
        self.EliminarBoton = ttk.Button(self, text="Eliminar",style="BotonesRechazar.TButton",command=self.eliminar_sucursal)
        self.EliminarBoton.place(x=220, y=100)
        self.EliminarBoton.config(state="disabled")
        ttk.Button(self, text="Limpiar",style="BotonesEstilo.TButton", command=self.limpiar_campos).place(x=320, y=100)

    # -------- FUNCIONES --------

    def buscar_sucursal(self):
        id= self.txt_id.get().strip()

        if id == "":
            messagebox.showwarning("Error", "Ingresa una id a buscar")
            return

        db = dbSucursal()
        sucursal = db.buscar(id)

        if sucursal:
            self.txt_id.delete(0, END)
            self.txt_id.insert(0, sucursal["id"])
            
            self.txt_direccion.delete(0, END)
            self.txt_direccion.insert(0, sucursal["direccion"])

            self.EliminarBoton.config(state="normal")
        else:
            messagebox.showerror(parent=self,title="Error",message="sucursal no encontrada")
            self.txt_id.delete(0,END)

    def guardar_sucursal(self,sucursal,ruta):
        id_sucursal = self.txt_id.get().strip()
        direccion = self.txt_direccion.get().strip()

        if direccion == "":
            messagebox.showwarning("Error", "No hay una direccion asignada")
            return

        db = dbSucursal()

        if id_sucursal != "":
            ok = db.actualizar(id_sucursal, direccion)
            if ok:
                messagebox.showinfo("OK", "sucursal actualizada")
                if id_sucursal == sucursal['id']:
                    sucursal['direccion'] = direccion
                    with open (ruta + "/Recursos/sucursal.json","w") as archivo:
                        json.dump({'id' : id_sucursal,'direccion' : direccion},archivo,indent=4, ensure_ascii=False)
            else:
                messagebox.showerror("Error", "No se pudo actualizar")
        else:
            ok = db.insertar(direccion)
            if ok:
                messagebox.showinfo("OK", "sucursal guardada")
            else:
                messagebox.showerror("Error", "No se pudo guardar")

        self.limpiar_campos()

    def eliminar_sucursal(self):
        id_sucursal = self.txt_id.get().strip()

        if id_sucursal == "":
            messagebox.showwarning("Error", "Ingresa un ID")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Eliminar sucursal?")

        if confirm:
            db = dbSucursal()
            ok = db.eliminar(id_sucursal)

            if ok:
                messagebox.showinfo("OK", "sucursal eliminado")
                self.limpiar_campos()
                if id_sucursal == self.sucursal['id']:
                    self.sucursal['id'] = 0
                    self.sucursal['direccion'] = "No especificado"
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    def limpiar_campos(self):
        self.txt_id.delete(0, END)
        self.txt_direccion.delete(0, END)
        self.EliminarBoton.config(state="disabled")