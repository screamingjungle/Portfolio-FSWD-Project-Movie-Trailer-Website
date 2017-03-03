import os, sys, traceback
from media import Movie, Movies

#create new movie entry using user inputs if parameters are None
def create_movie(name=None, trailer=None, poster=None, overview=None):

    if name is None:
        name = input("Please enter a title: ")
    if trailer is None:
        trailer = input("Please enter the trailer url: ")
    if poster is None:
        poster = input("Please enter the poster image url: ")
    if overview is None:
        overview = input("Please enter a quick overview of the movie: ")

    movie = Movie(name, trailer, poster, overview)
    return movie

# search themoviedb.org API for movie title and request addition to Movies list
def search_movie_from_tmdb(m):

    if (len(m.search_results) < 1):
        title = input("Please enter the movie title to search for on themoviedb.org: ")
        
        response = m.search_movie_from_tmdb(title)

        if response is None or not m.search_results:
            print("Could not find a movie with the title! " + title)
            return

    i = 1
    for s in m.search_results:
        print( str(i) + ": ", s['title'], s['release_date'] )
        i += 1
    if i > 2: print( "n: No Movie" )

    pick_text = "Select the movie you wish to add: " if len(m.search_results) > 1 else "Add the movie to your list? (y/n): "
    pick = input(pick_text)

    if pick == "y": pick = 1
    if pick.isdigit() and int(pick) < i:
        mid = int(pick)-1

        # select the 1st trailer
        trailers = m.get_videos_from_tmdb( m.search_results[ mid ]['id'] )
        trailer = 'https://youtube.com/watch?v=' + trailers['results'][0]['key'] if len(trailers['results']) > 0 else ""

        image = "https://image.tmdb.org/t/p/original" + m.search_results[ mid ]['poster_path'] if m.search_results[ mid ]['poster_path'] != None else ""

        m.add_movie(create_movie(
                                   m.search_results[ mid ]['title'], 
                                   trailer,
                                   image,
                                   m.search_results[ mid ]['overview']
        ))

        print( m.search_results[ mid ]['title'] + " added to the movie list." )
        m.clear_search_results()
    else:
       if pick.lower() != "n":
          print("No match!!")
          search_movie_from_tmdb(m)
       elif pick.lower() == "n":
          m.clear_search_results()

# option triggers
def opt_add_movie(m):
    m.add_movie(create_movie())

def opt_delete_movie(m):
    print()
    for i in range(len(m.movies)):
        print('%s: %s' % (str(i + 1), m.movies[i].title))
    print('x: go back (do not delete)')
    
    try:
        deleteChoice = int( input("\nPlease choose the number of the movie to delete: ") ) - 1

        if not m.remove_movie(deleteChoice): print("Not a valid option")

    except ValueError:
        print("No movie deleted")

def opt_search_movie(m):
    search_movie_from_tmdb(m)

def opt_sort_movie(m):
    m.sort_movies()
    for i in range(len(m.movies)):
        print('%s: %s' % (str(i + 1), m.movies[i].title))

def opt_view_movies(m):
    print()
    for i in range(len(m.movies)):
        print('%s: %s' % (str(i + 1), m.movies[i].title))

def opt_generate_movies(m):
   m.generate_webpage()
   m.save_movies_to_file()  # save file while generation takes place

def opt_exit(m):
  m.save_movies_to_file()
  sys.exit(0)

def main():
    apifile = "api_key.txt"
    apikey = ""
    try:
        with open(apifile, 'r') as f: 
            apikey = f.read()
            f.close()
    except:
       print( "themoviedb.org API KEY not found in " + apifile + ". Skipping movie search function." )
       apikey = ""

    try:
        m = Movies(apikey)
        m.load_movies_from_file()

        opt = None
        while(opt != 'x'):

            opt = input( "\nSelect an option:\n"
                         "v - View the movie list\n"
                         "a - Add your own movie to the list\n"
                         "f - Find a movie on themoviedb.org\n"
                         "r - Remove a movie from the list\n"
                         "s - Sort the movie list\n"
                      + ("g - Generate your movie web page\n" if apikey != "" else "") +
                         "x - Exit\n"
                         "> "
                       ).lower()

            options = { 
                        'v' : opt_view_movies,
                        'a' : opt_add_movie,
                        'f' : opt_search_movie,
                        'r' : opt_delete_movie,
                        's' : opt_sort_movie,
                        'g' : opt_generate_movies,
                        'x' : opt_exit
                      }
            try:
              options[opt](m)
            except KeyError:
                print("Unknown option - try again...")
        sys.exit(0)
    except KeyboardInterrupt:
        print( "Shutdown requested...exiting" )
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()
