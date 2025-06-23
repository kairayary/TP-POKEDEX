# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):

    #Para obtener todas las imágenes como lista de Card
    images = services.getAllImages() #Se llama para conseguir todas las tarjetas de Pokémon
    
    #Para obtener Lista de Favoritos, si no hay usuario logueado, devuelve una lista vacia []
    if request.user.is_authenticated:
        favourite_list= services.getAllFavourites(request)
    else:
        favourite_list = []  

    return render(request, 'home.html', {
        'images': images, 
        'favourite_list': favourite_list
          })


# función utilizada en el buscador.
def search(request):
 
  if request.method == 'POST': 
    name = request.POST.get('query', '').strip()

    # Llamamos al servicio: si name es "", filterByCharacter devolverá todas las imágenes
    images = services.filterByCharacter(name)
    # Obtenemos favoritos solo si el usuario está logueado
    if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
    else:
            favourite_list = []

    return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    # Si por algún motivo entraron con GET, redirigimos a home
    return redirect('home')
  
# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '').strip()

    if type:
        images = services.filterByType(type) # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = services.getAllFavourites(request) if request.user.is_authenticated else []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función para registrar nuevo usuario
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Verificamos si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Ese nombre de usuario ya está registrado.'})
        
        # Creamos el nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('login')

    return render(request, 'register.html')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
   favourite_cards = services.getAllFavourites(request)
   return render(request, 'favourites.html', {
        'favourite_list': favourite_cards
    })
@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')