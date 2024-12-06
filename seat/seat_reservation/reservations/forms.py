from django import forms
from .models import Reservation, Seat

class SeatReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available seats
        self.fields['seat'].queryset = Seat.objects.filter(is_reserved=False)
