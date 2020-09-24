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
    #Movies de compañia 
    print('Productora encontrada: ' + compa['producer'])
    print('Promedio: ' + str(compa['average_rating']))
    print('Total de libros: ' + str(lt.size(compa['cantidad'])))
    iterator = it.newIterator(compa['movie'])
    while it.hasNext(iterator):
        peli = it.next(iterator)
        print("Título: "+peli )

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
        print(movies)

    elif int(inputs[0]) == 4:
        nombre = input("Ingrese el nombre del director que desea conocer:\n")
        director = controller.getMoviesByDirector(cont, nombre)
        print(director)
    else:
        sys.exit(0)
sys.exit(0)