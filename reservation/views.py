from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from product.models import StockItem
from .models import ReservationPage, MyReservation
from .forms import EditReservationForm, StoreReservationForm


def my_reservations(request):
    reservation_page = ReservationPage.objects.all(
        ).order_by('-updated_on').first()
    # Get all active reservations
    active_reservation = MyReservation.objects.filter(
        reserved_by=request.user, reservation_complete__lt=2).order_by(
        '-reservation_id')
    old_reservations = MyReservation.objects.filter(
        reserved_by=request.user, reservation_complete=2)

    # For form processing, handle a specific reservation
    # based on reservation_id (if passed)

    reservation_id = request.POST.get('reservation_id')
    if reservation_id:
        reservation = get_object_or_404(
            MyReservation, reservation_id=reservation_id)
    else:
        reservation = None

    # Handle form submission for editing the specific reservation
    if request.method == 'POST' and reservation:
        form = StoreReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()  # Save changes to the reservation
            return redirect('reservation')  # Redirect back to reservation list
    else:
        form = StoreReservationForm(
            instance=reservation) if reservation else None

    return render(
        request,
        'reservation/reservations_list.html',
        {
            "reservation_page": reservation_page,
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

    return render(request, 'reservation/reservations_list.html', {
        'reservation': reservation,
        'form': form
    })


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
    reservation = get_object_or_404(
            MyReservation,
            reservation_id=reservation_id)

    if reservation.reservation_complete == 0:
        # Only complete if not already done
        if request.method == "POST":
            form = StoreReservationForm(request.POST, instance=reservation)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.reservation_complete = 1  # Mark as reserved
                reservation.save()

                stock_items = reservation.get_stock_items()
                for stock_item in stock_items:
                    stock_item.status = 1  # Mark as reserved
                    stock_item.save()

                messages.add_message(
                request, messages.SUCCESS,
                    'Your reservation is stored, no more items can be added'
            )

                return redirect('reservation')
            else:
                print(form.errors)
        else:
            form = StoreReservationForm(instance=reservation)

    else:
        form = None

    return render(request, 'reservation/reservations_list.html', {
            'form': form,
            'reservation': reservation,
    })


def edit_reservation(request, reservation_id):
    # Get the current reservation by reservation_id
    reservation = get_object_or_404(
        MyReservation, reservation_id=reservation_id)

    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation')
        
        messages.add_message(
                request, messages.SUCCESS,
                 'Your reservation is updated and stored'
            )
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'reservation/reservations_list.html', {
        'form': form,
        'reservation': reservation,
    })


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(
        MyReservation, reservation_id=reservation_id)

    # Ensure that the reservation is either "Started" (0) or "Reserved" (1)
    if reservation.reservation_complete in [0, 1]:
        # Update stock items to make them available again
        for stock_item in reservation.stock_items.all():
            stock_item.status = 0  # Mark stock item as available
            stock_item.save()

        messages.add_message(
                request, messages.SUCCESS,
                 'Your reservation is deleted'
            )

        # Delete the reservation
        reservation.delete()

    return redirect('reservation')
