from django.contrib import admin
from .models import MovieCategory, Movie, Reservation

admin.site.register(MovieCategory)
admin.site.register(Movie)
admin.site.register(Reservation)
