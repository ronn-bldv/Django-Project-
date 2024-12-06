from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Seat(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="seats")
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Row {self.row}, Seat {self.number} in {self.venue.name}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} reserved {self.seat}"
