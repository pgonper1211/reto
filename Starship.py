class Starship:
    def __init__(self,id,name,model,manufacturer,cost_in_credits,length,max_atmosphering_speed,crew,passengers,cargo_capacity,consumables,hyperdrive_rating,mglt,starship_class,pilots,films):
        self.id = id
        self.name = name
        self.model = model
        self.manufacturer = manufacturer
        self.cost_in_credits = cost_in_credits
        self.max_atmosphering_speed = max_atmosphering_speed
        self.length = length
        self.crew = crew
        self.passengers = passengers
        self.cargo_capacity = cargo_capacity
        self.consumables = consumables
        self.hyperdrive_rating = hyperdrive_rating
        self.mglt = mglt
        self.starship_class = starship_class
        self.pilots = pilots
        self.films = films


    def pilots_str(self):
        if len(self.pilots) > 0:
            piloto_str = "Pilotos:\n"
            for piloto in self.pilots:
                piloto_str += f"- {piloto.name}\n"
            
            return piloto_str
        else:
            return "Esta nave espacial no tiene pilotos asociados."
    

    def films_str(self):
        if len(self.films) > 0:
            film_str = "Films en los que aparece:\n"
            for film in self.films:
                film_str += f"- {film.title}\n"
            
            return film_str
        else:
            return "Esta nave espacial no aparece en ningún film."


    
    def show_atr(self):
        return f"ID: {self.id}\nNombre: {self.name}\nModelo: {self.model}\nFabricante: {self.manufacturer}\nCosto en créditos: {self.cost_in_credits}\nLongitud: {self.length} metros\nPasajeros: {self.passengers}\nCapacidad de carga: {self.cargo_capacity}\nVelocidad máxima de atmósfera: {self.max_atmosphering_speed}\nConsumibles: {self.consumables}\nRating del hiperdrive: {self.hyperdrive_rating}\nMGLT: {self.mglt}\nClase de nave espacial: {self.starship_class}\n{self.pilots_str()}\n{self.films_str()}\n"

