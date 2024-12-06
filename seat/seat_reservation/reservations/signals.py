from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Venue, Seat

@receiver(post_save, sender=Venue)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for row in range(1, instance.rows + 1):
            for seat_number in range(1, instance.seats_per_row + 1):
                Seat.objects.create(venue=instance, row=row, number=seat_number)
