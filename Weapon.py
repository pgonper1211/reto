class Weapon:
    def __init__(self, id, name, model, manufacturer, cost_in_credits, length, type, description, films):
        self.id = id
        self.name = name
        self.model = model
        self.manufacturer = manufacturer
        self.cost_in_credits = cost_in_credits
        self.length = length
        self.type = type
        self.description = description
        self.films = films

    def films_str(self):
        if len(self.films) > 0:
            film_str = "Films en los que aparece:\n"
            for film in self.films:
                film_str += f"- {film.title}\n"
            
            return film_str
        else:
            return "Este vehiculo no aparece en ningún film."
    
    def show_atr(self):
        return f"ID: {self.id}\nNombre: {self.name}\nModelo: {self.model}\nFabricante: {self.manufacturer}\nCosto en créditos: {self.cost_in_credits}\nLongitud: {self.length}\nTipo: {self.type}\nDescripción: {self.description}\n{self.films_str()}\n"