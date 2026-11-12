class Proveedor:
    def __init__(self, id=None, nombre="", correo="", telefono=""):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def getId(self): return self.id
    def getNombre(self): return self.nombre
    def getCorreo(self): return self.correo
    def getTelefono(self): return self.telefono