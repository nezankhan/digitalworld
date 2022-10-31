from django import forms
from .models import Customers


class QueryForm(forms.Form):
    customer_id = forms.IntegerField(help_text="Enter Customer ID no text")
    
    