# movie-trailer-website
Project 1 for Udacity - Full Stack Engineer nanodegree:
You will write server-side code to store a list of your favorite movies, including box art imagery and a movie trailer URL. 
You will then serve this data as a web page allowing visitors to review their movies and watch the trailers.

Extra Features:
-Added menu to edit the list of movies: add, remove, sort
-Added a movie search feature using themoviedb.org API


## Install
This is currently tested for Python3.6

Download the repo and then install the additional libraries using the following command.

```
pip install -r requirements.txt
```

If you wish to search for a movie on themoviedb.org website, you will need to sign up for an API KEY. 
Enter your API KEY into the following text file. If this file is blank, the search option is disabled.
```
api_key.txt
```

## Libraries used
[requests](https://github.com/kennethreitz/requests) - Used to send and receive API requests
[tmdbsimple](https://github.com/celiao/tmdbsimple) - Connect via Request above to the themoviedb.org API


## Usage
Launch the app with the following command line:
```
python entertainment_center.py
```

User will be presented with a few options:

v - View the movie list<br />
a - Add your own movie to the list<br />
f - Find a movie on themoviedb.org<br />
r - Remove a movie from the list<br />
s - Sort the movie list<br />
g - Generate your movie web page (if valid API KEY exists)<br />
x - Exit<br />

```
g - Generate your movie web page
```
Creates a webpage, fresh_tomatoes.html, with the movie list with clickable links to play a trailer (Youtube).
Hovering the mouse cursor over a movie image will display the movie summary in a tooltip.<br>

