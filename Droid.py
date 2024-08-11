class Droid:
    """
    Clase que representa un droide en un contexto ficticio.

    Atributos:
        uid (int): Identificador único del droide.
        name (str): Nombre del droide.
        specie (obj): Especie o tipo de droide.
        modelo (str): Modelo del droide.
        manufacturer (str): Fabricante del droide.
        height (float): Altura del droide en centímetros.
        mass (float): Masa del droide en kilogramos.
        sensor_color (str): Color del sensor del droide.
        plating_color (str): Color de la plataforma del droide.
        primary_function (str): Función principal del droide.
        films (list): Lista de películas en las que aparece el droide.
    """

    def __init__(self, uid, name, specie, modelo, manufacturer, height, mass, sensor_color, plating_color, primary_function, films):
        """
        Inicializa un nuevo objeto Droid con los atributos dados.

        Args:
            uid (int): Identificador único del droide.
            name (str): Nombre del droide.
            specie (obj): Especie o tipo de droide.
            modelo (str): Modelo del droide.
            manufacturer (str): Fabricante del droide.
            height (float): Altura del droide en centímetros.
            mass (float): Masa del droide en kilogramos.
            sensor_color (str): Color del sensor del droide.
            plating_color (str): Color de la plataforma del droide.
            primary_function (str): Función principal del droide.
            films (list): Lista de películas en las que aparece el droide.
        """
        self.uid = uid  # Asigna el ID único del droide
        self.name = name  # Asigna el nombre del droide
        self.specie = specie  # Asigna la especie o tipo de droide
        self.modelo = modelo  # Asigna el modelo del droide
        self.manufacturer = manufacturer  # Asigna el fabricante del droide
        self.height = height  # Asigna la altura del droide en centímetros
        self.mass = mass  # Asigna la masa del droide en kilogramos
        self.sensor_color = sensor_color  # Asigna el color del sensor del droide
        self.plating_color = plating_color  # Asigna el color de la plataforma del droide
        self.primary_function = primary_function  # Asigna la función principal del droide
        self.films = films  # Asigna la lista de películas en las que aparece el droide

    def films_str(self):
        """
        Genera una cadena que describe las películas en las que aparece el droide.

        Returns:
            str: Una cadena que lista las películas o un mensaje indicando que no aparece en ninguna película.
        """
        if len(self.films) > 0:  # Verifica si el droide aparece en alguna película
            films_string = "Films en los que aparece:\n\n"
            for film in self.films:
                films_string += f"- {film.title}\n"  # Agrega el título de cada película a la cadena
            return films_string  # Devuelve la cadena final con los títulos de las películas
        else:
            return "Este droide no aparece en ningún film."  # Mensaje cuando no hay películas

    def mostrar(self):
        """
        Genera una cadena con todos los atributos principales del droide.

        Returns:
            str: Una cadena con la información detallada del droide.
        """
        return f"""
        - ID: {self.uid}
        - Nombre: {self.name}
        - Especie: {self.specie.name}
        - Modelo: {self.modelo}
        - Fabricante: {self.manufacturer}
        - Altura: {self.height} cm
        - Masa: {self.mass} kg
        - Color del sensor: {self.sensor_color}
        - Color de la plataforma: {self.plating_color}
        - Función principal: {self.primary_function}
        {self.films_str()}
        """  # Muestra todos los atributos clave del droide
