from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Movie, Reservation
from django.shortcuts import render

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Create the user
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()  # Create an empty form for GET requests

    return render(request, 'movies/register.html', {'form': form})
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('available_movies')
    return render(request, 'movies/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def available_movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies/available_movies.html', {'movies': movies})

def select_seats(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats')
        show_time = request.POST['show_time']

        for seat in selected_seats:
            row, number = seat.split('-')
            Reservation.objects.create(
                user=request.user,
                movie=movie,
                seat_number=seat,
                show_time=show_time,
            )
            movie.available_seats[row].remove(int(number))
        movie.save()
        return redirect('cart')

    return render(request, 'movies/select_seats.html', {
        'movie': movie,
        'available_seats': movie.available_seats,
    })

def cart(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'movies/cart.html', {'reservations': reservations})

def homepage(request):
    return render(request, 'movies/homepage.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})