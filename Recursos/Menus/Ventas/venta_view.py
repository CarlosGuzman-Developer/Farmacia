import tkinter as tk
from tkinter import ttk, messagebox, END
from .dbVenta import dbVenta
from ... import estilo

from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path= os.path.join(os.path.dirname(os.path.abspath(__file__)),"Gemini_api.env"))
Gemini_api = os.getenv("gemini_api")

class VentaView(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Ventas")
        self.geometry("500x650")
        self.configure(bg=estilo.backgroundColor)
          
        #configuración del estilo de los botones
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("BotonesEstilo.TButton",**estilo.buttonstyle)
        self.style.map("BotonesEstilo.TButton",**estilo.buttonmap)

        self.style.configure("BotonesAceptar.TButton",**estilo.buttonstyle_aceptar)
        self.style.map("BotonesAceptar.TButton",**estilo.buttonmap_aceptar)
        self.style.configure("BotonesRechazar.TButton",**estilo.buttonstyle_rechazar)
        self.style.map("BotonesRechazar.TButton",**estilo.buttonmap_rechazar)


        self.db = dbVenta()        

        self.ID = self.db.obtener_maxID() + 1

        ttk.Label(self, text="Cliente",background=estilo.backgroundColor).place(x=20, y=40)
        self.combo_cliente = ttk.Combobox(self, state="readonly")
        self.combo_cliente.place(x=150, y=40)

        ttk.Label(self, text="Producto",background=estilo.backgroundColor).place(x=20, y=80)
        self.combo_producto = ttk.Combobox(self, state="readonly")
        self.combo_producto.place(x=150, y=80)

        ttk.Label(self, text="Stock",background=estilo.backgroundColor).place(x=20, y=120)
        self.ent_stock = ttk.Entry(self,state="disabled")
        self.ent_stock.place(x=150, y=120)


        ttk.Label(self, text="Cantidad",background=estilo.backgroundColor).place(x=20, y=160)
        self.txt_cantidad = ttk.Entry(self)
        self.txt_cantidad.place(x=150, y=160)

        ttk.Label(self, text="Precio unitario",background=estilo.backgroundColor).place(x=20, y=200)
        self.lbl_precio = ttk.Label(self,text = "$0",background="White")
        self.lbl_precio.place(x=150, y=200)

        ttk.Label(self, text="Total: ",background=estilo.backgroundColor,font=("Arial",15)).place(x=300, y=540)
        self.str_total = tk.StringVar(value = "$0")
        self.txt_total = ttk.Label(self,textvariable = self.str_total,background="White",font=("Arial",15))
        self.txt_total.place(x=360, y=540)

        #definicion del arbol de ventas
        self.ventas_tree = ttk.Treeview(self,columns=("Producto","Cantidad","Precio"),show="headings",selectmode="browse")
        
        self.ventas_tree.column("Producto", width=220, stretch=True)
        self.ventas_tree.heading("Producto", text="Producto")

        self.ventas_tree.column("Cantidad", width=80, anchor=tk.CENTER)
        self.ventas_tree.heading("Cantidad", text="Cantidad")

        self.ventas_tree.column("Precio", width=120, anchor=tk.CENTER)
        self.ventas_tree.heading("Precio", text="Precio")

        self.ventas_tree.place(x = 10, y = 290)


        ttk.Button(self,text = "Añadir",style="BotonesAceptar.TButton",command=self.añadir).place(x=230, y=240)
        self.btt_eliminar = ttk.Button(self,text = "Eliminar",style="BotonesRechazar.TButton",state="disabled",command = self.eliminar)
        self.btt_eliminar.place(x=350, y=240)
        ttk.Button(self, text="Realizar Venta",style ="BotonesEstilo.TButton", command=self.realizar_venta).place(x=150, y=540)
        ttk.Button(self,text = "Chat ia",style ="BotonesEstilo.TButton",command=self.chat_ia).place(x = 350, y = 180)

        self.cargar_clientes()
        self.cargar_productos()

        self.combo_producto.bind("<<ComboboxSelected>>", self.mostrar_stock)
        self.ventas_tree.bind("<<TreeviewSelect>>",self.desbloquearEliminar)

    def chat_ia(self):     
       
       ventana = tk.Toplevel()
       ventana.geometry("300x800")
       try:
            self.client = genai.Client(api_key=Gemini_api)
       except:
            messagebox.showinfo(master = ventana,title="Error, no API detectada",message="Error, no se ha detectado ninguna API valida para usar el chat con ia" \
            "\nIntroduzca una en gemini_api.env\n" \
            "ubicacion: Recursos/Menus/Ventas")    
            ventana.destroy()
            return 
        
       frame_chat = ttk.Frame(ventana)
       frame_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

       self.scrollbar = ttk.Scrollbar(frame_chat)
       self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

       self.chat_display = tk.Text(
            frame_chat, 
            wrap=tk.WORD, 
            yscrollcommand=self.scrollbar.set,
            bg="#ffffff", 
            state="disabled", 
            font=("Arial", 10),
            padx=10,
            pady=10)
       
       self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       self.scrollbar.config(command=self.chat_display.yview)

       
       self.chat_display.tag_config("usuario", justify="right", foreground="#0b5ed7")
       self.chat_display.tag_config("bot", justify="left", foreground="#198754")
       self.chat_display.tag_config("sistema", justify="center", foreground="#6c757d")

       frame_input = ttk.Frame(ventana)
       frame_input.pack(padx=10, pady=(0, 10), fill=tk.X)

       self.entry_mensaje = ttk.Entry(frame_input, font=("Arial", 10))
       self.entry_mensaje.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
       self.entry_mensaje.bind("<Return>", lambda e: self.enviar_mensaje()) # Enviar con ENTER

       btn_enviar = ttk.Button(frame_input, text="Enviar", command=self.enviar_mensaje)
       btn_enviar.pack(side=tk.RIGHT)

       self.agregar_mensaje("Sistema", "Chat iniciado. Escribe un mensaje.", "sistema")

    def agregar_mensaje(self, emisor, texto, tag):
        self.chat_display.config(state="normal")
        
        self.chat_display.insert(tk.END, f"{emisor}: {texto}\n\n", tag)
        
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def enviar_mensaje(self):
        mensaje = self.entry_mensaje.get().strip()
        if not mensaje:
            return

        self.agregar_mensaje("Tú", mensaje, "usuario")
        self.entry_mensaje.delete(0, tk.END)

        self.after(1000, lambda: self.respuesta_automatica(mensaje))

    def respuesta_automatica(self, mensaje_usuario):
       
       contexto = types.GenerateContentConfig(
                  system_instruction=(
                    "Eres un farmaceutico con años de experiencia, un cliente te pregunta sobre la información de un producto, con los datos del cliente, determina si este producto es bueno para el. Sé lo más breve posible"
                    )
                )
       prompt = mensaje_usuario

       try:
            respuesta = self.client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config= contexto
            )
            self.agregar_mensaje("Gemini",respuesta.text,"bot")
       except Exception as e:
            self.agregar_mensaje("Sistema", f"No se pudo consultar Gemini: {e}","sistema")

    ###Fin del chat de IA

    #funciones del menu
    def añadir(self):
        if any(c.get() == "" for c in [self.combo_producto,self.txt_cantidad,self.ent_stock]):
            messagebox.showerror(title="Error producto no seleccionado",message="Seleccione un producto y su cantidad para empezar a añadirlo al carrito")
            return
        
       
        if int(self.txt_cantidad.get()) > int(self.ent_stock.get()):
          messagebox.showerror(title="Error, stock insuficiente",message="Error. Está solicitando más productos de los que tenemos en stock",parent=self)
        else:
            
            precios = self.db.obtener_productos()
            for precio in precios:
                if precio["nombre"] == self.combo_producto.get():
                  if precio["receta"] == 1:
                     if not messagebox.askyesno(title="Receta necesaria",message="El medicamento que quiere agregar necesita una receta ¿El cliente cuenta con una?",parent =self):
                        return
                     else:
                        break
                  break

            precios = float(precio["precio_venta"])


            if self.ventas_tree.get_children():
                encontrado = False
                for item in self.ventas_tree.get_children():
                    producto = self.ventas_tree.item(item,"values")
                    if producto[0] == self.combo_producto.get():
                        if int(producto[1]) + int(self.txt_cantidad.get()) > int(self.ent_stock.get()):
                          messagebox.showerror(title="Error, stock insuficiente",message="Error. Está solicitando más productos de los que tenemos en stock",parent=self)
                          return
                        else:
                         encontrado = True
                         self.ventas_tree.item(item, values=(producto[0],str(int(producto[1]) + int(self.txt_cantidad.get())), str(precios * (int(producto[1]) + int(self.txt_cantidad.get())))))
                
                if encontrado == False:
                    self.ventas_tree.insert("",END,values=(self.combo_producto.get(),self.txt_cantidad.get(),str(int(self.txt_cantidad.get()) * precios)))
            else:
                self.ventas_tree.insert("",END,values=(self.combo_producto.get(),self.txt_cantidad.get(),str(int(self.txt_cantidad.get()) * precios)))

        self.actualizarTotal()

    def eliminar(self):
        producto = self.ventas_tree.selection()
        nombre = str(self.ventas_tree.item(producto,"values")[0])

        confirmacion = messagebox.askyesno(title="Confirmación",message="¿Está seguro que desea elimiar " + nombre,parent=self)


        if confirmacion == True:
            self.ventas_tree.delete(producto)
            self.actualizarTotal()
            

    
    def actualizarTotal(self):
        costo_total = 0
        for item in self.ventas_tree.get_children(): 
         producto = self.ventas_tree.item(item,"values")
         costo_total = costo_total + float(producto[2])
        
        self.str_total.set("$" + str(costo_total))

    def desbloquearEliminar(self,event=None):
        seleccion = self.ventas_tree.selection()

        if seleccion:
         self.btt_eliminar.config(state = "normal")
        else:
           self.btt_eliminar.config(state = "disabled") 
         

    def cargar_clientes(self):
        self.lista_clientes = self.db.obtener_clientes()
        self.combo_cliente["values"] = [c["nombre"] for c in self.lista_clientes]

    def cargar_productos(self):
        self.lista_productos = self.db.obtener_productos()
        self.combo_producto["values"] = [p["nombre"] for p in self.lista_productos]

    def obtener_id_cliente(self):
        nombre = self.combo_cliente.get()
        for c in self.lista_clientes:
            if c["nombre"] == nombre:
                return c["id"]
        return None

    def obtener_producto(self):
        nombre = self.combo_producto.get()
        for p in self.lista_productos:
            if p["nombre"] == nombre:
                return p
        return None

    def mostrar_stock(self, event=None):
        producto = self.obtener_producto()
        if producto:
            self.ent_stock.config(state="normal")
            self.ent_stock.delete(0,END)
            self.ent_stock.insert(0,str(producto["stock"]))
            self.ent_stock.config(state="disabled")

            self.lbl_precio.config(text = "$" + str(producto["precio_venta"]))

    def realizar_venta(self):
        id_cliente = self.obtener_id_cliente()
        #producto = self.obtener_producto()
        #cantidad = self.txt_cantidad.get()

        costo_total = 0
        for item in self.ventas_tree.get_children(): 
         producto = self.ventas_tree.item(item,"values")
         costo_total = costo_total + float(producto[2])


        """if not id_cliente or not producto:
            messagebox.showwarning("Error", "Selecciona cliente y producto")
            return

        if cantidad == "":
            messagebox.showwarning("Error", "Ingresa cantidad")
            return

        ok, mensaje = self.db.registrar(self.id_venta,id_cliente, producto["id"], cantidad)"""
 
        if self.combo_cliente.get() == "":
           messagebox.showerror(title = "Error, cliente no seleccionado", message="No ha seleccionado a ningún cliente",parent= self)
           return
        
        productos = []
        if self.ventas_tree.get_children():
            for item in self.ventas_tree.get_children():
              datos = self.ventas_tree.item(item, 'values')
              productos.append((datos[0],datos[1],datos[2]))
        else:
          messagebox.showerror(title="Error. Sin productos",message="Error, sin productos en el carrito. Agrege algunos para completar la compra",parent= self)
          return


        ok, mensaje = self.db.registrar(self.ID,id_cliente, productos,costo_total)

        if ok:
            messagebox.showinfo("OK", mensaje,parent=self)
            self.lbl_precio.config(text = "$0")
            self.str_total.set("$0")
            self.ventas_tree.delete(*self.ventas_tree.get_children())
            self.limpiar()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje,parent=self)

    def limpiar(self):
        self.ID = self.db.obtener_maxID() + 1
        self.combo_cliente.set("")
        self.combo_producto.set("")
        self.txt_cantidad.delete(0, END)
        self.ent_stock.config(state="normal")
        self.ent_stock.delete(0,END)
        self.ent_stock.config(state="disabled")