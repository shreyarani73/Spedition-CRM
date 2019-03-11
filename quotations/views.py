from django.shortcuts import render, redirect
from .models import Quotation, QuotationItem
from django.views import View
from .forms import QuotationForm, QuotationUpdateForm, NewQuotationItemForm, QuotationItemUpdateForm
from django.contrib import messages

def index(request):
    quotations = Quotation.objects.all().order_by("-pk")

    return render(request, "quotations/index.html", {
        "quotations": quotations,
    })

def addQuotationItem(request, quotation_id):
    form = NewQuotationItemForm(request.POST)    
    item = form.save(commit=False)
    quotation = Quotation.objects.get(pk=quotation_id)
    item.quotation = quotation
    
    service_total = item.quantity * item.rate * item.exchange_rate
    taxes = service_total * item.tax_rate / 100

    item.total = service_total + taxes
    quotation.service_total = quotation.service_total + service_total + taxes
    item.save()    
    quotation.save()

    messages.add_message(request, messages.SUCCESS, "Quotation item added succesfully")

    return redirect("quotations:view", quotation_id=quotation_id)

def updateQuotationItem(request, quotation_id, quotation_item_id):
    quotation = Quotation.objects.get(pk=quotation_id)
    quotation_item = QuotationItem.objects.get(pk=quotation_item_id)

    form = QuotationItemUpdateForm(request.POST, instance=quotation_item)
    qitem = form.save(commit=False)

    total = qitem.quantity * qitem.rate * qitem.exchange_rate
    taxes = total * qitem.tax_rate/100

    qitem.total = total + taxes
    qitem.save()

    qitems_all = QuotationItem.objects.filter(quotation=quotation)
    st = 0
    for each in qitems_all:
        st = st + each.total 
        quotation.service_total = st
        quotation.save()

    messages.add_message(request, messages.SUCCESS, "Quotation item been updated")

    return redirect("quotations:view", quotation_id=quotation_id)

def deleteQuotationItem(request, quotation_id, quotation_item_id):
    quotation = Quotation.objects.get(pk=quotation_id)
    quotation_item = QuotationItem.objects.get(pk=quotation_item_id)
    quotation_item.delete()
    
    quotation_items_all = QuotationItem.objects.filter(quotation=quotation)
    st = 0
    for each in quotation_items_all:
        st = st + each.total 
        quotation.service_total = st
        quotation.save()

       
        
    messages.add_message(request, messages.SUCCESS, "Quotation item successfully deleted")

    return redirect("quotations:view", quotation_id=quotation_id)


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
        quotation.save()

        messages.add_message(request, messages.SUCCESS, "Quotation has been succesfully created")

        return redirect("quotations:view", quotation_id=quotation.id)


class ViewQuotation(View):
    def get(self, request, quotation_id):
        quotation = Quotation.objects.get(pk=quotation_id)
        formq = QuotationUpdateForm(instance=quotation)

        quotation_items = QuotationItem.objects.filter(quotation=quotation).order_by("-pk")
        new_quotation_item_form = NewQuotationItemForm()
        quotation_item_forms = []
        for each in quotation_items:
            record = {
                "id": each.id,
                "form": QuotationItemUpdateForm(instance=each)
            }
            quotation_item_forms.append(record)

        return render(request, "quotations/view.html", {
            "form":formq, "quotation": quotation, "quotation_items": quotation_item_forms,
            "new_quotation_item_form": new_quotation_item_form,
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
