from django.db import models
from django.contrib.auth.models import User
from product.models import StockItem


class ReservationPage(models.Model):
    """
    Represents a static page that displays reservation information.

    **Fields**

    `title`
        The title of the reservation page.
    `updated_on`
        The timestamp when the page was last updated.
    `content`
        The main content or body of the reservation page.

    **String Representation**

    Returns the title of the reservation page.
    """
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title


# Choices for reservation status, representing the lifecycle of a reservation.
RESERVE_STATUS = (
        (0, 'Started'),
        (1, 'Reserved'),
        (2, 'Complete'),
    )


class MyReservation(models.Model):
    """
    Represents a reservation made by a user.

    **Fields**

    `reservation_id`
        The unique ID for the reservation (auto-incremented).
    `reserved_by`
        A foreign key linking to :model:`auth.User`,
        representing the user who made the reservation.
    `reserved_note`
        Optional notes provided by the user for the reservation.
    `reserved_date`
        The date when the reservation is intended to be picked up.
    `reservation_complete`
        An integer field representing the status of the reservatio
        (Started, Reserved, Complete).
    `updated_on`
        The timestamp when the reservation was last updated.

    **String Representation**

    Returns a string representation of the reservation, including its ID,
    status, and the user who made the reservation.
    """
    reservation_id = models.AutoField(primary_key=True)
    reserved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    reserved_note = models.CharField(max_length=100, blank=True)
    reserved_date = models.DateField(null=True, blank=True)
    reservation_complete = models.IntegerField(
        choices=RESERVE_STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):

        return (
            f"{self.reservation_id} - "
            f"{self.get_reservation_complete_display()} by {self.reserved_by}"
        )

    def get_stock_items(self):
        """
       Retrieves all stock items associated with this reservation.

        **Returns**

        `QuerySet`
            A Django QuerySet containing all :model:`product.StockItem` objects
            linked to this reservation instance.
        """
        return StockItem.objects.filter(reservation=self)
