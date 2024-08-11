class Pelicula:
    """
    Clase que representa una película en un contexto ficticio.

    Atributos:
        uid (int): Identificador único de la película.
        title (str): Título de la película.
        episode_id (int): Número de episodio de la película.
        release_date (str): Fecha de lanzamiento de la película.
        opening_crawl (str): Texto de apertura de la película.
        director (str): Nombre del director de la película.
    """

    def __init__(self, uid, title, episode_id, release_date, opening_crawl, director):
        """
        Inicializa un nuevo objeto Pelicula con los atributos dados.

        Args:
            uid (int): Identificador único de la película.
            title (str): Título de la película.
            episode_id (int): Número de episodio de la película.
            release_date (str): Fecha de lanzamiento de la película.
            opening_crawl (str): Texto de apertura de la película.
            director (str): Nombre del director de la película.
        """
        self.uid = uid  # Asigna el ID único de la película
        self.title = title  # Asigna el título de la película
        self.episode_id = episode_id  # Asigna el número de episodio de la película
        self.release_date = release_date  # Asigna la fecha de lanzamiento de la película
        self.opening_crawl = opening_crawl  # Asigna el texto de apertura de la película
        self.director = director  # Asigna el nombre del director de la película

    def show_atr(self):
        """
        Genera una cadena con los principales atributos de la película.

        Returns:
            str: Una cadena con la información detallada de la película.
        """
        return (f"Título: {self.title}\n"
                f"Episodio: {self.episode_id}\n"
                f"Fecha de lanzamiento: {self.release_date}\n"
                f"Crawl de apertura: {self.opening_crawl}\n"
                f"Director: {self.director}")  # Muestra los atributos clave de la película

    def name_film(self):
        """
        Genera una cadena que combina el número de episodio y el título de la película.

        Returns:
            str: Una cadena con el formato "Episodio {episode_id}: {title}".
        """
        name_film = f"Episodio {self.episode_id}: {self.title}"  # Combina el número de episodio y el título
        return name_film  # Devuelve la cadena con el nombre completo de la película

    