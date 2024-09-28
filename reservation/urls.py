from . import views
from django.urls import path

urlpatterns = [
    path('', views.my_reservations, name='reservation'),
    path('<int:id>/', views.reservation_detail, name='reservation_detail'),
    path('store_reservation/<int:reservation_id>/', views.store_reservation, name='store_reservation'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]
