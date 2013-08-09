#coding: utf-8
import urllib
# подключили библиотеку urllib
from lxml import html
# подключили библиотеку lxml
import sys
import os
import re
import pickle
import twitter

HOST = 'http://kinozal.tv'
URL = 'http://kinozal.tv/top.php'
FILENAME = 'titles.txt'
CONSUMER_KEY = '***'
CONSUMER_SECRET = '***'
ACCESS_TOKEN = '***'
ACCESS_TOKEN_SECRET = '***'

def get_movies(url):
    item_list = []
    page = urllib.urlopen(url)
    d = html.fromstring(page.read())
    parced = d.xpath('//div[contains(concat(" ", @class, " "), " bx1 ")]//a')
    movies = []
    for movie in parced:
        t = re.search(ur".*?/", movie.get('title')).group()[:-1]
        movies.append(t + HOST + movie.get('href'))
    return movies

def save_movies(movies, filename):
        file = open(filename, 'w')
        pickle.dump(movies, file)
        file.close()
        print "Loaded %d movies" % len(movies)

def load_movies(filename):
        file = open(filename, 'r')
        movies = pickle.load(file)
        file.close()
        return movies

def new_movie(movie):
    print 'New movie: %s' % movie.encode('utf-8','replace')
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)
    api.PostUpdate(movie)

if __name__ == '__main__':
    if os.path.isfile(FILENAME):
        new_movies = get_movies(URL)
        old_movies = load_movies(FILENAME)
        new_movie_flag = False
        for movie in new_movies:
            if not movie in old_movies:
                new_movie_flag = True
                new_movie(movie)
        if new_movie_flag:
            save_movies(get_movies(URL), FILENAME)
        else:
            print 'No new movies :('
    else:
        save_movies(get_movies(URL), FILENAME)
