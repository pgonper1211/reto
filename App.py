import requests
import csv
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
        self.armas = []
    
    def api(self, url):
        response = requests.get(url)
        data = response.json()
        return data

    def cargar_planetas_api(self):
        url = "https://www.swapi.tech/api/planets"
        while url:
            planetas_api = self.api(url)
            for planet_gnrl in planetas_api["results"]:
                uid = planet_gnrl['uid']
                
                info_planet = self.api(planet_gnrl['url'])
                dict = info_planet['result']['properties']
                
                # Atributos del planeta
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

                # Crear objeto Planeta y agregarlo a la lista de planetas
                self.planetas.append(Planeta(uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url))
            url = planetas_api.get("next")
    

    def buscar_planet_url(self, url):
        for planeta in self.planetas:
            if planeta.url == url:
                return planeta
        return None


    def cargar_especies_api(self):
        url = "https://www.swapi.tech/api/species"
        while url:
            especies_api = self.api(url)
            for especie_gnrl in especies_api["results"]:
                uid = especie_gnrl['uid']
                info_especie = self.api(especie_gnrl['url'])
                dict = info_especie['result']['properties']
                
                # Atributos de la especie
                name = dict['name']
                classification = dict['classification']
                designation = dict['designation']
                average_height = dict['average_height']
                average_lifespan = dict['average_lifespan']
                hair_colors = dict['hair_colors']
                skin_colors = dict['skin_colors']
                eye_colors = dict['eye_colors']
                homeworld =  self.buscar_planet_url(dict['homeworld'])
                language = dict['language']
                created = dict['created']
                edited = dict['edited']
                url = dict['url']

                people = []
                episodes = []

                # Crear objeto Especie y agregarlo a la lista de especies
                self.especies.append(Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url))
            url = especies_api.get("next")

    def cargar_personajes_api(self):
        url = "https://www.swapi.tech/api/people"
        while url:
            personajes_api = self.api(url)
            for personaje_gnrl in personajes_api["results"]:
                uid = personaje_gnrl['uid']
                info_personaje = self.api(personaje_gnrl['url'])
                dict = info_personaje['result']['properties']
                
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
                homeworld = self.buscar_planet_url(dict['homeworld'])

                naves = []
                vehiculos = []
                episodes = []
                especie = None

                for esp in self.especies:
                    if esp.homeworld == dict['homeworld']:
                        especie = esp
                        esp.people.append(name)
                        break
                
                personaje = Personaje(uid, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, created, edited, homeworld, url, episodes, especie, naves, vehiculos)

                for esp in self.especies:
                    if esp.homeworld == dict['homeworld']:
                        esp.people.append(personaje)
                        break

                for planeta in self.planetas:
                    if planeta.url == dict['homeworld']:
                        planeta.personajes.append(personaje)
                        break
                
                self.personajes.append(personaje)


            url = personajes_api.get("next")
         
    def add_films_specie(self, url, pelicula):
        for especie in self.especies:
            if especie.url == url:
                especie.episodes.append(pelicula)

    def add_films_planet(self, url, pelicula):
        for planeta in self.planetas:
            if planeta.url == url:
                planeta.episodes.append(pelicula)
    
    def add_films_personaje(self, url, pelicula):
        for personaje in self.personajes:
            if personaje.url == url:
                personaje.episodes.append(pelicula)

    def cargar_peliculas_api(self):
        peliculas_api = self.api("https://www.swapi.tech/api/films/")
        for film_gnrl in peliculas_api["result"]:
            uid = film_gnrl['uid']
            title = film_gnrl['properties']['title']
            episode_id = film_gnrl['properties']['episode_id']
            release_date = film_gnrl['properties']['release_date']
            opening_crawl = film_gnrl['properties']['opening_crawl']
            director = film_gnrl['properties']['director']

            pelicula = Pelicula(uid, title, episode_id, release_date, opening_crawl, director)

            for api_especie in film_gnrl['properties']['species']:
                self.add_films_specie(api_especie, pelicula)

            for api_planet in film_gnrl['properties']['planets']:
                self.add_films_planet(api_planet, pelicula)

            for api_personaje in film_gnrl['properties']['characters']:
                self.add_films_personaje(api_personaje, pelicula)

            # Crear objeto Pelicula y agregarlo a la lista de peliculas
            self.peliculas.append(pelicula)

    def cargar_api(self):
        self.cargar_planetas_api()
        self.cargar_personajes_api()
        self.cargar_especies_api()
        self.cargar_peliculas_api()
        

    def cargar_especies_csv(self):
        uids_nombres_existentes = {(especie.uid, especie.name) for especie in self.especies}
        
        with open('csv/species.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el id y el name ya están en la lista
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
                    created, edited, url = None, None, None
                    people, episodes = [], []

                    # Crear un objeto Especie y añadirlo a la lista
                    especie = Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url)
                    self.especies.append(especie)

                    # Actualizar la lista de uids y nombres existentes
                    uids_nombres_existentes.add((uid, name))

    def cargar_naves_csv(self):
        pass

    def cargar_csv(self):
        pass

    def cargar(self):
        print("\nEsperando...\n")
        self.cargar_api()
        self.cargar_csv()
        print("\n...Carga exitosa")

    def listar_peliculas(self):
        for pelicula in self.peliculas:
            print(pelicula.show_atr())

    def listar_especies(self):
        for especie in self.especies:
            especie.mostrar()

    def listar_planetas(self):
        for planeta in self.planetas:
            planeta.mostrar()

    def buscar_personajes(self):
        nombre = input("\nIngresa el nombre del personaje: ").lower()

        resultadoPersonajes = []

        # Busca en la lista de personajes aquellos que contienen el nombre ingresado
        for personaje in self.personajes:
            if nombre in personaje.name.lower():
                resultadoPersonajes.append(personaje)
        
        if len(resultadoPersonajes) != 0:
            print("\n")
            count = 1
            # Imprime la lista de personajes  encontrados numerados
            for personaje in resultadoPersonajes:
                print(f"{count}. {personaje.name()}")
                print("\n")
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
                    resultadoPersonajes[index].mostrar()
                else:
                    # Si se selecciona la opción de salir, termina el bucle
                    break
        else:
            # Si no se encuentran personajes con el nombre ingresado, muestra un mensaje de error
            print("\nNo se encontraron personajes con el nombre ingresado.")

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
        """
        Vacía las listas de la instancia de la clase, eliminando todos los datos almacenados.
        """
        self.especies = []
        self.misiones = []
        self.naves = []
        self.peliculas = []
        self.planetas = []
        self.personajes = []
        self.armas = []
        
    def menu(self):
        print("\n")
        while True:
            print("\n==================================")
            print("BIENVENIDOS AL PROYECTO STAR WARS")
            print("=================================")
            print("1. Lista de Peliculas de la Saga\n2. Lista de las especies de seres vivos de la saga\n3. Lista de planetas\n4. Buscar Personajes\n5. Gráfico de cantidad de personajes nacidos en cada planeta\n6. Gráficos de características de naves\n7. Estadísticas sobre naves\n8. Gestion de Misiones\n9. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 10)):
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
        self.cargar()

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