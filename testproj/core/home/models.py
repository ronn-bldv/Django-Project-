from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Base Model to be inherited by other models
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

# Movie Category Model
class MovieCategory(BaseModel):
    category_name = models.CharField(max_length=100)

# Movie Model
class Movie(BaseModel):
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE, related_name="movies")
    movie_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.ImageField(null = True, blank = True, upload_to= "images/")
    available_dates = models.ManyToManyField('MovieDateTime', related_name="movies")

# Movie DateTime Model
class MovieDateTime(BaseModel):
    date = models.DateField()
    time = models.TimeField()

# Seat Model
class Seat(BaseModel):
    movie_datetime = models.ForeignKey(MovieDateTime, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    is_taken = models.BooleanField(default=False)

# Cart Model
class Cart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="carts")
    is_paid = models.BooleanField(default=False)

# CartItems Model
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_datetime = models.ForeignKey(MovieDateTime, on_delete=models.CASCADE)  # ForeignKey to MovieDateTime
    seat = models.ForeignKey(Seat, null=True, blank=True, on_delete=models.CASCADE)  # Keep for single seat bookings if needed
    seat_numbers = models.CharField(max_length=255, null=True, blank=True)  # To store comma-separated seat numbers

