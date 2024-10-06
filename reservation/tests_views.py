from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import cloudinary.uploader
from product.models import Item, Quantity, Preserve, StockItem
from reservation.models import MyReservation


class TestProductReservation(TestCase):

    @patch('cloudinary.uploader.upload')
    def setUp(self, mock_upload):
        mock_upload.return_value = {
            'secure_url': 'http://example.com/test-image.jpg'
        }

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="user@test.com"
        )

        self.client.login(username="testuser", password="password123")

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

        self.stock_item = StockItem.objects.create(
            item=self.item,
            item_quantity=5,
            quantity=self.quantity,
            preserve=self.preserve,
            status=0
        )

        self.reservation = MyReservation.objects.create(
            reserved_note="This is a test reservation",
            reserved_date="2024-10-05",
            reserved_by=self.user,
            reservation_complete=0
        )

        self.reservation.stock_items.add(self.stock_item)

    def test_add_to_reservation(self):
        # Test adding a stock item to the reservation
        response = self.client.get(reverse(
            'add_to_reservation', args=[self.stock_item.id]))

        # Check that the reservation was created and the stock item was added
        reservation = MyReservation.objects.get(
            reserved_by=self.user, reservation_complete=0
            )
        self.assertIn(self.stock_item, reservation.stock_items.all())
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('reservation'))

    def test_view_reservation_list(self):
        # Test that the user can view their reservations
        response = self.client.get(reverse('reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reservations")
        self.assertIn(self.stock_item,
                      self.reservation.stock_items.all())

    def test_delete_reservation(self):
        response = self.client.post(reverse(
            'delete_reservation', args=[self.reservation.reservation_id])
            )
        with self.assertRaises(MyReservation.DoesNotExist):
            MyReservation.objects.get(
                reservation_id=self.reservation.reservation_id)
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.status, 0)
        self.assertRedirects(response, reverse('reservation'))

    def test_edit_reservation(self):
        response = self.client.post(reverse(
            'edit_reservation',
            args=[self.reservation.reservation_id]), {
            'reserved_note': 'Updated test reservation',
            'reserved_date': '2024-10-06'
        })
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.reserved_note,
                         'Updated test reservation')
        self.assertEqual(str(self.reservation.reserved_date), '2024-10-06')
        self.assertRedirects(response, reverse('reservation'))

    def test_add_to_existing_reservation(self):
        second_stock_item = StockItem.objects.create(
            item=self.item,
            item_quantity=3,
            quantity=self.quantity,
            preserve=self.preserve,
            status=0  # Available
        )
        response = self.client.get(reverse(
            'add_to_reservation', args=[second_stock_item.id]))
        self.reservation.refresh_from_db()
        self.assertIn(self.stock_item, self.reservation.stock_items.all())
        self.assertIn(second_stock_item, self.reservation.stock_items.all())
        self.assertRedirects(response, reverse('reservation'))

    def test_cannot_add_to_completed_reservation(self):
        self.reservation.reservation_complete = 2
        self.reservation.save()
        response = self.client.get(reverse(
            'add_to_reservation', args=[self.stock_item.id]))
        self.reservation.refresh_from_db()
        self.assertNotIn(self.stock_item, self.reservation.stock_items.all())
        self.assertRedirects(response, reverse('reservation'))

    def test_successful_reservation_submission(self):
        # Test for submitting a reservation
        reservation_data = {
            'reserved_note': 'This is a test reservation',
            'reserved_date': '2024-10-05',
        }
        response = self.client.post(reverse(
            'add_to_reservation', args=[self.stock_item.id]), reservation_data)

        # Check the response status code
        self.assertEqual(response.status_code, 302)

        # Check that the reservation was created
        reservation = MyReservation.objects.get(reserved_by=self.user)
        self.assertEqual(
            reservation.reserved_note,
            'This is a test reservation'
            )
        self.assertEqual(str(reservation.reserved_date), '2024-10-05')

        # Check if the correct success message is displayed
        response = self.client.get(reverse('reservation'))
        self.assertIn(
            b'Sample Item added to your reservation',
            response.content
            )
