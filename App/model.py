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

    catalog['movies1'] = lt.newList('SINGLE_LINKED', compareMovieIds)
    catalog['movies2'] = lt.newList('SINGLE_LINKED', compareMovieIds)
    catalog['moviesID1'] = mp.newMap(2000,
                                maptype='CHAINING',
                                loadfactor= 1,
                                comparefunction=compareMapMoviesIds)
    catalog['moviesID2'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=1,
                                   comparefunction=compareMapMoviesIds)
    catalog['production_companies'] = mp.newMap(4000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareProductionCompanies)
    catolog['directors'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=1,
                                   comparefunction=compareMapMoviesIds)
    catolog['actors'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=1,
                                   comparefunction=compareMapMoviesIds)
    catolog['genres'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=1,
                                   comparefunction=compareMapMoviesIds) 
    catolog['country'] = mp.newMap(2000    ,
                                   maptype='CHAINING',
                                   loadfactor=1,
                                   comparefunction=compareMapMoviesIds)

    return catalog





# Funciones para agregar informacion al catalogo

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

def addMoviesByActor(catalog, movie)
    
def newProducer(movie_product):
   entry = {'producer': "", "movies": None, "average": [0.0,1.1], "cantidad": 0}
   entry['producer'] = movie_product
   entry['movies'] = lt.newList('SINGLE_LINKED', compareProductionCompanies)
   return entry

def compareProductionCompanies(company, entry):
    ret=0
    compa = me.getKey(entry)
    if (company > compa):
        ret=1
    return ret



# ==============================
# Funciones de consulta
# ==============================


def getMoviesByProductionCompanie(catalog, production_companies):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    production = mp.get(catalog['production_companies'], production_companies)
    if production:
        return me.getValue(production)
    return None





# ==============================
# Funciones de Comparacion
# ==============================


def compareProductionCompanies(company, entry):
    """
    Compara dos prductoras de peliculas
    """
    companyentry = me.getKey(entry)
    if (company == companyentry):
        return 0
    elif (company > companyentry):
        return 1
    else:
        return -1
def compareMovieIds(id1, id2):
    """
    Compara dos ids de peliculas
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareMapMovieIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1


def compareAuthorsByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareTagNames(name, tag):
    tagentry = me.getKey(tag)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1


def compareTagIds(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0


def compareMapYear(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0


def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

# ==============================
# Funciones de Comparacion
# ==============================


