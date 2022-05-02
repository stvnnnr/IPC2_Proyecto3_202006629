
class servicio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.alias = []
    
    def setAlias(self,alia):
        self.alias.append(alia)
    
    def getAlias(self):
        return self.alias