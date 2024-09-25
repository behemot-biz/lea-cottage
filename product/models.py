from django.db import models
# from reservation.models import MyReservation


# class Meta:
#         ordering = ["created_on"]
#     def __str__(self):

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
    
    def get_ingredient_ids(self):
        return list(self.ingredients.values_list('id', flat=True))


class Quantity(models.Model):
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.unit
    

class Preserve(models.Model):
    method = models.CharField(max_length=50)

    def __str__(self):
        return self.method


STATUS = ((0, "Available"), (1, "Reserved"), (2, "Sold"))


class StockItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    item_quantity = models.IntegerField()
    quantity = models.ForeignKey(Quantity, on_delete=models.CASCADE)
    preserve = models.ForeignKey(Preserve, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    reservation = models.ForeignKey('reservation.MyReservation', on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_items')  # Use string reference


    def __str__(self):
        return f"{self.item.name} - {self.item_quantity} {self.quantity.unit} {self.created_on} ({self.preserve.method}) {self.status}"
    
    