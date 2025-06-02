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

   #Obtiene todas las imágenes como Cards llamando a getAllImages().
   #Recorre cada Card y verifica si 'name' (sin distinción de mayúsculas)
   #está contenido en card.name. Si coincide, lo agrega a filtered_cards.
   #Devuelve filtered_cards, que es una lista de Card.
   
    filtered_cards = []
    name_lower = name.lower()
    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name_lower in card.name.lower():
         filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    #Obtiene todas las imágenes como Cards llamando a getAllImages().
    #Recorre cada Card; dentro de cada card.types (lista de strings), busca si
    #alguno coincide con type_filter (sin distinción de mayúsculas).  
    #Si coincide, agrega esa Card a filtered_cards y sale del bucle interno.
    #Devuelve filtered_cards, que es una lista de Card.
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
     #Convierte los datos del request.POST en un objeto Card usando translator.fromTemplateIntoCard.
     #Asigna fav.user = get_user(request) para asociar esa Card al usuario autenticado.
     #Llama a repositories.save_favourite(fav) para persistirla en la base de datos.
     #Devuelve el Favourite recién creado (o None si hubo error)
    fav = translator.fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
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
    #Extrae favId = request.POST.get('id').
    #Llama a repositories.delete_favourite(favId) para eliminar ese registro en la BD.
    #Devuelve True si se eliminó, False si no existía o hubo error.
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    #Busca type_id en config.TYPE_ID_MAP usando type_name.lower().
    #Si no existe, retorna None.
    #Si existe, llama a transport.get_type_icon_url_by_id(type_id) y devuelve su URL.
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)