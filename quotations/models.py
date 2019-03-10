from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

CURRENCY_CHOICES = (
    ("INR", "INR"),
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("GBP", "GBP"),
)

class Quotation(models.Model):
    date_added = models.DateField(default=timezone.now)
    revision_code = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=25)
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(blank=True, max_length=10)    
    service_total = models.FloatField(default=0.00, blank=True, null=True)
    taxes = models.FloatField(default=18.00, choices=(
        (5, "5% GST"),
        (12, "12% GST"),
        (18, "18% GST"),        
    ))
    sales_person = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Draft", choices=(
        ("Draft", "Draft"),
        ("Complete", "Complete"),
    ))

    def __str__(self):
        return self.customer_name


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    serial_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=150)
    quantity = models.IntegerField(default=1)
    currency = models.CharField(max_length=3, default="INR", choices=CURRENCY_CHOICES)
    rate = models.FloatField(default=1.00)
    exchange_rate = models.FloatField(default=1.00)
    tax_rate = models.FloatField(default=18.00)
    total = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "Quotation item for quotation id: %s" % self.quotation.id