import requests
from Planeta import Planeta
from Especie import Especie
from Pelicula import Pelicula
from Personaje import Personaje

class App:
    def __init__(self):
        self.especies = []
        self.misiones = []
        self.naves = []
        self.peliculas = []
        self.planetas = []
        self.personajes = []
    
    def api(self, url):
        response = requests.get(url)
        data = response.json()

        return data
    
    def cargar_planetas(self):
        planetas_api = self.api("https://www.swapi.tech/api/planets/")
        for planet_gnrl in planetas_api["results"]:
            uid = planet_gnrl['uid']

            info_planet = self.api(planet_gnrl['url'])
            dict = info_planet['result']['properties']
            
            #Atributos del planeta
            name = dict['name']
            diameter = dict['diameter']
            rotation_period = dict['rotation_period']
            orbital_period = dict['orbital_period']
            gravity = dict['gravity']
            population = dict['population']
            climate = dict['climate']
            terrain = dict['terrain']
            surface_water = dict['surface_water']
            created = dict['created']
            edited = dict['edited']
            url = dict['url']

            #Crear objeto Planeta y agregarlo a la lista de planetas
            self.planetas.append(Planeta(uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url))


    def cargar_especies(self):
        especies_api = self.api("https://www.swapi.tech/api/species/")
        for especie_gnrl in especies_api["results"]:
            uid = especie_gnrl['uid']
            info_especie = self.api(especie_gnrl['url'])
            dict = info_especie['result']['properties']
            
            #Atributos de la especie
            name = dict['name']
            classification = dict['classification']
            designation = dict['designation']
            average_height = dict['average_height']
            average_lifespan = dict['average_lifespan']
            hair_colors = dict['hair_colors']
            skin_colors = dict['skin_colors']
            eye_colors = dict['eye_colors']
            homeworld = dict['homeworld']
            language = dict['language']
            created = dict['created']
            edited = dict['edited']
            url = dict['url']

            people = []

            for api_people in dict['people']:
                people.append(self.api(api_people)['result']['properties']['name'])

            episodes = []
            
            #Crear objeto Especie y agregarlo a la lista de especies
            self.especies.append(Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url))

    def cargar_personajes(self):
        personajes_api = self.api("https://www.swapi.tech/api/people/")
        for personaje_gnrl in personajes_api["results"]:
            uid = personaje_gnrl['uid']
            
            info_personaje = self.api(personaje_gnrl['url'])
            dict = info_personaje['result']['properties']
            
            #Atributos del personaje
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
            homeworld = self.api(dict['homeworld'])['result']['properties']['name']

            naves = []
            vehiculos = []
            episodes = []

            especie = ""

            for especie in self.especies:
                if especie.homeworld == homeworld:
                    especie = especie.name
                    especie.people.append(name)
                    break
            
            for planeta in self.planetas:
                if planeta.name == homeworld:
                    planeta.personajes.append(name)
                    break

            self.personajes.append(Personaje(uid,name,height, mass, hair_color, skin_color, eye_color, birth_year, gender, created, edited, homeworld, url, episodes, especie, naves, vehiculos))
         
    def add_films_specie(self, url, title):
        for especie in self.especies:
            if especie.url == url:
                especie.episodes.append(title)

    def add_films_planet(self, url, title):
        for planeta in self.planetas:
            if planeta.url == url:
                planeta.episodes.append(title)
    
    def add_films_personaje(self, url, title):
        for personaje in self.personajes:
            if personaje.url == url:
                personaje.episodes.append(title)

    def cargar_peliculas(self):
        peliculas_api = self.api("https://www.swapi.tech/api/films/")
        for film_gnrl in peliculas_api["result"]:
            uid = film_gnrl['uid']
            title = film_gnrl['properties']['title']
            episode_id = film_gnrl['properties']['episode_id']
            release_date = film_gnrl['properties']['release_date']
            opening_crawl = film_gnrl['properties']['opening_crawl']
            director = film_gnrl['properties']['director']

            name_film = f"Episodio {episode_id}: {title}"

            for api_especie in film_gnrl['properties']['species']:
                self.add_films_specie(api_especie, name_film)

            for api_planet in film_gnrl['properties']['planets']:
                self.add_films_planet(api_planet, name_film)

            for api_personaje in film_gnrl['properties']['characters']:
                self.add_films_personaje(api_personaje, name_film)

            #Crear objeto Pelicula y agregarlo a la lista de peliculas
            self.peliculas.append(Pelicula(uid, title, episode_id, release_date, opening_crawl, director))

    def cargar_api(self):
        print("\nEsperando...\n")
        self.cargar_planetas()
        self.cargar_personajes()
        self.cargar_especies()
        self.cargar_peliculas()
        print("\n...Api Cargada con exito")
    

    def cargar_naves(self):
        pass

    def listar_peliculas(self):
        pass

    def listar_especies(self):
        pass

    def listar_planetas(self):
        for planeta in self.planetas:
            planeta.mostrar()

    def buscar_personajes(self):
        pass

    def grafico_personajes_planetas(self):
        pass

    def graficos_naves(self):
        pass

    def estadistica_naves(self):
        pass
    def gestion_misiones(self):
        pass

    def guardar_misiones(self):
        pass

    def vaciar(self):
        pass

    def menu(self):
        print("\n")
        while True:
            print("\n==================================")
            print("BIENVENIDOS AL PROYECTO STAR WARS")
            print("=================================")
            print("1. Lista de Peliculas de la Saga\n2. Lista de las especies de seres vivos de la saga\n3. Lista de planetas\n4. Buscar Personajes\n5. Gráfico de cantidad de personajes nacidos en cada planeta\n6. Gráficos de características de naves\n7. Estadísticas sobre naves\n8. Gestion de Misiones\n9. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 8)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")

            # Realiza la acción correspondiente según la opción seleccionada
            if opcion == "1":
                self.listar_peliculas()
            elif opcion == "2":
                self.listar_especies()
            elif opcion == "3":
                self.listar_planetas()
            elif opcion == "4":
                self.buscar_personajes()
            elif opcion == "5":
                self.grafico_personajes_planetas()
            elif opcion == "6":
                self.graficos_naves()
            elif opcion == "7":
                self.estadistica_naves()
            elif opcion == "8":
                self.gestion_misiones()
            else:
                self.guardar_misiones()
                self.vaciar()
                print("\nAdiós.")
                break

    def cargar_misiones(self):
        pass

    def iniciar(self):
        self.cargar_api()

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
                self.cargar_misiones()
                self.menu()
            elif opcion == "2":
                self.menu()
            else:
                # Termina el bucle y finaliza la función
                break

        #for especie in self.especies:
        #    print(especie.show_atr())
        #    print("\n================================================")

        #for planeta in self.planetas:
        #    print(planeta.show_atr())
        #    print("\n================================================")
