from django.urls import path
from . import views

urlpatterns = [
    path('', views.reserve_seat, name='reserve_seat'),  # Main reservation page at /reserve/
    path('signup/', views.signup, name='signup'),  # Signup page at /reserve/signup/
]
