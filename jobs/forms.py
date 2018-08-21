from django import forms
from django.forms import ModelForm
from .models import Job

class NewJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ["date_added"]

class UpdateJobForm(ModelForm):
    class Meta:
        model = Job
        fields = "__all__"        