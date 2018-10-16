from django.db import models
from django.utils import timezone
from customers.models import Customer
from django.contrib.auth.models import User
from crm import choices

JOB_STATUS = (
    ("Open", "Open"),    
    ("Closed", "Closed")
)

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
    job_status = models.CharField(max_length=25, default="Open", choices=JOB_STATUS)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    shipping_from = models.CharField(max_length=25)
    shipping_to = models.CharField(max_length=25)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Job number " + str(self.pk) + " for client:" + self.client.company_name + " from " + str(self.shipping_from) + " " + str(self.shipping_to)


class Process(models.Model):
    date_added = models.DateField(default=timezone.now)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    process_name = models.CharField(max_length=150)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    closed = models.BooleanField(default=False, choices=choices.YESNO)
    send_email = models.BooleanField(default=False, choices=choices.YESNO)

    def __str__(self):
        return "Process for Job id: %s" % str(self.job.id )