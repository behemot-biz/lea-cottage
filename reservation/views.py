from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ReservationPage, MyReservation
from .forms import EditReservationForm, StoreReservationForm


@login_required
def my_reservations(request):
    """
    Displays the list of active and past reservations for the
    logged-in user.

    **Context**

    `reservation_page`
        The most recently updated instance of
        :model:`reservation.ReservationPage`.
    `active_reservation`
        All active instances of :model:`reservation.MyReservation` where the
        status is not complete.
    `old_reservations`
        All past instances of :model:`reservation.MyReservation` where the
        reservation is complete.
    `form`
        The form to edit the currently selected reservation if applicable.

    **Template:**

    :template:`reservation/reservations_list.html`
    """
    reservation_page = ReservationPage.objects.all(
        ).order_by('-updated_on').first()
    active_reservation = MyReservation.objects.filter(
        reserved_by=request.user, reservation_complete__lt=2).order_by(
        '-reservation_id')
    old_reservations = MyReservation.objects.filter(
        reserved_by=request.user, reservation_complete=2)

    return render(
        request,
        'reservation/reservations_list.html',
        {
            "reservation_page": reservation_page,
            'active_reservation': active_reservation,
            'old_reservations': old_reservations,
        }
    )


@login_required
def store_reservation(request, reservation_id):
    """
    Marks a reservation as complete and stores it.

    **Context**

    `reservation`
        The instance of :model:`reservation.MyReservation` being updated.
    `form`
        The form used to update the reservation.

    **Messages:**

    A success message is displayed once the reservation is marked as complete.

    **Redirects to:**

    :view:`reservation`
    """
    reservation = get_object_or_404(
            MyReservation,
            reservation_id=reservation_id)

    if reservation.reserved_by != request.user:
        messages.add_message(
            request, messages.ERROR,
            'You are not allowed to alter this reservation.'
        )
        return redirect('reservation')

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
                messages.add_message(
                    request, messages.ERROR,
                    'There was an error with the form submission.'
                    )
        else:
            form = StoreReservationForm(instance=reservation)

    else:
        form = None

    return render(request, 'reservation/reservations_list.html', {
            'form': form,
            'reservation': reservation,
    })


@login_required
def edit_reservation(request, reservation_id):
    """
    Allows the user to edit an existing reservation.

    **Context**

    `reservation`
        The instance of :model:`reservation.MyReservation` being edited.
    `form`
        The form used to edit the reservation.

    **Messages:**

    A success message is displayed once the reservation is updated.

    **Redirects to:**

    :view:`reservation`
    """
    reservation = get_object_or_404(
        MyReservation, reservation_id=reservation_id)

    if reservation.reserved_by != request.user:
        messages.add_message(
            request, messages.ERROR,
            'You are not allowed to alter this reservation.'
        )
        return redirect('reservation')

    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)

        if form.is_valid():
            form.save()

            messages.add_message(
                request, messages.SUCCESS,
                'Your reservation is updated and stored!'
            )

            return redirect('reservation')

        else:
            messages.add_message(
                messages.ERROR,
                'There was an error with the form submission.'
            )
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'reservation/reservations_list.html', {
        'form': form,
        'reservation': reservation,
    })


@login_required
def delete_reservation(request, reservation_id):
    """
    Deletes a reservation and updates the stock item statuses.

    **Context**

    `reservation`
        The instance of :model:`reservation.MyReservation` being deleted.

    **Messages:**

    A success message is displayed once the reservation is deleted.

    **Redirects to:**

    :view:`reservation`
    """
    reservation = get_object_or_404(
        MyReservation, reservation_id=reservation_id)

    if reservation.reserved_by == request.user:
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

            reservation.delete()
        else:
            messages.add_message(
                request, messages.ERROR,
                'You cannot delete a completed reservation'
            )
    else:
        messages.add_message(
            request, messages.ERROR,
            'you are not allowed to delete this reservation'
        )

    return redirect('reservation')
