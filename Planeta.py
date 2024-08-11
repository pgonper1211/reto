class Planeta:
    """
    Clase que representa un planeta en un contexto ficticio.

    Atributos:
        uid (int): Identificador único del planeta.
        name (str): Nombre del planeta.
        diameter (float): Diámetro del planeta en kilómetros.
        rotation_period (float): Período de rotación del planeta en días.
        orbital_period (float): Período orbital del planeta en días.
        gravity (str): Gravedad del planeta en m/s².
        population (int): Población del planeta.
        climate (str): Clima del planeta.
        terrain (str): Tipo de terreno del planeta.
        surface_water (float): Porcentaje de la superficie cubierta de agua.
        created (str): Fecha de creación del registro del planeta.
        edited (str): Fecha de la última edición del registro del planeta.
        url (str): URL con información adicional del planeta.
        episodes (list): Lista de episodios en los que aparece el planeta.
        personajes (list): Lista de personajes asociados al planeta.
    """

    def __init__(self, uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url):
        """
        Inicializa un nuevo objeto Planeta con los atributos dados.

        Args:
            uid (int): Identificador único del planeta.
            name (str): Nombre del planeta.
            diameter (float): Diámetro del planeta en kilómetros.
            rotation_period (float): Período de rotación del planeta en días.
            orbital_period (float): Período orbital del planeta en días.
            gravity (str): Gravedad del planeta en m/s².
            population (int): Población del planeta.
            climate (str): Clima del planeta.
            terrain (str): Tipo de terreno del planeta.
            surface_water (float): Porcentaje de la superficie cubierta de agua.
            created (str): Fecha de creación del registro del planeta.
            edited (str): Fecha de la última edición del registro del planeta.
            url (str): URL con información adicional del planeta.
        """
        self.uid = uid  # Asigna el ID único del planeta
        self.name = name  # Asigna el nombre del planeta
        self.diameter = diameter  # Asigna el diámetro del planeta
        self.rotation_period = rotation_period  # Asigna el período de rotación del planeta
        self.orbital_period = orbital_period  # Asigna el período orbital del planeta
        self.gravity = gravity  # Asigna la gravedad del planeta
        self.population = population  # Asigna la población del planeta
        self.climate = climate  # Asigna el clima del planeta
        self.terrain = terrain  # Asigna el tipo de terreno del planeta
        self.surface_water = surface_water  # Asigna el porcentaje de agua superficial del planeta
        self.created = created  # Asigna la fecha de creación del registro
        self.edited = edited  # Asigna la fecha de la última edición del registro
        self.url = url  # Asigna la URL con información adicional
        self.episodes = []  # Inicializa la lista de episodios en los que aparece el planeta
        self.personajes = []  # Inicializa la lista de personajes asociados al planeta

    def episodes_str(self):
        """
        Genera una cadena que describe los episodios en los que aparece el planeta.

        Returns:
            str: Una cadena que lista los episodios o un mensaje indicando que no hay episodios relacionados.
        """
        if len(self.episodes) != 0:  # Verifica si hay episodios relacionados
            episodes_string = "Lista de episodios donde aparece el planeta:\n\n"
            for episode in self.episodes:
                episodes_string += f"-{episode.name_film()}\n"  # Agrega cada nombre de episodio a la cadena
            return episodes_string  # Devuelve la cadena final con los nombres de los episodios
        else:
            return "Este planeta no tiene episodios relacionados."  # Mensaje cuando no hay episodios

    def personajes_str(self):
        """
        Genera una cadena que describe los personajes asociados con el planeta.

        Returns:
            str: Una cadena que lista los personajes o un mensaje indicando que no hay personajes relacionados.
        """
        if len(self.personajes) != 0:  # Verifica si hay personajes asociados
            personajes_string = "Lista de personajes de este planeta:\n\n"
            for personaje in self.personajes:
                personajes_string += f"-{personaje.name}\n"  # Agrega cada nombre de personaje a la cadena
            return personajes_string  # Devuelve la cadena final con los nombres de los personajes
        else:
            return "Este planeta no tiene personajes relacionados."  # Mensaje cuando no hay personajes

    def show_atr(self):
        """
        Genera una cadena con todos los atributos del planeta, incluyendo los episodios y personajes.

        Returns:
            str: Una cadena con la información detallada del planeta.
        """
        return f"""
        - Nombre: {self.name}
        - Diámetro: {self.diameter} km
        - Período de rotación: {self.rotation_period} días
        - Período orbital: {self.orbital_period} días
        - Gravedad: {self.gravity} m/s²
        - Población: {self.population}
        - Clima: {self.climate}
        - Terreno: {self.terrain}
        - Porcentaje de agua superficial: {self.surface_water}%
        - Creado: {self.created}
        - Editado: {self.edited}
        - URL: {self.url}
        {self.episodes_str()}
        {self.personajes_str()}
        """  # Muestra todos los atributos del planeta

    def mostrar(self):
        """
        Imprime los principales atributos del planeta, junto con la lista de episodios y personajes asociados.

        Returns:
            None
        """
        print(f"""
        - Nombre: {self.name}
        - Período de rotación: {self.rotation_period} días
        - Período orbital: {self.orbital_period} días
        - Población: {self.population}
        - Clima: {self.climate}
        - URL: {self.url}
        {self.episodes_str()}
        {self.personajes_str()}
        """)  # Imprime una versión más corta de los atributos del planeta
