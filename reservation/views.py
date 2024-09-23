from django.shortcuts import render, get_object_or_404, redirect
from .models import StockItem, MyReservation
from .models import Reservation

# Create your views here.
# def my_reservations(request):
#     stock_items = StockItem.objects.filter(status=1)  # Access StockItem data

#     return render(request, 'reservationn/reservations_list.html', {'stock_items': stock_items})


def my_reservations(request):
    """
    Renders the my_reservations page
    """
    reservation_page = Reservation.objects.all().order_by('-updated_on').first()
    stock_items = StockItem.objects.filter(status=1)
    old_stock_items = StockItem.objects.filter(status=2)
    

    return render(
        request,
        "reservation/reservations_list.html",
        {
            "reservation_page": reservation_page,
             "stock_items": stock_items,
             "old_stock_items": old_stock_items,
        },
    )



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
    
    return redirect('reservation_detail')