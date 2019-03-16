from django.db import models
from django.utils import timezone
from customers.models import Customer
from jobs.models import Job

CURRENCY_CHOICES = (
    ("INR", "INR"),
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("GBP", "GBP"),
)

PAYMENT_MODES = (
    ("Cash", "Cash"),
    ("NEFT/RTGS/IMPS", "NEFT/RTGS/IMPS"),
    ("Bank Deposit", "Bank Deposit"),
    ("Cheque", "Cheque"),
)

class Invoice(models.Model):    
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now)
    invoice_id = models.CharField(max_length=150, blank=True, null=True, unique=True)
    due_date = models.DateField(blank=True, null=True)    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    total = models.FloatField(default=0.00, blank=True, null=True)
    balance_due = models.FloatField(default=0.00, blank=True, null=True)

    def __str__(self):
        return "Invoice Id: " + str(self.pk)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    serial_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=150)
    quantity = models.IntegerField(default=1)
    currency = models.CharField(max_length=3, default="INR", choices=CURRENCY_CHOICES)
    rate = models.FloatField(default=1.00)
    exchange_rate = models.FloatField(default=1.00)
    tax_rate = models.FloatField(default=18.00)
    total = models.FloatField(blank=True, null=True)
    

    def __str__(self):
        return "Invoice item for invoice id:" + str(self.invoice)


class Payments(models.Model):
    date_added = models.DateField(default=timezone.now, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    payment_mode = models.CharField(max_length=200, choices=PAYMENT_MODES)
    notes = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "Payment of " + str(self.amount) + "for invoice id " + str(self.invoice)