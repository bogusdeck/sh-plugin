from django import forms



class GlobalSettingsForm(forms.Form):
    STOCK_LOCATION_CHOICES = [
        ('all', 'All'),
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    LOOKBACK_CHOICES = [
        (30, '30 days'),
        (60, '60 days'),
        (90, '90 days'),
        (180, '6 months'),
    ]

    schedule_frequency = forms.ChoiceField(
        choices=[('hourly', 'Hourly'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('custom', 'Custom')],
        widget=forms.RadioSelect(attrs={'class': 'mr-2'})
    )
    custom_start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'})
    )
    custom_stop_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'})
    )
    custom_frequency_in_hours = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'})
    )
    stock_location = forms.ChoiceField(
        choices=STOCK_LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'})
    )
    lookback_period = forms.ChoiceField(
        choices=LOOKBACK_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2'
        })
    )