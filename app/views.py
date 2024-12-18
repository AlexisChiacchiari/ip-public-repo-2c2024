# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    home = request.POST.get('query', '')
    images = []
    images = services.getAllImages(home)
    favourite_list = []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images = services.getAllImages(search_msg)
        return render(request, 'home.html', { 'images': images})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        favourite_id = request.POST.get('favourite_id')
        if favourite_id:
            success = services.saveFavourite(request.user, favourite_id)
            if success:
                return redirect('favourites')
    return redirect('home')
    pass

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        favourite_id = request.POST.get('favourite_id')
        if favourite_id:
            success = services.deleteFavourite(request.user, favourite_id)
            if success:
                return redirect('favourites')
    return redirect('home')
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('index')
    pass