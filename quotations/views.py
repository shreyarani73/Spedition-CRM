from django.shortcuts import render, redirect
from .models import Quotation
from django.views import View
from .forms import QuotationForm, QuotationUpdateForm
from django.contrib import messages

def index(request):
    quotations = Quotation.objects.all().order_by("-pk")

    return render(request, "quotations/index.html", {
        "quotations": quotations,
    })

class AddQuotation(View):
    def get(self, request):
        form = QuotationForm()

        return render(request, "quotations/add.html", {
            "form": form,
        })

    def post(self, request):
        form = QuotationForm(request.POST)
        if form.errors:
            print (form.errors)
        quotation = form.save(commit=False)

        total = quotation.service_quantity * quotation.service_rate * quotation.service_exch_rate
        taxes = total*quotation.taxes/100
        quotation.service_total = total + taxes

        quotation.save()

        messages.add_message(request, messages.SUCCESS, "Quotation has been succesfully created")

        return redirect("quotations:view", quotation_id=quotation.id)


class ViewQuotation(View):
    def get(self, request, quotation_id):
        quotation = Quotation.objects.get(pk=quotation_id)
        form = QuotationUpdateForm(instance=quotation)

        return render(request, "quotations/view.html", {
            "form":form, "quotation": quotation,
        })
    
    def post(self, request, quotation_id):
        quotation_object = Quotation.objects.get(pk=quotation_id)
        form = QuotationUpdateForm(request.POST, instance=quotation_object)
        if form.errors:
            print (form.errors)
        quotation = form.save(commit=False)
        total = quotation.service_quantity * quotation.service_rate * quotation.service_exch_rate
        taxes = total*quotation.taxes/100
        quotation.service_total = total + taxes

        quotation.save()

        messages.add_message(request, messages.SUCCESS, "Quotation has been succesfully updated")

        return redirect("quotations:view", quotation_id=quotation_id)
