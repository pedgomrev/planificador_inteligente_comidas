import os
import ssl
from bs4 import  BeautifulSoup as bs
import urllib.request
import lxml
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

'''
En este fichero vamos a extraer los datos necesarios para la aplicación. Así como poblar la base de datos.
Los datos se van a extructurar en una lista de diccionarios. Cada diccionario representará una receta.
Cada receta tendrá los siguientes campos:
    - Nombre : Nombre de la receta.
    - Comensales : Número de comensales para los que está pensada la receta.
    - Tiempo : Tiempo de preparación de la receta.
    - Dificultad : Dificultad de la receta.
    - Ocasion : Ocasión para la que está pensada la receta.
    - Ingredientes : Lista de ingredientes necesarios para la receta.
    - Elaboración : Pasos a seguir para elaborar la receta.
Ej de receta de la seccion de postres:
[ "postres",
    {
        'Nombre': 'Tarta de queso',
        'Comensales': 4,
        'Tiempo': 60,
        'Dificultad': 'Fácil',
        'Ocasion': 'Merienda',
        'Ingredientes': [{Queso: 200g}, {Azúcar: 100g}, {Huevos: 3}],
        'Elaboración': ['Mezclar los ingredientes y hornear.', 'Dejar enfriar y servir.']
    }
]

'''
url = "https://www.recetasgratis.net/"

def obtener_recetas():
    '''
    Función principal para obtener todas las recetas de la web Recetas gratis.
    '''
    res = []
    sopa = bs(urllib.request.urlopen(url),"lxml")
    secciones = sopa.find('main').find('div',{"data-js-selector":"items"}).find("div",{"class":"categorias-home clear"}).find_all("div",{"class":"categoria"})
    link_secciones = [seccion.find("a",{"class":"titulo"}).get('href') for seccion in secciones if seccion.get("data-label") != "Consejos de cocina" and seccion.get("data-label") != "Cócteles y bebidas"]
    for link in link_secciones:
        recetas = obtener_recetas_seccion(link)
        res.append(recetas)
    return res

def obtener_recetas_seccion(link):
    '''
    Función para obtener todas las recetas de una sección. Al final de este proceso recetas será una lista de diccionarios como esta:
    { "postres":
        {
            'Nombre': 'Tarta de queso',
            'Comensales': 4,
            'Tiempo': 60,
            'Dificultad': 'Fácil',
            'Ingredientes': [{Queso: 200g}, {Azúcar: 100g}, {Huevos: 3}],
            'Elaboración': ['Mezclar los ingredientes y hornear.', 'Dejar enfriar y servir.']
        }
    }
    '''
    recetas = dict()
    sopa = bs(urllib.request.urlopen(link),"lxml")
    paginador = sopa.find("div",{"class":"paginator"})
    paginas = [a.get("href") for a in paginador.find_all("a")[:-1]]
    nombre_seccion = sopa.find("ul",{"class":"breadcrumb"}).find_all("li")[1].text
    print(nombre_seccion.upper().center(200,"-"))
    recetas[nombre_seccion] = []
    obtener_recetas_pagina(link,recetas,nombre_seccion)
    for pagina in paginas:
        obtener_recetas_pagina(pagina,recetas,nombre_seccion)
    print("Número de recetas obtenidas: ",len(recetas[nombre_seccion]))
    return recetas
        


def obtener_recetas_pagina(link,recetas,nombre_seccion):
    '''
    Función para obtener todas las recetas de una página. 
    '''
    sopa = bs(urllib.request.urlopen(link),"lxml")
    divs = sopa.find_all("div",{"class":"resultado link"})
    link_recetas = [div.find("a",{"class":"titulo titulo--resultado"}) for div in divs]
    for link in link_recetas:
        if "recetas" in link.text.lower() or "receta" not in link.text.lower():
            continue
        receta = obtener_receta(link.get('href'))
        recetas[nombre_seccion].append(receta)

def obtener_receta(link):
    '''
    Función para obtener los datos de una receta.
    '''
    receta = dict()
    sopa = bs(urllib.request.urlopen(link),"lxml")
    nombre = sopa.find("h1",{"class":"titulo titulo--articulo"}).get_text(strip=True)
    receta['Nombre'] = nombre
    print("\n" + nombre.upper().center(80,"-") + "\n")
    detalles = sopa.find("div",{"class":"recipe-info"})
    try:
        comensales = detalles.find("span",{"class":"property comensales"}).get_text(strip=True)
    except Exception as e:
        comensales = "No especificado"
        print(f"Error en comensales: {e}")
    try:
        duracion = detalles.find("span",{"class":"property duracion"}).get_text(strip=True)
    except Exception as e: 
        duracion = "No especificada"
        print(f"Error en duracion: {e}")
    try:
        comida = detalles.find("span",{"class":"property para"}).get_text(strip=True)
    except Exception as e:
        comida = "Otra"
        print(f"Error en tipo de ocasion: {e }")
    try:
        filtros_prov = [tags.get_text(strip=True) for tags in detalles.find("div",{"class":"properties inline"}).contents[2:]]
        filtros = []
        for filtro in filtros_prov:
            for tag in filtro.split(","):
                if tag != "":
                    filtros.append(tag.strip())
    except Exception as e:
        filtros = "generico"
        print(f"Error en filtros: {e}")
    try:
        dificultad = detalles.find("span",{"class":"property dificultad"}).get_text(strip=True)
    except Exception as e:
        dificultad = "No especificada"
        print(f"Error en dificultad: {e}")
    try:
        ingredientes = detalles.find("ul").find_all("li",{"class":"ingrediente"})
        lista_ing = [li.find("label").get_text(strip=True) for li in ingredientes if "titulo" not in li.get("class") ]
        elaboracion = [div.find_next().get_text(strip=True) for div in sopa.find_all("div",{"class":"orden"})]
    except Exception as e:
        print(f"Error fatal en ingredientes o elaboracion: {e} se devuelve None")
        return None
    receta['Imagen'] = sopa.find("img",{"alt":nombre}).get('src')
    receta['Comensales'] = comensales
    receta['Tiempo'] = duracion
    receta['Dificultad'] = dificultad
    receta['Ingredientes'] = lista_ing
    receta['Ocasion'] = comida
    receta['Elaboracion'] = elaboracion
    receta['Filtros'] = filtros
    print(f"Todos los datos de la receta {nombre} han sido obtenidos.")
    return receta
if __name__ == '__main__':
    obtener_recetas()

