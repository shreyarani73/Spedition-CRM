from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Quotation(models.Model):
    date_added = models.DateField(default=timezone.now)
    customer_name = models.CharField(max_length=25)
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=50)
    mobile = models.BigIntegerField()
    service_description = models.CharField(max_length=150)
    service_quantity = models.IntegerField()
    service_rate = models.FloatField()
    service_currency = models.CharField(max_length=4, choices=(
        ("INR", "INR"),
        ("USD", "USD"),
        ("GBP", "GBP"),
        ("EUR", "EUR")
    ))
    service_exch_rate = models.FloatField(default=1.00)
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