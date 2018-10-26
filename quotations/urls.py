from django.urls import path
from . import views

app_name = "quotations"

urlpatterns = [
    path('view/<int:quotation_id>', views.ViewQuotation.as_view(), name="view"),
    path('add/', views.AddQuotation.as_view(), name="add"),    
    path("", views.index, name="index"),
]