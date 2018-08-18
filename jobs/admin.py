from django.contrib import admin
from .models import JobCategory, Job


admin.site.register(Job)
admin.site.register(JobCategory)