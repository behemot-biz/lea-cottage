from django.contrib import admin
from .models import Ingredient, Item, Quantity, Preserve, StockItem
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Item)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name', 'get_ingredient_names') #maybe remove id from list display
    list_display_links = ('name',)
    filter_horizontal = ('ingredients',)

    #return list of ingredient names, separated with commas
    def get_ingredient_names(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])
    
    get_ingredient_names.short_description = 'Ingredients'


@admin.register(Ingredient)
class IngredientAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name')


@admin.register(Quantity)
class QuantityAdmin(SummernoteModelAdmin):
    list_display = ('id', 'unit')


@admin.register(Preserve)
class PreserveAdmin(SummernoteModelAdmin):
    list_display = ('id', 'method')


@admin.register(StockItem)
class StockItemAdmin(SummernoteModelAdmin):
    list_display = ('id', 'item', 'item_quantity', 'quantity', 'preserve', 'created_on', 'status')
    list_display_links = ('item',)
    list_filter = ('status', 'item', 'created_on')
    search_fields = ['item']
    #summernote_fields = ('item',)