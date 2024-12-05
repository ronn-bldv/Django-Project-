from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class MovieCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE)
    available_seats = models.JSONField(default=dict)  # Seat layout as JSON
    show_times = models.JSONField()  # E.g., {"times": ["12:00", "15:00", "18:00"]}

    def __str__(self):
        return self.title

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)  # Format: Row-Number (e.g., A-1)
    show_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat {self.seat_number}"
