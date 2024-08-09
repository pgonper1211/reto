class Mision:
    def __init__(self, nombre, planeta, nave, armas, integrantes):
        self.nombre = nombre
        self.planeta = planeta
        self.nave = nave
        self.armas = armas
        self.integrantes = integrantes


    def armas_str(self):
        if len(self.armas)!= 0:
            armas_string = "Armas utilizadas durante la misión:\n\n"
            for arma in self.armas:
                armas_string += f"-{arma.show_atr()}\n"
            
            return armas_string
        else:
            return "No hay armas utilizadas durante la misión."
        
    def integrantes_str(self):
        if len(self.integrantes)!= 0:
            integrantes_string = "Integrantes de la misión:\n\n"
            for integrante in self.integrantes:
                integrantes_string += f"-{integrante.mostrar()}\n"
            
            return integrantes_string
        else:
            return "No hay integrantes en la misión."


    def show_atr(self):
        return f"Nombre: {self.nombre}\nPlaneta: {self.planeta.name}\nNave:\n{self.nave.show_atr()}\n\nArmas: {self.armas_str()}\n\n{self.integrantes_str()}\n"