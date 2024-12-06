from django.shortcuts import render, redirect
from .models import Movie, MovieDateTime, Seat, Cart, CartItems
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User

# Home view showing all movies
def home(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, "home.html", context)

# Login view
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        
        if not user_obj.exists():
            messages.error(request, "Username not found")
            return redirect('/login/')
        
        user_obj = authenticate(username=username, password=password)
        
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        
        messages.error(request, "Wrong Password")
        return redirect('/login/')
    
    return render(request, "login.html")

# Register view
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')  # Add password confirmation

        # Check if passwords match
        if password != password_confirmation:
            messages.error(request, "Passwords do not match")
            return redirect('/register/')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is taken")
            return redirect('/register/')
        
        # Create the user
        user_obj = User.objects.create(username=username)
        user_obj.set_password(password)
        user_obj.save()
        
        # Inform the user and redirect to login
        messages.success(request, "Account created successfully!")
        return redirect('/login/')
    
    return render(request, "register.html")


# Add movie to the cart with selected date, time, and seat
@login_required(login_url='/login/')
def add_cart(request, movie_uid):
    movie_obj = Movie.objects.get(uid=movie_uid)
    date = request.POST.get('date')
    time = request.POST.get('time')
    seat_number = request.POST.get('seat')  # Assuming 'seat' is the seat number

    # Debugging the date and time before processing
    print(f"Selected date: {date}")
    print(f"Selected time: {time}")

    # Find the MovieDateTime instance matching the selected date and time
    try:
        movie_datetime = MovieDateTime.objects.filter(date=date, time=time).first()

        if not movie_datetime:
            messages.error(request, "Invalid date or time selected.")
            return redirect('/error_page/')  # Replace with an actual error page URL

        # Find the Seat instance matching the selected seat number and the movie datetime
        seat = Seat.objects.filter(movie_datetime=movie_datetime, seat_number=seat_number, is_taken=False).first()

        if not seat:
            # Handle case where the seat is not available
            return redirect('/error_page/')  # Replace with an actual error page URL

        # Create a cart if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        print(f"Cart created: {created}, Cart ID: {cart.id}")

        # Add the movie to the cart with the selected date, time, and seat
        CartItems.objects.create(
            cart=cart,
            movie=movie_obj,
            movie_datetime=movie_datetime,  # Pass the MovieDateTime instance
            seat=seat  # Pass the Seat instance
        )

        # Mark the seat as taken after it is added to the cart
        seat.is_taken = True
        seat.save()

        return redirect('/cart/')

    except MovieDateTime.DoesNotExist:
        messages.error(request, "Invalid date or time selected.")
        return redirect('/error_page/')  # Replace with an actual error page URL

# View cart showing selected movies, dates, times, and seats
@login_required(login_url='/login/')
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        print(f"Cart items: {cart.cart_items.all()}")  # Debugging Cart items
        context = {'cart': cart}
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    return render(request, "cart.html", context)

# Remove movie from cart
@login_required(login_url='/login/')
def remove_cart_item(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        messages.error(request, "Error removing the cart item.")
        return redirect('/cart/')

# Handle payment (Optional)
@login_required(login_url='/login/')
def pay(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        cart.is_paid = True
        cart.save()
        for item in cart.cart_items.all():
            item.is_paid = True
            item.save()

        messages.success(request, "Payment successful!")
        return redirect('/')
    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('/')

@login_required(login_url="/login/")
def book_movie(request, movie_uid):
    movie = Movie.objects.get(uid=movie_uid)
    available_dates_times = movie.available_dates.all()

    if request.method == "POST":
        # Get the selected date and time from the form
        selected_date = request.POST.get('date')
        selected_time = request.POST.get('time')
        selected_seat_numbers = request.POST.getlist('seats')  # List of selected seat numbers

        # Validate the selected date and time
        if not selected_date or not selected_time:
            messages.error(request, "Please select both a date and time.")
            return redirect('book_movie', movie_uid=movie_uid)

        try:
            # Convert the selected date from the format "Dec. 12, 2024" to "YYYY-MM-DD"
            selected_date_obj = datetime.strptime(selected_date, "%b. %d, %Y").date()
            print(f"Converted selected date: {selected_date_obj}")  # Debugging print

            # Normalize the time string to match the expected format
            normalized_time = selected_time.strip().replace('a.m.', 'AM').replace('p.m.', 'PM')
            print(f"Normalized selected time: {normalized_time}")  # Debugging print

            # Convert the selected time from "6 AM" format to 24-hour format (e.g., "06:00")
            selected_time_obj = datetime.strptime(normalized_time, "%I %p").strftime("%H:%M")
            print(f"Converted selected time: {selected_time_obj}")  # Debugging print

            # Find the MovieDateTime instance matching the selected date and time
            movie_datetime = MovieDateTime.objects.get(
                date=selected_date_obj, time=selected_time_obj
            )
        except ValueError as e:
            messages.error(request, f"Invalid date or time format. {e}")
            return redirect('book_movie', movie_uid=movie_uid)
        except MovieDateTime.DoesNotExist:
            messages.error(request, "Invalid date or time selected.")
            return redirect('book_movie', movie_uid=movie_uid)

        # Find the corresponding seats that the user has selected
        seats_to_book = Seat.objects.filter(
            movie_datetime=movie_datetime,
            seat_number__in=selected_seat_numbers,
            is_taken=False  # Only select available seats
        )

        # Check if all selected seats are available
        if len(seats_to_book) != len(selected_seat_numbers):
            messages.error(request, "Some selected seats are already taken.")
            return redirect('book_movie', movie_uid=movie_uid)

        # Create or get the user's cart if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        print(f"Cart created: {created}, Cart UID: {cart.uid}")  # Debugging print (use cart.uid)

        # Add the selected seats as a single cart item (storing seat numbers as a comma-separated string)
        seat_numbers_str = ",".join(selected_seat_numbers)

        CartItems.objects.create(
            cart=cart,
            movie=movie,
            movie_datetime=movie_datetime,
            seat_numbers=seat_numbers_str  # Store the seat numbers as a string
        )

        # Mark the selected seats as taken
        for seat in seats_to_book:
            print(f"Marking {seat.seat_number} as taken")  # Debugging print
            seat.is_taken = True  # Mark the seat as taken
            seat.save()

        messages.success(request, f"{len(seats_to_book)} seats booked successfully!")
        return redirect('cart')  # Redirect to the cart page

    return render(request, "book_movie.html", {
        'movie': movie,
        'available_dates_times': available_dates_times,
    })

@login_required(login_url="/login/")
def cancel_ticket(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)

        # If a single seat is assigned, update its 'is_taken' status
        if cart_item.seat:
            cart_item.seat.is_taken = False
            cart_item.seat.save()
        elif cart_item.seat_numbers:
            # If no single seat assigned, but seat numbers exist
            seat_numbers = cart_item.seat_numbers.split(',')
            for seat_number in seat_numbers:
                try:
                    seat = Seat.objects.get(seat_number=seat_number)  # Use 'seat_number' field
                    seat.is_taken = False
                    seat.save()
                except Seat.DoesNotExist:
                    messages.error(request, f"Seat number {seat_number} not found.")
                    return redirect('cart')
            messages.info(request, "Seat numbers freed, but no specific seat was assigned.")
        else:
            # If neither seat nor seat numbers exist
            messages.error(request, "No seat information available to cancel.")
            return redirect('cart')

        # Delete the cart item after handling the seat(s)
        cart_item.delete()
        messages.success(request, "Ticket canceled successfully.")
        return redirect('cart')

    except CartItems.DoesNotExist:
        messages.error(request, "Ticket not found.")
        return redirect('cart')

@login_required(login_url="/login/")
def checkout(request):
    cart = Cart.objects.get(user=request.user, is_paid=False)

    if not cart.cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    # You could process payment or confirmation here
    cart.is_paid = True
    cart.save()

    messages.success(request, "Your order has been successfully placed.")
    return redirect('home')

def error_page(request):
    return render(request, 'error_page.html')

def logout_user(request):
    logout(request)
    messages.success(request, "User logged out")
    return redirect('/login/')