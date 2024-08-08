class Droid:
    def __init__(self, uid, name, specie, modelo, manufacturer, height, mass, sensor_color, plating_color, primary_function, films):
        self.uid = uid
        self.name = name
        self.specie = specie
        self.modelo = modelo
        self.manufacturer = manufacturer
        self.height = height
        self.mass = mass
        self.sensor_color = sensor_color
        self.plating_color = plating_color
        self.primary_function = primary_function
        self.films = films

    def films_str(self):
        if len(self.films) > 0:
            films_string = "Films en los que aparece:\n\n"
            for film in self.films:
                films_string += f"- {film.title}\n"
            
            return films_string
        else:
            return "Este droid no aparece en ningún film."

    def mostrar(self):
        return f"""
        - ID: {self.uid}
        - Nombre: {self.name}
        - Especie: {self.specie.name}
        - Modelo: {self.modelo}
        - Fabricante: {self.manufacturer}
        - Altura: {self.height} cm
        - Masa: {self.mass} kg
        - Color del sensor: {self.sensor_color}
        - Color de la plataforma: {self.plating_color}
        - Función principal: {self.primary_function}
        {self.films_str}
        """