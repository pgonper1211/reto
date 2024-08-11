class Starship:
    """
    Clase que representa una nave espacial en un contexto ficticio.

    Atributos:
        id (int): Identificador único de la nave espacial.
        name (str): Nombre de la nave espacial.
        model (str): Modelo de la nave espacial.
        manufacturer (str): Fabricante de la nave espacial.
        cost_in_credits (float): Costo de la nave espacial en créditos.
        max_atmosphering_speed (float): Velocidad máxima de la nave en la atmósfera.
        length (float): Longitud de la nave espacial.
        crew (int): Número de tripulantes requeridos.
        passengers (int): Capacidad de pasajeros de la nave.
        cargo_capacity (float): Capacidad de carga de la nave espacial.
        consumables (str): Duración de los consumibles a bordo.
        hyperdrive_rating (float): Calificación del hiperdrive de la nave.
        mglt (float): Velocidad de la nave en Megalights por hora.
        starship_class (str): Clase de la nave espacial.
        pilots (list): Lista de pilotos que han pilotado la nave espacial.
        films (list): Lista de películas donde aparece la nave espacial.
    """

    def __init__(self, id, name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, hyperdrive_rating, mglt, starship_class, pilots, films):
        """
        Inicializa un nuevo objeto Starship con los atributos dados.

        Args:
            id (int): Identificador único de la nave espacial.
            name (str): Nombre de la nave espacial.
            model (str): Modelo de la nave espacial.
            manufacturer (str): Fabricante de la nave espacial.
            cost_in_credits (float): Costo de la nave espacial en créditos.
            max_atmosphering_speed (float): Velocidad máxima de la nave en la atmósfera.
            length (float): Longitud de la nave espacial.
            crew (int): Número de tripulantes requeridos.
            passengers (int): Capacidad de pasajeros de la nave.
            cargo_capacity (float): Capacidad de carga de la nave espacial.
            consumables (str): Duración de los consumibles a bordo.
            hyperdrive_rating (float): Calificación del hiperdrive de la nave.
            mglt (float): Velocidad de la nave en Megalights por hora.
            starship_class (str): Clase de la nave espacial.
            pilots (list): Lista de pilotos que han pilotado la nave espacial.
            films (list): Lista de películas donde aparece la nave espacial.
        """
        self.id = id  # Asigna el ID de la nave espacial
        self.name = name  # Asigna el nombre de la nave espacial
        self.model = model  # Asigna el modelo de la nave espacial
        self.manufacturer = manufacturer  # Asigna el fabricante de la nave espacial
        self.cost_in_credits = cost_in_credits  # Asigna el costo de la nave espacial en créditos
        self.max_atmosphering_speed = max_atmosphering_speed  # Asigna la velocidad máxima en la atmósfera
        self.length = length  # Asigna la longitud de la nave espacial
        self.crew = crew  # Asigna la cantidad de tripulantes requeridos
        self.passengers = passengers  # Asigna la capacidad de pasajeros de la nave
        self.cargo_capacity = cargo_capacity  # Asigna la capacidad de carga de la nave espacial
        self.consumables = consumables  # Asigna la duración de los consumibles a bordo
        self.hyperdrive_rating = hyperdrive_rating  # Asigna la calificación del hiperdrive de la nave
        self.mglt = mglt  # Asigna la velocidad de la nave en Megalights por hora
        self.starship_class = starship_class  # Asigna la clase de la nave espacial
        self.pilots = pilots  # Asigna la lista de pilotos asociados
        self.films = films  # Asigna la lista de películas donde aparece la nave espacial

    def pilots_str(self):
        """
        Genera una cadena que describe los pilotos asociados con la nave espacial.

        Returns:
            str: Una cadena que lista los pilotos o un mensaje indicando que no hay pilotos asociados.
        """
        if len(self.pilots) > 0:  # Verifica si hay pilotos asociados
            piloto_str = "Pilotos:\n"
            for piloto in self.pilots:
                piloto_str += f"- {piloto.name}\n"  # Agrega cada nombre de piloto a la cadena
            return piloto_str  # Devuelve la cadena final con los nombres de los pilotos
        else:
            return "Esta nave espacial no tiene pilotos asociados."  # Mensaje cuando no hay pilotos

    def films_str(self):
        """
        Genera una cadena que describe las películas en las que aparece la nave espacial.

        Returns:
            str: Una cadena que lista las películas o un mensaje indicando que no aparece en ninguna.
        """
        if len(self.films) > 0:  # Verifica si la lista de películas no está vacía
            film_str = "Films en los que aparece:\n"
            for film in self.films:
                film_str += f"- {film.title}\n"  # Agrega cada título de película a la cadena
            return film_str  # Devuelve la cadena final con los títulos de las películas
        else:
            return "Esta nave espacial no aparece en ningún film."  # Mensaje cuando no hay películas

    def show_atr(self):
        """
        Genera una cadena con todos los atributos de la nave espacial, incluyendo los pilotos y las películas.

        Returns:
            str: Una cadena con la información de la nave espacial y los pilotos y películas asociados.
        """
        return (f"ID: {self.id}\n"
                f"Nombre: {self.name}\n"
                f"Modelo: {self.model}\n"
                f"Fabricante: {self.manufacturer}\n"
                f"Costo en créditos: {self.cost_in_credits}\n"
                f"Longitud: {self.length} metros\n"
                f"Pasajeros: {self.passengers}\n"
                f"Capacidad de carga: {self.cargo_capacity}\n"
                f"Velocidad máxima de atmósfera: {self.max_atmosphering_speed}\n"
                f"Consumibles: {self.consumables}\n"
                f"Rating del hiperdrive: {self.hyperdrive_rating}\n"
                f"MGLT: {self.mglt}\n"
                f"Clase de nave espacial: {self.starship_class}\n"
                f"{self.pilots_str()}\n"  # Incluye la información de los pilotos
                f"{self.films_str()}\n")  # Incluye la información de las películas
