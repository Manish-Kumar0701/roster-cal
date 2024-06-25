# forms.py
from django import forms

class SeatAllocationForm(forms.Form):
    total_seats = forms.IntegerField(
        label="Enter the total number of seats",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of seats'})
    )
