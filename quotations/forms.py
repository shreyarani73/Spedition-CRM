from django import forms
from django.forms import ModelForm
from .models import Quotation, QuotationItem

class QuotationForm(ModelForm):
    class Meta:
        model = Quotation
        exclude = ["date_added"]
        widgets = {
            "service_total": forms.TextInput(attrs={"disabled":True})
        }

class QuotationUpdateForm(ModelForm):
    class Meta:
        model = Quotation
        fields = "__all__"
        widgets = {
            # "date_added": forms.TextInput(attrs={"disabled":True}),
            "service_total": forms.TextInput(attrs={"disabled":True}),
        }

class NewQuotationItemForm(ModelForm):
    class Meta:
        model = QuotationItem
        exclude = ["quotation", "serial_number"]
        widgets = {
            "total":forms.TextInput(attrs={"disabled":True})
        }

class QuotationItemUpdateForm(ModelForm):
    class Meta:
        model = QuotationItem
        exclude = ["quotation", "serial_number"]
        widgets = {
            "total":forms.TextInput(attrs={"disabled":True})
        }
