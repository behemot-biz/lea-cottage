from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from django.db.models import Count, Min
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservation.models import MyReservation
from .models import StockItem


class StockItemList(generic.ListView):
    """
    Displays all available stock items in :model:`product.StockItem`.

    **Context**

    ``queryset``
        A QuerySet of all instances of :model:`product.StockItem`
        with status=0.
    ``stock_items_with_ingredients``
        A list of unique stock items along with their available count.
    """
    queryset = StockItem.objects.filter(status=0).order_by("-created_on")
    template_name = "product/index.html"
    context_object_name = "stock_items"

    def get_context_data(self, **kwargs):
        """
        Adds unique stock items and their available count to the context.
        """
        context = super().get_context_data(**kwargs)

        # Group by item, preserve method, and quantity to avoid duplicates
        stock_items = StockItem.objects.filter(status=0).values(
            'item__name', 'item__item_image',
            'preserve__method', 'quantity__unit'
        ).annotate(
            available_count=Count('id'),
            lowest_id=Min('id'),
            item_quantity=Min('item_quantity')
        ).order_by('item__name', 'preserve__method')

        context['stock_items'] = stock_items
        return context


@login_required
def add_to_reservation(request, stock_item_id):
    """
    Adds a stock item to the current user's active reservation
    in :model:`reservation.MyReservation`.
    """
    stock_item = get_object_or_404(StockItem, id=stock_item_id)

    # Get or create an active reservation (RESERVE == 0)
    reservation, created = MyReservation.objects.get_or_create(
        reserved_by=request.user,
        reservation_complete=0,  # Status is "Started"
    )

    if created:
        reservation.save()

    # Assign the stock item to the reservation
    stock_item.reservation = reservation
    stock_item.status = 1  # Mark the stock item as reserved
    stock_item.save()

    messages.add_message(
        request, messages.SUCCESS,
        f'{stock_item.item.name} added to your reservation'
    )

    return redirect(reverse('reservation'))


def stock_item_detail(request, id):
    """
    Displays the details of a single stock item.
    """
    stock_item = get_object_or_404(StockItem, id=id)

    return render(
        request,
        "product/stock_item_detail.html",
        {"stock_item": stock_item},
    )
