from django.db import models
from django.contrib.auth.models import User 
from product.models import StockItem

# Create your models here.

class Reservation(models.Model):
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title
status = models.IntegerField


RESERVE = ((0, "Started"), (1, "Complete"))
class MyReservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reserved_note = models.CharField(max_length=100, blank=True)
    reserved_date = models.DateField(null=True, blank=True)
    reservation_complete = models.IntegerField(choices=RESERVE, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reservation_id} - {self.get_reservation_complete_display()} by {self.reserved_by}"

    def get_stock_items(self):
        return StockItem.objects.filter(reservation=self)