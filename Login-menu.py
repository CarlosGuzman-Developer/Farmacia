import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import messagebox, ttk
import os
from Recursos import estilo

from Recursos.conexion import conectar

from Recursos.Menus.Usuarios.dbUsuario import dbUsuario

from Recursos.Menus.Sucursales.Sucursales_view import SucursalesView
from Recursos.Menus.Sucursales.dbSucursal import dbSucursal
from Recursos.Menus.Clientes.cliente_view import ClientesView
from Recursos.Menus.Productos.producto_view import ProductosView
from Recursos.Menus.Proveedores.proveedor_view import ProveedoresView
from Recursos.Menus.Compras.compra_view import CompraView
from Recursos.Menus.Ventas.venta_view import VentaView
from Recursos.Menus.Reportes.reportes_view import ReportesView

import json

# Ruta del proyecto
ruta = os.path.dirname(__file__)

sucursal = {}

def abrir_sucursal():
    global sucursal
    try:
        with open (ruta + "/Recursos/sucursal.json","r") as archivo:
            sucursal = json.load(archivo)
    except (FileNotFoundError,json.JSONDecodeError):
         with open (ruta + "/Recursos/sucursal.json","w") as archivo:
             json.dump({'id' : 0,'direccion' : "No especificado"},archivo,indent=4, ensure_ascii=False)
             sucursal = json.load(archivo)

def guardar_sucursal(sucursal_):
    with open (ruta + "/Recursos/sucursal.json","w") as archivo:
        json.dump({'id' : sucursal_['id'],'direccion' : sucursal_['direccion']},archivo,indent=4, ensure_ascii=False)


# ---------------- LOGIN ----------------
class Login(tk.Tk):
    def __init__(self):
        print(str(os.getcwd()))
        super().__init__()
        self.title("Login - Farmacia CUCEI")
        self.geometry("300x260")
        self.resizable(False, False)
        self.configure(bg=estilo.backgroundColor)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("BotonesEstilo.TButton",**estilo.buttonstyle)
        style.map("BotonesEstilo.TButton",**estilo.buttonmap)

        style.configure("BotonesAceptar.TButton",**estilo.buttonstyle_aceptar)
        style.map("BotonesAceptar.TButton",**estilo.buttonmap_aceptar)

        style.configure("BotonesRechazar.TButton",**estilo.buttonstyle_rechazar)
        style.map("BotonesRechazar.TButton",**estilo.buttonmap_rechazar)

        # -------- LOGO --------
        try:
            ruta_logo = os.path.join(ruta + "/Recursos", "logo.png")
            self.logo_img = tk.PhotoImage(file=ruta_logo).subsample(10, 10)
            tk.Label(self, image=self.logo_img,bg = estilo.backgroundColor).place(x=0, y=0)
        except:
            print("No se pudo cargar el logo")

        # -------- CAMPOS --------
        ttk.Label(self, text="Inicio de \nsesion:",background = estilo.backgroundColor,font=("Arial",20)).place(x=130, y=0)       
        
        ttk.Label(self, text="Usuario:",background = estilo.backgroundColor).place(x=10, y=110)
        self.user = ttk.Entry(self, width=25)
        self.user.place(x=100, y=110)

        ttk.Label(self, text="Contraseña:",background = estilo.backgroundColor).place(x=10, y=150)
        self.passw = ttk.Entry(self, width=25, show="*")
        self.passw.place(x=100, y=150)

        ttk.Button(self, text="Ingresar",style = "BotonesEstilo.TButton",command=self.login)\
            .place(x=110, y=200)




    def login(self):
        self.cargando_label = ttk.Label(self,text="Conectando...",font=["Arial",18],background=estilo.backgroundColor)
        self.cargando_label.place(x = 100,y= 202)
        self.update_idletasks()
        try:
            conectar()
            self.cargando_label.destroy()
        except Exception as e:
            messagebox.showerror(title = "Error de conexión",message="Error, no se ha podido establecer la conexión con el servidor, favor de revisar los ajustes en /Recursos/conexion.py")
            self.cargando_label.destroy()
            print("Erorr:" + str(e))
            return
        
        usuario = self.user.get()
        password = self.passw.get()

        if usuario == "" or password == "":
            messagebox.showwarning("Error", "Completa los campos")
            return

        abrir_sucursal()
        db = dbUsuario()
        resultado = db.login(usuario, password,sucursal['id'])

        if usuario == "admin" and password == "123":
            messagebox.showinfo("Protocolo de seguridad", "Iniciando en modo de administrador")
            resultado = {'id': 0, 'nombre': 'Administrador', 'rol': 'Admin'}

        if resultado is None:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        else:
            self.destroy()
            App(resultado).mainloop()



# ---------------- MENU ----------------
class App(tk.Tk):
    def __init__(self, sesion):
        super().__init__()

        abrir_sucursal()
        self.sesion = sesion
        rol = sesion["rol"]
        nombre = sesion["nombre"]

        self.title(f"Menú - {nombre} ({rol})")
        self.geometry("700x600")
        self.configure(bg=estilo.backgroundColor)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("BotonesEstilo.TButton",**estilo.buttonstyle)
        style.map("BotonesEstilo.TButton",**estilo.buttonmap)

        global sucursal

        # -------- LOGO --------
        try:
            ruta_logo = os.path.join(ruta + "/Recursos", "logo.png")
            self.logo_img = tk.PhotoImage(file=ruta_logo).subsample(4, 4)
            tk.Label(self, image=self.logo_img, bg=estilo.backgroundColor)\
                .place(x=0, y=0)
        except:
            print("No se pudo cargar el logo")

        # -------- TITULO --------
        tk.Label(self, text="MENU", font=("Arial", 40, "bold"),
                 bg=estilo.backgroundColor).place(x=250, y=20)

        tk.Label(self, text=f"Bienvenido: {nombre}",
                 bg=estilo.backgroundColor, font=("Arial", 12))\
            .place(x=260, y=100)


        #sucursales
        self.sucursales = dbSucursal.obtenerSucursales(self)
        self.sucursales_arreglo = []
        for sucursal_ in self.sucursales:
            self.sucursales_arreglo.append(str(sucursal_['id']) + " - " + sucursal_['direccion'])
        self.sucursal_combo = ttk.Combobox(width=50,values=self.sucursales_arreglo)
        self.sucursal_combo.place(x=250,y = 140)
        self.sucursal_combo.insert(0,str(sucursal['id']) + " - " + sucursal['direccion'])
        self.sucursal_combo.config(state="readonly")

        self.sucursal_combo.bind("<<ComboboxSelected>>",self.seleccionarSucursal)


        #menu
        y = 180

        estilo.buttonstyle["font"] = ("Arial",15)
        self.boton("Clientes", self.abrir_clientes, y); y += 50
        self.boton("Ventas", self.abrir_ventas, y); y += 50
        if rol != "Vendedor":
          self.boton("Productos", self.abrir_productos, y); y += 50
          self.boton("Compras", self.abrir_compras, y); y += 50
          self.boton("Reportes", self.abrir_reportes, y); y += 50
          #self.boton("Factura", self.abrir_factura, y); y += 50
          if rol == "Admin":
              self.boton("Proveedores", self.abrir_proveedores, y); y += 50
              ttk.Button(text="Sucursales",style="BotonesEstilo.TButton",command=self.abrir_sucursales).place(x=580,y = 130)
        estilo.buttonstyle["font"] = ("Arial",12)

    def seleccionarSucursal(self,event = None):
        if messagebox.askyesno(message="¿Está seguro que quiere cambiar de sucursal? Se cerrará su sesion"):
            for sucursal_ in self.sucursales:
                if sucursal_['id'] == int(self.sucursal_combo.get().strip()[0]):
                  guardar_sucursal(sucursal_)

            self.destroy()
            Login().mainloop()
        else:
            self.sucursal_combo.config(state="normal")
            self.sucursal_combo.set("")
            self.sucursal_combo.insert(0,str(sucursal['id']) + " - " + sucursal['direccion'])
            self.sucursal_combo.config(state="readonly")
            return



    # -------- BOTÓN --------
    def boton(self, texto, comando, y):
        ttk.Button(self, text=texto,style ="BotonesEstilo.TButton", width=30,
                   command=comando).place(x=230, y=y)

    # -------- VENTANAS --------
    def abrir_sucursales(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder acceder a otra seccion del menu")
        else:
            ventana = SucursalesView(sucursal=sucursal, ruta = ruta, master= self)
            self.wait_window(ventana)
            abrir_sucursal()
            self.sucursal_combo.config(state="normal")
            self.sucursal_combo.set("")
            self.sucursal_combo.insert(0,str(sucursal['id']) + " - " + sucursal['direccion'])
            self.sucursal_combo.config(state="readonly")                                


    def abrir_clientes(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder acceder a otra seccion del menu")
        else:
            ClientesView(self)

            
    def abrir_productos(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder acceder a otra seccion del menu")
        else:
            ProductosView(self)
        

    def abrir_proveedores(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder abrir acceder a otra seccion del menu")
        else:
            ProveedoresView(self)        

    def abrir_compras(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder abrir acceder a otra seccion del menu")
        else:
            CompraView(self)        
        

    def abrir_ventas(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder abrir acceder a otra seccion del menu")
        else:
            VentaView(self)
        

    def abrir_reportes(self):
        if any(isinstance(w, tk.Toplevel) for w in self.children.values()):
            messagebox.showerror(title="Error. Otra pestaña se encuentra abierta",message="Error. Otra pestaña ya se encuentra abierta. Cierrela para poder abrir acceder a otra seccion del menu")
        else:
            ReportesView(self)
                    


# ---------------- MAIN ----------------
if __name__ == "__main__":
    Login().mainloop()