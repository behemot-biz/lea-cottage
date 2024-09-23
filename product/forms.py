from .models import StockItem
from django import forms


class ReservItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ('item',)