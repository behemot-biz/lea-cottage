from django.contrib import admin
from .models import Ingredient, Item

# Register your models here.
@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_ingredient_names') #maybe remove id from list display
    list_display_links = ('name',)
    filter_horizontal = ('ingredients',)

    #return list of ingredient names, separated with commas
    def get_ingredient_names(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])
    
    get_ingredient_names.short_description = 'Ingredients'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')