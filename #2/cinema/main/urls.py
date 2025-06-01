from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('film/', views.film, name='film'),
    path('sale/', views.sale, name='sale'),
    path('proiezioni/', views.proiezioni, name='proiezioni'),

    path('api/film/', views.film_api, name='api_film'),
    path('api/sale/', views.sale_api, name='sale_api'),
    path('api/proiezioni/', views.proiezioni_api, name='proiezioni_api'),

    path('film/insert/', views.film_insert, name='film_insert'),
    path('film/update/', views.film_update, name='film_update'),
    path('film/delete/<str:codice>/', views.film_delete, name='film_delete'),
]
