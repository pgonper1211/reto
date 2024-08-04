class Especie:
    def __init__(self, uid,name, classification, designation, average_height, average_lifespan, hair_colors, skin_colors, eye_colors, homeworld, language, created, edited, people, episodes, url):
        self.uid = uid
        self.name = name
        self.classification = classification
        self.designation = designation
        self.average_height = average_height
        self.average_lifespan = average_lifespan
        self.hair_colors = hair_colors
        self.skin_colors = skin_colors
        self.eye_colors = eye_colors
        self.homeworld = homeworld
        self.language = language
        self.created = created
        self.edited = edited
        self.url = url
        self.people = people
        self.episodes = episodes
    
    def personajes_str(self):
        if len(self.people) != 0:
            personajes_string = "\nPersonajes relacionados con esta especie:\n\n"
            for personaje in self.people:
                personajes_string += f"-{personaje}\n" 
            
            return personajes_string
        else:
            return "Esta especie no tiene personajes relacionados."
    
    def episoder_str(self):
        if len(self.episodes) != 0:
            episodios_string = "Episodios relacionados con esta especie:\n\n"
            for episodio in self.episodes:
                episodios_string += f"-{episodio}\n" 
            
            return episodios_string
        else:
            return "Esta especie no tiene episodios relacionados."
    
    def show_atr(self):
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
            Edit: {self.edited}
            URL: {self.url}
                        {self.personajes_str()}
                        {self.episoder_str()}    
            """
        
