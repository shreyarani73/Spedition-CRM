from django.urls import path
from . import views

app_name="customers"

urlpatterns = [
    path('', views.Customers.as_view(), name="index"),
    path('add', views.AddCustomer.as_view(), name="add"),
    path('view/<int:customer_id>/upload-document', views.CustomerFileUpload, name="upload-document"),
    path('view/<int:customer_id>', views.CustomerView.as_view(), name="view"),
]