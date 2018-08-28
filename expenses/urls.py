from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path('view/<int:expense_id>', views.ExpenseView.as_view(), name="view"),    
    path('add', views.AddExpense.as_view(), name="add"),
    path('', views.index, name="index"),
]