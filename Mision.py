class Mision:
    """
    Clase que representa una misión en un contexto ficticio.

    Atributos:
        nombre (str): Nombre de la misión.
        planeta (obj): Objeto que representa el planeta en el que se realiza la misión.
        nave (obj): Objeto que representa la nave utilizada en la misión.
        armas (list): Lista de objetos que representan las armas utilizadas en la misión.
        integrantes (list): Lista de objetos que representan a los integrantes de la misión.
    """

    def __init__(self, nombre, planeta, nave, armas, integrantes):
        """
        Inicializa un nuevo objeto Mision con los atributos dados.

        Args:
            nombre (str): Nombre de la misión.
            planeta (obj): Objeto que representa el planeta en el que se realiza la misión.
            nave (obj): Objeto que representa la nave utilizada en la misión.
            armas (list): Lista de objetos que representan las armas utilizadas en la misión.
            integrantes (list): Lista de objetos que representan a los integrantes de la misión.
        """
        self.nombre = nombre  # Asigna el nombre de la misión
        self.planeta = planeta  # Asigna el planeta donde se realiza la misión
        self.nave = nave  # Asigna la nave utilizada en la misión
        self.armas = armas  # Asigna la lista de armas utilizadas en la misión
        self.integrantes = integrantes  # Asigna la lista de integrantes de la misión

    def armas_str(self):
        """
        Genera una cadena que describe las armas utilizadas durante la misión.

        Returns:
            str: Una cadena que lista las armas o un mensaje indicando que no hay armas.
        """
        if len(self.armas) != 0:  # Verifica si hay armas en la misión
            armas_string = "Armas utilizadas durante la misión:\n\n"
            for arma in self.armas:
                armas_string += f"-{arma.show_atr()}\n"  # Agrega la descripción de cada arma a la cadena
            return armas_string  # Devuelve la cadena final con las armas
        else:
            return "No hay armas utilizadas durante la misión."  # Mensaje cuando no hay armas

    def integrantes_str(self):
        """
        Genera una cadena que describe los integrantes de la misión.

        Returns:
            str: Una cadena que lista los integrantes o un mensaje indicando que no hay integrantes.
        """
        if len(self.integrantes) != 0:  # Verifica si hay integrantes en la misión
            integrantes_string = "Integrantes de la misión:\n\n"
            for integrante in self.integrantes:
                integrantes_string += f"-{integrante.mostrar()}\n"  # Agrega la descripción de cada integrante a la cadena
            return integrantes_string  # Devuelve la cadena final con los integrantes
        else:
            return "No hay integrantes en la misión."  # Mensaje cuando no hay integrantes

    def show_atr(self):
        """
        Genera una cadena con todos los atributos principales de la misión.

        Returns:
            str: Una cadena con la información detallada de la misión.
        """
        return (f"Nombre: {self.nombre}\n"
                f"Planeta: {self.planeta.name}\n"
                f"Nave:\n{self.nave.show_atr()}\n\n"
                f"Armas: {self.armas_str()}\n\n"
                f"{self.integrantes_str()}\n")  # Muestra todos los atributos clave de la misión

    def armas_a_nombres(self):
        """
        Convierte la lista de armas en una lista de nombres de armas.

        Returns:
            list: Lista de nombres de las armas utilizadas en la misión.
        """
        armas = []
        for arma in self.armas:
            armas.append(arma.name)  # Agrega el nombre de cada arma a la lista
        return armas  # Devuelve la lista de nombres de armas

    def integrantes_a_nombres(self):
        """
        Convierte la lista de integrantes en una lista de nombres de integrantes.

        Returns:
            list: Lista de nombres de los integrantes de la misión.
        """
        integrantes = []
        for integrante in self.integrantes:
            integrantes.append(integrante.name)  # Agrega el nombre de cada integrante a la lista
        return integrantes  # Devuelve la lista de nombres de integrantes

    def convert_str(self):
        """
        Genera una cadena que describe la misión de forma resumida, incluyendo nombres de armas e integrantes.

        Returns:
            str: Una cadena con el formato "nombre, planeta, nave, 'armas', 'integrantes'".
        """
        armas_str = ", ".join(self.armas_a_nombres())  # Combina los nombres de las armas en una cadena
        integrantes_str = ", ".join(self.integrantes_a_nombres())  # Combina los nombres de los integrantes en una cadena
        
        return f"{self.nombre}, {self.planeta.name}, {self.nave.name}, '{armas_str}', '{integrantes_str}'"  # Devuelve la cadena con el resumen de la misión
