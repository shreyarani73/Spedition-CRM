from django.urls import path
from . import views

app_name = "quotations"

urlpatterns = [
    path('view/<int:quotation_id>/edit-quotation-item/<int:quotation_item_id>', views.updateQuotationItem, name="edit-quotation-item"),
    path('view/<int:quotation_id>/delete-quotation-item/<int:quotation_item_id>', views.deleteQuotationItem, name="delete-quotation-item"),
    path('view/<int:quotation_id>/add-quotation-item', views.addQuotationItem, name="add-quotation-item"),
    path('view/<int:quotation_id>', views.ViewQuotation.as_view(), name="view"),
    path('add/', views.AddQuotation.as_view(), name="add"),    
    path("", views.index, name="index"),
]