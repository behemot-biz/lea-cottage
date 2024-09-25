from django.shortcuts import render, get_object_or_404, redirect
from product.models import StockItem
from .models import Reservation, MyReservation
from .forms import CompleteReservationForm

# Create your views here.
# def my_reservations(request):
#     stock_items = StockItem.objects.filter(status=1)  # Access StockItem data

#     return render(request, 'reservationn/reservations_list.html', {'stock_items': stock_items})


def my_reservations(request):
    """
    Renders the my_reservations page
    """
    reservation_page = Reservation.objects.all().order_by('-updated_on').first()
    current_reservation = MyReservation.objects.all().order_by('-reservation_id').first()
    old_reservation = MyReservation.objects.filter(reservation_complete=1)
    stock_items = StockItem.objects.filter(status=1)
    # old_stock_items = StockItem.objects.filter(status=2)
    


    # Pass the form for the specific reservation
    if current_reservation:
        form = CompleteReservationForm(instance=current_reservation)
    else:
        form = None


    return render(
        request,
        "reservation/reservations_list.html",
        # "reservation/reservations_list.html",
        {
            "reservation_page": reservation_page,
            "current_reservation": current_reservation,
            "stock_items": stock_items,
            "old_reservation": old_reservation,
            # "old_stock_items": old_stock_items,
            'form': form  # Pass the form here
        },
    )


def reservation_detail(request, id):
    # Change the filter to reservation_id instead of id
    reservation = get_object_or_404(MyReservation, reservation_id=id)
     # Only show the form if the reservation is not complete
    if reservation.reservation_complete == 0:
        form = CompleteReservationForm(instance=reservation)
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

def complete_reservation(request, reservation_id):
    reservation = get_object_or_404(MyReservation, reservation_id=reservation_id)

    if reservation.reservation_complete == 0:  # Only complete if not already done
        if request.method == "POST":
            form = CompleteReservationForm(request.POST, instance=reservation)
            if form.is_valid():
                # Update the reservation with the note and pickup date
                reservation = form.save(commit=False)
                reservation.reservation_complete = 1  # Mark as complete
                reservation.save()

                # Mark all associated stock items as reserved (status=1)
                stock_items = reservation.get_stock_items()
                for stock_item in stock_items:
                    stock_item.status = 1  # Mark as reserved
                    stock_item.save()

                return redirect('reservation')
                # return redirect('reservation', id=reservation.reservation_id)
                # return redirect('reservation_detail', id=reservation.reservation_id)
        else:
            form = CompleteReservationForm(instance=reservation)
    else:
        form = None

    return render(request, 'reservation', {'reservation': reservation, 'form': form})
    # return render(request, 'reservations_list.html', {'reservation': reservation, 'form': form})
    # return render(request, 'reservation/reservations_list.html', {'reservation': reservation, 'form': form})