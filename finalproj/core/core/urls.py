from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('remove_cart_item/<cart_item_uid>', remove_cart_item, name='remove_cart'),
    path('add_cart/<movie_uid>', add_cart , name="add-cart"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path("admin/", admin.site.urls),
    path('logout_user', views.logout_user, name='logout'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
if settings.DEBUG :
    urlpatterns +=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
     
urlpatterns += staticfiles_urlpatterns()