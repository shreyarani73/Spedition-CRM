from django.db import models
from django.utils import timezone
from crm.choices import YESNO

class Customer(models.Model):
    date_added = models.DateField(default=timezone.now)
    company_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    landline = models.BigIntegerField(blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst = models.CharField(max_length=150, blank=True, null=True)
    credit_amount = models.FloatField(default=0.00)
    credit_days = models.IntegerField(default=30)
    approved = models.BooleanField(default=False, choices=YESNO)

    def __str__(self):
        return self.company_name

class Documents(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=150)
    document_file = models.FileField(max_length=250, upload_to="documents")

    def __str__(self):
        return self.document_type + " for " + self.customer.company_name