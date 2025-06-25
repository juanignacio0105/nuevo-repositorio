# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():

    # traer un listado de imágenes crudas desde la API (ver transport.py)
    json_collection = transport.getAllImages() #esto hace que el json collection sea transportado con imagenes crudas  
    images = [] # lista que contendrá las cards transformadas a partir de las imágenes crudas.
    for object in json_collection:#se recorre el listado de imágenes crudas.
        card = translator.fromRequestIntoCard(object) #usa informacion de la api para transformarlo en cards
        types_aux = []#se crea una lista auxiliar para almacenar los iconos de los tipos de cada card.
        #se recorre cada tipo de la card y se obtiene el icono correspondiente a cada tipo usando su nombre.
        for t in card.types:
            types_aux.append(get_type_icon_url_by_name(t)) #se obtiene el icono de cada tipo de Pokemon usando su nombre.
        card.types_imgs = types_aux 
        images.append(card) 
 
    return images
 # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas. 

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py)''
    fav.user = get_user(request) # le asignamos el usuario correspondiente.
    existing= repositories.get_all_favourites(fav.user)#buscamos si ya existe un favorito con el mismo ID
    if any(f[ ' name ']== fav.name for f in existing):
        return None 
    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user) # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []
        for favourite in favourite_list:
            card = translator.fromFavouriteIntoCard(favourite)  # desde un favorito obtenemos la Card
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