from django.contrib.auth.models import User
from django.test import TestCase
from product.models import Item, Quantity, Preserve, StockItem
from reservation.models import MyReservation

class TestReservationModels(TestCase):

    def setUp(self):
        # Create a mock user
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="user@test.com"
        )

        # Create mock Item, Quantity, and Preserve instances
        self.item = Item.objects.create(
            name="Sample Item",
            item_image="placeholder"
        )
        self.quantity = Quantity.objects.create(
            unit="Pieces"
        )
        self.preserve = Preserve.objects.create(
            method="Fresh"
        )

        # Create a StockItem associated with the Item, Quantity, and Preserve
        self.stock_item = StockItem.objects.create(
            item=self.item,
            item_quantity=5,
            quantity=self.quantity,
            preserve=self.preserve,
            status=0  # Available stock item
        )

    def test_create_reservation(self):
        # Test that a reservation can be created with valid data
        reservation = MyReservation.objects.create(
            reserved_note="This is a test reservation",
            reserved_date="2024-10-05",
            reserved_by=self.user,
            reservation_complete=0  # 'Started' status
        )
        self.assertEqual(reservation.reserved_note, "This is a test reservation")
        self.assertEqual(str(reservation.reserved_date), "2024-10-05")
        self.assertEqual(reservation.reserved_by, self.user)
        self.assertEqual(reservation.reservation_complete, 0)  # 'Started' status

    def test_stockitem_association(self):
        # Test that a StockItem can be associated with a reservation
        reservation = MyReservation.objects.create(
            reserved_note="Test reservation with stock",
            reserved_date="2024-10-05",
            reserved_by=self.user,
            reservation_complete=0
        )
        reservation.stock_items.add(self.stock_item)
        self.assertIn(self.stock_item, reservation.stock_items.all())

    def test_complete_reservation(self):
        # Test that the reservation status can be updated to complete
        reservation = MyReservation.objects.create(
            reserved_note="Reservation to complete",
            reserved_date="2024-10-05",
            reserved_by=self.user,
            reservation_complete=0
        )
        reservation.reservation_complete = 2  # Mark as 'complete'
        reservation.save()
        self.assertEqual(reservation.reservation_complete, 2)

    def test_auto_increment_reservation_id(self):
        # Test that the reservation_id is automatically incremented in the database
        reservation1 = MyReservation.objects.create(
            reserved_note="First reservation",
            reserved_date="2024-10-05",
            reserved_by=self.user
        )
        reservation2 = MyReservation.objects.create(
            reserved_note="Second reservation",
            reserved_date="2024-10-06",
            reserved_by=self.user
        )
        self.assertTrue(reservation1.reservation_id < reservation2.reservation_id)

    def test_delete_reservation_restores_stock(self):
        # Test that when a reservation is deleted, the stock items become available again
        reservation = MyReservation.objects.create(
            reserved_note="Reservation with stock to delete",
            reserved_date="2024-10-05",
            reserved_by=self.user,
            reservation_complete=0
        )
        reservation.stock_items.add(self.stock_item)
        reservation.delete()

        # Refresh the StockItem to check if its status is restored
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.status, 0)  # Ensure it's available again
