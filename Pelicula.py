class Pelicula:
    def __init__(self, uid, title, episode_id, release_date, opening_crawl, director):
        self.title = title
        self.episode_id = episode_id
        self.release_date = release_date
        self.opening_crawl = opening_crawl
        self.director = director

    def show_atr(self):
        return f"Título: {self.title}\nEpisodio: {self.episode_id}\nFecha de lanzamiento: {self.release_date}\nCrawl de apertura: {self.opening_crawl}\nDirector: {self.director}"
    
    def name_film(self):
        name_film = f"Episodio {self.episode_id}: {self.title}"
        return name_film
    