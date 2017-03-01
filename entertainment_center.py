import os, sys, traceback
from media import Movie
from fresh_tomatoes import open_movies_page
#from tmdb_api import search_movie, get_movie_by_id
import json
import re

import tmdbsimple as tmdb

# delete movie from list if valid index
def load_movies(datfile = 'movies.json'):
    with open(datfile) as json_data:
      d = json.load(json_data)

    m = []

    try:
      for movies in d:
        m.append( Movie(  d[movies]['title'],
                          d[movies]['url'],
                          d[movies]['image'],
                          d[movies]['description']
        ))
      
      return m

    except (ValueError, KeyError, TypeError):
      print( "JSON format error" )

# delete movie from list if valid index
def remove_movie(movies, index):
    if index < len(movies):
        movies.pop(index)
    else:
        print("Not a valid option")

#create new movie entry using user inputs if parameters are None
def create_movie(title=None, trailer=None, poster=None, overview=None):

    if title is None:
        title = input("Please enter a title: ")
    if trailer is None:
        trailer = input("Please enter the trailer url: ")
    if poster is None:
        poster = input("Please enter the poster image url: ")
    if overview is None:
        overview = input("Please enter a quick overview of the movie: ")

    movie = Movie(title, trailer, poster, overview)
    return movie

# write Movies to json file
def save_movies_to_file(movies, datfile = "movies.json"):

    with open('movies.json') as json_data:
       j = json.load(json_data)

    if( len(j) != len(movies) ):
        d = {}
        i = 0
        for movie in movies:
            m = {}
            m[ 'title' ] = movie.title
            m[ 'url' ] = movie.trailer_youtube_url
            m[ 'image' ] = movie.poster_image_url
            m[ 'description' ] = movie.overview
            d[i] = m
            i += 1

        with open(datfile, 'w') as f:
            json.dump(d, f, indent=2, ensure_ascii=False)

# search themoviedb.org API for movie title and request addition to Movies list
def search_movie_from_tmdb(movies):

    title = input("Please enter the movie title to search for on themoviedb.org: ")

    search = tmdb.Search()
    response = search.movie(query='The Bourne')

    if response is None:
        print("Could not find a movie with that title!")
        return

    i = 1
    for s in search.results:
        print( str(i) + ":", s['title'], s['release_date'] )
        i += 1
    print( "n: No Movie" )

    pick_text = "Select the movie you wish to add:" if len(search.results) > 1 else "Add the movie to your list? (y/n): "
    pick = input(pick_text)

    if pick == "y": pick = 1
    if pick.isdigit() and int(pick) < i:
        mid = int(pick)-1
        tmdb_id = search.results[ mid ]['id']

        movie = tmdb.Movies(tmdb_id)

        # select the 1st trailer
        trailers = movie.videos()
        trailer = 'https://youtube.com/watch?v=' + trailers['results'][0]['key'] if len(trailers['results']) > 0 else ""

        image = "https://image.tmdb.org/t/p/original" + search.results[ mid ]['poster_path'] if search.results[ mid ]['poster_path'] != None else ""

        movies.append( create_movie( search.results[ mid ]['title'], 
                                   trailer,
                                   image,
                                   search.results[ mid ]['overview']))

        print(search.results[ mid ]['title'] + " added to the movie list.")
    else:
       if pick.lower() != "n": print("No match!!")


def search_movie_from_tmdb_old(movies):

    title = input("Please enter the movie title to search for on themoviedb.org: ")
    mid = search_movie(title)
    
    if mid is None:
        print("Could not find a movie with that title!")
        return

    movie = get_movie_by_id(mid)

    print("Found movie: %s" % movie['title'])
    if input("Add the movie to your list? (y/n): ") == 'y':
        movies.append( create_movie( movie['title'], 
                                   movie['trailer'],
                                   movie['poster'],
                                   movie['overview']))

# option triggers
def opt_add_movie(movies):
    movies.append(create_movie())
    save_movies_to_file(movies)

def opt_deleter_movie(movies):
    print()
    for index in range(len(movies)):
        print('%s: %s' % (str(index), movies[index].title))
    print('x: go back (do not delete)')
    
    try:
        deleteChoice = int( input("\nPlease choose the number of the movie to delete: ") )
        remove_movie(movies, deleteChoice)
        save_movies_to_file(movies)
    except ValueError:
        print("No movie deleted")

def opt_search_movie(movies):
    search_movie_from_tmdb(movies)
    save_movies_to_file(movies)

def opt_view_movies(movies):
    m = [mov.title for mov in movies]
    print("\nMovie List: " + str(m))

def opt_generate_movies(movies):
   open_movies_page(movies)

def opt_exit(movies):
  save_movies_to_file(movies)
  sys.exit(0)

def main():
    # setup tmdb
    apifile="api_key.txt"
    try:
        with open(apifile) as f: 
            apifile = open('api_key.txt', 'r')
            tmdb.API_KEY = apifile.read()
            apifile.close()
    except:
       print( "themoviedb.org API KEY not found in " + apifile + ". Skipping movie search function." )

    try:
        movies = load_movies()

        opt = None
        while(opt != 'x'):

            opt = input( "\nSelect an option:\n"
                         "v - View the movie list\n"
                         "a - Add your own movie to the list\n"
                         "f - Find a movie on themoviedb.org\n"
                         "r - Remove a movie from the list\n"
                      + ("g - Generate your movie web page\n" if tmdb.API_KEY else "") +
                         "x - Exit\n"
                       ).lower()

            options = { 'a' : opt_add_movie,
                        'f' : opt_search_movie,
                        'r' : opt_deleter_movie,
                        'v' : opt_view_movies,
                        'g' : opt_generate_movies,
                        'x' : opt_exit
                      }
            options[opt](movies)
        sys.exit(0)
    except KeyboardInterrupt:
        save_movies_to_file(movies)
        print( "Shutdown requested...exiting" )
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()
