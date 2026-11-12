class Compra:
    def __init__(self, id=None, producto_id=None, proveedor="", cantidad=0, precio_compra=0, fecha=""):
        self.id = id
        self.producto_id = producto_id
        self.proveedor = proveedor
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.fecha = fecha

    def getId(self): return self.id
    def getProducto_id(self): return self.producto_id
    def getProveedor(self): return self.proveedor
    def getCantidad(self): return self.cantidad
    def getPrecio_compra(self): return self.precio_compra
    def getFecha(self): return self.fecha