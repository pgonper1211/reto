class Planeta:
    def __init__(self, uid, name, diameter, rotation_period, orbital_period, gravity, population, climate, terrain, surface_water, created, edited, url):
        self.uid = uid
        self.name = name
        self.diameter = diameter
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.gravity = gravity
        self.population = population
        self.climate = climate
        self.terrain = terrain
        self.surface_water = surface_water
        self.created = created
        self.edited = edited
        self.url = url
        self.episodes = []
        self.personajes = []

    def episodes_str(self):
        if len(self.episodes) != 0:
            episodes_string = "Lista de episodios donde aparece el planeta:\n\n"
            for episode in self.episodes:
                episodes_string += f"-{episode.name_film()}\n" 
            
            return episodes_string
        else:
            return "Este planeta no tiene episodios relacionados."
    
    def personajes_str(self):
        if len(self.personajes) != 0:
            personajes_string = "Lista de personajes de este planeta:\n\n"
            for personaje in self.personajes:
                personajes_string += f"-{personaje.name}\n" 
            
            return personajes_string
        else:
            return "Este planeta no tiene personajes relacionados."

    
    def show_atr(self):
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
        """
    
    def mostrar(self):
        print(f"""
        - Nombre: {self.name}
        - Período de rotación: {self.rotation_period} días
        - Período orbital: {self.orbital_period} días
        - Población: {self.population}
        - Clima: {self.climate}
        - URL: {self.url}
        {self.episodes_str()}
        {self.personajes_str()}
        """)
        
