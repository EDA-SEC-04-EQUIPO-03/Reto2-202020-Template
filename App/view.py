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

import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
from time import process_time
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones y por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________
smallmoviesfile= "Movies/SmallMoviesDetailsCleaned.csv"
smallcastingfile= "Movies/MoviesCastingRaw-small.csv"
moviesfile= "Movies/AllMoviesDetailsCleaned.csv"
castingfile= "Movies/1AllMoviesCastingRaw.csv"




# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________
def PrintRQ1(compa):
    #Imprimir Movies de compañia
    peliss=[] 
    print('Productora es: ' + compa['producer'])
    print('Promedio es: ' + str(compa['average'][1]))
    print('Total de películas: ' + str(lt.size(compa['movies'])))
    iterator = it.newIterator(compa["movies"])
    i=0
    while it.hasNext(iterator) and i<6:
        peli = it.next(iterator)
        if peli["original_title"] not in peliss:
            peliss.append(peli["original_title"])
            print("Título #" + str(i) +" "+ str(peli["original_title"]) )
            i+=1
    

def PrintRQ2(direc):
    #Imprimir Movies de director 
    peliss=[]
    print('Director es: ' + direc['director'])
    print('Promedio: ' + str(direc['average'][1]))
    print('Total de películas: ' + str(lt.size(direc['movies'])))
    i = 0
    for x in direc["movieN"]:
            print("Título #" + str(i) +" "+ x )
            i+=1

def PrintRQ3(aktor):
    #Imprimir Movies de actor
    peliss=[] 
    print('Actor es: ' + aktor['actor']) #actor se define en model NewActor
    print('Promedio es: ' + str(aktor['vote_average'][1]))
    print('Total de películas: ' + str(lt.size(aktor['movies'])))
    print("El director con más colaboraciones es: " + str(alkor["dmayor"]))
    iterator = it.newIterator(aktor['movies'])   #Operación fallando en model NewActor
    i = 0
    for x in aktor["movieN"]:
            print("Título #" + str(i) +" "+ x )
            i+=1

def PrintRQ4(genre):
    #Imprimir Movies de genero 
    peliss=[]
    print('Genero encontrado: ' + genre['genero'])
    print('Promedio: ' + str(genre['count'][1]))
    print('Total de películas: ' + str(lt.size(genre['movies'])))
    iterator = it.newIterator(genre['movies'])
    i=0
    while it.hasNext(iterator) and i<6:
        peli = it.next(iterator)
        if peli["original_title"] not in peliss:
            peliss.append(peli["original_title"])
            print("Título #" + str(i) + " "+ peli["original_title"] )
            i+=1

def PrintRQ5(paiz):
    peliss=[]
    #Imprimir Movies de un país 
    print('Pais encontrado: ' + paiz['pais'])
    print('Promedio: ' + str(paiz['vote_average'][1]))
    print('Total de películas: ' + str(lt.size(paiz['movies'])))
    iterator = it.newIterator(paiz['movies'])
    i=0
    while it.hasNext(iterator) and i<6:
        peli = it.next(iterator)
        if peli["original_title"] not in peliss:
            peliss.append(peli["original_title"])
            print("Título #" + str(i) + " "+ peli["original_title"] )
            print("La fecha de lanzamiento es o fue: "+peli["release_date"])
            i+=1

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo de películas")
    print("2- Cargar información en el catálogo")
    print("3- Descubrir productoras de cine")
    print("4- Conocer un director")
    print("5- Conocer un actor")
    print("6- Entender un género cinematográfico")
    print("7- Consultar películas por país")
    print("0- Salir")

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        cont = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont, smallmoviesfile, smallcastingfile, moviesfile, castingfile)
        t1_start = process_time()
        print('Peliculas (Details) cargadas: ' + str(controller.movies1Size(cont)))
        print('Peliculas (CastingRaw) cargadas: ' + str(controller.movies2Size(cont)))
        t1_stop = process_time()

    elif int(inputs[0]) == 3:
        t1_start = process_time()
        nombre = input("Digite el nombre de la compañia:")
        movies = controller.getMoviesByProductionCompanie(cont, nombre)
        PrintRQ1(movies)

    elif int(inputs[0]) == 4:
        nombre = input("Ingrese el nombre del director que desea conocer:\n")
        director = controller.getMoviesByDirector(cont, nombre)
        PrintRQ2(director)
    elif int(inputs[0]) == 5:
        nombre = input("Ingrese el nombre de un actor que desea conocer:\n")
        director = controller.getMoviesByActor(cont, nombre)
        PrintRQ3(director)
    elif int(inputs[0]) == 6:
        nombre = input("Ingrese el genero de película que desea conocer:\n")
        director = controller.getMoviesByGenre(cont, nombre)
        PrintRQ4(director)
    elif int(inputs[0]) == 7:
        nombre = input("Ingrese el nombre del país a filtrar:\n")
        director = controller.getMoviesByPais(cont, nombre)
        PrintRQ5(director)
    else:
        sys.exit(0)
sys.exit(0)