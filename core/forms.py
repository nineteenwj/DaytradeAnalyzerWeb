"""
Define Django forms for user input.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StockData

class StockDataForm(forms.ModelForm):
    class Meta:
        model = StockData
        fields = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Use a date picker for the date field
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("This field is required.")
        return date


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

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

class TradingOpeningForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pc_code = forms.CharField(max_length=10)
    strategy_choices = [
        ('Pre-market Close', 'Pre-market Close'),
        ('Pre-market Avg', 'Pre-market Avg'),
        ('Pre-market Weighted', 'Pre-market Weighted'),
        ('Intraday Open', 'Intraday Open')
    ]
    strategy = forms.ChoiceField(choices=strategy_choices)
    buy_code1 = forms.CharField(max_length=10)
    buy_code2 = forms.CharField(max_length=10)
    buy_price_up_ratio = forms.FloatField()
    quantity = forms.IntegerField(initial=10)
    take_profit = forms.FloatField()
    stop_loss = forms.FloatField()