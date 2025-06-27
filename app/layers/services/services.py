# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    raw_list = transport.getAllImages()
    card_list = []
    for raw in raw_list:
        card = translator.fromRequestIntoCard(raw)
        card_list.append(card)
    return card_list

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):

    name_lower = name.strip().lower()
    if not name_lower:
        # Si no ingresaron dato, devolvemos todas las imágenes
        return getAllImages()
    filtered_cards = []
    for card in getAllImages():
        if name_lower in card.name.lower():
            filtered_cards.append(card)
    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []
    filter_lower = type_filter.lower()
    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        for t in card.types:
            if t.lower() == filter_lower:
                filtered_cards.append(card)
                break

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)# transformamos un request en una Card (ver translator.py
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    # Chequeamos si ya existe ese favorito para ese usuario
    existing = repositories.find_favourite_by_name_and_user(fav.name, fav.user)
    if existing:
        raise Exception("Ya está en favoritos")  # Se atrapa en views.py

    return repositories.save_favourite(fav)


# usados desde el template 'favourites.html'
def getAllFavourites(request):

    #Si el usuario NO está autenticado, retorna lista vacía.
    #Si está autenticado, pide a repositories.get_all_favourites(user) la lista de diccionarios,
    #luego convierte cada diccionario en Card con translator.fromRepositoryIntoCard.
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user) # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for fav_dict in favourite_list:
            card = translator.fromRepositoryIntoCard(fav_dict) # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
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