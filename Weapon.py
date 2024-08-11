class Weapon:
    """
    Clase que representa un arma en un contexto ficticio.

    Atributos:
        id (int): Identificador único del arma.
        name (str): Nombre del arma.
        model (str): Modelo del arma.
        manufacturer (str): Fabricante del arma.
        cost_in_credits (float): Costo del arma en créditos.
        length (float): Longitud del arma.
        type (str): Tipo de arma.
        description (str): Descripción del arma.
        films (list): Lista de películas donde aparece el arma.
    """

    def __init__(self, id, name, model, manufacturer, cost_in_credits, length, type, description, films):
        """
        Inicializa un nuevo objeto Weapon con los atributos dados.

        Args:
            id (int): Identificador único del arma.
            name (str): Nombre del arma.
            model (str): Modelo del arma.
            manufacturer (str): Fabricante del arma.
            cost_in_credits (float): Costo del arma en créditos.
            length (float): Longitud del arma.
            type (str): Tipo de arma.
            description (str): Descripción del arma.
            films (list): Lista de películas donde aparece el arma.
        """
        self.id = id  # Asigna el ID del arma
        self.name = name  # Asigna el nombre del arma
        self.model = model  # Asigna el modelo del arma
        self.manufacturer = manufacturer  # Asigna el fabricante del arma
        self.cost_in_credits = cost_in_credits  # Asigna el costo del arma en créditos
        self.length = length  # Asigna la longitud del arma
        self.type = type  # Asigna el tipo de arma
        self.description = description  # Asigna la descripción del arma
        self.films = films  # Asigna la lista de películas donde aparece el arma

    def films_str(self):
        """
        Genera una cadena que describe las películas en las que aparece el arma.

        Returns:
            str: Una cadena que lista las películas o un mensaje indicando que no aparece en ninguna.
        """
        if len(self.films) > 0:  # Verifica si la lista de películas no está vacía
            film_str = "Films en los que aparece:\n"
            for film in self.films:
                film_str += f"- {film.title}\n"  # Agrega cada título de película a la cadena
            return film_str  # Devuelve la cadena final con los títulos de las películas
        else:
            return "Este vehículo no aparece en ningún film."  # Mensaje cuando no hay películas

    def show_atr(self):
        """
        Genera una cadena con todos los atributos del arma, incluyendo las películas en las que aparece.

        Returns:
            str: Una cadena con la información del arma y las películas en las que aparece.
        """
        return (f"ID: {self.id}\n"
                f"Nombre: {self.name}\n"
                f"Modelo: {self.model}\n"
                f"Fabricante: {self.manufacturer}\n"
                f"Costo en créditos: {self.cost_in_credits}\n"
                f"Longitud: {self.length}\n"
                f"Tipo: {self.type}\n"
                f"Descripción: {self.description}\n"
                f"{self.films_str()}\n")  # Incluye la información de las películas
