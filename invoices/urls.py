from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path('add', views.AddInvoice.as_view(), name="add"),
    path('view/<int:invoice_id>', views.InvoiceView.as_view(), name="view"),
    path('view/<int:invoice_id>/add-invoice-item', views.NewInvoiceItem, name="add-invoice-item"),
    path('view/<int:invoice_id>/add-payment', views.AddPaymentToInvoice, name="add-payment"),
    path('', views.Index, name="index"),
]