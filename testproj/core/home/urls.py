# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_cart/<uuid:movie_uid>/', views.add_cart, name='add-cart'),
    path('error_page/', views.error_page, name='error_page'),
    path('book_movie/<uuid:movie_uid>/', views.book_movie, name='book_movie'),

    # Add any other URLs for your app here
]
