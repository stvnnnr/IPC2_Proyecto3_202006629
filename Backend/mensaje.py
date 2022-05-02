class mensajito:
    def __init__(self, lugar, fecha, hora, usuario, redSocial, msjLimpio):
        self.lugar = lugar
        self.fecha = fecha
        self.hora = hora
        self.usuario = usuario
        self.redSocial = redSocial
        self.msjLimpio = msjLimpio
        self.sentimiento = None
        self.empresas = []
        self.positivas = None
        self.negativas = None
        self.porcenPosi = None
        self.porcenNega = None
    
    def setSentimiento(self,sentimiento):
        self.sentimiento = sentimiento
    
    def getSentimiento(self):
        return self.sentimiento

    def setEmpresa(self,empresa):
        self.empresas.append(empresa)
    
    def getEmpresa(self):
        return self.empresas

    def setPositivas(self,sentimiento):
        self.positivas = sentimiento
    
    def getPositivas(self):
        return self.positivas

    def setNegativas(self,sentimiento):
        self.negativas = sentimiento
    
    def getNegativas(self):
        return self.negativas
    
    def setPorcePositivas(self,sentimiento):
        self.porcenPosi = sentimiento
    
    def getPorcePositivas(self):
        return self.porcenPosi

    def setPorceNegativas(self,sentimiento):
        self.porcenNega = sentimiento
    
    def getPorceNegativas(self):
        return self.porcenNega
