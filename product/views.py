from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from reservation.models import MyReservation
from .models import Item, StockItem


class StockItemList(generic.ListView):
    """
    Displays all available stock items in :model:`product.StockItem`.

    **Context**

    ``queryset``
        A QuerySet of all instances of :model:`product.StockItem`
        with status=0.
    ``stock_items_with_ingredients``
        A list of stock items along with their associated ingredients.

    **Template:**

    :template:`product/index.html`
    """
    queryset = StockItem.objects.all(
        ).filter(status=0).order_by("-created_on")
    template_name = "product/index.html"
    context_object_name = "stock_items"

    def get_context_data(self, **kwargs):
        """
        Adds stock items and their ingredients to the context.

        **Context**

        ``stock_items_with_ingredients``
            A list of stock items along with their related ingredients.
        """
        context = super().get_context_data(**kwargs)

        # Add stock items and their associated ingredients to the context
        stock_items_with_ingredients = []
        for stock_item in context['stock_items']:
            # Fetch related ingredients from the linked Item
            ingredients = stock_item.item.ingredients.all()
            stock_items_with_ingredients.append({
                'stock_item': stock_item,
                'ingredients': ingredients,
            })

        context['stock_items_with_ingredients'] = stock_items_with_ingredients
        return context


def stock_item_detail(request, id):
    """
    Displays the details of a single stock item in :model:`product.StockItem`.

    **Context**

    ``stock_item``
        An instance of :model:`product.StockItem` corresponding
        to the provided ID.

    **Template:**

    :template:`product/stock_item_detail.html`
    """
    stock_item = get_object_or_404(StockItem, id=id)

    return render(
        request,
        "product/stock_item_detail.html",
        {
            "stock_item": stock_item,
        },
    )


def reservation_detail(request, id):
    """
    Displays the details of a reservation in
    :model:`reservation.MyReservation`.

    **Context**

    ``reservation``
        An instance of :model:`reservation.MyReservation`
        corresponding to the provided ID.

    **Template:**

    :template:`reservation/reservation_detail.html`
    """
    reservation = get_object_or_404(MyReservation, id=id)
    return render(request, 'reservation/reservation_detail.html', {
        'reservation': reservation})


def add_to_reservation(request, stock_item_id):
    """
    Adds a stock item to the current user's active reservation
    in :model:`reservation.MyReservation`.

    If the user doesn't have an active reservation, a new one is created.

    **Context**

    ``stock_item``
        An instance of :model:`product.StockItem` corresponding
        to the provided stock item ID.
    ``reservation``
        The current user's active reservation.

    **Messages:**

    A success message is added upon successfully adding the stock
    item to the reservation.

    **Redirects to:**

    :view:`reservation` - The reservation page.
    """
    stock_item = get_object_or_404(StockItem, id=stock_item_id)

    # Get or create an active reservation (RESERVE == 0)
    reservation, created = MyReservation.objects.get_or_create(
        reserved_by=request.user,
        reservation_complete=0,  # Status is "Started"
    )

    # Ensure the reservation is saved if it was just created
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
