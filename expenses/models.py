from django.db import models
from django.utils import timezone
from jobs.models import Job
from customers.models import Customer

class Category(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    date_added = models.DateField(default=timezone.now)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Expense for Job id: " + str(self.job)
    