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
    catalog = {'movies': None,
               'movieIds': None,
               'production_companies': None,
               }

    catalog['movies'] = lt.newList('SINGLE_LINKED', compareMovieIds)
    catalog['MovieIds'] = mp.newMap(200,
                                   maptype='PROBING',
                                   loadfactor=0.4,
                                   comparefunction=compareMapMovieIds)
    catalog['production_companies'] = mp.newMap(4000,
                                   maptype='PROBING',
                                   loadfactor=0.4,
                                   comparefunction=compareProductionCompanies)

    return catalog






# Funciones para agregar informacion al catalogo

#def loadCSVFile (file, cmpfunction):
    #lst=lt.newList("ARRAY_LIST", cmpfunction)
    #dialect = csv.excel()
    #dialect.delimiter=";"
    #try:
        #with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
           # row = csv.DictReader(csvfile, dialect=dialect)
           # for elemento in row: 
                #ls.addLast(lst,elemento)
    #except:
        #print("Hubo un error con la carga del archivo")
    #return lst

def addMovie(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    lt.addLast(catalog['movies'], movie)

def addMoviesids(catalog, movie):
    ids = catalog['movieIds']
    movie_id = movie['id']
    existid = mp.contains(ids, movie_id)
    if existid:
        entry = mp.get(ids, movie_id)
        id_m = me.getValue(entry)
    else:
        id_m = newId(movie_id)
        mp.put(ids, movie_id, id_m)
    lt.addLast(id_m['movies'], movie)

def newId(movie_id):
   entry = {'id': "", "movies": None}
   entry['id'] = movie_id
   entry['movies'] = lt.newList('SINGLE_LINKED', compareMovieIds)
   return entry



def addProducer(catalog, movie):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    producers = catalog['production_companies']
    movie_product = movie['production_companies']
    existprodu = mp.contains(producers, movie_product)
    if existprodu:
        entry = mp.get(producers, movie_product)
        producer = me.getValue(entry)
    else:
        producer = newProducer(movie_product)
        mp.put(producers, movie_product, producer)
    lt.addLast(producer['movies'], movie)

def newProducer(movie_product):
   """
   Esta funcion crea la estructura de libros asociados
   a un año.
   """
   entry = {'producer': "", "movies": None}
   entry['producer'] = movie_product
   entry['movies'] = lt.newList('SINGLE_LINKED', compareProductionCompanies)
   return entry


# def addBook(catalog, book):
#     """
#     Esta funcion adiciona un libro a la lista de libros,
#     adicionalmente lo guarda en un Map usando como llave su Id.
#     Finalmente crea una entrada en el Map de años, para indicar que este
#     libro fue publicaco en ese año.
#     """
#     lt.addLast(catalog['books'], book)
#     mp.put(catalog['bookIds'], book['goodreads_book_id'], book)
#     addBookYear(catalog, book)


# def addBookYear(catalog, book):
#     """
#     Esta funcion adiciona un libro a la lista de libros que
#     fueron publicados en un año especifico.
#     Los años se guardan en un Map, donde la llave es el año
#     y el valor la lista de libros de ese año.
#     """
#     years = catalog['years']
#     pubyear = book['original_publication_year']
#     pubyear = int(float(pubyear))
#     existyear = mp.contains(years, pubyear)
#     if existyear:
#         entry = mp.get(years, pubyear)
#         year = me.getValue(entry)
#     else:
#         year = newYear(pubyear)
#         mp.put(years, pubyear, year)
#     lt.addLast(year['books'], book)


# def newYear(pubyear):
#     """
#     Esta funcion crea la estructura de libros asociados
#     a un año.
#     """
#     entry = {'year': "", "books": None}
#     entry['year'] = pubyear
#     entry['books'] = lt.newList('SINGLE_LINKED', compareYears)
#     return entry


# def addBookAuthor(catalog, authorname, book):
#     """
#     Esta función adiciona un libro a la lista de libros publicados
#     por un autor.
#     Cuando se adiciona el libro se actualiza el promedio de dicho autor
#     """
#     authors = catalog['authors']
#     existauthor = mp.contains(authors, authorname)
#     if existauthor:
#         entry = mp.get(authors, authorname)
#         author = me.getValue(entry)
#     else:
#         author = newAuthor(authorname)
#         mp.put(authors, authorname, author)
#     lt.addLast(author['books'], book)

#     authavg = author['average_rating']
#     bookavg = book['average_rating']
#     if (authavg == 0.0):
#         author['average_rating'] = float(bookavg)
#     else:
#         author['average_rating'] = (authavg + float(bookavg)) / 2


# def addTag(catalog, tag):
#     """
#     Adiciona un tag a la tabla de tags dentro del catalogo
#     """
#     newtag = newTagBook(tag['tag_name'], tag['tag_id'])
#     mp.put(catalog['tags'], tag['tag_name'], newtag)
#     mp.put(catalog['tagIds'], tag['tag_id'], newtag)


# def addBookTag(catalog, tag):
#     """
#     Agrega una relación entre un libro y un tag.
#     Para ello se adiciona el libro a la lista de libros
#     del tag.
#     """
#     bookid = tag['goodreads_book_id']
#     tagid = tag['tag_id']
#     entry = mp.get(catalog['tagIds'], tagid)

#     if entry:
#         tagbook = mp.get(catalog['tags'], me.getValue(entry)['name'])
#         tagbook['value']['total_books'] += 1
#         tagbook['value']['count'] += int(tag['count'])
#         book = mp.get(catalog['bookIds'], bookid)
#         if book:
#             lt.addLast(tagbook['value']['books'], book['value'])


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


def compareProductionCompanies(pc1, pc2):
    """
    Compara dos prductoras de peliculas
    """
    if (pc1 == pc2):
        return 0
    elif pc1 > pc2:
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


