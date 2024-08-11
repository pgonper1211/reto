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
        uids_nombres_existentes = {personaje.name for personaje in self.personajes}
        
        with open('csv/characters.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el id y el name ya están en la lista
                if name not in uids_nombres_existentes:
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
    
    def buscar_nombre_personajes(self, nombres, nombre_nuevo):
        for nombre in nombres:
            if nombre == nombre_nuevo:
                return True
        return False
    
    def cargar_droids_csv(self):
        uids_nombres_existentes = [personaje.name for personaje in self.personajes]
        
        with open('csv/droids.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la primera fila de encabezados
            for row in reader:
                uid = row[0]
                name = row[1]
                
                # Verificar si el id y el name ya están en la lista
                if not self.buscar_nombre_personajes(uids_nombres_existentes, name):
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
                    uids_nombres_existentes.append(name)

        
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

    def guardar_hyperdrive_rating(self, hyperdrive):   
        if hyperdrive == "":
            hyperdrive = 0.0
            return hyperdrive
        else:
            return hyperdrive
        

    def nave_piloto(self, nave, nombres_str):
        nombres = nombres_str.split(",")

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre:
                    personaje.naves.append(nave)
                    break
            

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
                max_atmosphering_speed = row[6]
                crew = row[7]
                passengers = row[8]
                cargo_capacity = row[9]
                consumables = row[10]
                hyperdrive_rating = self.guardar_hyperdrive_rating(row[11])
                mglt = row[12]
                starship_class = row[13]
                pilots = self.nombres_a_personajes(row[14])
                films = self.titulos_a_films(row[15])

                
                    
                # Crear un objeto Especie y añadirlo a la lista
                nave = Starship(id,name,model,manufacturer,cost_in_credits,length,max_atmosphering_speed,crew,passengers,cargo_capacity,consumables,hyperdrive_rating,mglt,starship_class,pilots, films)

                self.nave_piloto(nave, row[14])

                self.naves.append(nave)

    
    def personajes_vehiculos(self, nombres_str, vehiculo):
        nombres = nombres_str.split(",")

        for nombre in nombres:
            for personaje in self.personajes:
                if personaje.name == nombre:
                    personaje.vehiculos.append(vehiculo)
                    break

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

                self.personajes_vehiculos(row[12], vehiculo)
                
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

    def borrar_personajes_repetidos(self):
        personajes_unicos = []
        nombres_encontrados = set()

        for personaje in self.personajes:
            if personaje.name not in nombres_encontrados:
                personajes_unicos.append(personaje)
                nombres_encontrados.add(personaje.name)
        
        self.personajes = personajes_unicos
           
    #CARGAR API Y LUEGO CSV
    def cargar(self):
        print("\nEsperando...\n")
        self.cargar_api()
        self.cargar_csv()
        self.borrar_personajes_repetidos()
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
            print(personaje.name)
            print("")
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

###################################################################################################################

    # FUNCIONALIDADES DE GRAFICOS Y ESTADISTICAS

    def grafico_personajes_planetas(self):
        # Filtra planetas que tienen episodios
        planetas_con_episodios = [planeta for planeta in self.planetas if len(planeta.episodes) > 0]

        # Inicializar el defaultdict con un valor inicial para 'Unknown'
        personajes_por_planeta = defaultdict(int)
        personajes_por_planeta['Unknown'] = 0

        # Contar personajes por planeta
        for personaje in self.personajes:
            if isinstance(personaje, Personaje):
                if personaje.homeworld is None:
                    personajes_por_planeta['Unknown'] += 1
                else:
                    for planeta in planetas_con_episodios:
                        if personaje.homeworld.name == planeta.name:
                            personajes_por_planeta[planeta.name] += 1

        # Preparar datos para el gráfico
        planeta_names = list(personajes_por_planeta.keys())
        counts = list(personajes_por_planeta.values())

        # Crear el gráfico
        plt.figure(figsize=(80, 5))
        plt.bar(planeta_names, counts, color='skyblue')
        plt.xlabel('Planetas')
        plt.ylabel('Número de Personajes')
        plt.title('Número de personajes nacidos en cada planeta')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def graficos_naves(self):
        # Preparar los datos
        nombres = [nave.name for nave in self.naves]
        longitudes = [float(nave.length) if nave.length else 0 for nave in self.naves]
        capacidades_carga = [float(nave.cargo_capacity) if nave.cargo_capacity else 0 for nave in self.naves]
        
        clasificaciones_hiperimpulsor = []
        for nave in self.naves:
            if nave.hyperdrive_rating is not None:
                clasificaciones_hiperimpulsor.append(float(nave.hyperdrive_rating))

        mglt = [float(nave.mglt) if nave.mglt else 0 for nave in self.naves]

        while True:
            # Menú de opciones
            print("\nSeleccione el gráfico que desea ver:\n1. Longitud de la nave\n2. Capacidad de carga\n3. Clasificación de hiperimpulsor\n4. MGLT (Modern Galactic Light Time)\n5. Salir")

            opcion = input("Ingrese el número de la opción deseada: ")
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 6)):
                print("Error!!! Dato Inválido.")
                opcion = input("Ingrese el número de la opción deseada: ")

            # Mostrar el gráfico correspondiente o salir
            if opcion == '1':
                plt.figure(figsize=(15, 7))  # Tamaño más razonable
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
                break

            plt.xticks(rotation=90, fontsize=12)
            plt.yticks(fontsize=12)
            plt.tight_layout()
            plt.show()

    def estadistica_naves(self):
        # Preparar los datos
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
                if v in frecuencia:
                    frecuencia[v] += 1
                else:
                    frecuencia[v] = 1
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


    def agregar_armas(self, armas):
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
        else:
            print("\nNo se puede agregar más de 7 armas.")

    def eliminar_armas(self, armas):

        if len(armas) > 0:
        
            count = 1
            for arma in armas:
                print(f"{count}. {arma.name}")
                count += 1

            while armas > 0:
                print("\n1. Eliminar Arma\n2. Salir")
                    
                # Solicita al usuario que ingrese una opción y valida que sea un número válido
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                        
                if opcion == "1":
                    opcion_armas = input("\nIngrese el numero de arma que desea eliminar de la mision: ")
                    while (not opcion_armas.isnumeric()) or (not int(opcion_armas) in range(1, len(armas)+1)):
                        print("Error!!! Dato Inválido.")
                        opcion_armas = input("\nIngrese el numero de arma que desea eliminar de la mision: ")
                    
                    index = int(opcion_armas) - 1

                    armas.pop(index)       
                else:
                    break
        else:
            print("\nNo hay armas para eliminar.")
        

    def agregar_integrantes(self, integrantes):
        
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

        else:
            print("\nNo se puede agregar más de 7 integrantes.")

    def eliminar_integrantes(self, integrantes):
            
        if len(integrantes) > 0:
            count = 1
                
            for personaje in integrantes:
                print(f"{count}. {personaje.name}")
                count += 1

            while len(integrantes) < 7:
                print("\n1. Eliminar Integrante\n2. Salir")
                
                # Solicita al usuario que ingrese una opción y valida que sea un número válido
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                while (not opcion.isnumeric()) or (not int(opcion) in range(1, 3)):
                    print("Error!!! Dato Inválido.")
                    opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
                    
                if opcion == "1":
                    opcion_integrante = input("\nIngrese el numero de integrante que desea eliminar de la mision: ")
                    while (not opcion_integrante.isnumeric()) or (not int(opcion_integrante) in range(1, len(integrantes)+1)):
                        print("Error!!! Dato Inválido.")
                        opcion_integrante = input("\nIngrese el numero de integrante que desea eliminar de la mision: ")
                    
                    index = int(opcion_integrante) - 1
                    integrantes.pop(index)        
                else:
                    break 
        else:
            print("\nNo hay integrantes para eliminar.")


    def modificar_mision(self):
        print("\n============================================")
        print("            MODIFICAR MISIONES")
        print("============================================")

        count = 1
        
        for mision in self.misiones:
            print(f"{count}. {mision.nombre}")
            count += 1

        opcion_mision = input("\nIngrese el numero de la mision que desea modificar: ")
        while (not opcion_mision.isnumeric()) or (not int(opcion_mision) in range(1, len(self.misiones)+1)):
            print("Error!!! Dato Inválido.")
            opcion_mision = input("\nIngrese el numero de la mision que desea modificar: ")
        
        index = int(opcion_mision) - 1
        
        mision_modif = self.misiones[index]

        while True:
            print("\nQue caracteristica deseas modificar?\n1. Nombre\n2. Planeta\n3. Nave\n4. Armas\n5. Integrantes\n6. Salir")

            opcion_modificacion = input("\nIngrese el numero de la acción que desea realizar: ")
            while (not opcion_modificacion.isnumeric()) or (not int(opcion_modificacion) in range(1, 7)):
                print("Error!!! Dato Inválido.")
                opcion_modificacion = input("\nIngrese el numero de la acción que desea realizar: ")

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
            
        print("\nMision modificada exitosamente.\n")


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

                print(self.misiones[index].show_atr())      
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

#################################################################################################################

    #FUNCIONALIDADES GENERALES

    def guardar_misiones(self):
        with open("misiones.txt", 'w') as file:
            for mision in self.misiones:
                file.write(mision.convert_str() + "\n")

    def vaciar(self):
        """
        Vacía las listas de la instancia de la clase, eliminando todos los datos almacenados.
        """
        self.misiones = []
        
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


    def nombres_a_armas(self, nombres_str):
        armas = []
        nombres = nombres_str.split(",")

        for nombre in nombres:
            for arma in self.armas:
                if arma.name == nombre:
                    armas.append(arma)
                    break    
        
        return armas
    

    def nombre_a_nave(self, nombre):
        for nave in self.naves:
            if nave.name == nombre:
                return nave
            

    def nombres_a_personajes2(self, nombres_str):
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