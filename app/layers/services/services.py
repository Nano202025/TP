# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    """
    Una funcion simple que recupera los datos crudos de todas las
    imagenes, las convierte en tarjetas y devuelve una lista de 
    tarjetas.
    """
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    list_of_cards = []                                          # Gody//guarda una lista de tarjetas
    for raw_image in transport.getAllImages():                  # Gody//un bucle que toma los datos crudos y los transforma en tarjetas
        card = translator.fromRequestIntoCard(raw_image)        # Gody//
        
        type_url = []                                           # Gody//
        for type in card.types:                                 # Gody//
            type_url.append(get_type_icon_url_by_name(type))    # Gody//

        card.types_url = type_url                               # Gody//
        list_of_cards.append(card)                              # Gody//

    return list_of_cards                                        # Gody//retorna las imagenes como una lista de tarjetas

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    """
    Una funcion simple que recibe como argumento una cadena
    con el nombre del Pokemon buscado. Y retorna una lista con las
    tarjetas que contengan, en su nombre, la cadena ingresada como
    argumento.
    """
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name in card.name:                        # Gody//agrege el if para que filtre por nombre
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    """
    Una funcion simple que recibe como argumento una cadena
    con el tipo de Pokemon buscado. Y retorna una lista con las
    tarjetas que corresponden con el tipo ingresado como argumento.
    """
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        if type_filter in card.types:                 # Gody//agregue el if para que filtre por tipo
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con los datos que se quiere agregar a favoritos.
    Esos datos se convierten en una tarjeta y se le asocia los datos
    del usuario. La tarjeta es guardada en los favoritos del usuario
    y se retorna una respuesta http.
    """
    fav = translator.fromTemplateIntoCard(request) # Gody//transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    """
    Una funcion simple que recibe como parametro una peticion http
    con la informacion del usuario, si es que éste ingresó sus credenciales.
    Si el usuario se autenticó, la función obtiene del repositorio los favoritos
    asociados al usuario, los convierte en tarjetas y devuelve una lista de tarjetas.
    En caso contrario devuelve una lista vacía.
    """
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user) # Gody//buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite) # Gody//convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion que debe borrarse de favoritos.
    Elimina el elemento de favoritos y devuelve una respuesta http.
    """
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    """
    Una funcion simple que recibe como argumento un tipo de pokemon
    y devuelve la url del icono que representa dicho tipo.
    """
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)