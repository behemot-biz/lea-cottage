from django.shortcuts import render
from django.views import generic
from .models import Item, StockItem


# Create your views here.
class ItemList(generic.ListView):
    queryset = Item.objects.all().order_by("name")
    template_name = "product/item_list.html"
    context_object_name = "items"


class StockItemList(generic.ListView):
    #model = StockItem
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