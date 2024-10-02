from django import forms
from django.utils import timezone
from reservation.models import MyReservation


class StoreReservationForm(forms.ModelForm):
    """
    A form for users to create or update a reservation with an optional
    note and a pickup date.

    **Fields**

    `reserved_note`
        A text field for users to leave an optional message about the
        reservation.
    `reserved_date`
        A date input field for users to select the pickup date for the
        reservation.

    **Customizations**

    - The `reserved_note` field is optional.
    - The `reserved_date` field is auto-populated with today's date
      if no date is provided.

    **Meta Options**

    `model`
        The form is linked to the :model:`reservation.MyReservation` model.
    `fields`
        The fields included in the form: `reserved_note` and `reserved_date`.
    `labels`
        Custom labels for the fields.
    `widgets`
        The `reserved_date` is rendered with a custom widget for HTML5
        date input.

    **Initialization**

    The form auto-populates the `reserved_date` field with the current date if
    no date is set,
    and makes the `reserved_note` field optional.
    """
    class Meta:
        model = MyReservation
        fields = ['reserved_note', 'reserved_date']
        labels = {
            'reserved_note': 'Leave a message (optional) ',  # Custom label
            'reserved_date': 'Select a pickup date',  # Custom label
        }
        widgets = {
            'reserved_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Initializes the form. If the `reserved_date` is not set, it populates the
        field with today's date. The `reserved_note` field is optional by default.
        """
        if not self.instance.reserved_date:
            self.initial['reserved_date'] = timezone.now().date()

        self.fields['reserved_note'].required = False  # Make note optional


class EditReservationForm(forms.ModelForm):
    """
    A form for users to edit an existing reservation, allowing them to modify
    the note and pickup date.

    **Fields**

    `reserved_note`
        A text field for users to edit their message about the reservation.
    `reserved_date`
        A date input field for users to update the pickup date for the
        reservation.

    **Meta Options**

    `model`
        The form is linked to the :model:`reservation.MyReservation` model.
    `fields`
        The fields included in the form: `reserved_note` and `reserved_date`.
    `labels`
        Custom labels for the fields.
    `widgets`
        The `reserved_date` is rendered with a custom widget for HTML5
        date input.

    **Initialization**

    The form auto-populates the `reserved_date` field with the
    current date if no date is set.
    """
    class Meta:
        model = MyReservation
        fields = ['reserved_note', 'reserved_date']
        labels = {
            'reserved_note': 'Edit your message (optional)',
            'reserved_date': 'Update pickup date',
        }
        widgets = {
            'reserved_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form. If the `reserved_date` is not set, it populates
        the field with today's date.
        """
        super().__init__(*args, **kwargs)
        if not self.instance.reserved_date:
            self.initial['reserved_date'] = timezone.now().date()
