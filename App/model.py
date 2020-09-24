"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import liststructure as ls
assert config
import config as cf
import csv

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------
def newCatalog():
    """ Inicializa el catálogo de peliculas

    Crea una lista vacia para guardar todas las peliculas

    Se crean indices (Maps) por los siguientes criterios:
    Título de las películas
    Fecha de estreno
    Promedio votacion
    Numero de votos
    Idioma 

    Retorna el catalogo inicializado.
    """
    catalog = {'movies1': None,
               'movies2': None,
               'moviesID1': None,
               'moviesID2': None,
               'production_companies': None
               }

    catalog['movies1'] = lt.newList('SINGLE_LINKED', compareMovieIds)  #Casting
    catalog['movies2'] = lt.newList('SINGLE_LINKED', compareMovieIds)  #Detalles
    catalog['moviesID1'] = mp.newMap(2000,
                                maptype='CHAINING',
                                loadfactor=0.7,
                                comparefunction=compareMapMoviesIds)
    catalog['moviesID2'] = mp.newMap(2000,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareMapMoviesIds)
    catalog['production_companies'] = mp.newMap(2000,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareProductionCompanies)
    catalog['directors'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareDirectors)
    catalog['actors'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareMapMoviesIds)
    catalog['genres'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareMapMoviesIds) 
    catalog['countries'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareMapMoviesIds)

    return catalog

def addMovie1(catalog, movie):
    lt.addLast(catalog['movies1'], movie)
    mp.put(catalog['movieID1'], movie['id'], movie)

def addMovie2(catalog, movie):
    lt.addLast(catalog['movies2'], movie)
    mp.put(catalog['movieID2'], movie['id'], movie)
    producer_name=movie["production_companies"].split(",")
    for producer in producer_name:
        addMovieByProducer(catalog, movie, producer)


def addMovieByProducer(catalog, movie,movie_product):
    producers = catalog['production_companies']
    existprodu = mp.contains(producers, movie_product)
    if existprodu:
        entry = mp.get(producers, movie_product)
        producer = me.getValue(entry)
    else:
        producer = newProducer(movie_product)
        mp.put(producers, movie_product, producer)
    lt.addLast(producer['movies'], movie)

    promedioporpeli = movie['vote_average']
    if producer["average"][0]==0.0:
        producer["average"][0]=promedioporpeli
        producer["cantidad"] = 1
    else:
        producer["average"][0]= producer["average"][0] + promedioporpeli
        producer["cantidad"] += 1
    producer["average"][1]=producer["average"][0] / producer["cantidad"]

def addMovieByDirector(catalog, movie, movie_director):
    directors = catalog['directors']
    checkDirector = mp.contains(directors, movie_director)
    if checkDirector:
        entry = mp.get(directors, movie_director)
        director = me.getValue(entry)
    else:
        director = newDirector(movie_director)
        mp.put(directors, movie_director, director)
    lt.addLast(director['movies'], movie)

    promedioporpeli = movie['vote_average']
    if director["average"][0]==0.0:
        director["average"][0]=promedioporpeli
        director["cantidad"] = 1
    else:
        director["average"][0]= director["average"][0] + promedioporpeli
        director["cantidad"] += 1
    director["average"][1]=director["average"][0] / director["cantidad"]

# Funciones de consulta

def getmoviesByDirector(catalog, name_director):
    director = mp.get(catalog['directors'], name_director)
    if director:
        return me.getValue(director)
    return None
def getmoviesByActor(catalog, name_actor):
    actor = mp.get(catalog['actors'], name_actor)
    if actor:
        return me.getValue(actor)
    return None
def getmoviesByProductionCompany(catalog, companyname):
    company = mp.get(catalog['production_companies'], companyname)
    if company:
        return me.getValue(company)
    return None
def getmoviesByGenres(catalog, genero):
    genre = mp.get(catalog['genres'], genero)
    if genre:
        return me.getValue(genre)
    return None
def getmoviesByCountry(catalog,countryname):
    country = mp.get(catalog['countries'], countryname)
    if country:
        return me.getValue(country)
    return None

#Funciones de carga

def newProducer(movie_product):
   entry = {'producer': "", "movies": None, "average": [0.0,1.1], "cantidad": 0}
   entry['producer'] = movie_product
   entry['movies'] = lt.newList('ARRAY_LIST', compareProductionCompanies)
   return entry

def newDirector(name_director):
   entry = {'director': "", "movies": None, "average": [0.0,1.1], "cantidad": 0}
   entry['director'] = name_director
   entry['movies'] = lt.newList('ARRAY_LIST', compareDirectors)
   return entry

def NewCountry(countryName):
    entry = {'pais': "", "movies": None, 'vote_average': [0.0,1.1], 'cantidad': 0}
    entry['pais'] = countryName
    entry['movies'] = lt.newList('ARRAY_LIST', compareCountry)
    return entry

def NewActor(actorName):
    entry = {'actor': "", "movies": None, 'vote_average': [0.0,1.1], 'cantidad': 0}
    entry['actor'] = actorName
    entry['movies'] = lt.newList('ARRAY_LIST', compareActors)
    return entry

def NewGenre(genreName):
    entry = {'genero': "", "movies": None, 'vote_average': [0.0,1.1], 'cantidad': 0}
    entry['genero'] = genreName
    entry['movies'] = lt.newList('ARRAY_LIST', compareGenres)
    return entry

#Funciones Comparación 

def compareMovieIds(id1, id2):
    if (int(id1) == int(id2)):
        return 0
    elif int(id1) > int(id2):
        return 1
    else:
        return -1
def compareMapMoviesIds(id, entry):
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def compareProductionCompanies(company, entry):
    companyentry = me.getKey(entry)
    if (company == companyentry):
        return 0
    elif (company > companyentry):
        return 1
    else:
        return 0
    
def compareDirectors(director, entry):
    directorentry = me.getKey(entry)
    if (director == directorentry):
        return 0
    elif (director > directorentry):
        return 1
    else:
        return -1

def compareActors(actor, entry):
    actorentry = me.getKey(entry)
    if (actor == actorentry):
        return 0
    elif (actor > actorentry):
        return 1
    else:
        return -1

def compareGenres(genre, entry):
    genreentry = me.getKey(entry)
    if (genre == genreentry):
        return 0
    elif (genre > genreentry):
        return 1
    else:
        return -1

def compareCountry(country, entry):
    countryentry = me.getKey(entry)
    if (country == countryentry):
        return 0
    elif (country > countryentry):
        return 1
    else:
        return 0 

#Funciones Size

def CastingSize(catalog):
    return lt.size(catalog['movies1'])
def DetailsSize(catalog):
    return lt.size(catalog['movies2'])
def ActorsSize(catalog):
    return mp.size(catalog['actors'])
def GenresSize(catalog):
    return mp.size(catalog['genres'])
def CountriesSize(catalog):
    return mp.size(catalog['countries'])
def ProductionCompaniesSize(catalog):
    return mp.size(catalog['production_companies'])


