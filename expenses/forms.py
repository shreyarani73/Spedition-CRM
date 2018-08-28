from django import forms
from django.forms import ModelForm
from .models import Expense

class NewExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"

class UpdateExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        widgets = {
            
        }