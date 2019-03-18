from django import forms
from django.forms import ModelForm
from .models import Job, Process, Customer

class NewJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = [ "date_added"]
    
    def __init__(self, user=None, **kwargs):
        super(NewJobForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset = models.Customer.objects.filter(user=user)
        
        #def __init__(self,user, *args, **kwargs):
            #super(NewTicket, self).__init__(*args, **kwargs)
            #try:
                #client_id = UserExtend.objects.values_list('client_id', flat=True).get(user=user)
                #self.client.approved.queryset=client.objects.filter(client_d=client_id)

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

