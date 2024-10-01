from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from product.models import StockItem
from .models import ReservationPage, MyReservation


@admin.register(ReservationPage)
class ReservationAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


# Inline model for displaying StockItems in the reservation admin
class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 0
    fields = ['item', 'item_quantity', 'status']
    readonly_fields = ['item', 'item_quantity', 'status']
    can_delete = False


@admin.register(MyReservation)
class MyReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'reserved_by', 'reservation_complete',
                    'reserved_date', 'updated_on')
    inlines = [StockItemInline]
    search_fields = ['reservation_id', 'reserved_by__username']
    list_filter = ['reservation_complete', 'reserved_date']
    readonly_fields = ['updated_on']

    def get_queryset(self, request):
        # Optionally customize the queryset to
        # optimize performance or add filters
        return super().get_queryset(request).select_related('reserved_by')
