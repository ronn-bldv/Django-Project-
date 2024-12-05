"""
URL configuration for MovieReservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movies import views
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Root URL now points to the homepage
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('movies/', views.available_movies, name='available_movies'),
    path('movies/int:movie_id/select_seats/', views.select_seats, name='select_seats'),
    path('cart/', views.cart, name='cart'),
    path('admin/', admin.site.urls),
]
