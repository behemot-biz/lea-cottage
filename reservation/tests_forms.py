from django.test import TestCase
from .forms import StoreReservationForm


class TestStoreReservationForm(TestCase):
    # 'reserved_note', 
    # 'reserved_date'
    def test_form_is_valid(self):
        store_reservation = StoreReservationForm({
            'reserved_note': 'This is a great cake',
            'reserved_date': '2024-10-03'  # YYYY-MM-DD format
            })
        self.assertTrue(store_reservation.is_valid(), msg="Form is invalid")

    def test_form_is_invalid(self):
        store_reservation = StoreReservationForm({
            'reserved_note': 'This is a great cake',
            'reserved_date': '2'  # YYYY-MM-DD format
            })
        self.assertFalse(store_reservation.is_valid(), msg="Form is valid")