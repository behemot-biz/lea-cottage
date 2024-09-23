from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Item, StockItem
from .forms import ReservItemForm


# Create your views here.
class ItemList(generic.ListView):
    queryset = Item.objects.all().order_by("name")
    template_name = "product/item_list.html"
    context_object_name = "items"


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

    if request.method == "POST":
        reserve_form = ReservItemForm(data=request.POST, instance=stock_item)
        if reserve_form.is_valid():
            stock_item = reserve_form.save(commit=False)
            stock_item.status = 1
            stock_item.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your reservation is stored'
            )

    reserve_form = ReservItemForm(instance=stock_item)

    return render(
        request,
        "product/stock_item_detail.html",
        {
            "stock_item": stock_item,
            "reserve_form": reserve_form
        },
    )