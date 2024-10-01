from django.urls import path
from . import views

urlpatterns = [
    path('', views.StockItemList.as_view(), name='home'),
    path('stock/<int:id>/', views.stock_item_detail, name='stock_item_detail'),
    path('add_to_reservation/<int:stock_item_id>/', views.add_to_reservation, name='add_to_reservation'),
    # path('reservation/<int:id>/', views.reservation_detail, name='reservation_detail'),
]