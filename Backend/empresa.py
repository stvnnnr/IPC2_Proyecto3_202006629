
class empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.Servicios = []
    
    def setServicio(self,servicio):
        self.Servicios.append(servicio)
    
    def getServicios(self):
        return self.Servicios