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
from DISClib.DataStructures import listiterator as it
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

    catalog['movies1'] = lt.newList('ARRAY_LIST', compareMovieIds)
    catalog['movies2'] = lt.newList('ARRAY_LIST', compareMovieIds)
    catalog['moviesID1'] = mp.newMap(2000,
                                maptype='PROBING',
                                loadfactor= 0.5,
                                comparefunction=compareMapMovieIds)
    catalog['moviesID2'] = mp.newMap(2000    ,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapMovieIds)
    catalog['production_companies'] = mp.newMap(2000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareProductionCompanies)
    catalog['directors'] = mp.newMap(2000   ,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareDirectors)
    catalog['actors'] = mp.newMap(2000    ,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareActors)
    catalog['genres'] = mp.newMap(2000    ,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareGenres) 
    catalog['country'] = mp.newMap(2000    ,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareCountry)

    return catalog

def addMovie1(catalog, movie):
    lt.addLast(catalog['movies1'], movie)
    mp.put(catalog['moviesID1'], movie['id'], movie)

def addMovie2(catalog, movie):
    lt.addLast(catalog['movies2'], movie)
    mp.put(catalog['moviesID2'], movie['id'], movie)
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

    promedioporpeli = float(movie['vote_average'])
    if producer["average"][0]==0.0:
        producer["average"][0]=promedioporpeli
        producer["cantidad"] = 1
    else:
        producer["average"][0]= producer["average"][0] + promedioporpeli
        producer["cantidad"] += 1
    producer["average"][1]=producer["average"][0] / producer["cantidad"]

def addMovieByDirector(catalog, movie, movie_director, extra, iD):
    movie2 = mp.get(extra, iD)
    movie2VC = me.getValue(movie2)['vote_average']
    movieN = me.getValue(movie2)['original_title']
    directors = catalog['directors']
    checkDirector = mp.contains(directors, movie_director)
    if checkDirector:
        entry = mp.get(directors, movie_director)
        director = me.getValue(entry)
    else:
        director = newDirector(movie_director)
        mp.put(directors, movie_director, director)
    lt.addLast(director['movies'], movie)
    director["movieN"].append(movieN)

    promedioporpeli = float(movie2VC)
    if director["average"][0]==0.0:
        director["average"][0]=promedioporpeli
        director["cantidad"] = 1
    else:
        director["average"][0]= director["average"][0] + promedioporpeli
        director["cantidad"] += 1
    director["average"][1]=director["average"][0] / director["cantidad"]

def addMovieByGenre(catalog, movie, gender):
    genders = catalog['genres']
    revisarGen = mp.contains(genders, gender)
    if revisarGen:
        entry = mp.get(genders, gender)
        gener_mov = me.getValue(entry)
    else:
        gener_mov = newGenre(gender)
        mp.put(genders, gender, gener_mov)
    lt.addLast(gener_mov['movies'], movie)

    promedioporpeli = float(movie['vote_count'])
    if gener_mov["count"][0]==0.0:
        gener_mov["count"][0]=promedioporpeli
        gener_mov["cantidad"] = 1
    else:
        gener_mov["count"][0]= gener_mov["count"][0] + promedioporpeli
        gener_mov["cantidad"] += 1
    gener_mov["count"][1]=gener_mov["count"][0] / gener_mov["cantidad"]


def addMoviesByCountry(catalog, movie, country):
    paises = catalog["country"]
    checkCountry = mp.contains(paises, country)
    if checkCountry:
        entry = mp.get(paises, country)
        pais_movie = me.getValue(entry)
    else:
        pais_movie = newGenre(country)
        mp.put(paises, country, pais_movie)
    lt.addLast(pais_movie['genres'], movie)
    
    promedio_peli=float(movie["vote_average"])
    if pais_movie["vote_average"][0]==0.0:
        pais_movie["vote_average"][0]=promedio_peli
        pais_movie["cantidad"] = 1
    else:
        pais_movie["vote_average"][0]= pais_movie["vote_average"][0] + promedio_peli
        pais_movie["cantidad"] += 1
    pais_movie["vote_average"][1]=pais_movie["vote_average"][0] / pais_movie["vote_average"]

#def addMoviesByCountry(catalog)
def addMovieByActor(catalog, movie, movie_actor, extra, iD):
    movie2 = mp.get(extra, iD)
    movie2VC = me.getValue(movie2)['vote_average']
    movieN = me.getValue(movie2)['original_title']
    actors = catalog['actors']
    checkActor = mp.contains(actors, movie_actor)
    if checkActor:
        entry = mp.get(actors, movie_actor)
        actor = me.getValue(entry)
    else:
        actor = newActor(movie_actor)
        mp.put(actors, movie_actor, actor)
    lt.addLast(actor['movies'], movie)
    actor["movieN"].append(movieN)

    

    iterator = it.newIterator(actor["movies"])
    while it.hasNext(iterator):
        element = it.next(iterator)
        if element["director_name"] in actor["ddict"].keys():
            actor["ddict"][element["director_name"]] += 1

        else:
            actor["ddict"][element["director_name"]] = 1

    for key in actor["ddict"].keys():
        if actor["ddict"][key]>actor["mayor"]:
            actor["mayor"] = actor["ddict"][key]
            actor["dmayor"] = key 

    promedioporpeli = float(movie2VC)
    if actor["vote_average"][0]==0.0:
        actor["vote_average"][0]=promedioporpeli
        actor["cantidad"] = 1
    else:
        actor["vote_average"][0]= actor["vote_average"][0] + promedioporpeli
        actor["cantidad"] += 1
    actor["vote_average"][1]=actor["vote_average"][0] / actor["cantidad"]

    



# Funciones de consulta (get)


def getMoviesByDirector(catalog, name_director):
    director = mp.get(catalog['directors'], name_director)
    if director:
        return me.getValue(director)
    return None

def getMoviesByActor(catalog, name_actor):
    actor = mp.get(catalog['actors'], name_actor)
    if actor:
        return me.getValue(actor)
    return None
def getMoviesByCompany(catalog, companyname):
    company = mp.get(catalog['production_companies'], companyname)
    listNames = company
    if company:
        return me.getValue(company)
    return None
def getMovieByGenre(catalog, genero):
    genre = mp.get(catalog['genres'], genero)
    if genre:
        return me.getValue(genre)
    return None
def getMoviesByCountry(catalog,countryname):
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
   entry = {'director': "", "movies": None, "average": [0.0,1.1], "cantidad": 0, "movieN":[]}
   entry['director'] = name_director
   entry['movies'] = lt.newList('ARRAY_LIST', compareDirectors)
   return entry


def newCountry(countryName):
    entry = {'pais': "", "movies": None, 'vote_average': [0.0,1.1], 'cantidad': 0}
    entry['pais'] = countryName
    entry['movies'] = lt.newList('ARRAY_LIST', compareCountry)
    return entry

def newActor(actorName):
    entry = {'actor': "", "movies": None, 'vote_average': [0.0,1.1], 'cantidad': 0, "ddict":{}, "mayor": 0, "dmayor":"", "movieN":[] }
    entry['actor'] = actorName
    entry['movies'] = lt.newList('ARRAY_LIST', compareActors)
    return entry

def newGenre(gender):
    entry = {'genero': "", "movies": None, "count": [0.0,1.1], "cantidad": 0, "movieN": []}
    entry['genero'] = gender
    entry['movies'] = lt.newList('ARRAY_LIST', compareProductionCompanies)
    return entry

#Funciones Comparación 

def compareMovieIds(id1, id2):
    if (int(id1) == int(id2)):
        return 0
    elif int(id1) > int(id2):
        return 1
    else:
        return -1
        
def compareMapMovieIds(id, entry):
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


#Funciones Size catalogo - map

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


