import json
import requests
import webbrowser
import urllib
import tmdbsimple as tmdb
from fresh_tomatoes import open_movies_page

class Movies():
    """
    Methods to load/save movies to file  and find movies on themoviedb.org
    Implements tmdbsimple (https://github.com/celiao/tmdbsimple)

    Attributes:
            apikey - TMDb API Key (https://www.themoviedb.org/documentation/api)
            datfile - local file to save movie updates

    Methods:
            load_movies_from_file() - load movie list from initialised filename. Initial movie list is empty.
            save_movies_to_file() - save movie list to initialised filename
            add_movie(Movie) - add a movie to the end of the movie list
            get_movies() - return a list of Movies
            remove_movie(index) - remove the Movie in the specified position in the movie list (starting at position 0)
            sort_movies() - sort the list using the Movie.title alphabetically
            search_movie_from_tmdb(text) - search themoviedb.org for movies. The results are stored in search_results.
            clear_search_results() - clear the stored search_results
            get_movie_from_tmdb(id) - get movie information from themoviedb.org - used to get the trailer URLs
            get_videos_from_tmdb(id) - get the trailer URLs from themoviedb.org
            generate_webpage() - create a webpage using fresh_tomatoes.py template
    """
    
    def __init__(self, apikey = "", datfile = 'movies.json'):
        tmdb.API_KEY = apikey
        self.datfile = datfile
        self.movies = []
        self.search_results = {}

    def _clear_movies(self):
        self.movies = []
        
    def get_movies(self):
        return self.movies

    def sort_movies(self):
        self.movies.sort(key = lambda x: x.title)

    def add_movie(self, movie):
        if not isinstance(movie, Movie):
            raise TypeError
      
        self.movies.append(movie)

    def remove_movie(self, movie_id: int):
        if movie_id < len(self.movies):
            self.movies.pop(movie_id)
            return True
        return False

    def generate_webpage(self):
       open_movies_page(self.movies)


    def __load_json_file(self):
        d = ''
        try:
            with open(self.datfile) as json_data: 
                d = json.load(json_data)
        except (ValueError):
            print( "JSON format error" )
        return d

    def load_movies_from_file(self):
        d = self.__load_json_file()
        self._clear_movies()

        for movies in d:
            self.movies.append( Movie( d[movies]['title'],
                                       d[movies]['url'],
                                       d[movies]['image'],
                                       d[movies]['description']
            ))

    def __save_json_file(self, contents):
        try:
            with open(self.datfile, 'w') as f:
                json.dump(contents, f, indent=2, ensure_ascii=False)
        except ValueError as e:
            print( "JSON saving error: " + str(e) )


    def save_movies_to_file(self):
        j = self.__load_json_file() if len(self.movies) > 0 else []

        if( len(j) != len(self.movies) ):
            d = {}
            i = 0
            for movie in self.movies:
                m = {}
                m[ 'title' ] = movie.title
                m[ 'url' ] = movie.trailer_youtube_url
                m[ 'image' ] = movie.poster_image_url
                m[ 'description' ] = movie.overview
                d[i] = m
                i += 1

            self.__save_json_file(d)

    def remove_movie(self, i):
        if i < len(self.movies):
            self.movies.pop(i)
            return True
        return False

    def search_movie_from_tmdb(self, str_to_search):
        search = tmdb.Search()
        response = search.movie(query=str_to_search)
        self.search_results = search.results
        return response

    def clear_search_results(self):
        self.search_results = {}

    def get_movie_from_tmdb(self, tmdb_id):
        return tmdb.Movies(tmdb_id)

    def get_videos_from_tmdb(self, tmdb_id):
        movie = self.get_movie_from_tmdb(tmdb_id)
        return movie.videos()


class Movie(object):
    """
    Represents a movie, containing information that a user may want to know about the movie

    Attributes:
            title - Title of the movie
            trailer_youtube_url - Link to the (youtube) video of the movie's trailer
            poster_image_url - Link to an image file of the movie's poster
            overview - Quick synopsis of the movie's plot
    """

    def __init__(self, title, trailer_youtube_url, poster_image_url, overview):
        self.title = title
        self.trailer_youtube_url = trailer_youtube_url
        self.poster_image_url = poster_image_url
        self.overview = overview
