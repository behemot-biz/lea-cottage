from . import views
from django.urls import path

urlpatterns = [
    # path('', views.StockItemList.as_view(), name='home'),
    # path('stock/<int:id>/', views.stock_item_detail, name='stock_item_detail'),
    path('', views.my_reservations, name='reservation'),
]