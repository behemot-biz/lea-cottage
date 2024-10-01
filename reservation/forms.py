from django import forms
from django.utils import timezone
from reservation.models import MyReservation


class StoreReservationForm(forms.ModelForm):
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
        # Auto-populate the reserved_date with today's date
        if not self.instance.reserved_date:
            self.initial['reserved_date'] = timezone.now().date()

        self.fields['reserved_note'].required = False  # Make note optional


class EditReservationForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)
        if not self.instance.reserved_date:
            self.initial['reserved_date'] = timezone.now().date()
