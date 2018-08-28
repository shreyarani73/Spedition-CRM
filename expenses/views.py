from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Expense
from .forms import NewExpenseForm, UpdateExpenseForm


def index(request):
    expenses = Expense.objects.all().order_by("-date_added")

    return render(request, "expenses/index.html", {
        "expenses": expenses,
    })


class AddExpense(View):
    def get(self, request):
        form = NewExpenseForm()

        return render(request, "expenses/add.html", {
            "form": form,
        })
    
    def post(self, request):        
        form = NewExpenseForm(request.POST)
        expense = form.save()
        messages.add_message(request, messages.SUCCESS, "Expense has been added")

        return redirect("expenses:view", expense_id=expense.id)


class ExpenseView(View):
    def get(self, request, expense_id):
        expense = Expense.objects.get(pk=expense_id)
        form = UpdateExpenseForm(instance=expense)

        return render(request, "expenses/view.html", {
            "expense": expense, "form": form,
        })

    def post(self, request, expense_id):
        expense = Expense.objects.get(pk=expense_id)
        form = UpdateExpenseForm(request.POST, instance=expense)
        form.save()

        messages.add_message(request, messages.SUCCESS, "Expense has been updated")

        return redirect("expenses:view", expense_id=expense_id)