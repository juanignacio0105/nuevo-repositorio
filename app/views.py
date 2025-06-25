# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login #se importan las funciones de autenticación y login
from django.contrib import messages # #se importa el módulo de mensajes para mostrar mensajes al usuario


def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')

def index_page(request):
    return render(request, 'index.html')

def getAllImagesAndFavouriteList(request):
    images = services.getAllImages()
    return images 

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = getAllImagesAndFavouriteList(request)
    favourite_list = services.getAllFavourites(request) # obtenemos el listado de favoritos del usuario logueado.
    favourite_list_ids = [f["id"] for f in favourite_list] # obtenemos los ids de los favoritos para poder compararlos con las imágenes.

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourite_list_ids': favourite_list_ids })
# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')
    images = getAllImagesAndFavouriteList(request)

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = getAllImagesAndFavouriteList(request) #llamamos a la funcion: getAllImagesAndFavouriteList(request) que trae todas las imágenes de la API.
        imagenesf = []
        for img in images:
            if name.lower() in img.name.lower():#se compara si el nombre de la imagen contiene lo que escribió el usuario (name), sin importar mayúsculas/minúsculas (lower()).
                imagenesf.append(img)# agregamos a la lista imagenesf las imágenes que cumplen con el criterio de búsqueda.
    else:
                imagenesf = images # si el usuario no ingresó nada, se muestran todas las imágenes.


    favourite_list = []
    
    return render(request, 'home.html', { 'images': imagenesf, 'favourite_list': favourite_list })

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get("type", "")
    if type != '':
        images = getAllImagesAndFavouriteList(request)
        filtered_images = []
        for img in images:
            if any(type == t.lower() for t in img.types):
                filtered_images.append(img)
        favourite_list = []
        return render(request, 'home.html', { 'images': filtered_images, 'favourite_list':favourite_list})        
        
    
    return redirect("home")
    

        

    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, "favourites.html", {"favourite_list": favourite_list})

    

@login_required
def saveFavourite(request):
       if request.method == 'POST':
        services.saveFavourite(request)
        return redirect('home')

    

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
        return redirect('get-favourites')
    

@login_required
def exit(request):
    logout(request)
    return redirect('home')
