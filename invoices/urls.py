from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path('add', views.AddInvoice.as_view(), name="add"),
    path('view/<int:invoice_id>', views.InvoiceView.as_view(), name="view"),
    path('view/<int:invoice_id>/add-invoice-item', views.NewInvoiceItem, name="add-invoice-item"),
    path('view/<int:invoice_id>/add-payment', views.AddPaymentToInvoice, name="add-payment"),
    path('view/<int:invoice_id>/update-invoice-item/<int:invoice_item_id>', views.UpdateInvoiceItem, name="update-invoice-item"),
    path('view/<int:invoice_id>/delete-invoice-item/<int:invoice_item_id>', views.DeleteInvoiceItem, name="delete-invoice-item"),
    path('view/<int:invoice_id>/update-payment/<int:payment_id>', views.updatePayment, name="update-payment"),
    path('view/<int:invoice_id>/delete-payment/<int:payment_id>', views.deletePayment, name="delete-payment"),
    path('', views.Index, name="index"),
]