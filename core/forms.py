"""
Define Django forms for user input.
"""
from django import forms

class TickerForm(forms.Form):
    """
    Form for inputting a stock ticker.

    This form is used for fetching stock data from the network.
    """
    ticker = forms.CharField(
        max_length=10,
        label="Ticker",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AAPL'})
    )

class DateRangeForm(forms.Form):
    """
    Form for entering a date range.
    The start_date and end_date fields require input in the format YYYY-MM-DD.
    The HTML5 date input is used to help ensure the correct format.
    """
    start_date = forms.ChoiceField(
        label="Start Date",
        choices=[],  # initially empty
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    end_date = forms.ChoiceField(
        label="End Date",
        choices=[],  # initially empty
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    interval = forms.ChoiceField(
        label="Interval",
        choices=[("1m", "1m"), ("5m", "5m"), ("15m", "15m"), ("30m", "30m"), ("1h", "1h"), ("1d", "1d")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        date_choices = kwargs.pop('date_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['start_date'].choices = date_choices
        self.fields['end_date'].choices = date_choices