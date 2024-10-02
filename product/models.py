from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class Ingredient(models.Model):
    """
    Represents an ingredient used in items.

    **Fields**

    `name`
        The name of the ingredient (e.g., flour, sugar).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Represents a product that contains ingredients and has an associated image.

    **Fields**

    `name`
        The name of the item (e.g., bread, jam).
    `item_image`
        An image of the item stored in Cloudinary.
    `ingredients`
        A many-to-many relationship with :model:`product.Ingredient`,
        representing the ingredients of the item.
    """
    name = models.CharField(max_length=100)
    item_image = CloudinaryField('image', default='placeholder')
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name

    def get_ingredient_ids(self):
        """
        Returns the list of ingredient IDs associated with this item.

        **Returns**
        List of ingredient IDs.
        """
        return list(self.ingredients.values_list('id', flat=True))


class Quantity(models.Model):
    """
    Represents a unit of measurement for an item quantity (e.g.,
    grams, pieces).

    **Fields**

    `unit`
        The unit of measurement for the quantity.
    """
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.unit


class Preserve(models.Model):
    """
    Represents the preservation method for stock items (e.g., fresh,
    frozen, canned).

    **Fields**

    `method`
        The preservation method for the stock item.
    """
    method = models.CharField(max_length=50)

    def __str__(self):
        return self.method


STATUS = ((0, "Available"), (1, "Reserved"), (2, "Sold"))


class StockItem(models.Model):
    """
    Represents a specific stock item that can be reserved or sold.

    **Fields**

    `item`
        A foreign key linking to :model:`product.Item`,
        representing the product.
    `item_quantity`
        The quantity of the item available in stock.
    `quantity`
        A foreign key linking to :model:`product.Quantity`,
        representing the unit of the item.
    `preserve`
        A foreign key linking to :model:`product.Preserve`,
        representing the preservation method.
    `created_on`
        A timestamp indicating when the stock item was added to the inventory.
    `status`
        An integer field indicating the status of the stock item
        (e.g., Available, Reserved, Sold).
    `reservation`
        A foreign key linking to :model:`reservation.MyReservation`,
        representing the reservation associated
        with the stock item, if applicable.
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    item_quantity = models.IntegerField()
    quantity = models.ForeignKey(Quantity, on_delete=models.CASCADE)
    preserve = models.ForeignKey(Preserve, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    reservation = models.ForeignKey(
        'reservation.MyReservation',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='stock_items')

    def __str__(self):
        return (
            f"{self.item.name} - {self.item_quantity} "
            f"{self.quantity.unit} {self.created_on} "
            f"({self.preserve.method}) {self.status}"
        )
