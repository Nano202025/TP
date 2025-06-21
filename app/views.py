# capa de vista/presentación
import requests
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Favourite

def index_page(request):
    return render(request, 'index.html')

# punto (1) views.py:
# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos,
# ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourites = Favourite.objects.filter(user=request.user) if request.user.is_authenticated else []
    favourite_list_names = [f.name for f in favourites]

    
    return render(request, 'home.html', {
        'images': images,
        'favourite_list_names': favourite_list_names,
    })



# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip()

    if name == '':
        return redirect('home')  # si está vacío, volvemos a home

    images = services.filterByCharacter(name)
    favourite_list = services.getAllFavourites(request) if request.user.is_authenticated else []

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })



# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = services.filterByType(type) # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = services.getAllFavourites(request) if request.user.is_authenticated else []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    
    favourite_list = services.getAllFavourites(request)
    
    return render(request, 'favourites.html', {
        'favourite_list': favourite_list
    })

@login_required
def saveFavourite(request):
    
    if request.method == 'POST':
        
        result = services.saveFavourite(request)
        if result:  # se guardó correctamente
            return redirect('home')
        else:
            return render(request, 'error.html', { 'message': 'No se pudo guardar el favorito.' })
    return redirect('home')


@login_required
def deleteFavourite(request):
    
    if request.method == 'POST':
        
        services.deleteFavourite(request)
    return redirect('favoritos')


@login_required
def exit(request):
    logout(request)
    return redirect('home')