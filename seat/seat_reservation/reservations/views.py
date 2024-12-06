from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Seat, Reservation
from .forms import SeatReservationForm

from django.shortcuts import render

def reserve_seat(request):
    # Define the seat grid: rows and columns
    seat_rows = ['A', 'B', 'C', 'D']
    seat_columns = range(1, 11)

    # Example: list of reserved seats (this would typically come from a database or session)
    reserved_seats = ['A1', 'B3', 'C5']  # Placeholder list

    # Generate seat IDs like A1, A2, ..., D10
    seats = [f"{row}{col}" for row in seat_rows for col in seat_columns]

    # Organize seats with their status (available or reserved)
    seat_status = {
        seat: 'reserved' if seat in reserved_seats else 'available'
        for seat in seats
    }

    if request.method == "POST":
        selected_seat = request.POST.get("seat")
        reserved_seats.append(selected_seat)  # Mark the seat as reserved
        seat_status[selected_seat] = 'reserved'
        return render(request, "reservation_success.html", {"seat": selected_seat})

    return render(request, "reserve_seat.html", {"seat_status": seat_status})

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})