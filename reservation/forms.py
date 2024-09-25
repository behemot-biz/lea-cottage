from django import forms
from reservation.models import MyReservation
from django.utils import timezone

class CompleteReservationForm(forms.ModelForm):
    class Meta:
        model = MyReservation
        fields = ['reserved_note', 'reserved_date']
        labels = {
            'reserved_note': 'Leave a message (optional) ',  # Custom label
            'reserved_date': 'Select a pickup date',  # Custom label
        }
        widgets = {
            'reserved_date': forms.DateInput(attrs={'type': 'date'}),  # Use HTML date input type
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-populate the reserved_date with today's date
        if not self.instance.reserved_date:
            self.initial['reserved_date'] = timezone.now().date()

        self.fields['reserved_note'].required = False  # Make note optional
