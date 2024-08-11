import requests
import csv
import re
import matplotlib.pyplot as plt
from collections import defaultdict
from Planeta import Planeta
from Especie import Especie
from Pelicula import Pelicula
from Personaje import Personaje
from Droid import Droid
from Starship import Starship
from Vehicle import Vehicle
from Weapon import Weapon
from Mision import Mision

class App:
    """
    Clase principal que maneja la lógica de la aplicación.

    Atributos:
        especies (list): Lista de especies registradas en la aplicación.
        misiones (list): Lista de misiones registradas en la aplicación.
        naves (list): Lista de naves registradas en la aplicación.
        peliculas (list): Lista de películas registradas en la aplicación.
        planetas (list): Lista de planetas registrados en la aplicación.
        personajes (list): Lista de personajes registrados en la aplicación.
        armas (list): Lista de armas registradas en la aplicación.
        vehiculos (list): Lista de vehículos registrados en la aplicación.
    """

    def __init__(self):
        """
        Inicializa una nueva instancia de la clase App.

        Este constructor inicializa todas las listas que contendrán los diferentes objetos manejados por la aplicación.
        """
        self.especies = []  # Lista que almacenará las especies
        self.misiones = []  # Lista que almacenará las misiones
        self.naves = []  # Lista que almacenará las naves
        self.peliculas = []  # Lista que almacenará las películas
        self.planetas = []  # Lista que almacenará los planetas
        self.personajes = []  # Lista que almacenará los personajes
        self.armas = []  # Lista que almacenará las armas
        self.vehiculos = []  # Lista que almacenará los vehículos

####################################################################################################################

    # CARGAR API
    
    def api(self, url):
        """
        Realiza una solicitud GET a la URL proporcionada y devuelve los datos en formato JSON.

        Args:
            url (str): La URL a la que se realizará la solicitud.

        Returns:
            dict: Los datos obtenidos de la respuesta en formato JSON.
        """
        response = requests.get(url)  # Realiza la solicitud GET a la URL proporcionada
        data = response.json()  # Convierte la respuesta en formato JSON a un diccionario
        return data  # Devuelve los datos en formato JSON


    def cargar_planetas_api(self):
        """
        Carga los datos de los planetas desde la API y los agrega a la lista de planetas en la aplicación.

        Este método realiza múltiples solicitudes a la API para obtener todos los planetas, crea objetos Planeta
        con los datos obtenidos, y los almacena en la lista `self.planetas`.

        Utiliza paginación para obtener todos los planetas disponibles en la API.

        Args:
            None

        Returns:
            None
        """
        url = "https://www.swapi.tech/api/planets"  # URL inicial para obtener los datos de los planetas
        while url:  # Continua mientras haya una URL para la siguiente página
            planetas_api = self.api(url)  # Llama al método api para obtener los datos de la URL actual
            for planet_gnrl in planetas_api["results"]:
                uid = planet_gnrl['uid']  # Obtiene el UID del planeta

                info_planet = self.api(planet_gnrl['url'])  # Obtiene los detalles del planeta usando su URL específica
                dict = info_planet['result']['properties']  # Extrae las propiedades del planeta del JSON

                # Atributos del planeta
                name = dict['name']  # Nombre del planeta
                diameter = dict['diameter']  # Diámetro del planeta
                rotation_period = dict['rotation_period']  # Período de rotación del planeta
                orbital_period = dict['orbital_period']  # Período orbital del planeta
                gravity = dict['gravity']  # Gravedad del planeta
                population = dict['population']  # Población del planeta
                climate = dict['climate']  # Clima del planeta
                terrain = dict['terrain']  # Tipo de terreno del planeta
                surface_water = dict['surface_water']  # Porcentaje de agua superficial del planeta
                created = dict['created']  # Fecha de creación del registro del planeta
                edited = dict['edited']  # Fecha de la última edición del registro del planeta
                url = dict['url']  # URL con información adicional del planeta

                # Crear objeto Planeta y agregarlo a la lista de planetas
                self.planetas.append(Planeta(uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url))
            
            url = planetas_api.get("next")  # Actualiza la URL para la siguiente página de resultados, si existe

    
    def buscar_planet_url(self, url):
        """
        Busca un planeta en la lista de planetas por su URL.

        Args:
            url (str): La URL del planeta a buscar.

        Returns:
            Planeta: El objeto Planeta si se encuentra, de lo contrario None.
        """
        for planeta in self.planetas:
            if planeta.url == url:  # Compara la URL del planeta actual con la URL proporcionada
                return planeta  # Retorna el planeta si coincide
        return None  # Retorna None si no se encuentra el planeta
                    

    def cargar_especies_api(self):
        """
        Carga los datos de las especies desde la API y los agrega a la lista de especies en la aplicación.

        Utiliza paginación para obtener todas las especies disponibles en la API.
        """
        url = "https://www.swapi.tech/api/species"  # URL inicial para obtener los datos de las especies
        while url:  # Continua mientras haya una URL para la siguiente página
            especies_api = self.api(url)  # Llama al método api para obtener los datos de la URL actual
            for especie_gnrl in especies_api["results"]:
                uid = especie_gnrl['uid']  # Obtiene el UID de la especie
                info_especie = self.api(especie_gnrl['url'])  # Obtiene los detalles de la especie usando su URL específica
                dict = info_especie['result']['properties']  # Extrae las propiedades de la especie del JSON
                    
                # Atributos de la especie
                name = dict['name']
                classification = dict['classification']
                designation = dict['designation']
                average_height = dict['average_height']
                average_lifespan = dict['average_lifespan']
                hair_colors = dict['hair_colors']
                skin_colors = dict['skin_colors']
                eye_colors = dict['eye_colors']
                homeworld = self.buscar_planet_url(dict['homeworld'])  # Busca el planeta de origen usando la URL
                language = dict['language']
                created = dict['created']
                edited = dict['edited']
                url = dict['url']

                people = []  # Lista vacía de personajes asociados a la especie
                episodes = []  # Lista vacía de episodios donde aparece la especie

                # Crear objeto Especie y agregarlo a la lista de especies
                especie = Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url)
                self.especies.append(especie)  # Agrega la especie a la lista de especies
            
            url = especies_api.get("next")  # Actualiza la URL para la siguiente página de resultados, si existe

    def buscar_especie_planeta(self, planeta):
        """
        Busca una especie asociada a un planeta específico.

        Args:
            planeta (obj): Objeto Planeta para buscar la especie asociada.

        Returns:
            Especie: El objeto Especie si se encuentra una especie en el planeta, de lo contrario None.
        """
        for especie in self.especies:
            if especie.homeworld.name == planeta.name:  # Compara el nombre del planeta de origen con el planeta proporcionado
                return especie  # Retorna la especie si coincide
        return None  # Retorna None si no se encuentra ninguna especie asociada al planeta

    def cargar_personajes_api(self):
        """
        Carga los datos de los personajes desde la API y los agrega a la lista de personajes en la aplicación.

        También asocia los personajes con su especie y planeta de origen si están disponibles.
        """
        url = "https://www.swapi.tech/api/people"  # URL inicial para obtener los datos de los personajes
        while url:  # Continua mientras haya una URL para la siguiente página
            personajes_api = self.api(url)  # Llama al método api para obtener los datos de la URL actual
            for personaje_gnrl in personajes_api["results"]:
                uid = personaje_gnrl['uid']  # Obtiene el UID del personaje
                info_personaje = self.api(personaje_gnrl['url'])  # Obtiene los detalles del personaje usando su URL específica
                dict = info_personaje['result']['properties']  # Extrae las propiedades del personaje del JSON
                    
                # Atributos del personaje
                name = dict['name']
                height = dict['height']
                mass = dict['mass']
                hair_color = dict['hair_color']
                skin_color = dict['skin_color']
                eye_color = dict['eye_color']
                birth_year = dict['birth_year']
                gender = dict['gender']
                created = dict['created']
                edited = dict['edited']
                url = dict['url']
                homeworld = self.buscar_planet_url(dict['homeworld'])  # Busca el planeta de origen usando la URL
                naves = []  # Lista vacía para las naves asociadas al personaje
                vehiculos = []  # Lista vacía para los vehículos asociados al personaje
                episodes = []  # Lista vacía para los episodios donde aparece el personaje
                especie = self.buscar_especie_planeta(homeworld)  # Busca la especie asociada al planeta de origen
                
                # Crear objeto Personaje
                personaje = Personaje(uid, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, created, edited, homeworld, url, episodes, especie, naves, vehiculos)

                # Asocia el personaje con su especie si se encuentra
                for esp in self.especies:
                    if esp.homeworld.url == dict['homeworld']:
                        esp.people.append(personaje)
                        break

                # Asocia el personaje con su planeta de origen si se encuentra
                for planeta in self.planetas:
                    if planeta.url == dict['homeworld']:
                        planeta.personajes.append(personaje)
                        break
                    
                # Agrega el personaje a la lista de personajes
                self.personajes.append(personaje)

            url = personajes_api.get("next")  # Actualiza la URL para la siguiente página de resultados, si existe

         
    def add_films_specie(self, url, pelicula):
        """
        Asocia una película con una especie específica en la lista de especies.

        Args:
            url (str): La URL de la especie a la que se asociará la película.
            pelicula (Pelicula): El objeto Pelicula que se asociará a la especie.

        Returns:
            None
        """
        for especie in self.especies:
            if especie.url == url:  # Compara la URL de la especie con la URL proporcionada
                especie.episodes.append(pelicula)  # Agrega la película a la lista de episodios de la especie

    def add_films_planet(self, url, pelicula):
        """
        Asocia una película con un planeta específico en la lista de planetas.

        Args:
            url (str): La URL del planeta al que se asociará la película.
            pelicula (Pelicula): El objeto Pelicula que se asociará al planeta.

        Returns:
            None
        """
        for planeta in self.planetas:
            if planeta.url == url:  # Compara la URL del planeta con la URL proporcionada
                planeta.episodes.append(pelicula)  # Agrega la película a la lista de episodios del planeta

    def add_films_personaje(self, url, pelicula):
        """
        Asocia una película con un personaje específico en la lista de personajes.

        Args:
            url (str): La URL del personaje al que se asociará la película.
            pelicula (Pelicula): El objeto Pelicula que se asociará al personaje.

        Returns:
            None
        """
        for personaje in self.personajes:
            if personaje.url == url:  # Compara la URL del personaje con la URL proporcionada
                personaje.episodes.append(pelicula)  # Agrega la película a la lista de episodios del personaje

    def cargar_peliculas_api(self):
        """
        Carga los datos de las películas desde la API y las agrega a la lista de películas en la aplicación.

        Además, asocia cada película con las especies, planetas y personajes correspondientes.
        """
        peliculas_api = self.api("https://www.swapi.tech/api/films/")  # Obtiene los datos de las películas desde la API
        for film_gnrl in peliculas_api["result"]:
            uid = film_gnrl['uid']  # Obtiene el UID de la película
            title = film_gnrl['properties']['title']  # Obtiene el título de la película
            episode_id = film_gnrl['properties']['episode_id']  # Obtiene el número de episodio
            release_date = film_gnrl['properties']['release_date']  # Obtiene la fecha de lanzamiento
            opening_crawl = film_gnrl['properties']['opening_crawl']  # Obtiene el texto de apertura
            director = film_gnrl['properties']['director']  # Obtiene el nombre del director

            pelicula = Pelicula(uid, title, episode_id, release_date, opening_crawl, director)  # Crea un objeto Pelicula

            # Asocia la película con las especies que aparecen en ella
            for api_especie in film_gnrl['properties']['species']:
                self.add_films_specie(api_especie, pelicula)

            # Asocia la película con los planetas que aparecen en ella
            for api_planet in film_gnrl['properties']['planets']:
                self.add_films_planet(api_planet, pelicula)

            # Asocia la película con los personajes que aparecen en ella
            for api_personaje in film_gnrl['properties']['characters']:
                self.add_films_personaje(api_personaje, pelicula)

            # Agrega la película a la lista de películas
            self.peliculas.append(pelicula)

    def cargar_api(self):
        """
        Carga todos los datos necesarios desde la API en el orden adecuado.

        Este método se encarga de llamar a los métodos que cargan planetas, especies, personajes y películas.
        """
        self.cargar_planetas_api()  # Carga los planetas desde la API
        self.cargar_especies_api()  # Carga las especies desde la API
        self.cargar_personajes_api()  # Carga los personajes desde la API
        self.cargar_peliculas_api()  # Carga las películas desde la API

####################################################################################################################

    # CARGAR CSV

    def cargar_films_csv(self):
        """
        Carga los datos de las películas desde un archivo CSV y los agrega a la lista de películas en la aplicación.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Pelicula.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        with open('csv/films.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                title = row[1]  # Obtiene el título de la película
                episode_id = row[0]  # Obtiene el número de episodio (se utiliza también como UID)
                uid = row[0]  # Establece el UID de la película
                release_date = row[2]  # Obtiene la fecha de lanzamiento
                opening_crawl = row[4]  # Obtiene el texto de apertura
                director = row[3]  # Obtiene el nombre del director

                # Crear objeto Pelicula y agregarlo a la lista de películas
                self.peliculas.append(Pelicula(uid, title, episode_id, release_date, opening_crawl, director))


    def buscar_planeta_nombre(self, nombre):
        """
        Busca un planeta en la lista de planetas por su nombre.

        Args:
            nombre (str): El nombre del planeta a buscar.

        Returns:
            Planeta: El objeto Planeta si se encuentra, de lo contrario None.
        """
        for planeta in self.planetas:
            if planeta.name == nombre:  # Compara el nombre del planeta actual con el nombre proporcionado
                return planeta  # Retorna el planeta si coincide
        return None  # Retorna None si no se encuentra el planeta

    def buscar_especie_nombre(self, nombre):
        """
        Busca una especie en la lista de especies por su nombre.

        Args:
            nombre (str): El nombre de la especie a buscar.

        Returns:
            Especie: El objeto Especie si se encuentra, de lo contrario None.
        """
        for especie in self.especies:
            if especie.name == nombre:  # Compara el nombre de la especie actual con el nombre proporcionado
                return especie  # Retorna la especie si coincide
        return None  # Retorna None si no se encuentra la especie

    def cargar_characters_csv(self):
        """
        Carga los datos de los personajes desde un archivo CSV y los agrega a la lista de personajes en la aplicación,
        evitando duplicados basados en el nombre del personaje.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Personaje.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        uids_nombres_existentes = {personaje.name for personaje in self.personajes}  # Conjunto de nombres de personajes ya existentes
            
        with open('csv/characters.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                    
                # Verificar si el nombre ya está en la lista
                if name not in uids_nombres_existentes:
                    # Atributos del personaje usando índices de columnas
                    specie = row[2]
                    gender = row[3]
                    height = row[4]
                    mass = row[5]
                    hair_color = row[6]
                    eye_color = row[7]
                    skin_color = row[8]
                    year_born = row[9]
                    homeworld = self.buscar_planeta_nombre(row[10])  # Busca el planeta de origen por nombre
                    created, edited, url = None, None, None  # Atributos vacíos para datos no disponibles en el CSV
                    episodes, naves, vehiculos = [], [], []  # Listas vacías para los atributos relacionados
                    
                    # Crear un objeto Personaje y añadirlo a la lista
                    personaje = Personaje(uid, name, height, mass, hair_color, skin_color, eye_color, year_born, gender, created, edited, homeworld, url, episodes, specie, naves, vehiculos)
                    self.personajes.append(personaje)  # Agrega el personaje a la lista de personajes

                    # Actualizar la lista de nombres existentes
                    uids_nombres_existentes.add(name)  # Agrega el nombre del personaje al conjunto para evitar duplicados


    def buscar_especie_droid(self):
        """
        Busca y retorna la especie 'Droid' en la lista de especies.

        Returns:
            Especie: El objeto Especie correspondiente a 'Droid' si se encuentra, de lo contrario None.
        """
        for especie in self.especies:
            if especie.name == "Droid":  # Verifica si la especie es 'Droid'
                return especie  # Retorna la especie 'Droid'

    def buscar_film_nombre(self, nombres_str, films):
        """
        Busca películas por nombre y las agrega a una lista de películas.

        Args:
            nombres_str (str): Una cadena de nombres de películas separadas por comas.
            films (list): Lista a la que se agregarán las películas encontradas.

        Returns:
            list: La lista actualizada de películas.
        """
        nombres = nombres_str.split(",")  # Separa los nombres de películas por comas
        for pelicula in self.peliculas:
            for nombre in nombres:
                if pelicula.title == nombre.strip():  # Compara el título de la película con el nombre proporcionado
                    films.append(pelicula)  # Agrega la película a la lista
                    break     
        return films  # Retorna la lista de películas

    def buscar_nombre_personajes(self, nombres, nombre_nuevo):
        """
        Verifica si un nombre ya existe en una lista de nombres de personajes.

        Args:
            nombres (list): Lista de nombres de personajes existentes.
            nombre_nuevo (str): Nombre de personaje a verificar.

        Returns:
            bool: True si el nombre ya existe, False de lo contrario.
        """
        for nombre in nombres:
            if nombre == nombre_nuevo:  # Compara cada nombre existente con el nuevo nombre
                return True  # Retorna True si el nombre ya existe
        return False  # Retorna False si el nombre no existe

    def cargar_droids_csv(self):
        """
        Carga los datos de los droides desde un archivo CSV y los agrega a la lista de personajes en la aplicación,
        evitando duplicados basados en el nombre del droide.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Droid.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        uids_nombres_existentes = [personaje.name for personaje in self.personajes]  # Lista de nombres de personajes ya existentes
            
        with open('csv/droids.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                    
                # Verificar si el nombre ya está en la lista
                if not self.buscar_nombre_personajes(uids_nombres_existentes, name):
                    # Atributos del droide usando índices de columnas
                    specie = self.buscar_especie_droid()  # Busca la especie 'Droid'
                    model = row[2]
                    manufacturer = row[3]
                    height = row[4]
                    mass = row[5]
                    sensor_color = row[6]
                    plating_color = row[7]
                    primary_function = row[8]
                    nombres_str = row[9]
                    films = []
                    self.buscar_film_nombre(nombres_str, films)  # Busca las películas asociadas al droide

                    # Crear un objeto Droid y añadirlo a la lista
                    droid = Droid(uid, name, specie, model, manufacturer, height, mass, sensor_color, plating_color, primary_function, films)
                    self.personajes.append(droid)  # Agrega el droide a la lista de personajes

                    # Actualizar la lista de nombres existentes
                    uids_nombres_existentes.append(name)

    def cargar_personajes_csv(self):
        """
        Carga los datos de personajes y droides desde archivos CSV y los agrega a la lista de personajes en la aplicación.

        Este método llama a cargar_characters_csv y cargar_droids_csv para manejar ambos tipos de datos.

        Returns:
            None
        """
        self.cargar_characters_csv()  # Carga los personajes desde el archivo CSV
        self.cargar_droids_csv()  # Carga los droides desde el archivo CSV


    def nombres_a_personajes(self, nombres_str):
        """
        Convierte una cadena de nombres de personajes en una lista de objetos Personaje.

        Args:
            nombres_str (str): Una cadena de nombres de personajes separados por comas.

        Returns:
            list: Lista de objetos Personaje que coinciden con los nombres proporcionados.
        """
        personajes = []
        nombres = nombres_str.split(",")  # Divide la cadena de nombres en una lista

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre.strip():  # Compara el nombre del personaje con el nombre proporcionado
                    personajes.append(personaje)  # Agrega el personaje a la lista si coincide
                    break    
            
        return personajes  # Retorna la lista de personajes

    def titulos_a_films(self, film_str):
        """
        Convierte una cadena de títulos de películas en una lista de objetos Pelicula.

        Args:
            film_str (str): Una cadena de títulos de películas separados por comas.

        Returns:
            list: Lista de objetos Pelicula que coinciden con los títulos proporcionados.
        """
        films = []
        nombres = film_str.split(",")  # Divide la cadena de títulos en una lista
        
        for nombre in nombres:
            for pelicula in self.peliculas:
                if pelicula.title == nombre.strip():  # Compara el título de la película con el título proporcionado
                    films.append(pelicula)  # Agrega la película a la lista si coincide
                    break

        return films  # Retorna la lista de películas
                

    def cargar_planetas_csv(self):
        """
        Carga los datos de los planetas desde un archivo CSV y los agrega a la lista de planetas en la aplicación,
        evitando duplicados basados en el UID y el nombre del planeta.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Planeta.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        uids_nombres_existentes = {(planeta.uid, planeta.name) for planeta in self.planetas}  # Conjunto de UIDs y nombres de planetas ya existentes
            
        with open('csv/species.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el UID y el nombre ya están en la lista
                if (uid, name) not in uids_nombres_existentes:
                    # Atributos del planeta usando índices de columnas
                    diameter = row[2]
                    rotation_period = row[3]
                    orbital_period = row[4]
                    gravity = row[5]
                    population = row[6]
                    climate = row[7]
                    terrain = row[8]
                    surface_water = row[9]
                    residents = row[10]  # Nombres de los residentes del planeta
                    films_str = row[11]  # Títulos de las películas en las que aparece el planeta
                    created, edited, url = None, None, None  # Atributos vacíos para datos no disponibles en el CSV
                    
                    people = self.nombres_a_personajes(residents)  # Convierte los nombres de los residentes en objetos Personaje

                    # Crear un objeto Planeta y añadirlo a la lista
                    planeta = Planeta(uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url)

                    planeta.personajes = people  # Asigna los personajes residentes al planeta

                    planeta.films = self.titulos_a_films(films_str)  # Asigna las películas al planeta

                    self.planetas.append(planeta)  # Agrega el planeta a la lista de planetas

                    # Actualizar la lista de UIDs y nombres existentes
                    uids_nombres_existentes.add((uid, name))  # Agrega el UID y el nombre del planeta al conjunto para evitar duplicados


    def personaje_en_especie(self, nombre_especie, personajes):
        """
        Agrega a la lista de personajes aquellos que pertenecen a una especie específica.

        Args:
            nombre_especie (str): El nombre de la especie a buscar.
            personajes (list): La lista en la que se agregarán los personajes que pertenecen a la especie.

        Returns:
            list: La lista actualizada de personajes que pertenecen a la especie.
        """
        for personaje in self.personajes:
            if isinstance(personaje.specie, Especie) and personaje.specie.name == nombre_especie:  # Verifica si la especie del personaje coincide con el nombre proporcionado
                personajes.append(personaje)  # Agrega el personaje a la lista
        
        return personajes  # Retorna la lista de personajes

    def asignar_especies_a_personajes(self):
        """
        Asigna la especie correcta a cada personaje si el atributo specie es un nombre en lugar de un objeto Especie.

        Returns:
            None
        """
        for personaje in self.personajes:
            if isinstance(personaje.specie, str):  # Verifica si el atributo specie es una cadena de texto
                personaje.specie = self.buscar_especie_nombre(personaje.specie)  # Reemplaza el nombre con el objeto Especie correspondiente

    def cargar_especies_csv(self):
        """
        Carga los datos de las especies desde un archivo CSV y los agrega a la lista de especies en la aplicación,
        evitando duplicados basados en el UID y el nombre de la especie.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Especie.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        uids_nombres_existentes = {(especie.uid, especie.name) for especie in self.especies}  # Conjunto de UIDs y nombres de especies ya existentes
        
        with open('csv/species.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el UID y el nombre ya están en la lista
                if (uid, name) not in uids_nombres_existentes:
                    # Atributos de la especie usando índices de columnas
                    classification = row[2]
                    designation = row[3]
                    average_height = row[4]
                    skin_colors = row[5]
                    hair_colors = row[6]
                    eye_colors = row[7]
                    average_lifespan = row[8]
                    language = row[9]
                    homeworld = row[10]
                    created, edited, url = None, None, None  # Atributos vacíos para datos no disponibles en el CSV
                    people, episodes = [], []

                    self.personaje_en_especie(name, people)  # Agrega los personajes que pertenecen a esta especie a la lista people
                    
                    # Crear un objeto Especie y añadirlo a la lista
                    especie = Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url)
                    self.especies.append(especie)  # Agrega la especie a la lista de especies

                    # Actualizar la lista de UIDs y nombres existentes
                    uids_nombres_existentes.add((uid, name))  # Agrega el UID y el nombre de la especie al conjunto para evitar duplicados
        
        self.asignar_especies_a_personajes()  # Asigna las especies correctas a los personajes si es necesario


    def guardar_hyperdrive_rating(self, hyperdrive):   
        """
        Convierte el valor del hyperdrive rating a un valor numérico si está vacío.

        Args:
            hyperdrive (str): El valor del hyperdrive rating como cadena de texto.

        Returns:
            float: El valor del hyperdrive rating, 0.0 si estaba vacío.
        """
        if hyperdrive == "":
            hyperdrive = 0.0  # Asigna 0.0 si el valor está vacío
            return hyperdrive
        else:
            return float(hyperdrive)  # Convierte y retorna el valor como float

    def nave_piloto(self, nave, nombres_str):
        """
        Asocia una nave con sus pilotos basados en una cadena de nombres de personajes.

        Args:
            nave (Starship): El objeto Starship que se asociará a los pilotos.
            nombres_str (str): Una cadena de nombres de personajes separados por comas.

        Returns:
            None
        """
        nombres = nombres_str.split(",")  # Divide la cadena de nombres en una lista

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre.strip():  # Compara el nombre del personaje con el nombre proporcionado
                    personaje.naves.append(nave)  # Agrega la nave a la lista de naves del personaje
                    break

    def cargar_naves_csv(self):
        """
        Carga los datos de las naves desde un archivo CSV y los agrega a la lista de naves en la aplicación.

        También asocia cada nave con sus pilotos y las películas en las que aparece.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Starship.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        with open('csv/starships.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                id = row[0]
                name = row[1]
                model = row[2]
                manufacturer = row[3]
                cost_in_credits = row[4]
                length = row[5]
                max_atmosphering_speed = row[6]
                crew = row[7]
                passengers = row[8]
                cargo_capacity = row[9]
                consumables = row[10]
                hyperdrive_rating = self.guardar_hyperdrive_rating(row[11])  # Procesa el hyperdrive rating
                mglt = row[12]
                starship_class = row[13]
                pilots = self.nombres_a_personajes(row[14])  # Convierte los nombres de los pilotos en objetos Personaje
                films = self.titulos_a_films(row[15])  # Convierte los títulos de películas en objetos Pelicula

                # Crear un objeto Starship y añadirlo a la lista
                nave = Starship(id, name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, hyperdrive_rating, mglt, starship_class, pilots, films)

                self.nave_piloto(nave, row[14])  # Asocia la nave con sus pilotos

                self.naves.append(nave)  # Agrega la nave a la lista de naves

    def personajes_vehiculos(self, nombres_str, vehiculo):
        """
        Asocia un vehículo con los personajes basados en una cadena de nombres de personajes.

        Args:
            nombres_str (str): Una cadena de nombres de personajes separados por comas.
            vehiculo (Vehicle): El objeto Vehicle que se asociará a los personajes.

        Returns:
            None
        """
        nombres = nombres_str.split(",")  # Divide la cadena de nombres en una lista

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre.strip():  # Compara el nombre del personaje con el nombre proporcionado
                    personaje.vehiculos.append(vehiculo)  # Agrega el vehículo a la lista de vehículos del personaje
                    break

    def cargar_vehiculos_csv(self):
        """
        Carga los datos de los vehículos desde un archivo CSV y los agrega a la lista de vehículos en la aplicación.

        También asocia cada vehículo con sus pilotos y las películas en las que aparece.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Vehicle.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        with open('csv/vehicles.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                id = row[0]
                name = row[1]
                model = row[2]
                manufacturer = row[3]
                cost_in_credits = row[4]
                length = row[5]
                max_atmosphering_speed = row[6]
                crew = row[7]
                passengers = row[8]
                cargo_capacity = row[9]
                consumables = row[10]
                vehicle_class = row[11]
                pilots = self.nombres_a_personajes(row[12])  # Convierte los nombres de los pilotos en objetos Personaje
                films = self.titulos_a_films(row[13])  # Convierte los títulos de películas en objetos Pelicula
                    
                # Crear un objeto Vehicle y añadirlo a la lista
                vehiculo = Vehicle(id, name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, vehicle_class, pilots, films)

                self.personajes_vehiculos(row[12], vehiculo)  # Asocia el vehículo con sus personajes

                self.vehiculos.append(vehiculo)  # Agrega el vehículo a la lista de vehículos

    def cargar_armas_csv(self):  
        """
        Carga los datos de las armas desde un archivo CSV y los agrega a la lista de armas en la aplicación.

        El archivo CSV debe estar en la carpeta 'csv' y debe contener las columnas necesarias para crear objetos Weapon.
        La primera fila del archivo se omite porque se asume que contiene los encabezados.

        Returns:
            None
        """
        with open('csv/weapons.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                id = row[0]
                name = row[1]
                model = row[2]
                manufacturer = row[3]
                cost_in_credits = row[4]
                length = row[5]
                type = row[6]
                description = row[7]
                films = self.titulos_a_films(row[8])  # Convierte los títulos de películas en objetos Pelicula
                    
                # Crear un objeto Weapon y añadirlo a la lista
                arma = Weapon(id, name, model, manufacturer, cost_in_credits, length, type, description, films)
                
                self.armas.append(arma)  # Agrega el arma a la lista de armas

    def cargar_csv(self):
        """
        Carga todos los datos necesarios desde los archivos CSV en el orden adecuado.

        Este método se encarga de llamar a los métodos que cargan films, personajes, especies, naves, vehículos y armas.

        Returns:
            None
        """
        self.cargar_films_csv()  # Carga los films desde el archivo CSV
        self.cargar_personajes_csv()  # Carga los personajes (incluyendo droides) desde el archivo CSV
        self.cargar_especies_csv()  # Carga las especies desde el archivo CSV
        self.cargar_naves_csv()  # Carga las naves desde el archivo CSV
        self.cargar_vehiculos_csv()  # Carga los vehículos desde el archivo CSV
        self.cargar_armas_csv()  # Carga las armas desde el archivo CSV

        
###################################################################################################################

    #FUNCION PRINCIPAL DE CARGA

    def borrar_personajes_repetidos(self):
        """
        Elimina personajes duplicados en la lista de personajes, manteniendo solo el primero encontrado.

        La función compara los nombres de los personajes y elimina aquellos que tengan nombres repetidos,
        dejando solo la primera aparición de cada nombre.

        Returns:
            None
        """
        personajes_unicos = []  # Lista para almacenar personajes únicos
        nombres_encontrados = set()  # Conjunto para almacenar los nombres ya encontrados

        for personaje in self.personajes:
            if personaje.name not in nombres_encontrados:  # Verifica si el nombre del personaje ya ha sido encontrado
                personajes_unicos.append(personaje)  # Agrega el personaje a la lista de únicos
                nombres_encontrados.add(personaje.name)  # Añade el nombre al conjunto de nombres encontrados
        
        self.personajes = personajes_unicos  # Actualiza la lista de personajes con solo personajes únicos

    # CARGAR API Y LUEGO CSV
    def cargar(self):
        """
        Carga los datos desde la API y luego desde archivos CSV, eliminando personajes duplicados.

        Este método coordina la carga de datos desde la API y archivos CSV, y luego limpia la lista de personajes
        para eliminar duplicados basados en el nombre del personaje.

        Returns:
            None
        """
        print("\nEsperando...\n")
        self.cargar_api()  # Carga los datos desde la API
        self.cargar_csv()  # Carga los datos desde archivos CSV
        self.borrar_personajes_repetidos()  # Elimina personajes duplicados de la lista
        print("\n...Carga exitosa")

###################################################################################################################

    #FUNCIONALIDADES RELACIONADAS A LA API

    def listar_peliculas(self):
        """
        Imprime los atributos de todas las películas en la lista de películas.

        Este método recorre la lista de películas y llama al método `show_atr()` de cada película
        para mostrar sus atributos de forma detallada.

        Returns:
            None
        """
        for pelicula in self.peliculas:
            print(pelicula.show_atr())  # Imprime los atributos de la película

    def listar_especies(self):
        """
        Muestra la información de todas las especies en la lista de especies.

        Este método recorre la lista de especies y llama al método `mostrar()` de cada especie
        para mostrar su información.

        Returns:
            None
        """
        for especie in self.especies:
            especie.mostrar()  # Muestra la información de la especie

    def listar_planetas(self):
        """
        Muestra la información de todos los planetas en la lista de planetas.

        Este método recorre la lista de planetas y llama al método `mostrar()` de cada planeta
        para mostrar su información.

        Returns:
            None
        """
        for planeta in self.planetas:
            planeta.mostrar()  # Muestra la información del planeta

    def buscar_personajes(self):
        """
        Permite al usuario buscar personajes por nombre y ver sus detalles.

        El usuario ingresa un nombre, y la función busca en la lista de personajes aquellos cuyos nombres contienen 
        la cadena ingresada. Luego, el usuario puede elegir ver más detalles sobre un personaje específico.

        Returns:
            None
        """
        nombre = input("\nIngresa el nombre del personaje: ").lower()

        resultadoPersonajes = []

        # Busca en la lista de personajes aquellos que contienen el nombre ingresado
        for personaje in self.personajes:
            print(personaje.name)
            print("")
            if nombre in personaje.name.lower():  # Compara el nombre ingresado con el nombre de cada personaje
                resultadoPersonajes.append(personaje)  # Agrega el personaje a la lista de resultados
        
        if len(resultadoPersonajes) != 0:
            print("\n")
            count = 1
            # Imprime la lista de personajes encontrados numerados
            for personaje in resultadoPersonajes:
                print(f"{count}. {personaje.name}")
                count += 1
            
            while True:
                print("\n1. Ver más a Detalle un Personaje\n2. Salir")

                # Solicita al usuario que ingrese una opción y valida que sea un número válido
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
                if opcion == "1":
                    # Solicita al usuario que ingrese el número del personaje para ver más detalles y valida la entrada
                    opcion_personaje = input("\nIngrese el número del personaje del que quiere ver más a detalle: ")
                    while (not opcion_personaje.isnumeric()) or (not int(opcion_personaje) in range(1, len(resultadoPersonajes) + 1)):
                        print("Error!!! Dato Inválido.")
                        opcion_personaje = input("\nIngrese el número del personaje del que quiere ver más a detalle: ")

                    index = int(opcion_personaje) - 1

                    # Muestra los atributos del personaje seleccionado
                    print("\n")
                    print(resultadoPersonajes[index].mostrar())
                else:
                    # Si se selecciona la opción de salir, termina el bucle
                    break
        else:
            # Si no se encuentran personajes con el nombre ingresado, muestra un mensaje de error
            print("\nNo se encontraron personajes con el nombre ingresado.")

###################################################################################################################

    # FUNCIONALIDADES DE GRAFICOS Y ESTADISTICAS

    def grafico_personajes_planetas(self):
        """
        Genera un gráfico de barras que muestra el número de personajes nacidos en cada planeta.

        La función filtra los planetas que tienen episodios asociados y cuenta cuántos personajes tienen
        como planeta de origen cada uno de esos planetas. Los personajes cuyo planeta de origen es desconocido
        se contabilizan bajo 'Unknown'.

        Returns:
            None
        """
        # Filtra planetas que tienen episodios
        planetas_con_episodios = [planeta for planeta in self.planetas if len(planeta.episodes) > 0]

        # Inicializar el defaultdict con un valor inicial para 'Unknown'
        personajes_por_planeta = defaultdict(int)
        personajes_por_planeta['Unknown'] = 0  # Cuenta para personajes con planeta de origen desconocido

        # Contar personajes por planeta
        for personaje in self.personajes:
            if isinstance(personaje, Personaje):
                if personaje.homeworld is None:  # Si el personaje no tiene un planeta de origen definido
                    personajes_por_planeta['Unknown'] += 1
                else:
                    for planeta in planetas_con_episodios:
                        if personaje.homeworld.name == planeta.name:  # Si el personaje pertenece a un planeta con episodios
                            personajes_por_planeta[planeta.name] += 1

        # Preparar datos para el gráfico
        planeta_names = list(personajes_por_planeta.keys())
        counts = list(personajes_por_planeta.values())

        # Crear el gráfico
        plt.figure(figsize=(15, 10))
        plt.bar(planeta_names, counts, color='skyblue')
        plt.xlabel('Planetas')
        plt.ylabel('Número de Personajes')
        plt.title('Número de personajes nacidos en cada planeta')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()  # Muestra el gráfico generado


    def graficos_naves(self):
        """
        Genera gráficos de barras para diferentes atributos de las naves, incluyendo longitud, capacidad de carga,
        clasificación de hiperimpulsor y MGLT (Modern Galactic Light Time).

        El usuario puede seleccionar qué gráfico desea ver a través de un menú interactivo.

        Returns:
            None
        """
        # Preparar los datos
        nombres = [nave.name for nave in self.naves]  # Lista de nombres de las naves
        longitudes = [float(nave.length) if nave.length else 0 for nave in self.naves]  # Lista de longitudes de las naves
        capacidades_carga = [float(nave.cargo_capacity) if nave.cargo_capacity else 0 for nave in self.naves]  # Lista de capacidades de carga de las naves
        
        # Lista de clasificaciones de hiperimpulsor
        clasificaciones_hiperimpulsor = []
        for nave in self.naves:
            if nave.hyperdrive_rating is not None:
                clasificaciones_hiperimpulsor.append(float(nave.hyperdrive_rating))

        mglt = [float(nave.mglt) if nave.mglt else 0 for nave in self.naves]  # Lista de MGLT de las naves

        while True:
            # Menú de opciones
            print("\nSeleccione el gráfico que desea ver:\n1. Longitud de la nave\n2. Capacidad de carga\n3. Clasificación de hiperimpulsor\n4. MGLT (Modern Galactic Light Time)\n5. Salir")

            opcion = input("Ingrese el número de la opción deseada: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 6)):
                print("Error!!! Dato Inválido.")
                opcion = input("Ingrese el número de la opción deseada: ")

            # Mostrar el gráfico correspondiente o salir
            if opcion == '1':
                plt.figure(figsize=(15, 7))  # Tamaño del gráfico
                plt.bar(nombres, longitudes, color='skyblue')
                plt.title('Longitud de la nave', fontsize=16)
                plt.ylabel('Longitud (metros)', fontsize=14)
            elif opcion == '2':
                plt.figure(figsize=(15, 7))
                plt.bar(nombres, capacidades_carga, color='lightgreen')
                plt.title('Capacidad de carga', fontsize=16)
                plt.ylabel('Capacidad de carga (kg)', fontsize=14)
            elif opcion == '3':
                plt.figure(figsize=(15, 7))
                plt.bar(nombres, clasificaciones_hiperimpulsor, color='lightcoral')
                plt.title('Clasificación de hiperimpulsor', fontsize=16)
                plt.ylabel('Clasificación de hiperimpulsor', fontsize=14)
            elif opcion == '4':
                plt.figure(figsize=(15, 7))
                plt.bar(nombres, mglt, color='lightseagreen')
                plt.title('MGLT (Modern Galactic Light Time)', fontsize=16)
                plt.ylabel('MGLT', fontsize=14) 
            else:
                break  # Sale del bucle y termina la función si se selecciona 'Salir'

            # Configuraciones del gráfico
            plt.xticks(rotation=90, fontsize=12)  # Rota las etiquetas del eje X para que sean legibles
            plt.yticks(fontsize=12)
            plt.tight_layout()  # Ajusta el diseño para evitar solapamientos
            plt.show()  # Muestra el gráfico generado


    def estadistica_naves(self):
        """
        Calcula y muestra estadísticas sobre las naves agrupadas por clase.

        Las estadísticas incluyen el promedio, la moda, el valor máximo y el valor mínimo de las variables:
        hyperdrive_rating, mglt, max_atmosphering_speed y cost_in_credits.

        Returns:
            None
        """
        # Preparar los datos agrupados por clase de nave
        clases_naves = {}
        
        for nave in self.naves:
            clase = nave.starship_class
            
            if clase not in clases_naves:
                clases_naves[clase] = {
                    "hyperdrive_rating": [],
                    "mglt": [],
                    "max_atmosphering_speed": [],
                    "cost_in_credits": []
                }
            
            if nave.hyperdrive_rating is not None:
                clases_naves[clase]["hyperdrive_rating"].append(float(nave.hyperdrive_rating))
            
            if nave.mglt is not None and nave.mglt != "":
                clases_naves[clase]["mglt"].append(float(nave.mglt))
            
            if nave.max_atmosphering_speed is not None and nave.max_atmosphering_speed != "":
                clases_naves[clase]["max_atmosphering_speed"].append(float(nave.max_atmosphering_speed))
            
            if nave.cost_in_credits is not None and nave.cost_in_credits != "" :
                clases_naves[clase]["cost_in_credits"].append(float(nave.cost_in_credits))

        # Funciones auxiliares para cálculos de estadísticas
        def calcular_promedio(valores):
            return sum(valores) / len(valores) if valores else None

        def calcular_moda(valores):
            if not valores:
                return None
            frecuencia = {}
            for v in valores:
                frecuencia[v] = frecuencia.get(v, 0) + 1
            moda = max(frecuencia, key=frecuencia.get)
            return moda

        def calcular_maximo(valores):
            return max(valores) if valores else None

        def calcular_minimo(valores):
            return min(valores) if valores else None

        # Mostrar estadísticas por clase de nave
        print(f"{'Clase de Nave':<30} {'Variable':<25} {'Promedio':<10} {'Moda':<10} {'Máximo':<10} {'Mínimo':<10}")
        print("="*100)

        for clase, datos in clases_naves.items():
            for variable, valores in datos.items():
                promedio = calcular_promedio(valores)
                moda = calcular_moda(valores)
                maximo = calcular_maximo(valores)
                minimo = calcular_minimo(valores)

                # Usar "-" si el valor es None
                promedio_str = f"{promedio:<10.2f}" if promedio is not None else "-"
                moda_str = f"{moda:<10.2f}" if moda is not None else "-"
                maximo_str = f"{maximo:<10.2f}" if maximo is not None else "-"
                minimo_str = f"{minimo:<10.2f}" if minimo is not None else "-"
                
                print(f"{clase:<30} {variable:<25} {promedio_str} {moda_str} {maximo_str} {minimo_str}")

#################################################################################################################

    #FUNCIONALIDADES DE MISIONES

    def elegir_planeta(self):
        """
        Permite al usuario seleccionar un planeta de la lista de planetas disponibles.

        Muestra una lista numerada de planetas y solicita al usuario que ingrese el número correspondiente
        al planeta deseado. Valida la entrada del usuario y devuelve el objeto Planeta seleccionado.

        Returns:
            Planeta: El objeto Planeta seleccionado por el usuario.
        """
        print("\n============================================")
        print("           PLANETAS DISPONIBLES")
        print("============================================")
        
        count = 1
        for planeta in self.planetas:
            print(f"{count}. {planeta.name}")
            count += 1

        opcion_planeta = input("\nIngrese el número de planeta donde desea realizar la misión: ")
        while (not opcion_planeta.isnumeric()) or (not int(opcion_planeta) in range(1, len(self.planetas) + 1)):
            print("Error!!! Dato Inválido.")
            opcion_planeta = input("\nIngrese el número de planeta donde desea realizar la misión: ")
        
        index = int(opcion_planeta) - 1
        planeta = self.planetas[index]

        return planeta

    def elegir_nave(self):
        """
        Permite al usuario seleccionar una nave de la lista de naves disponibles.

        Muestra una lista numerada de naves y solicita al usuario que ingrese el número correspondiente
        a la nave deseada. Valida la entrada del usuario y devuelve el objeto Starship seleccionado.

        Returns:
            Starship: El objeto Starship seleccionado por el usuario.
        """
        print("\n============================================")
        print("             NAVES DISPONIBLES")
        print("============================================")
        
        count = 1
        for nave in self.naves:
            print(f"{count}. {nave.name}")
            count += 1 

        opcion_nave = input("\nIngrese el número de nave que desea utilizar: ")
        while (not opcion_nave.isnumeric()) or (not int(opcion_nave) in range(1, len(self.naves) + 1)):
            print("Error!!! Dato Inválido.")
            opcion_nave = input("\nIngrese el número de nave que desea utilizar: ")
        
        index = int(opcion_nave) - 1
        nave = self.naves[index]

        return nave

    def elegir_armas(self):
        """
        Permite al usuario seleccionar armas de la lista de armas disponibles.

        Muestra una lista numerada de armas y solicita al usuario que ingrese el número correspondiente
        a las armas deseadas. El usuario puede seleccionar hasta 7 armas. Valida la entrada del usuario
        y devuelve una lista de objetos Weapon seleccionados.

        Returns:
            list: Una lista de objetos Weapon seleccionados por el usuario.
        """
        print("\n============================================")
        print("              ARMAS DISPONIBLES")
        print("============================================")

        armas = []
        
        count = 1
        for arma in self.armas:
            print(f"{count}. {arma.name}")
            count += 1

        while len(armas) < 7:
            print("\n1. Añadir Arma\n2. Salir")
            
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
            if opcion == "1":
                opcion_armas = input("\nIngrese el número de arma que desea agregar a la misión: ")
                while (not opcion_armas.isnumeric()) or (not int(opcion_armas) in range(1, len(self.armas)+1)):
                    print("Error!!! Dato Inválido.")
                    opcion_armas = input("\nIngrese el número de arma que desea agregar a la misión: ")
                
                index = int(opcion_armas) - 1
                arma = self.armas[index]
                armas.append(arma)        
            else:
                break
        
        return armas

    def elegir_integrantes(self):
        """
        Permite al usuario seleccionar integrantes de la lista de personajes disponibles.

        Muestra una lista numerada de personajes y solicita al usuario que ingrese el número correspondiente
        a los personajes deseados. El usuario puede seleccionar hasta 7 personajes. Valida la entrada del usuario
        y devuelve una lista de objetos Personaje seleccionados.

        Returns:
            list: Una lista de objetos Personaje seleccionados por el usuario.
        """
        print("\n============================================")
        print("         INTEGRANTES DISPONIBLES")
        print("============================================")

        integrantes = []
        
        count = 1
        for personaje in self.personajes:
            print(f"{count}. {personaje.name}")
            count += 1

        while len(integrantes) < 7:
            print("\n1. Añadir personaje\n2. Salir")
            
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
            if opcion == "1":
                opcion_integrante = input("\nIngrese el número de integrante que desea agregar a la misión: ")
                while (not opcion_integrante.isnumeric()) or (not int(opcion_integrante) in range(1, len(self.personajes)+1)):
                    print("Error!!! Dato Inválido.")
                    opcion_integrante = input("\nIngrese el número de integrante que desea agregar a la misión: ")
                
                index = int(opcion_integrante) - 1
                integrante = self.personajes[index]
                integrantes.append(integrante)        
            else:
                break
        
        return integrantes

    def crear_mision(self):
        """
        Crea una nueva misión si el número de misiones actuales es menor a 5.

        Solicita al usuario que ingrese los detalles de la misión, incluyendo nombre, planeta,
        nave, armas e integrantes. Si se cumplen las condiciones, la misión se agrega a la lista
        de misiones.

        Returns:
            None
        """
        if len(self.misiones) < 5:
            print("\nIngrese los detalles de la misión:")
            nombre = input("Ingrese el nombre: ")
            planeta = self.elegir_planeta()
            nave = self.elegir_nave()
            armas = self.elegir_armas()
            integrantes = self.elegir_integrantes()

            mision = Mision(nombre, planeta, nave, armas, integrantes)
            self.misiones.append(mision)
            print("\nMisión creada exitosamente.\n")
        else:
            print("\nNo se puede crear más de 5 misiones.")


    def agregar_armas(self, armas):
        """
        Permite al usuario agregar armas a una misión, hasta un máximo de 7 armas.

        Muestra una lista de armas disponibles y solicita al usuario que seleccione las armas para agregar
        a la misión. Valida las entradas del usuario y actualiza la lista de armas de la misión.

        Args:
            armas (list): La lista actual de armas en la misión.

        Returns:
            None
        """
        if len(armas) < 7:
            print("\n============================================")
            print("              ARMAS DISPONIBLES")
            print("============================================")
            
            count = 1
            for arma in self.armas:
                print(f"{count}. {arma.name}")
                count += 1

            while len(armas) < 7:
                print("\n1. Añadir Arma\n2. Salir")
                
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                    
                if opcion == "1":
                    opcion_armas = input("\nIngrese el número de arma que desea agregar a la misión: ")
                    while (not opcion_armas.isnumeric()) or (not int(opcion_armas) in range(1, len(self.armas)+1)):
                        print("Error!!! Dato Inválido.")
                        opcion_armas = input("\nIngrese el número de arma que desea agregar a la misión: ")
                    
                    index = int(opcion_armas) - 1
                    arma = self.armas[index]
                    armas.append(arma)        
                else:
                    break     
        else:
            print("\nNo se puede agregar más de 7 armas.")

    def eliminar_armas(self, armas):
        """
        Permite al usuario eliminar armas de una misión.

        Muestra una lista de armas actualmente en la misión y solicita al usuario que seleccione
        las armas para eliminar. Valida las entradas del usuario y actualiza la lista de armas de la misión.

        Args:
            armas (list): La lista actual de armas en la misión.

        Returns:
            None
        """
        if len(armas) > 0:
            count = 1
            for arma in armas:
                print(f"{count}. {arma.name}")
                count += 1

            while len(armas) > 0:
                print("\n1. Eliminar Arma\n2. Salir")
                    
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                        
                if opcion == "1":
                    opcion_armas = input("\nIngrese el número de arma que desea eliminar de la misión: ")
                    while (not opcion_armas.isnumeric()) or (not int(opcion_armas) in range(1, len(armas)+1)):
                        print("Error!!! Dato Inválido.")
                        opcion_armas = input("\nIngrese el número de arma que desea eliminar de la misión: ")
                    
                    index = int(opcion_armas) - 1
                    armas.pop(index)       
                else:
                    break
        else:
            print("\nNo hay armas para eliminar.")

        
    def agregar_integrantes(self, integrantes):
        """
        Permite al usuario agregar personajes a la lista de integrantes de una misión, hasta un máximo de 7 integrantes.

        Muestra una lista de personajes disponibles y solicita al usuario que seleccione los personajes para agregar
        a la misión. Valida las entradas del usuario y actualiza la lista de integrantes de la misión.

        Args:
            integrantes (list): La lista actual de integrantes en la misión.

        Returns:
            None
        """
        if len(integrantes) < 7:
            print("\n============================================")
            print("         INTEGRANTES DISPONIBLES")
            print("============================================")
            
            count = 1
            for personaje in self.personajes:
                print(f"{count}. {personaje.name}")
                count += 1

            while len(integrantes) < 7:
                print("\n1. Añadir personaje\n2. Salir")
                
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                    
                if opcion == "1":
                    opcion_integrante = input("\nIngrese el número de integrante que desea agregar a la misión: ")
                    while (not opcion_integrante.isnumeric()) or (not int(opcion_integrante) in range(1, len(self.personajes)+1)):
                        print("Error!!! Dato Inválido.")
                        opcion_integrante = input("\nIngrese el número de integrante que desea agregar a la misión: ")
                    
                    index = int(opcion_integrante) - 1
                    integrante = self.personajes[index]
                    integrantes.append(integrante)        
                else:
                    break

        else:
            print("\nNo se puede agregar más de 7 integrantes.")

    def eliminar_integrantes(self, integrantes):
        """
        Permite al usuario eliminar personajes de la lista de integrantes de una misión.

        Muestra una lista de personajes actualmente en la misión y solicita al usuario que seleccione
        los personajes para eliminar. Valida las entradas del usuario y actualiza la lista de integrantes
        de la misión.

        Args:
            integrantes (list): La lista actual de integrantes en la misión.

        Returns:
            None
        """
        if len(integrantes) > 0:
            count = 1
            for personaje in integrantes:
                print(f"{count}. {personaje.name}")
                count += 1

            while len(integrantes) > 0:
                print("\n1. Eliminar Integrante\n2. Salir")
                
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                    
                if opcion == "1":
                    opcion_integrante = input("\nIngrese el número de integrante que desea eliminar de la misión: ")
                    while (not opcion_integrante.isnumeric()) or (not int(opcion_integrante) in range(1, len(integrantes)+1)):
                        print("Error!!! Dato Inválido.")
                        opcion_integrante = input("\nIngrese el número de integrante que desea eliminar de la misión: ")
                    
                    index = int(opcion_integrante) - 1
                    integrantes.pop(index)        
                else:
                    break 
        else:
            print("\nNo hay integrantes para eliminar.")


    def modificar_mision(self):
        """
        Permite al usuario modificar las características de una misión existente.

        El usuario puede seleccionar una misión de la lista de misiones y luego elegir qué características
        modificar, como el nombre, el planeta, la nave, las armas o los integrantes. Valida las entradas del usuario
        y actualiza la misión con las nuevas características.

        Returns:
            None
        """
        print("\n============================================")
        print("            MODIFICAR MISIONES")
        print("============================================")

        if len(self.misiones) > 0:
            count = 1
            
            # Muestra una lista numerada de misiones
            for mision in self.misiones:
                print(f"{count}. {mision.nombre}")
                count += 1

            opcion_mision = input("\nIngrese el número de la misión que desea modificar: ")
            while (not opcion_mision.isnumeric()) or (not int(opcion_mision) in range(1, len(self.misiones) + 1)):
                print("Error!!! Dato Inválido.")
                opcion_mision = input("\nIngrese el número de la misión que desea modificar: ")
            
            index = int(opcion_mision) - 1
            mision_modif = self.misiones[index]

            while True:
                print("\n¿Qué característica deseas modificar?\n1. Nombre\n2. Planeta\n3. Nave\n4. Armas\n5. Integrantes\n6. Salir")

                opcion_modificacion = input("\nIngrese el número de la acción que desea realizar: ")
                while (not opcion_modificacion.isnumeric()) or (not int(opcion_modificacion) in range(1, 7)):
                    print("Error!!! Dato Inválido.")
                    opcion_modificacion = input("\nIngrese el número de la acción que desea realizar: ")

                if opcion_modificacion == "1":
                    nombre = input("Ingrese el nuevo nombre: ")
                    mision_modif.nombre = nombre
                elif opcion_modificacion == "2":
                    planeta = self.elegir_planeta()
                    mision_modif.planeta = planeta
                elif opcion_modificacion == "3":
                    nave = self.elegir_nave()
                    mision_modif.nave = nave
                elif opcion_modificacion == "4":
                    print("1. Agregar armas\n2. Eliminar armas\n3. Salir")
                    
                    opcion_armas = input("\nIngrese el número de la acción que desea realizar: ")
                    while (not opcion_armas.isnumeric()) or (not int(opcion_armas) in range(1, 4)):
                        print("Error!!! Dato Inválido.")
                        opcion_armas = input("\nIngrese el número de la acción que desea realizar: ")
                    
                    if opcion_armas == "1":
                        self.agregar_armas(mision_modif.armas)
                    elif opcion_armas == "2":
                        self.eliminar_armas(mision_modif.armas)

                elif opcion_modificacion == "5":
                    print("1. Agregar Integrantes\n2. Eliminar Integrantes\n3. Salir")
                    
                    opcion_integrantes = input("\nIngrese el número de la acción que desea realizar: ")
                    while (not opcion_integrantes.isnumeric()) or (not int(opcion_integrantes) in range(1, 4)):
                        print("Error!!! Dato Inválido.")
                        opcion_integrantes = input("\nIngrese el número de la acción que desea realizar: ")
                    
                    if opcion_integrantes == "1":
                        self.agregar_integrantes(mision_modif.integrantes)
                    elif opcion_integrantes == "2":
                        self.eliminar_integrantes(mision_modif.integrantes)
                else:
                    break
                
            print("\nMisión modificada exitosamente.\n")

        else:
            print("\nNo hay misiones para modificar.")


    def visualizar_mision(self):
        """
        Permite al usuario visualizar los detalles de las misiones existentes.

        Muestra una lista numerada de misiones y permite al usuario seleccionar una misión para ver sus detalles.
        Si no hay misiones disponibles, muestra un mensaje indicando que no hay misiones para visualizar.

        Returns:
            None
        """
        print("\n============================================")
        print("            VISUALIZAR MISIONES")
        print("============================================")

        if len(self.misiones) > 0:
            count = 1
            
            # Muestra la lista numerada de misiones disponibles
            for mision in self.misiones:
                print(f"{count}. {mision.nombre}")
                count += 1

            while True:
                print("\n1. Ver detalle de una misión\n2. Salir")
                
                # Solicita al usuario que ingrese una opción y valida que sea un número válido
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                    
                if opcion == "1":
                    opcion_mision = input("\nIngrese el número de la misión para visualizar sus detalles: ")
                    while (not opcion_mision.isnumeric()) or (not int(opcion_mision) in range(1, len(self.misiones) + 1)):
                        print("Error!!! Dato Inválido.")
                        opcion_mision = input("\nIngrese el número de la misión para visualizar sus detalles: ")
                    
                    index = int(opcion_mision) - 1

                    # Muestra los detalles de la misión seleccionada
                    print(self.misiones[index].show_atr())      
                else:
                    break 
        else:
            print("\nNo hay misiones para visualizar.")


    def gestion_misiones(self):
        """
        Módulo de gestión de misiones que permite al usuario crear, modificar y visualizar misiones.

        Muestra un menú interactivo con opciones para crear una nueva misión, modificar una misión existente,
        visualizar los detalles de una misión, o salir del módulo. Valida las entradas del usuario para asegurarse
        de que sean válidas antes de realizar las acciones correspondientes.

        Returns:
            None
        """
        print("\n")
        while True:
            print("\n============================================")
            print("BIENVENIDOS AL MODULO DE GESTION DE MISIONES")
            print("============================================")
            print("1. Crear Misión\n2. Modificar Misiones\n3. Visualizar Misión\n4. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 5)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            
            if opcion == "1":
                self.crear_mision()
            elif opcion == "2":
                self.modificar_mision()
            elif opcion == "3":
                self.visualizar_mision()
            else:
                print("Has salido del módulo de gestión de misiones.")
                break


#################################################################################################################

    #FUNCIONALIDADES GENERALES

    def guardar_misiones(self):
        """
        Guarda las misiones actuales en un archivo de texto llamado 'misiones.txt'.

        Convierte cada misión en una cadena de texto utilizando el método `convert_str()` y escribe cada
        misión en una nueva línea del archivo.

        Returns:
            None
        """
        with open("misiones.txt", 'w') as file:
            for mision in self.misiones:
                file.write(mision.convert_str() + "\n")  # Escribe cada misión en el archivo

    def vaciar(self):
        """
        Vacía la lista de misiones actuales.

        Este método se utiliza para limpiar la lista de misiones después de guardarlas o cuando se requiere
        reiniciar la lista de misiones.

        Returns:
            None
        """
        self.misiones = []  # Resetea la lista de misiones a una lista vacía

    def menu(self):
        """
        Muestra el menú principal del proyecto Star Wars y maneja la interacción del usuario.

        El menú permite al usuario seleccionar entre varias opciones, como listar películas, especies, planetas,
        buscar personajes, visualizar gráficos, gestionar misiones, y salir. Al salir, guarda las misiones en un
        archivo y vacía la lista de misiones.

        Returns:
            None
        """
        print("\n")
        while True:
            print("\n==================================")
            print("BIENVENIDOS AL PROYECTO STAR WARS")
            print("=================================")
            print("1. Lista de Películas de la Saga\n2. Lista de las especies de seres vivos de la saga\n3. Lista de planetas\n4. Buscar Personajes\n5. Gráfico de cantidad de personajes nacidos en cada planeta\n6. Gráficos de características de naves\n7. Estadísticas sobre naves\n8. Gestión de Misiones\n9. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 10)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")

            # Realiza la acción correspondiente según la opción seleccionada
            if opcion == "1":
                self.listar_peliculas()  # Llama al método para listar las películas
            elif opcion == "2":
                self.listar_especies()  # Llama al método para listar las especies
            elif opcion == "3":
                self.listar_planetas()  # Llama al método para listar los planetas
            elif opcion == "4":
                self.buscar_personajes()  # Llama al método para buscar personajes
            elif opcion == "5":
                self.grafico_personajes_planetas()  # Llama al método para mostrar el gráfico de personajes por planeta
            elif opcion == "6":
                self.graficos_naves()  # Llama al método para mostrar gráficos de naves
            elif opcion == "7":
                self.estadistica_naves()  # Llama al método para mostrar estadísticas de naves
            elif opcion == "8":
                self.gestion_misiones()  # Llama al método para gestionar misiones
            else:
                self.guardar_misiones()  # Guarda las misiones antes de salir
                self.vaciar()  # Vacía la lista de misiones
                print("\nAdiós.")
                break  # Sale del bucle y termina el programa


    def nombres_a_armas(self, nombres_str):
        """
        Convierte una cadena de nombres de armas separadas por comas en una lista de objetos Weapon.

        Args:
            nombres_str (str): Cadena de nombres de armas separadas por comas.

        Returns:
            list: Lista de objetos Weapon correspondientes a los nombres dados.
        """
        armas = []
        nombres = nombres_str.split(",")

        for nombre in nombres:
            for arma in self.armas:
                if arma.name == nombre:
                    armas.append(arma)
                    break    
            
        return armas

    def nombre_a_nave(self, nombre):
        """
        Encuentra y devuelve un objeto Starship basado en su nombre.

        Args:
            nombre (str): El nombre de la nave a buscar.

        Returns:
            Starship: El objeto Starship correspondiente al nombre dado, o None si no se encuentra.
        """
        for nave in self.naves:
            if nave.name == nombre:
                return nave

    def nombres_a_personajes2(self, nombres_str):
        """
        Convierte una cadena de nombres de personajes separadas por comas en una lista de objetos Personaje.

        Args:
            nombres_str (str): Cadena de nombres de personajes separadas por comas.

        Returns:
            list: Lista de objetos Personaje correspondientes a los nombres dados.
        """
        print(nombres_str)
        personajes = []
    
        nombres = nombres_str.split(",")
        print(nombres)

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre:
                    personajes.append(personaje)
                    break    
            
        return personajes

    def cargar_misiones(self):
        """
        Carga misiones desde un archivo de texto y las convierte en objetos Mision.

        Lee cada línea del archivo 'misiones.txt', la divide en sus componentes, 
        y utiliza esos componentes para crear objetos Mision que se agregan a la lista de misiones.

        Returns:
            None
        """
        with open("misiones.txt", 'r') as file:
            for linea in file:
                # Usar regex para dividir respetando las comillas simples
                partes = re.split(r",\s*(?=(?:[^']*'[^']*')*[^']*$)", linea.strip())
                
                # Extraer los datos
                nombre = partes[0]
                planeta = self.buscar_planeta_nombre(partes[1])
                nave = self.nombre_a_nave(partes[2])
                
                # Quitar las comillas simples y convertir las listas de armas e integrantes
                armas = self.nombres_a_armas(partes[3].strip("'"))
                integrantes = self.nombres_a_personajes2(partes[4].strip("'").replace(" ", ""))

                # Crear el objeto Misiones y agregarlo a la lista
                mision = Mision(nombre, planeta, nave, armas, integrantes)
                self.misiones.append(mision)

    def iniciar(self):
        """
        Inicia el programa y presenta al usuario la opción de cargar misiones anteriores o empezar de nuevo.

        Dependiendo de la elección del usuario, carga las misiones anteriores desde el archivo
        'misiones.txt' o empieza con una lista vacía de misiones, y luego muestra el menú principal.

        Returns:
            None
        """
        self.cargar()  # Carga los datos iniciales

        while True:
            print("\n==================================")
            print("BIENVENIDOS AL PROYECTO STAR WARS")
            print("=================================")
            print("1. Cargar Misiones Anteriores\n2. No Cargar Misiones Anteriores\n3. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 4)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            
            if opcion == "1":
                self.cargar_misiones()  # Carga misiones anteriores
                self.menu()  # Muestra el menú principal
            elif opcion == "2":
                self.menu()  # Muestra el menú principal sin cargar misiones anteriores
            else:
                # Termina el bucle y finaliza la función
                break
