from django.contrib import admin
from .models import JobCategory, Job, Process


admin.site.register(Job)
admin.site.register(JobCategory)
admin.site.register(Process)