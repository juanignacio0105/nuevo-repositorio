from django.contrib import admin
from django.urls import path 
from . import views
from .views import login_view



urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('home/', views.home, name='home'),
    path('login/', login_view, name='login'),
    
    path('buscar/', views.search, name='buscar'),
    path('filter_by_type/', views.filter_by_type, name='filter_by_type'),

    path('favourites/', views.getAllFavouritesByUser, name='get-favourites'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('exit/', views.exit, name='exit'),
]