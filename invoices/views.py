from django.shortcuts import render, redirect
from django.views import View
from .models import Invoice, InvoiceItem, Payments
from .forms import NewInvoice, InvoiceItemForm, NewInvoiceItemForm, InvoicePaymentForm, NewInvoicePaymentForm
from django.contrib import messages
from django.db.models import Sum

def Index(request):
    invoices = Invoice.objects.all()

    return render(request, "invoices/index.html", {
        "invoices":invoices,
    })


class AddInvoice(View):
    def get(self, request):
        form = NewInvoice()

        return render(request, "invoices/add.html", {
            "form": form,
        })

    def post(self, request):
        form = NewInvoice(request.POST)
        invoice = form.save(commit=False)
        invoice.total = 0
        invoice.balance_due = 0 
        invoice.save()
        invoice.invoice_id="SPEDITION/INVOICE/%s" % (invoice.pk)
        invoice.save()


        return redirect("invoices:view", invoice_id=invoice.pk)


class InvoiceView(View):
    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice_items = InvoiceItem.objects.filter(invoice=invoice)
        invoice_items_forms = []
        new_invoice_item_form = NewInvoiceItemForm()        

        payments = Payments.objects.filter(invoice=invoice)
        payment_forms = []
        new_payment_form = NewInvoicePaymentForm()
        for each in payments:
            record = {
                "id": each.id,
                "form": InvoicePaymentForm(instance=each)
            }
            payment_forms.append(record)
        
        for each in invoice_items:
            record = {
                "id" : each.id,
                "form": InvoiceItemForm(instance=each)
            }
            invoice_items_forms.append(record)

        return render(request, "invoices/view.html", {
            "invoice": invoice, "invoice_items": invoice_items_forms,
            "new_invoice_item_form": new_invoice_item_form, "payment_forms": payment_forms,
            "new_payment_form": new_payment_form
        })

    def post(self, request, invoice_id):
        pass


def NewInvoiceItem(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    form = NewInvoiceItemForm(request.POST)
    invoice_item = form.save(commit=False)
    invoice_item.invoice = invoice
    sub_total = invoice_item.quantity * invoice_item.rate * invoice_item.exchange_rate
    tax = sub_total * invoice_item.tax_rate/100
    sub_total = sub_total + tax
    

    invoice_item.total = sub_total

    invoice.total = invoice.total + sub_total
    invoice.balance_due = invoice.balance_due + sub_total
    
    client = invoice.job.client
    client.credit_amount = client.credit_amount - sub_total
    if client.credit_amount < 0:
        messages.add_message(request, messages.SUCCESS, "Credit amount not enough for client")
        return redirect("invoices:view", invoice_id=invoice_id)
    else:
        client.save()

        invoice.save()
        invoice_item.save()

        messages.add_message(request, messages.SUCCESS, "Invoice item added")

        return redirect("invoices:view", invoice_id=invoice_id)

def UpdateInvoiceItem(request, invoice_id, invoice_item_id):
    #invoice = Invoice.objcets.get(pk=invoice_id)
    invoice_item = InvoiceItem.objects.get(pk=invoice_item_id)
    invoice = invoice_item.invoice
    form = InvoiceItemForm(request.POST, instance=invoice_item)
    update_item = form.save(commit=False)
    update_item.invoice = invoice
    
    sub_total = update_item.quantity * update_item.rate * update_item.exchange_rate
    tax = sub_total * update_item.tax_rate/100
    sub_total = sub_total + tax
    update_item.total = sub_total
    update_item.save()
    items_all = InvoiceItem.objects.filter(invoice=invoice)
    st = 0
    for each in items_all:
        st = st + each.total 
    invoice.total = st
    invoice.balance_due = st

    client = invoice.job.client
    client.credit_amount = client.credit_amount - sub_total
    #invoice.total = invoice.total + sub_total
    #invoice.balance_due  = invoice.balance_due + sub_total
    client.save()
    invoice.save()
    

    messages.add_message(request, messages.SUCCESS, "Invoice item updated")

    return redirect ("invoices:view", invoice_id=invoice_id)

def DeleteInvoiceItem(request, invoice_id, invoice_item_id):
    #invoice = Invoice.objects.get(pk=invoice_id)
    invoice_item = InvoiceItem.objects.get(pk=invoice_item_id)
    invoice = invoice_item.invoice
    invoice_item.delete()

    items_all = InvoiceItem.objects.filter(invoice=invoice)
    st = 0
    for each in items_all:
        st = st + each.total
    invoice.total = st 
    invoice.balance_due = st
    
    #client = invoice.job.client
    #client.credit_amount = client.credit_amount - sub_total 
    #client.save()
    invoice.save()

    messages.add_message(request, messages.SUCCESS, "Invoice item updated")
    
    return redirect ("invoices:view", invoice_id=invoice_id)


def AddPaymentToInvoice(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    form = NewInvoicePaymentForm(request.POST)
    payment = form.save(commit=False)
    
    invoice.balance_due = invoice.balance_due - payment.amount
    client = invoice.job.client
    client.credit_amount = client.credit_amount + payment.amount
    
    client.save()
    payment.save()
    invoice.save()
    
    messages.add_message(request, message.SUCCESS, "Payment added")
    return redirect("invoices:view", invoice_id=invoice_id)


def updatePayment(request, invoice_id, payment_id):
    payment = Payments.objects.get(pk=payment_id)
    invoice = payment.invoice

    form = InvoicePaymentForm(request.POST, instance=payment)
    update = form.save()

    invoices_sum = InvoiceItem.objects.filter(invoice=invoice).aggregate(Sum("total"))
    payments_sum = Payments.objects.filter(invoice=invoice).aggregate(Sum("amount"))

    invoice.balance_due = invoices_sum["total__sum"]-payments_sum["amount__sum"]
    invoice.save()

    messages.add_message(request, messsage.SUCCESS, "Payment Updated") 
    return redirect("invoices:view", invoice_id=invoice_id)

def deletePayment(request, invoice_id, payment_id):
    payment = Payments.objects.get(pk=payment_id)    
    invoice = payment.invoice
    payment.delete()

    #payment_all = Payments.objects.filter(invoice=invoice)
    
    invoices_sum = InvoiceItem.objects.filter(invoice=invoice).aggregate(Sum("total"))["total__sum"]
    payments_sum = Payments.objects.filter(invoice=invoice).aggregate(Sum("amount"))["amount__sum"]

    if invoices_sum == None:
        invoices_sum = 0
    if payments_sum == None:
        payments_sum = 0
    

    amount_due = invoices_sum - payments_sum
    invoice.balance_due = amount_due
    invoice.save()

    messages.add_message(request, messages.SUCCESS, "Payment deleted")

    return redirect("invoices:view", invoice_id=invoice_id)