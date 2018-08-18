from django import forms
from django.forms import ModelForm
from .models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ["date_added", "approved"]

class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "date_added": forms.TextInput(attrs={"disabled":True}),
            "sales_person": forms.TextInput(attrs={"disabled":True}),
            "company_name": forms.TextInput(attrs={"disabled":True}),
            "credit_amount": forms.TextInput(attrs={"disabled":True}),
            "credit_days": forms.TextInput(attrs={"disabled":True}),
            "approved": forms.TextInput(attrs={"disabled":True}),
        }
