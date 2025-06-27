# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    #Para obtener todas las imágenes como lista de Card
    images = services.getAllImages()#Se llama para conseguir todas las tarjetas de Pokémon

     #Para obtener Lista de Favoritos, si no hay usuario logueado, devuelve una lista vacia []
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)
        #Se extare solos los nombres favoritos para facilitar comparación en el template
        favourite_names = [fav.name for fav in favourite_list]
    else:
        favourite_list = []
        favourite_names = []

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list,
        'favourite_names': favourite_names  # variables enviadas al template
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
 #agregar favorito
def agregar_favorito(request):
    try:
        services.saveFavourite(request)
       #messages.success(request, "¡Pokémon agregado a favoritos!")
    except Exception as e:
        messages.warning(request, str(e))  # muestra el mensaje real del error
    return redirect('home/')

# función para registrar nuevo usuario
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validación
        if not all([first_name, last_name, username, email, password]):
            return render(request, 'register.html', {'error': 'Todos los campos son obligatorios.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Ese nombre de usuario ya existe.'})

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Enviar mail con credenciales
        subject = 'Registro exitoso en la App Pokémon'
        message = f"Hola {first_name},\n\nTu cuenta fue creada exitosamente.\n\nUsuario: {username}\nContraseña: {password}\n\n¡Bienvenido!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

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
    result = services.saveFavourite(request)

    if result is None:
        messages.warning(request, 'Ese Pokémon ya está en tus favoritos.')
    else:
        messages.success(request, '¡Pokémon agregado a favoritos!')

    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')