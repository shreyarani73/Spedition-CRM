from django.db import models
from django.utils import timezone
from customers.models import Customer
from django.contrib.auth.models import User

class JobCategory(models.Model):
    date_added = models.DateField(default=timezone.now)
    category_code = models.CharField(max_length=25)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Job(models.Model):
    date_added = models.DateField(default=timezone.now)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    shipping_from = models.CharField(max_length=25)
    shipping_to = models.CharField(max_length=25)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Job number " + self.pk + " for client:" + self.client.company_name + " from " + self.shipping_from + " " + self.shipping_to

    