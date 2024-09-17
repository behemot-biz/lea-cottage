from django.db import models


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


# class Meta:
#         ordering = ["created_on"]
#     def __str__(self):