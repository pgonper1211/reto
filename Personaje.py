class Personaje:
    def __init__(self, uid, name, height, mass,hair_color, skin_color, eye_color, birth_year, gender, created, edited, homeworld, url, episodes, specie, naves, vehiculos):
        self.uid = uid
        self.name = name
        self.height = height
        self.mass = mass
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.eye_color = eye_color
        self.birth_year = birth_year
        self.gender = gender
        self.created = created
        self.edited = edited
        self.homeworld = homeworld
        self.url = url
        self.episodes = episodes
        self.specie = specie
        self.naves = naves
        self.vehiculos = vehiculos

    def set_specie(self, specie):
        self.specie = specie
        

    def episodes_str(self):
        if len(self.episodes)!= 0:
            episodes_string = "Episodios en los que aparece este personaje:\n\n"
            for episode in self.episodes:
                episodes_string += f"-{episode.name_film()}\n"
            
            return episodes_string
        else:
            return "Este personaje no tiene episodios relacionados."
        
    def naves_str(self):
        if len(self.naves)!= 0:
            naves_string = "Naves en las que aparece este personaje:\n\n"
            for nave in self.naves:
                naves_string += f"-{nave}\n"
            
            return naves_string
        else:
            return "Este personaje no aparece en naves."
    
    def vehiculos_str(self):
        if len(self.vehiculos)!= 0:
            vehiculos_string = "Vehículos en los que aparece este personaje:\n\n"
            for vehiculo in self.vehiculos:
                vehiculos_string += f"-{vehiculo}\n"
            
            return vehiculos_string
        else:
            return "Este personaje no aparece en vehículos."

    def show_atr(self):
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
        """
    
    def especie_str(self):
        if self.specie == None:
            return "Unknown"
        else:
            return self.specie.name
    
    def mostrar(self):
        print(f"""
        - Nombre: {self.name}
        - Género: {self.gender}
        - Planeta de origen: {self.homeworld.name}
        - Especie: {self.especie_str()}
        {self.episodes_str()}
        {self.naves_str()}
        {self.vehiculos_str()}
        """)
    
    
    