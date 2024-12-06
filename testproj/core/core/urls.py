"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from home.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('', home, name='home'),
    path('book_movie/<uuid:movie_uid>/', book_movie, name='book_movie'),
    path('cart/', cart, name='cart'),
    path('cancel_ticket/<uuid:cart_item_uid>/', cancel_ticket, name='cancel_ticket'),
    path('checkout/', checkout, name='checkout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('', views.home, name='home'),
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
if settings.DEBUG :
    urlpatterns +=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
     
urlpatterns += staticfiles_urlpatterns()
