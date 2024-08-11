class Especie:
    """
    Clase que representa una especie en un contexto ficticio.

    Atributos:
        uid (int): Identificador único de la especie.
        name (str): Nombre de la especie.
        classification (str): Clasificación biológica de la especie.
        designation (str): Designación de la especie (por ejemplo, sentiente, no sentiente).
        average_height (float): Altura promedio de la especie en metros.
        average_lifespan (int): Tiempo promedio de vida de la especie en años.
        hair_colors (str): Colores de cabello comunes en la especie.
        skin_colors (str): Colores de piel comunes en la especie.
        eye_colors (str): Colores de ojos comunes en la especie.
        homeworld (obj): Objeto que representa el planeta de origen de la especie.
        language (str): Lengua o idioma hablado por la especie.
        created (str): Fecha de creación del registro de la especie.
        edited (str): Fecha de la última edición del registro de la especie.
        people (list): Lista de personajes que pertenecen a esta especie.
        episodes (list): Lista de episodios donde aparece esta especie.
        url (str): URL con información adicional sobre la especie.
    """

    def __init__(self, uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url):
        """
        Inicializa un nuevo objeto Especie con los atributos dados.

        Args:
            uid (int): Identificador único de la especie.
            name (str): Nombre de la especie.
            classification (str): Clasificación biológica de la especie.
            designation (str): Designación de la especie (por ejemplo, sentiente, no sentiente).
            average_height (float): Altura promedio de la especie en metros.
            average_lifespan (int): Tiempo promedio de vida de la especie en años.
            hair_colors (str): Colores de cabello comunes en la especie.
            skin_colors (str): Colores de piel comunes en la especie.
            eye_colors (str): Colores de ojos comunes en la especie.
            homeworld (obj): Objeto que representa el planeta de origen de la especie.
            language (str): Lengua o idioma hablado por la especie.
            created (str): Fecha de creación del registro de la especie.
            edited (str): Fecha de la última edición del registro de la especie.
            people (list): Lista de personajes que pertenecen a esta especie.
            episodes (list): Lista de episodios donde aparece esta especie.
            url (str): URL con información adicional sobre la especie.
        """
        self.uid = uid  # Asigna el ID único de la especie
        self.name = name  # Asigna el nombre de la especie
        self.classification = classification  # Asigna la clasificación biológica de la especie
        self.designation = designation  # Asigna la designación de la especie
        self.average_height = average_height  # Asigna la altura promedio de la especie
        self.average_lifespan = average_lifespan  # Asigna el tiempo promedio de vida de la especie
        self.hair_colors = hair_colors  # Asigna los colores de cabello comunes en la especie
        self.skin_colors = skin_colors  # Asigna los colores de piel comunes en la especie
        self.eye_colors = eye_colors  # Asigna los colores de ojos comunes en la especie
        self.homeworld = homeworld  # Asigna el planeta de origen de la especie
        self.language = language  # Asigna la lengua hablada por la especie
        self.created = created  # Asigna la fecha de creación del registro
        self.edited = edited  # Asigna la fecha de la última edición del registro
        self.url = url  # Asigna la URL con información adicional
        self.people = people  # Asigna la lista de personajes que pertenecen a esta especie
        self.episodes = episodes  # Asigna la lista de episodios donde aparece esta especie

    def personajes_str(self):
        """
        Genera una cadena que describe los personajes relacionados con esta especie.

        Returns:
            str: Una cadena que lista los personajes o un mensaje indicando que no hay personajes relacionados.
        """
        if len(self.people) != 0:  # Verifica si hay personajes relacionados
            personajes_string = "\nPersonajes relacionados con esta especie:\n\n"
            for personaje in self.people:
                personajes_string += f"-{personaje.name}\n"  # Agrega el nombre de cada personaje a la cadena
            return personajes_string  # Devuelve la cadena final con los nombres de los personajes
        else:
            return "Esta especie no tiene personajes relacionados."  # Mensaje cuando no hay personajes

    def episoder_str(self):
        """
        Genera una cadena que describe los episodios relacionados con esta especie.

        Returns:
            str: Una cadena que lista los episodios o un mensaje indicando que no hay episodios relacionados.
        """
        if len(self.episodes) != 0:  # Verifica si hay episodios relacionados
            episodios_string = "Episodios relacionados con esta especie:\n\n"
            for episodio in self.episodes:
                episodios_string += f"-{episodio.name_film()}\n"  # Agrega el nombre de cada episodio a la cadena
            return episodios_string  # Devuelve la cadena final con los nombres de los episodios
        else:
            return "Esta especie no tiene episodios relacionados."  # Mensaje cuando no hay episodios

    def show_atr(self):
        """
        Genera una cadena con todos los atributos principales de la especie.

        Returns:
            str: Una cadena con la información detallada de la especie.
        """
        return f"""
            Nombre: {self.name}\n
            Clasificación: {self.classification}
            Designación: {self.designation} 
            Altura promedio: {self.average_height} mts 
            Tiempo promedio de vida: {self.average_lifespan} años 
            Colores de pelo: {self.hair_colors} 
            Colores de piel: {self.skin_colors} 
            Colores de ojos: {self.eye_colors}
            Planeta de origen: {self.homeworld} 
            Lengua: {self.language}
            Creado: {self.created}
            Editado: {self.edited}
            URL: {self.url}
            {self.personajes_str()}
            {self.episoder_str()}    
            """  # Muestra todos los atributos clave de la especie

    def mostrar(self):
        """
        Imprime una versión abreviada de los atributos principales de la especie.

        Returns:
            None
        """
        print(f"""
            Nombre: {self.name}\n
            Clasificación: {self.classification}
            Altura promedio: {self.average_height} mts 
            Planeta de origen: {self.homeworld} 
            Lengua: {self.language}
            {self.personajes_str()}
            {self.episoder_str()} 
        
        """)  # Imprime los atributos principales de la especie
