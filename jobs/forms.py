from django import forms
from django.forms import ModelForm
from .models import Job, Process

class NewJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ["date_added"]

class UpdateJobForm(ModelForm):
    class Meta:
        model = Job
        fields = "__all__"        

class ProcessForm(ModelForm):
    class Meta:
        model = Process
        exclude = ["date_added", "job"]
        widgets = {
            "notes": forms.TextInput()
        }

class UpdateProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = "__all__"