from . import views
from django.urls import path

urlpatterns = [
    path('', views.ItemList.as_view(), name='home'),
    path('stock_item', views.StockItemList.as_view(), name='stock_item_list'),
]