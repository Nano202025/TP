# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    """
    Una funcion simple que envia a renderizar la pagina
    de inicio.
    """
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    """
    Una funcion simple que se encarga de enviar a renderizar
    las imagenes en forma de tarjetas. Tambien envia informacion
    sobre los favoritos del usuario para renderizar el botón
    correspondiente.
    """
    images = services.getAllImages()                            # Gody//
    favourite_list = []

    for img_card in services.getAllFavourites(request):         # Gody//
        favourite_list.append(img_card.name)                    # Gody//
    
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    """
    Una funcion simple que recibe como argumento una peticion http con
    informacion del nombre que el usuario esta buscando. Realiza la
    busqueda y envia a renderizar las tarjetas resultantes de la busqueda.
    Tambien envia informacion de los favoritos para que se renderice
    correctamente el boton favoritos.
    """
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        for img_card in services.getAllFavourites(request):     # Gody//
            favourite_list.append(img_card.name)                # Gody//lista los nombres de pokemon en favoritos

        for img_card in services.getAllImages():                # Gody//filtra las imagenes por nombre
            if img_card.name == name.lower():                   # Gody//
                images.append(img_card)                         # Gody//
        
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    """
    Una funcion simple que recibe como argumento una peticion http con
    informacion del tipo que el usuario esta buscando. Realiza la
    busqueda y envia a renderizar las tarjetas resultantes de la busqueda.
    Tambien envia informacion de los favoritos para que se renderice
    correctamente el boton favoritos.
    """
    type = request.POST.get('type', '')
    print(type)

    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        for img_card in services.getAllFavourites(request):     # Gody//
            favourite_list.append(img_card.name)                # Gody//lista los nombres de pokemon en favoritos

        for img_card in services.getAllImages():                # Gody//un bucle que filtra las imagenes por tipo
            if type in img_card.types:                          # Gody//
                images.append(img_card)                         # Gody//
        
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion del usuario, si es que inició sesion. Y envia a
    renderizar, usando la plantilla favoritos, las imagenes de los 
    pokemon que esten agregados a favoritos.
    """
    favourite_list = services.getAllFavourites(request)         # Gody//
    return render(request, 'favourites.html', { 'favourite_list': favourite_list }) # Gody//

@login_required
def saveFavourite(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion de la tarjeta que el usuario que agregar a 
    favoritos. Se agrega la tajeta a favoritos y se vuelve a cargar la
    pantalla de galeria.
    """
    services.saveFavourite(request)
    return home(request)

@login_required
def deleteFavourite(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion de la tarjeta que el usuario quiere quitar de 
    favoritos. Se elimina la tajeta de favoritos y se vuelve a cargar la
    pantalla favoritos.
    """
    services.deleteFavourite(request)
    return getAllFavouritesByUser(request)

@login_required
def exit(request):
    """
    Una funcion simple que permite cerrar la sesion del usuario.
    Luego de cerrar sesion, se redirije al usuario a la pantalla
    de inicio.
    """
    logout(request)
    return redirect('home')