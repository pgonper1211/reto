import requests
import csv
import matplotlib as plt
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
    def __init__(self):
        self.especies = []
        self.misiones = []
        self.naves = []
        self.peliculas = []
        self.planetas = []
        self.personajes = []
        self.armas = []
        self.vehiculos = []

####################################################################################################################

    # CARGAR API
    
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


                especie = Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url)

                # Crear objeto Especie y agregarlo a la lista de especies
                self.especies.append(especie)
            url = especies_api.get("next")

    def buscar_especie_planeta(self, planeta):
        for especie in self.especies:
            if especie.homeworld.name == planeta.name:
                return especie
        return None

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
                especie = self.buscar_especie_planeta(homeworld)
                
                personaje = Personaje(uid, name, height, mass,hair_color, skin_color, eye_color, birth_year, gender, created, edited, homeworld, url, episodes, especie, naves, vehiculos)

                
                for esp in self.especies:
                    if esp.homeworld.url == dict['homeworld']:
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
        self.cargar_especies_api()
        self.cargar_personajes_api()
        self.cargar_peliculas_api()
####################################################################################################################

    # CARGAR CSV

    def cargar_films_csv(self):
        with open('csv/films.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                title = row[1]
                episode_id = row[0]
                uid = row[0]
                release_date = row[2]
                opening_crawl = row[4]
                director = row[3]

                # Crear objeto Pelicula y agregarlo a la lista de peliculas
                self.peliculas.append(Pelicula(uid, title, episode_id, release_date, opening_crawl, director))

    def buscar_planeta_nombre(self, nombre):
        for planeta in self.planetas:
            if planeta.name == nombre:
                return planeta
        return None
    
    def buscar_especie_nombre(self, nombre):
        for especie in self.especies:
            if especie.name == nombre:
                return especie
        return None
    
    def cargar_characters_csv(self):
        uids_nombres_existentes = {(personaje.uid, personaje.name) for personaje in self.personajes}
        
        with open('csv/characters.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el id y el name ya están en la lista
                if (uid, name) not in uids_nombres_existentes:
                    # Atributos de la especie usando índices de columnas
                    specie = row[2]
                    gender = row[3]
                    height = row[4]
                    mass = row[5]
                    hair_color = row[6]
                    eye_color = row[7]
                    skin_color = row[8]
                    year_born = row[9]
                    homeworld = self.buscar_planeta_nombre(row[10])
                    created, edited, url = None, None, None
                    episodes, naves, vehiculos = [], [], []
                    
                
                    # Crear un objeto Especie y añadirlo a la lista
                    personaje = Personaje(uid, name, height, mass, hair_color, skin_color, eye_color, year_born, gender, created, edited, homeworld, url, episodes, specie, naves, vehiculos)

                    self.personajes.append(personaje)

                    # Actualizar la lista de uids y nombres existentes
                    uids_nombres_existentes.add((uid, name))

    def buscar_especie_droid(self):
        for especie in self.especies:
            if especie.name == "Droid":
                return especie
            
    def buscar_film_nombre(self, nombres_str, films):
        nombres = nombres_str.split(",")
        for pelicula in self.peliculas:
            for nombre in nombres:
                if pelicula.title == nombre:
                    films.append(pelicula)
                    break     
        
        return films
    
    def cargar_droids_csv(self):
        uids_nombres_existentes = {(personaje.uid, personaje.name) for personaje in self.personajes}
        
        with open('csv/droids.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el id y el name ya están en la lista
                if (uid, name) not in uids_nombres_existentes:
                    # Atributos de la especie usando índices de columnas
                    specie = self.buscar_especie_droid()
                    model = row[2]
                    manufacturer = row[3]
                    height = row[4]
                    mass = row[5]
                    sensor_color = row[6]
                    plating_color = row[7]
                    primary_function = row[8]
                    nombres_str = row[9]
                    films = []
                    self.buscar_film_nombre(nombres_str, films)

                    # Crear un objeto Especie y añadirlo a la lista
                    droid = Droid(uid, name, specie, model, manufacturer, height,mass, sensor_color, plating_color, primary_function, films)

                    self.personajes.append(droid)

                    # Actualizar la lista de uids y nombres existentes
                    uids_nombres_existentes.add((uid, name))
        
    def cargar_personajes_csv(self):
        self.cargar_characters_csv()
        self.cargar_droids_csv()


    def nombres_a_personajes(self, nombres_str):
        personajes = []
        nombres = nombres_str.split(",")

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre:
                    personajes.append(personaje)
                    break    
        
        return personajes
    
    def titulos_a_films(self, film_str):
        films = []
        nombres = film_str.split(",")
        
        for nombre in nombres:
            for pelicula in self.peliculas:
                if pelicula.title == nombre:
                    films.append(pelicula)
                    break

        return films
            

    def cargar_planetas_csv(self):
        uids_nombres_existentes = {(planeta.uid, planeta.name) for planeta in self.planetas}
        
        with open('csv/species.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el id y el name ya están en la lista
                if (uid, name) not in uids_nombres_existentes:
                    # Atributos de la especie usando índices de columnas
                    diameter = row[2]
                    rotation_period = row[3]
                    orbital_period = row[4]
                    gravity = row[5]
                    population = row[6]
                    climate = row[7]
                    terrain = row[8]
                    surface_water = row[9]
                    residents = row[10]
                    films_str = row[11]
                    created, edited, url = None, None, None
                    
                    people = self.nombres_a_personajes(residents)

                    # Crear un objeto Especie y añadirlo a la lista
                    planeta = Planeta(uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url)

                    planeta.personajes = people

                    planeta.films = self.titulos_a_films(films_str)


                    self.planetas.append(planeta)

                    # Actualizar la lista de uids y nombres existentes
                    uids_nombres_existentes.add((uid, name))

    def personaje_en_especie(self, nombre_especie, personajes):
        for personaje in self.personajes:
            if isinstance(personaje.specie, Especie) and personaje.specie.name == nombre_especie:
                personajes.append(personaje)
        
        return personajes
    
    def asignar_especies_a_personajes(self):
        for personaje in self.personajes:
            if type(personaje.specie) is str:
                personaje.specie = self.buscar_especie_nombre(personaje.specie)
        
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

                    self.personaje_en_especie(name, people)
                    
                    # Crear un objeto Especie y añadirlo a la lista
                    especie = Especie(uid, name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url)
                    self.especies.append(especie)

                    # Actualizar la lista de uids y nombres existentes
                    uids_nombres_existentes.add((uid, name))
        
        self.asignar_especies_a_personajes()
        

    def cargar_naves_csv(self):
        
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
                crew = row[6]
                passengers = row[7]
                cargo_capacity = row[8]
                consumables = row[9]
                hyperdrive_rating = row[10]
                mglt = row[11]
                starship_class = row[12]
                pilots = self.nombres_a_personajes(row[13])
                films = self.titulos_a_films(row[14])
                    
                # Crear un objeto Especie y añadirlo a la lista
                nave = Starship(id, name, model, manufacturer, cost_in_credits, length, crew, passengers, cargo_capacity, consumables, hyperdrive_rating, mglt, starship_class, pilots, films)
                
                self.naves.append(nave)

    def cargar_vehiculos_csv(self):
        
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
                pilots = self.nombres_a_personajes(row[12])
                films = self.titulos_a_films(row[13])
                    
                # Crear un objeto Especie y añadirlo a la lista
                vehiculo = Vehicle(id, name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, vehicle_class, pilots, films)
                
                self.vehiculos.append(vehiculo)

    def cargar_armas_csv(self):
        
        
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
                films = self.titulos_a_films(row[8])
                    
                # Crear un objeto Especie y añadirlo a la lista
                arma = Weapon(id,name,model,manufacturer,cost_in_credits,length,type,description,films)
                
                self.armas.append(arma)

    def cargar_csv(self):
        self.cargar_films_csv()
        self.cargar_personajes_csv()
        self.cargar_especies_csv()
        self.cargar_naves_csv()
        self.cargar_vehiculos_csv()
        self.cargar_armas_csv()
        
####################################################################################################################

    #FUNCION PRINCIPAL DE CARGA

    #CARGAR API Y LUEGO CSV
    def cargar(self):
        print("\nEsperando...\n")
        self.cargar_api()
        self.cargar_csv()
        print("\n...Carga exitosa")

####################################################################################################################

    #FUNCIONALIDADES RELACIONADAS A LA API

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

####################################################################################################################

    # FUNCIONALIDADES DE GRAFICOS Y ESTADISTICAS

    def grafico_misiones_peliculas(self):
        pass

    def grafico_personajes_planetas(self):
        planetas_con_episodios = [planeta for planeta in self.planetas if len(planeta.episodes) > 0]

        personajes_por_planeta = defaultdict(int)

        for personaje in self.personajes:
            for planeta in planetas_con_episodios:
                if personaje.homeworld.name == planeta.name:
                    personajes_por_planeta[planeta.name] += 1

        print(personajes_por_planeta)


    def graficos_naves(self):
        pass

    def estadistica_naves(self):
        pass

####################################################################################################################

    #FUNCIONALIDADES DE MISIONES

    def elegir_planeta(self):
        print("\n============================================")
        print("           PLANETAS DISPONIBLES")
        print("============================================")
        
        count = 1
        # Imprime la lista de personajes  encontrados numerados
        for planeta in self.planetas:
            print(f"{count}. {planeta.name}")
            count += 1

        opcion_planeta = input("\nIngrese el numero de planeta donde desea realizar la mision: ")
        while (not opcion_planeta.isnumeric()) or (not int(opcion_planeta) in range(1, len(self.planetas) + 1)):
            print("Error!!! Dato Inválido.")
            opcion_planeta = input("\nIngrese el numero de planeta donde desea realizar la mision: ")
        
        index = int(opcion_planeta) - 1
        
        planeta = self.planetas[index]

        return planeta

    def elegir_nave(self):
        print("\n============================================")
        print("             NAVES DISPONIBLES")
        print("============================================")
        
        count = 1
        # Imprime la lista de personajes  encontrados numerados
        for nave in self.naves:
            print(f"{count}. {nave.name}")
            count += 1 

        opcion_nave = input("\nIngrese el numero de nave que desea utilizar: ")
        while (not opcion_nave.isnumeric()) or (not int(opcion_nave) in range(1, len(self.naves) + 1)):
            print("Error!!! Dato Inválido.")
            opcion_nave = input("\nIngrese el numero de nave que desea utilizar: ")
        
        index = int(opcion_nave) - 1
        
        nave = self.naves[index]

        return nave
    

    def elegir_armas(self):
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
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
            if opcion == "1":
                opcion_armas = input("\nIngrese el numero de arma que desea agreagar a la mision: ")
                while (not opcion_armas.isnumeric()) or (not int(opcion_armas) in range(1, len(self.armas)+1)):
                    print("Error!!! Dato Inválido.")
                    opcion_armas = input("\nIngrese el numero de arma que desea agreagar a la mision: ")
                
                index = int(opcion_armas) - 1

                arma = self.armas[index]

                armas.append(arma)        
            else:
                break
        
        return armas
    

    def elegir_integrantes(self):
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
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
            if opcion == "1":
                opcion_integrante = input("\nIngrese el numero de integrante que desea agreagar a la mision: ")
                while (not opcion_integrante.isnumeric()) or (not int(opcion_integrante) in range(1, len(self.personajes)+1)):
                    print("Error!!! Dato Inválido.")
                    opcion_integrante = input("\nIngrese el numero de integrante que desea agreagar a la mision: ")
                
                index = int(opcion_integrante) - 1

                integrante = self.personajes[index]

                integrantes.append(integrante)        
            else:
                break
        
        return integrantes

    def crear_mision(self):
        if len(self.misiones) < 5:
            print("\nIngrese los detalles de la mision:")
            nombre = input("Ingrese el nombre: ")
            planeta = self.elegir_planeta()
            nave = self.elegir_nave()
            armas = self.elegir_armas()
            integrantes = self.elegir_integrantes()

            mision = Mision(nombre, planeta, nave, armas, integrantes)
            
            self.misiones.append(mision)
            print("\nMision creada exitosamente.\n")
        else:
            print("\nNo se puede crear más de 5 misiones.")

    def modificar_mision(self):
        print("\n============================================")
        print("            MODIFICAR MISIONES")
        print("============================================")

        count = 1
        
        for mision in self.misiones:
            print(f"{count}. {mision.name}")
            count += 1


        while True:
            print("\n1. Ver detalle de una mision\n2. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
            if opcion == "1":
                opcion_mision = input("\nIngrese el numero de la mision para visualizar sus detalles: ")
                while (not opcion_mision.isnumeric()) or (not int(opcion_mision) in range(1, len(self.misiones)+1)):
                    print("Error!!! Dato Inválido.")
                    opcion_mision = input("\nIngrese el numero de la mision para visualizar sus detalles: ")
                
                index = int(opcion_mision) - 1

                print(self.personajes[index].show_atr())      
            else:
                break 


    def visualizar_mision(self):
        print("\n============================================")
        print("            VISUALIZAR MISIONES")
        print("============================================")

        count = 1
        
        for mision in self.misiones:
            print(f"{count}. {mision.nombre}")
            count += 1


        while True:
            print("\n1. Ver detalle de una mision\n2. Salir")
            
            # Solicita al usuario que ingrese una opción y valida que sea un número válido
            opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                print("Error!!! Dato Inválido.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                
            if opcion == "1":
                opcion_mision = input("\nIngrese el numero de la mision para visualizar sus detalles: ")
                while (not opcion_mision.isnumeric()) or (not int(opcion_mision) in range(1, len(self.misiones)+1)):
                    print("Error!!! Dato Inválido.")
                    opcion_mision = input("\nIngrese el numero de la mision para visualizar sus detalles: ")
                
                index = int(opcion_mision) - 1

                print(self.personajes[index].show_atr())      
            else:
                break 
    
    def gestion_misiones(self):
        print("\n")
        while True:
            print("\n============================================")
            print("BIENVENIDOS AL MODULO DE GESTION DE MISIONES")
            print("============================================")
            print("1. Crear Mision\n2. Modificar Misiones\n3. Visualizar Mision\n4. Salir")
            
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
                print("Has salido del modulo de gestio de misiones.")
                break

####################################################################################################################

    #FUNCIONALIDADES GENERALES

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