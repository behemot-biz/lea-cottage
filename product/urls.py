from . import views
from django.urls import path

urlpatterns = [
    # path('', views.ItemList.as_view(), name='home'),
    path('', views.StockItemList.as_view(), name='home'),
    path('item', views.ItemList.as_view(), name='item_list'),
]