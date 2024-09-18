from django.shortcuts import render
from django.views import generic
from .models import Item


# Create your views here.
class ItemList(generic.ListView):
    queryset = Item.objects.all().order_by("name")
    template_name = "product/item_list.html"
    context_object_name = "items"
