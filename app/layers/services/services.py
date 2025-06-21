# capa de servicio/lógica de negocio

from flask import redirect
from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from django.core.cache import cache

# función que devuelve un listado de cards. Cada card 
# representa una imagen de la API de Pokemon
# punto (2) services.py:
def getAllImages():
    cache_key = "pokemon_list_all"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data  # retorna desde la cache si ya existe

    # si no está en caché, se consulta la API usando transport.py
    raw_data_list = transport.getAllImages()
    cards = []

    for poke_data in raw_data_list:
        card = {
            "name": poke_data["name"].capitalize(),
            "id": poke_data["id"],
            "height": poke_data["height"],
            "weight": poke_data["weight"],
            "types": [t["type"]["name"] for t in poke_data["types"]],
            "base": poke_data["base_experience"],
            "image": poke_data["sprites"]["front_default"],
        }
        cards.append(card)

    cache.set(cache_key, cards, timeout=3600)  # guarda en caché 1 hora
    return cards


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card["name"].lower():
            filtered_cards.append(card)

    return filtered_cards


# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        if type_filter.lower() in card["types"]:
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        fav = translator.fromTemplateIntoCard(request)
        fav.user = get_user(request)
        return repositories.save_favourite(fav) # lo guardamos en la BD
    
    return redirect('home')
# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user) # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite) # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)