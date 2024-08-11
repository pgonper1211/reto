class Vehicle:
    """
    Clase que representa un vehículo en un contexto ficticio.

    Atributos:
        id (int): Identificador único del vehículo.
        name (str): Nombre del vehículo.
        model (str): Modelo del vehículo.
        manufacturer (str): Fabricante del vehículo.
        cost_in_credits (float): Costo del vehículo en créditos.
        length (float): Longitud del vehículo.
        max_atmosphering_speed (float): Velocidad máxima del vehículo en la atmósfera.
        crew (int): Número de tripulantes requeridos.
        passengers (int): Capacidad de pasajeros del vehículo.
        cargo_capacity (float): Capacidad de carga del vehículo.
        consumables (str): Duración de los consumibles a bordo.
        vehicle_class (str): Clase del vehículo.
        pilots (list): Lista de pilotos que han pilotado el vehículo.
        films (list): Lista de películas donde aparece el vehículo.
    """

    def __init__(self, id, name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, vehicle_class, pilots, films):
        """
        Inicializa un nuevo objeto Vehicle con los atributos dados.

        Args:
            id (int): Identificador único del vehículo.
            name (str): Nombre del vehículo.
            model (str): Modelo del vehículo.
            manufacturer (str): Fabricante del vehículo.
            cost_in_credits (float): Costo del vehículo en créditos.
            length (float): Longitud del vehículo.
            max_atmosphering_speed (float): Velocidad máxima del vehículo en la atmósfera.
            crew (int): Número de tripulantes requeridos.
            passengers (int): Capacidad de pasajeros del vehículo.
            cargo_capacity (float): Capacidad de carga del vehículo.
            consumables (str): Duración de los consumibles a bordo.
            vehicle_class (str): Clase del vehículo.
            pilots (list): Lista de pilotos que han pilotado el vehículo.
            films (list): Lista de películas donde aparece el vehículo.
        """
        self.id = id  # Asigna el ID del vehículo
        self.name = name  # Asigna el nombre del vehículo
        self.model = model  # Asigna el modelo del vehículo
        self.manufacturer = manufacturer  # Asigna el fabricante del vehículo
        self.cost_in_credits = cost_in_credits  # Asigna el costo del vehículo en créditos
        self.length = length  # Asigna la longitud del vehículo
        self.max_atmosphering_speed = max_atmosphering_speed  # Asigna la velocidad máxima en la atmósfera
        self.crew = crew  # Asigna la cantidad de tripulantes requeridos
        self.passengers = passengers  # Asigna la capacidad de pasajeros del vehículo
        self.cargo_capacity = cargo_capacity  # Asigna la capacidad de carga del vehículo
        self.consumables = consumables  # Asigna la duración de los consumibles a bordo
        self.vehicle_class = vehicle_class  # Asigna la clase del vehículo
        self.pilots = pilots  # Asigna la lista de pilotos asociados
        self.films = films  # Asigna la lista de películas donde aparece el vehículo

    def pilots_str(self):
        """
        Genera una cadena que describe los pilotos asociados con el vehículo.

        Returns:
            str: Una cadena que lista los pilotos o un mensaje indicando que no hay pilotos asociados.
        """
        if len(self.pilots) > 0:  # Verifica si hay pilotos asociados
            piloto_str = "Pilotos:\n"
            for piloto in self.pilots:
                piloto_str += f"- {piloto.name}\n"  # Agrega cada nombre de piloto a la cadena
            return piloto_str  # Devuelve la cadena final con los nombres de los pilotos
        else:
            return "Este vehículo no tiene pilotos asociados."  # Mensaje cuando no hay pilotos

    def films_str(self):
        """
        Genera una cadena que describe las películas en las que aparece el vehículo.

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
        Genera una cadena con todos los atributos del vehículo, incluyendo los pilotos y las películas.

        Returns:
            str: Una cadena con la información del vehículo y los pilotos y películas asociados.
        """
        return (f"ID: {self.id}\n"
                f"Nombre: {self.name}\n"
                f"Modelo: {self.model}\n"
                f"Fabricante: {self.manufacturer}\n"
                f"Costo en créditos: {self.cost_in_credits}\n"
                f"Longitud: {self.length}\n"
                f"Velocidad máxima atmosférica: {self.max_atmosphering_speed}\n"
                f"Tripulación: {self.crew}\n"
                f"Pasajeros: {self.passengers}\n"
                f"Capacidad de carga: {self.cargo_capacity}\n"
                f"Consumibles: {self.consumables}\n"
                f"Clase del vehículo: {self.vehicle_class}\n"
                f"{self.pilots_str()}\n"  # Incluye la información de los pilotos
                f"{self.films_str()}\n")  # Incluye la información de las películas
