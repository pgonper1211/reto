class Personaje:
    """
    Clase que representa un personaje en un contexto ficticio.

    Atributos:
        uid (int): Identificador único del personaje.
        name (str): Nombre del personaje.
        height (float): Altura del personaje en centímetros.
        mass (float): Masa del personaje en kilogramos.
        hair_color (str): Color de cabello del personaje.
        skin_color (str): Color de piel del personaje.
        eye_color (str): Color de ojos del personaje.
        birth_year (str): Año de nacimiento del personaje.
        gender (str): Género del personaje.
        created (str): Fecha de creación del registro del personaje.
        edited (str): Fecha de la última edición del registro del personaje.
        homeworld (obj): Objeto que representa el planeta de origen del personaje.
        url (str): URL con información adicional del personaje.
        episodes (list): Lista de episodios en los que aparece el personaje.
        specie (obj): Objeto que representa la especie del personaje.
        naves (list): Lista de naves en las que aparece el personaje.
        vehiculos (list): Lista de vehículos en los que aparece el personaje.
    """

    def __init__(self, uid, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, created, edited, homeworld, url, episodes, specie, naves, vehiculos):
        """
        Inicializa un nuevo objeto Personaje con los atributos dados.

        Args:
            uid (int): Identificador único del personaje.
            name (str): Nombre del personaje.
            height (float): Altura del personaje en centímetros.
            mass (float): Masa del personaje en kilogramos.
            hair_color (str): Color de cabello del personaje.
            skin_color (str): Color de piel del personaje.
            eye_color (str): Color de ojos del personaje.
            birth_year (str): Año de nacimiento del personaje.
            gender (str): Género del personaje.
            created (str): Fecha de creación del registro del personaje.
            edited (str): Fecha de la última edición del registro del personaje.
            homeworld (obj): Objeto que representa el planeta de origen del personaje.
            url (str): URL con información adicional del personaje.
            episodes (list): Lista de episodios en los que aparece el personaje.
            specie (obj): Objeto que representa la especie del personaje.
            naves (list): Lista de naves en las que aparece el personaje.
            vehiculos (list): Lista de vehículos en los que aparece el personaje.
        """
        self.uid = uid  # Asigna el ID único del personaje
        self.name = name  # Asigna el nombre del personaje
        self.height = height  # Asigna la altura del personaje
        self.mass = mass  # Asigna la masa del personaje
        self.hair_color = hair_color  # Asigna el color de cabello del personaje
        self.skin_color = skin_color  # Asigna el color de piel del personaje
        self.eye_color = eye_color  # Asigna el color de ojos del personaje
        self.birth_year = birth_year  # Asigna el año de nacimiento del personaje
        self.gender = gender  # Asigna el género del personaje
        self.created = created  # Asigna la fecha de creación del registro
        self.edited = edited  # Asigna la fecha de la última edición del registro
        self.homeworld = homeworld  # Asigna el planeta de origen del personaje
        self.url = url  # Asigna la URL con información adicional del personaje
        self.episodes = episodes  # Asigna la lista de episodios en los que aparece el personaje
        self.specie = specie  # Asigna la especie del personaje
        self.naves = naves  # Asigna la lista de naves en las que aparece el personaje
        self.vehiculos = vehiculos  # Asigna la lista de vehículos en los que aparece el personaje

    def set_specie(self, specie):
        """
        Asigna la especie del personaje.

        Args:
            specie (obj): Objeto que representa la especie del personaje.
        """
        self.specie = specie  # Asigna la especie del personaje

    def episodes_str(self):
        """
        Genera una cadena que describe los episodios en los que aparece el personaje.

        Returns:
            str: Una cadena que lista los episodios o un mensaje indicando que no hay episodios relacionados.
        """
        if len(self.episodes) != 0:  # Verifica si hay episodios relacionados
            episodes_string = "Episodios en los que aparece este personaje:\n\n"
            for episode in self.episodes:
                episodes_string += f"-{episode.name_film()}\n"  # Agrega cada nombre de episodio a la cadena
            return episodes_string  # Devuelve la cadena final con los nombres de los episodios
        else:
            return "Este personaje no tiene episodios relacionados."  # Mensaje cuando no hay episodios

    def naves_str(self):
        """
        Genera una cadena que describe las naves en las que aparece el personaje.

        Returns:
            str: Una cadena que lista las naves o un mensaje indicando que no aparece en naves.
        """
        if len(self.naves) != 0:  # Verifica si hay naves relacionadas
            naves_string = "Naves en las que aparece este personaje:\n\n"
            for nave in self.naves:
                naves_string += f"-{nave.show_atr()}\n"  # Agrega cada nave a la cadena
            return naves_string  # Devuelve la cadena final con la información de las naves
        else:
            return "Este personaje no aparece en naves."  # Mensaje cuando no hay naves

    def vehiculos_str(self):
        """
        Genera una cadena que describe los vehículos en los que aparece el personaje.

        Returns:
            str: Una cadena que lista los vehículos o un mensaje indicando que no aparece en vehículos.
        """
        if len(self.vehiculos) != 0:  # Verifica si hay vehículos relacionados
            vehiculos_string = "Vehículos en los que aparece este personaje:\n\n"
            for vehiculo in self.vehiculos:
                vehiculos_string += f"-{vehiculo.show_atr()}\n"  # Agrega cada vehículo a la cadena
            return vehiculos_string  # Devuelve la cadena final con la información de los vehículos
        else:
            return "Este personaje no aparece en vehículos."  # Mensaje cuando no hay vehículos

    def show_atr(self):
        """
        Genera una cadena con todos los atributos del personaje, incluyendo episodios, naves y vehículos.

        Returns:
            str: Una cadena con la información detallada del personaje.
        """
        return f"""
        - Nombre: {self.name}
        - Altura: {self.height} cm
        - Masa: {self.mass} kg
        - Color de pelo: {self.hair_color}
        - Color de piel: {self.skin_color}
        - Color de ojos: {self.eye_color}
        - Año de nacimiento: {self.birth_year}
        - Género: {self.gender}
        - Creado: {self.created}
        - Editado: {self.edited}
        - Planeta de origen: {self.homeworld}
        - URL: {self.url}
        - Especie: {self.specie}
        {self.episodes_str()}
        {self.naves_str()}
        {self.vehiculos_str()}
        """  # Muestra todos los atributos del personaje

    def especie_str(self):
        """
        Devuelve el nombre de la especie del personaje, o "Unknown" si no está definida.

        Returns:
            str: Nombre de la especie o "Unknown".
        """
        if self.specie is None:  # Verifica si la especie está definida
            return "Unknown"  # Devuelve "Unknown" si no hay especie
        else:
            return self.specie.name  # Devuelve el nombre de la especie

    def planeta_str(self):
        """
        Devuelve el nombre del planeta de origen del personaje, o "Unknown" si no está definido.

        Returns:
            str: Nombre del planeta de origen o "Unknown".
        """
        if self.homeworld is None:  # Verifica si el planeta de origen está definido
            return "Unknown"  # Devuelve "Unknown" si no hay planeta de origen
        else:
            return self.homeworld.name  # Devuelve el nombre del planeta de origen

    def mostrar(self):
        """
        Genera una cadena con una versión abreviada de los atributos del personaje, incluyendo episodios, naves y vehículos.

        Returns:
            str: Una cadena con la información básica del personaje.
        """
        return f"""
        - Nombre: {self.name}
        - Género: {self.gender}
        - Planeta de origen: {self.planeta_str()}
        - Especie: {self.especie_str()}
        {self.episodes_str()}
        {self.naves_str()}
        {self.vehiculos_str()}
        """  # Muestra una versión abreviada de los atributos del personaje
