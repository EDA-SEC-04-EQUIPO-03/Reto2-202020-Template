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

import config as cf
from App import model
import csv
from DISClib.DataStructures import liststructure as ls
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta. Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    print("Catalogo Creado !")
    return catalog

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def printUltimoyprim(TAD):
    lista=[]
    primis=(ls.firstElement(TAD))
    ultimis=(ls.lastElement(TAD)) 
    lista.append(primis)
    lista.append(ultimis)
    return lista

def loadData(catalog, smallmoviesfile, smallcastingfile, moviesfile , castingfile ):

    loadMovies(catalog, smallmoviesfile)
    loadCasting(catalog, smallcastingfile)
    
def loadCasting(catalog, smallcastingfile):
    """
    Carga cada una de las lineas del archivo de movies.
    - Se agrega cada movie al catalogo de movies
    - Por cada movie se encuentra su autor y por cada
      autor, se crea una lista con sus movies   
    """
    smallcastingfile = cf.data_dir + smallcastingfile
    dialect = csv.excel()
    dialect.delimiter=";"
    movie=csv.DictReader(open(smallcastingfile, encoding='utf-8-sig'),dialect=dialect)
    for m in movie:
        model.addMovie1(catalog, m)
        iD = m['id']
        lista_actors=[]
        lista_actors.append(m["actor1_name"])
        lista_actors.append(m["actor2_name"])
        lista_actors.append(m["actor3_name"])
        lista_actors.append(m["actor4_name"])
        lista_actors.append(m["actor5_name"])
        for actor in lista_actors:
            model.addMovieByActor(catalog,m, actor.strip(),catalog['moviesID2'], iD)
        director=m["director_name"]
        model.addMovieByDirector(catalog,m, director.strip(), catalog['moviesID2'], iD)
        #Agregar catalog de LoadMovies
    
def loadMovies(catalog, smallmoviesfile):
    """
    Carga en el catalogo los tags a partir de la informacion
    del archivo de etiquetas
    """
    smallmoviesfile = cf.data_dir + smallmoviesfile
    dialect = csv.excel()
    dialect.delimiter=";"
    movie=csv.DictReader(open(smallmoviesfile, encoding='utf-8-sig'),dialect=dialect)
    for m in movie:
        model.addMovie2(catalog, m)
        companion=m["production_companies"].split(",")
        for cada_companion in companion:
            model.addMovieByProducer(catalog, m, cada_companion)
        genre=m["genres"].split(" | ")
        for g in genre:
            model.addMovieByGenre(catalog,m,g)
        # genero y paizez

# ___________________________________________________
#  Funciones para consultas
# ____________________________________________

def getMoviesByProductionCompanie(catalog, production_company):
    "Retorna las películas según una productora dada"
    production_info=model.getMoviesByCompany(catalog, production_company)
    return production_info

def getMoviesByDirector(catalog, director):
    'Retorna las peliculas segun el director'
    directorMovies = model.getMoviesByDirector(catalog, director)
    return directorMovies

def getMoviesByActor(catalog, actor):
    'Retorna las peliculas segun el director'
    directorMovies = model.getMoviesByActor(catalog, actor)
    return directorMovies

def getMoviesByGenre(catalog, genre):
    'Retorna las peliculas segun el director'
    directorMovies = model.getMovieByGenre(catalog, genre)
    return directorMovies

def getMoviesByPais(catalog, pais):
    'Retorna las peliculas segun el director'
    directorMovies = model.getMoviesByCountry(catalog, pais)
    return directorMovies


def movies1Size(catalog):
    """Numero de libros leido
    """
    return model.CastingSize(catalog)

def movies2Size(catalog):
    """Numero de libros leido
    """
    return model.DetailsSize(catalog)

def getMoviesByActor(catalog, actor):
    'Retorna las peliculas segun el director'
    actorMovies = model.getMoviesByActor(catalog, actor)
    return actorMovies