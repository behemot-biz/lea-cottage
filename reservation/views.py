from django.shortcuts import render, get_object_or_404, redirect
from product.models import StockItem
from .models import Reservation, MyReservation
from .forms import EditReservationForm, StoreReservationForm

# Create your views here.

def my_reservations(request):
    reservation_page = Reservation.objects.all().order_by('-updated_on').first()
    current_reservation = MyReservation.objects.filter(reserved_by=request.user, reservation_complete__lt=2).first()
    active_reservation =  MyReservation.objects.filter(reserved_by=request.user, reservation_complete__lt=2)
    old_reservations = MyReservation.objects.filter(reserved_by=request.user, reservation_complete=2)

    # # Handle form submission for editing the reservation
    if request.method == 'POST' and current_reservation:
        form = StoreReservationForm(request.POST, instance=current_reservation)
        if form.is_valid():
            form.save()  # Save changes to the reservation
            return redirect('reservation')  # Redirect back to reservation list

    else:
        form =  StoreReservationForm (instance=current_reservation) if current_reservation else None

    return render(
        request,
        'reservation/reservations_list.html',
        {
            "reservation_page": reservation_page,
            'current_reservation': current_reservation,
            'active_reservation': active_reservation,
            'form': form,
            'old_reservations': old_reservations,
        }
    )


def reservation_detail(request, id):
    # Change the filter to reservation_id instead of id
    reservation = get_object_or_404(MyReservation, reservation_id=id)
     # Only show the form if the reservation is not complete
    if reservation.reservation_complete == 0:
        form = StoreReservationForm(instance=reservation)
    else:
        form = None

    # return render(request, 'reservation/reservation_detail.html', {
    return render(request, 'reservation/reservations_list.html', {
        'reservation': reservation,
        'form': form  # Ensure the form is passed here
    })
    # return render(request, 'reservation/reservation_detail.html', {'reservation': reservation})


def add_to_reservation(request, stock_item_id):
    stock_item = get_object_or_404(StockItem, id=stock_item_id)
    
    # Get or create a reservation
    reservation, created = MyReservation.objects.get_or_create(
        reserved_by=request.user,
        reservation_complete=0  # Active reservation
    )
    
    # Add the stock item to the reservation
    stock_item.reservation = reservation
    stock_item.status = 1  # Mark as reserved
    stock_item.save()
    
    # return redirect('reservation_detail')
    return redirect('reservation')

def store_reservation(request, reservation_id):
    reservation = get_object_or_404(MyReservation, reservation_id=reservation_id)

    if reservation.reservation_complete == 0:  # Only complete if not already done
        if request.method == "POST":
            form = StoreReservationForm(request.POST, instance=reservation)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.reservation_complete = 1  # Mark as complete
                reservation.save()

                stock_items = reservation.get_stock_items()
                for stock_item in stock_items:
                    stock_item.status = 1  # Mark as reserved
                    stock_item.save()

                return redirect('reservation')
            else:
                print(form.errors) 
        else:
            form = StoreReservationForm(instance=reservation)
        
    else:
        form = None

    return render(
    request,
    'reservation/reservations_list.html',
    {
        'form': form,  # Ensure 'form' is passed
        'reservation': reservation,
    }
)


def edit_reservation(request, reservation_id):
    # Get the current reservation by reservation_id
    reservation = get_object_or_404(MyReservation, reservation_id=reservation_id)
    
    if request.method == 'POST':
        # Process the form submission
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()  # Save the updated reservation
            return redirect('reservation')  # Redirect to the reservations list or detail view
    else:
        # Display the form with the current reservation data
        form = EditReservationForm(instance=reservation)

    return render(
    request,
    'reservation/reservations_list.html',
    {
        'form': form,  # Ensure 'form' is passed
        'reservation': reservation,
    }
)
