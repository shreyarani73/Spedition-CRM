from django.contrib import admin
from .models import Customer, Documents

class DocumentInline(admin.TabularInline):
    model = Documents
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]


admin.site.register(Documents)
admin.site.register(Customer, CustomerAdmin)