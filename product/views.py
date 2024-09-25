from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from .models import Item, StockItem
from reservation.models import MyReservation
from .forms import ReservItemForm
from django.http import HttpResponse


# Create your views here.

class StockItemList(generic.ListView):
    queryset = StockItem.objects.all().filter(status=0).order_by("item", "created_on", "preserve")
    template_name = "product/index.html"
    context_object_name = "stock_items"
  

    def get_context_data(self, **kwargs):
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
    stock_item = get_object_or_404(StockItem, id=id)

    # if request.method == "POST":
    #     reserve_form = ReservItemForm(data=request.POST, instance=stock_item)
    #     if reserve_form.is_valid():
    #         stock_item = reserve_form.save(commit=False)
    #         stock_item.status = 1
    #         stock_item.save()
    #         messages.add_message(
    #             request, messages.SUCCESS,
    #             'Your reservation is stored'
    #         )

    # reserve_form = ReservItemForm(instance=stock_item)

    return render(
        request,
        "product/stock_item_detail.html",
        {
            "stock_item": stock_item,
            # "reserve_form": reserve_form
        },
    )

def reservation_detail(request, id):
    reservation = get_object_or_404(MyReservation, id=id)
    return render(request, 'reservation/reservation_detail.html', {'reservation': reservation})


def add_to_reservation(request, stock_item_id):
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

    # Use reservation.reservation_id since it is the primary key
    # return redirect(reverse('reservation_detail', kwargs={'id': reservation.reservation_id}))
    return redirect(reverse('reservation'))