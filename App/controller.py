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
    print("Carga completa")
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

def loadMoviesArchivo ():
    lst = model.loadCSVFile("SmallMoviesDetailsCleaned.csv",None) 
    print("Datos cargados, " + str(ls.size(lst)) + " elementos cargados")

def loadData(catalog, smallmoviesfile, smallcastingfile, moviesfile , castingfile ):
    """
    Carga los datos de los archivos en el modelo
    """
    loadMovies(catalog, smallmoviesfile)
    loadCasting(catalog, smallcastingfile)
    
def loadMovies(catalog, smallmoviesfile):
    """
    Carga cada una de las lineas del archivo de libros.
    - Se agrega cada libro al catalogo de libros
    - Por cada libro se encuentran sus autores y por cada
      autor, se crea una lista con sus libros
    """
    smallmoviesfile = cf.data_dir + smallmoviesfile
    input_file = csv.DictReader(open(smallmoviesfile))
    for movie in input_file: 
            model.addMovie(catalog, movie)
            model.addMovieids(catalog, movie)
            model.addProducer(catalog, movie)


def loadCasting(catalog, smallcastingfile):
    """
    Carga en el catalogo los tags a partir de la informacion
    del archivo de etiquetas
    """
    smallcastingfile = cf.data_dir + smallcastingfile
    input_file = csv.DictReader(open(smallcastingfile))
    for cast in input_file:
        model.addCast(catalog, cast)

# ___________________________________________________
#  Funciones para consultas
# ____________________________________________

def getMoviesByProductionCompanie(catalog, production_companies):
    "Retorna las películas según una productora dada"
    production_info=model.getMoviesByProductionCompanie(catalog, production_companies)
    return production_info

#def moviesSize(catalog):
    """Numero de libros leido
    """
   # return model.moviesSize(catalog)

#def genresSize(catalog):
    """Numero de libros leido
    """
   # return model.genresSize(catalog)

#def getMoviesByCountry(catalog, country):
    """
    #countryinfo = model.getMoviesByCountry(catalog, country)
    return country 
    """
