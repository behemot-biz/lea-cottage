from . import views
from django.urls import path

urlpatterns = [
    path('', views.my_reservations, name='reservation'),
    path('<int:id>/', views.reservation_detail, name='reservation_detail'),
    # path('complete', views.complete_reservation, name='complete_reservation'),  
    path('complete/<int:reservation_id>/', views.complete_reservation, name='complete_reservation'),  
]
