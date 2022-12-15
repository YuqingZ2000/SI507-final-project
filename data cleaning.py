#!/usr/bin/env python
# coding: utf-8

##########################
### Name: Yuqing Zhang ###
### Uniqname: zhyuqing ###
##########################


import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import datetime


# ## Movie dataset
movie_ori = pd.read_csv(r'movies_initial.csv')
movie_validrating = movie_ori.dropna(subset=['imdbRating'])
movie = movie_validrating.drop(['released','writer','metacritic','imdbVotes','plot','fullplot','lastupdated','awards','type'], axis=1)
#movie


# ## Web Scraping
# Use web scraping to obtain the ranking(#/300) and the movie imdbID
def moviescraping(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_rankname = soup.select('h3.lister-item-header')
    for i in range(len(movie_rankname)):
        string_list = movie_rankname[i].get_text().split("\n")
        ranking = int(string_list[1].replace('.',''))
        imdbID = movie_rankname[i].a.get('href').split('/')[2][2:].lstrip("0")
        top300dict[ranking] = imdbID


# ## Caching
CACHE_FILENAME = "cache.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()


def load_webscraping_data():
    if open_cache():  # get data from cache
        return open_cache()
       
    else: # first time from web scraping
        moviescraping('https://www.imdb.com/list/ls050782187/')
        moviescraping('https://www.imdb.com/list/ls050782187/?sort=list_order,asc&st_dt=&mode=detail&page=2')
        moviescraping('https://www.imdb.com/list/ls050782187/?sort=list_order,asc&st_dt=&mode=detail&page=3')
        save_cache(top300dict)
        return top300dict


top300dict = {}
top300dict = open_cache()

## first time load from web scraping, run without the cache.json file
t1 = datetime.datetime.now().timestamp()
load_webscraping_data()
t2 = datetime.datetime.now().timestamp()

## second time load from cache
t3 = datetime.datetime.now().timestamp()
load_webscraping_data()
t4 = datetime.datetime.now().timestamp()


print("time without caching: ", (t2 - t1) * 1000, "ms")
print("time with caching: ", (t4 - t3) * 1000, "ms")


# # Merge web scraping ranking and movie csv
for i in range(len(top300dict)):
    for j in range(len(movie)):
        if int(top300dict[str(i+1)]) == movie.loc[j]["imdbID"]:
            movie.loc[j, "ranking"] = str(int(i+1))

movie = movie[['ranking','imdbID', 'title', 'year', 'rating', 'runtime', 'genre', 'director',
                                 'cast', 'imdbRating', 'poster', 'language', 'country']]
movie.to_csv('movie_combined.csv')

